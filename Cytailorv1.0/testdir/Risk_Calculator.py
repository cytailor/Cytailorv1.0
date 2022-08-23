from flask import Flask, jsonify, request, json
from flask_restful import Api, Resource
from elasticsearch import Elasticsearch

import Crud_functions

app = Flask(__name__)
api = Api(app)
ELASTIC_PASSWORD = "H*j6eoznPUYhmvmcz8LR"

# Create the client instance
es = Elasticsearch(
    "https://localhost:9200",
    # ca_certs="C:/Users/Public/certs/http_ca.crt",
    verify_certs=False,
    basic_auth=("elastic", ELASTIC_PASSWORD)
)


def asset_mapping(ide):
    assetvalues = {}
    assets = Crud_functions.get_assets()
    e_profile = Crud_functions.get_entrepriseprofile(ide=ide)
    e_profile2 = {}
    schema = Crud_functions.organizationprofile.columns_names()
    asset_mapping1 = Crud_functions.getassetmapping()
    asset_mapping2 = {}
    for i in range(len(e_profile[0])):
        e_profile2[schema[i]] = e_profile[0][i]
    print(e_profile2)
    for i in e_profile2.keys():
        mapping = []
        for j in asset_mapping1:
            if j[3] == i:
                mapping.append(j)
        for j in mapping:
            if j[4] is None:
                if j[3] == e_profile2[i] and j[7] == 'NONE':
                    if j[5] in assetvalues.keys():
                        if assetvalues[j[5]] < j[6]:
                            assetvalues[j[5]] = j[6]
                    else:
                        assetvalues[j[5]] = j[6]
                elif j[7] == 'INCLUDE':
                    for k in range(len(e_profile2[i])):
                        if k in j[3]:
                            if j[5] in assetvalues.keys():
                                if assetvalues[j[5]] < j[6]:
                                    assetvalues[j[5]] = j[6]
                            else:
                                assetvalues[j[5]] = j[6]
            else:
                if j[2] == i and j[7] == 'NONE' and j[5] == e_profile2[4] and j[8] == 'NONE':
                    if j[5] in assetvalues.keys():
                        if assetvalues[j[5]] < j[6]:
                            assetvalues[j[5]] = j[6]
                    else:
                        assetvalues[j[5]] = j[6]
                # elif j[2] == i and j[7] == 'NONE' and j[5] == e_profile2[4] and j[8] == 'NONE':




# getting the vulnerabilities list from the database
Vulnerabilities = sorted(Crud_functions.get_vulnerabilities(), key=lambda x: x[0])
# getting the  use-case vulnerability list from the database
Ucv = sorted(Crud_functions.get_uc_vulnerabilities(), key=lambda x: x[0])


# Functions that finds the vulnerabilities related to the user considering his answers to the questions as an input
def findvul(uc_answered_question, ucv, vul):
    # A blank list in which we will insert the different vulnerabilities discovered
    vul_list = []
    # we check if one of the answers weight overpass the threshold so that we know if the vulnerability exists or not
    for i in uc_answered_question.keys():
        # the threshold is defined null in the beginning
        threshold = 0
        for j in uc_answered_question[i].keys():
            # we extract the list of  choices from the database
            answers = Crud_functions.get_choices()
            for k in answers:
                # if the weight of the answer overpass the previous threshold ,then its weight is the new threshold
                if uc_answered_question[i][j] == k[0]:
                    threshold = k[3]
        # if the final value of the threshold overpass the one of the usecase,then the vulnerability exists
        if threshold > float(ucv[int(i[7:]) - 1][2]):
            vul_list.append(vul[ucv[int(i[7:]) - 1][1] - 1][0])
    return vul_list


# we define a Risk class with getter and setter  in order to be used later in the risk calculation
class Risk:
    def __init__(self, idr, title, impact_value, probability_value, risk_value, vulnerabilities, assets):
        self.idr = idr
        self.title = title
        self.impact_value = impact_value
        self.probability_value = probability_value
        self.risk_value = risk_value
        self.vulnerabilities = vulnerabilities
        self.assets = assets

    def get_idr(self):
        return self.idr

    def get_impact_value(self):
        return self.impact_value

    def get_title(self):
        return self.title

    def get_probability_value(self):
        return self.probability_value

    def get_value_risk(self):
        return self.risk_value

    def get_vulnerabilities(self):
        return self.vulnerabilities

    def get_assets(self):
        return self.assets

    def get_risk(self):
        return {'idr': self.idr, 'title': self.title, 'impact_value': self.impact_value,
                'probability_value': self.probability_value,
                'risk_value': self.risk_value, 'vulnerabilities': self.vulnerabilities, 'assets': self.assets}


# Getting the list of risks from the database
Risks = Crud_functions.get_risks()


def risk_calc(vulns, risks, ):
    # identifying risks without adding any risk or probabilities values
    preleminary_risks = {}
    # final user risks after adding the different values
    user_risks = []
    # first loop for in order to identify the risks depending on vulnerabilities
    for i in risks:
        for j in i[6]:
            # if the vulnerability is exists in the list of vulnerabilities related to the risk then the risk exists
            if j in vulns:
                # if the risk already in the list we add the vulnerability to the vulnerabilities list ,
                # if not we add the risk o preleminary_risks
                if i[0] not in preleminary_risks:
                    preleminary_risks[i[0]] = {'vul': [j], 'risk': i}
                else:
                    preleminary_risks[i[0]]['vul'].append(j)
    # loop for to add the different values
    for i in preleminary_risks.keys():
        # impact value defined as 0 and will be added later using asset_mapping
        impact_value = 0.0
        # calculating the factor of the probability , the pourcentage of the probab
        pv = (len(preleminary_risks[i]['vul']) / len(preleminary_risks[i]['risk'][6]))
        # calculating the new probability value depending on the number of vulnerabilities discovered
        probability_value = (preleminary_risks[i]['risk'][4]) * pv
        risk_value = preleminary_risks[i]['risk'][3] + probability_value
        user_risks.append(
            Risk(preleminary_risks[i]['risk'][0], preleminary_risks[i]['risk'][1], impact_value, probability_value,
                 risk_value,
                 preleminary_risks[i]['vul'], preleminary_risks[i]['risk'][7]))

    return user_risks


@app.route('/api/risk_calculator/', methods=['GET'])
def calculaterisk():
    requestdata = request.get_json()
    report = {'user': requestdata['user'], 'Risks': [], 'Assets': [], 'Vulnerabilities': [], }
    answers = es.search(index="answers", query={"match": {"user": requestdata['user']}})
    vulnerbilities = findvul(ucv=Ucv, vul=Vulnerabilities,
                             uc_answered_question=answers['hits']['hits'][0]['_source']['vulnerabilities'])
    risks = risk_calc(vulns=vulnerbilities, risks=Risks)
    for i in risks:
        report['Risks'].append(i.get_risk())
    for i in vulnerbilities:
        report['Vulnerabilities'].append({'vulnerability_id': i, 'title': Crud_functions.get_vulnerability(i)[0][0]})
    infos = es.index(index="risk",
                     document=report)
    return json.dumps(report, sort_keys=False), 200


if __name__ == '__main__':
    app.run(debug=True)
    # asset_mapping(1)
