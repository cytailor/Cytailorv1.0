from flask import Flask, request, json
from flask_restful import Api
from elasticsearch import Elasticsearch

import Crud_functions

app = Flask(__name__)
api = Api(app)
ELASTIC_PASSWORD = "vNBMw0eNQRhht5pbpuD1"

# Create the client instance
es = Elasticsearch(
    "https://localhost:9200",
    # ca_certs="C:/Users/Public/certs/http_ca.crt",
    verify_certs=False,
    basic_auth=("elastic", ELASTIC_PASSWORD)
)


def asset_mapping(ide):
    # This funnction will take as input the id of the current organization to which we are processing a risk assessment
    # it will get its profile defining the different answers of the survey filled in the beggining of the process
    # it will also get the asset mapping from the database and try to map each answer with its specific usecase and
    # it will return a dictionary with the different assets with values
    # # blank dictionary in which we will insert the different vales later
    assetvalues = {}
    # # list of all the assets from the database
    assets = Crud_functions.get_assets()
    # # entreprise profile from the database
    e_profile = Crud_functions.get_organizationprofile(ide=ide)
    # # blank dictionary where we will arrange the organization profile with the fiels and the value
    e_profile2 = {}
    # # getting the names of the different fields of the organization profile
    schema = Crud_functions.organizationprofile.columns_names()
    # # getting the asset mapping
    asset_mapping1 = Crud_functions.getassetmapping()
    asset_mapping2 = {}
    # Thhrough this function we will organize the  different fields and the values of the organization profile
    for i in range(1, len(e_profile[0])):
        e_profile2[schema[i]] = e_profile[0][i]
    print(e_profile2)
    # running through the profile of the organization and processing the different answers in order to get the
    # different values
    for i in e_profile2.keys():
        print(i)
        print(e_profile2[i])
        print(assetvalues)
        # a list to get all the asset mapping rows related to this field of the organization profile
        mapping = []
        for j in asset_mapping1:
            if j[1] == i:
                print(j)
                mapping.append(j)
        for j in mapping:
            print(j)
            if j[4] is None:
                if j[3] == e_profile2[i] and j[7] == 'EQUAL':
                    if j[5] in assetvalues.keys():
                        if assetvalues[j[5]] < j[6]:
                            assetvalues[j[5]] = int(j[6])
                    else:
                        assetvalues[j[5]] = int(j[6])
                elif j[7] == 'INCLUDE':
                    print(len(e_profile2[i]))
                    for k in range(len(e_profile2[i])):
                        if e_profile2[i][k] in j[2].split(','):
                            if j[5] in assetvalues.keys():
                                if assetvalues[j[5]] < j[6]:
                                    assetvalues[j[5]] = int(j[6])
                            else:
                                assetvalues[j[5]] = int(j[6])
                elif j[7] == 'LEN:EQUAL' and len(e_profile2[i]) == int(j[2]):
                    if j[5] in assetvalues.keys():
                        if assetvalues[j[5]] < j[6]:
                            assetvalues[j[5]] = int(j[6])
                    else:
                        assetvalues[j[5]] = int(j[6])
                elif j[7] == 'LEN:HIGHER OR EQUAL' and len(e_profile2[i]) >= int(j[2]):
                    if j[5] in assetvalues.keys():
                        if assetvalues[j[5]] < j[6]:
                            assetvalues[j[5]] = int(j[6])
                    else:
                        assetvalues[j[5]] = int(j[6])
                elif j[7] == 'NULL OR NOT':
                    if j[2] is None and e_profile2[i] is None:
                        if j[5] in assetvalues.keys():
                            if assetvalues[j[5]] < j[6]:
                                assetvalues[j[5]] = int(j[6])
                            else:
                                assetvalues[j[5]] = int(j[6])
                    elif j[2] is not None and e_profile2[i] is not None:
                        if j[5] in assetvalues.keys():
                            if assetvalues[j[5]] < j[6]:
                                assetvalues[j[5]] = int(j[6])
                            else:
                                assetvalues[j[5]] = int(j[6])
            else:
                if j[2] == e_profile2[i] and j[7] == 'EQUAL' and j[4] == e_profile2[j[3]] and j[8] == 'EQUAL':
                    if j[5] in assetvalues.keys():
                        if assetvalues[j[5]] < j[6]:
                            assetvalues[j[5]] = int(j[6])
                    else:
                        assetvalues[j[5]] = int(j[6])
                elif j[7] == 'INCLUDE' and j[4] == e_profile2[j[3]] and j[8] == 'EQUAL':
                    for k in range(len(e_profile2[i])):
                        if k in j[2]:
                            if j[5] in assetvalues.keys():
                                if assetvalues[j[5]] < j[6]:
                                    assetvalues[j[5]] = int(j[6])
                            else:
                                assetvalues[j[5]] = int(j[6])
                elif j[7] == 'INCLUDE' and j[8] == 'NULL OR NOT':
                    for k in range(len(e_profile2[i])):
                        if k in j[2] and j[4] is None and e_profile2[j[3]] is None:
                            if j[5] in assetvalues.keys():
                                if assetvalues[j[5]] < j[6]:
                                    assetvalues[j[5]] = int(j[6])
                            else:
                                assetvalues[j[5]] = int(j[6])
                        if k in j[2] and j[4] is not None and e_profile2[j[3]] is not None:
                            if j[5] in assetvalues.keys():
                                if assetvalues[j[5]] < j[6]:
                                    assetvalues[j[5]] = int(j[6])
                            else:
                                assetvalues[j[5]] = int(j[6])
                elif j[7] == 'INCLUDE' and j[8] == 'LEN:EQUAL' and len(e_profile2[j[3]]) == int(j[4]):
                    for k in range(len(e_profile2[i])):
                        if k in j[2]:
                            if j[5] in assetvalues.keys():
                                if assetvalues[j[5]] < j[6]:
                                    assetvalues[j[5]] = int(j[6])
                            else:
                                assetvalues[j[5]] = int(j[6])
                elif j[7] == 'INCLUDE' and j[8] == 'LEN:HIGHER OR EQUAL' and int(j[4]) >= len(e_profile2[j[3]]):
                    for k in range(len(e_profile2[i])):
                        if k in j[2]:
                            if j[5] in assetvalues.keys():
                                if assetvalues[j[5]] < j[6]:
                                    assetvalues[j[5]] = int(j[6])
                            else:
                                assetvalues[j[5]] = int(j[6])
                elif j[2] == e_profile2[i] and j[7] == 'EQUAL' and j[8] == 'INCLUDE':
                    for k in range(len(e_profile2[4])):
                        if k in j[4]:
                            if j[5] in assetvalues.keys():
                                if assetvalues[j[5]] < j[6]:
                                    assetvalues[j[5]] = int(j[6])
                            else:
                                assetvalues[j[5]] = int(j[6])

                elif j[2] == e_profile2[i] and j[7] == 'EQUAL' and j[8] == 'NULL OR NOT':
                    if j[4] is None and e_profile2[j[3]] is None:
                        if j[5] in assetvalues.keys():
                            if assetvalues[j[5]] < j[6]:
                                assetvalues[j[5]] = int(j[6])
                            else:
                                assetvalues[j[5]] = int(j[6])
                    elif j[4] is not None and e_profile2[j[3]] is not None:
                        if j[5] in assetvalues.keys():
                            if assetvalues[j[5]] < j[6]:
                                assetvalues[j[5]] = int(j[6])
                            else:
                                assetvalues[j[5]] = int(j[6])
                elif j[2] == e_profile2[i] and j[7] == 'EQUAL' and j[8] == 'LEN:HIGHER OR EQUAL' and int(j[4]) >= len(
                        e_profile2[j[3]]):
                    if j[5] in assetvalues.keys():
                        if assetvalues[j[5]] < j[6]:
                            assetvalues[j[5]] = int(j[6])
                    else:
                        assetvalues[j[5]] = int(j[6])
                elif j[2] == e_profile2[i] and j[7] == 'EQUAL' and j[8] == 'LEN:EQUAL' and int(j[4]) == len(
                        e_profile2[j[3]]):
                    if j[5] in assetvalues.keys():
                        if assetvalues[j[5]] < j[6]:
                            assetvalues[j[5]] = int(j[6])
                    else:
                        assetvalues[j[5]] = int(j[6])
                elif j[7] == 'NULL OR NOT' and j[4] == e_profile2[j[3]] and j[8] == 'EQUAL':
                    if j[2] is None and e_profile2[i] is None:
                        if j[5] in assetvalues.keys():
                            if assetvalues[j[5]] < j[6]:
                                assetvalues[j[5]] = int(j[6])
                            else:
                                assetvalues[j[5]] = int(j[6])
                    elif j[2] is not None and e_profile2[i] is not None:
                        if j[5] in assetvalues.keys():
                            if assetvalues[j[5]] < j[6]:
                                assetvalues[j[5]] = int(j[6])
                            else:
                                assetvalues[j[5]] = int(j[6])
                elif j[7] == 'NULL OR NOT' and j[4] == e_profile2[j[3]] and j[8] == 'INCLUDE':
                    for k in range(len(e_profile2[4])):
                        if k in j[4]:
                            if j[2] is None and e_profile2[i] is None:
                                if j[5] in assetvalues.keys():
                                    if assetvalues[j[5]] < j[6]:
                                        assetvalues[j[5]] = int(j[6])
                                    else:
                                        assetvalues[j[5]] = int(j[6])
                            elif j[2] is not None and e_profile2[i] is not None:
                                if j[5] in assetvalues.keys():
                                    if assetvalues[j[5]] < j[6]:
                                        assetvalues[j[5]] = int(j[6])
                                    else:
                                        assetvalues[j[5]] = int(j[6])
                elif j[2] == e_profile2[i] and j[7] == 'NULL OR NOT' and j[8] == 'LEN:EQUAL' and int(j[4]) == len(
                        e_profile2[j[3]]):
                    if j[2] is None and e_profile2[i] is None:
                        if j[5] in assetvalues.keys():
                            if assetvalues[j[5]] < j[6]:
                                assetvalues[j[5]] = int(j[6])
                            else:
                                assetvalues[j[5]] = int(j[6])
                    elif j[2] is not None and e_profile2[i] is not None:
                        if j[5] in assetvalues.keys():
                            if assetvalues[j[5]] < j[6]:
                                assetvalues[j[5]] = int(j[6])
                            else:
                                assetvalues[j[5]] = int(j[6])
                elif j[2] == e_profile2[i] and j[7] == 'NULL OR NOT' and j[8] == 'LEN:HIGHER OR EQUAL' and int(j[4]) >= len(
                        e_profile2[j[3]]):
                    if j[2] is None and e_profile2[i] is None:
                        if j[5] in assetvalues.keys():
                            if assetvalues[j[5]] < j[6]:
                                assetvalues[j[5]] = int(j[6])
                            else:
                                assetvalues[j[5]] = int(j[6])
                    elif j[2] is not None and e_profile2[i] is not None:
                        if j[5] in assetvalues.keys():
                            if assetvalues[int(j[5])] < int(j[6]):
                                assetvalues[int(j[5])] = int(j[6])
                            else:
                                assetvalues[j[5]] = int(j[6])
                elif j[7] == 'LEN:HIGHER OR EQUAL' and j[8] == 'EQUAL' and int(j[2]) >= len(e_profile2[i]) and int(j[4]) == \
                        e_profile2[j[3]]:
                    if j[5] in assetvalues.keys():
                        if assetvalues[j[5]] < j[6]:
                            assetvalues[j[5]] = int(j[6])
                    else:
                        assetvalues[j[5]] = int(j[6])
                elif j[7] == 'LEN:HIGHER OR EQUAL' and int(j[2]) >= len(e_profile2[i]) and j[8] == 'INCLUDE':
                    for k in range(len(e_profile2[j[3]])):
                        if k in j[4]:
                            # if j[2] is None and e_profile2[i] is None:
                            if j[5] in assetvalues.keys():
                                if assetvalues[int(j[5])] < int(j[6]):
                                    assetvalues[j[5]] = int(j[6])
                                else:
                                    assetvalues[j[5]] = int(j[6])
                            # elif j[2] is not None and e_profile2[i] is not None:
                            #     if j[5] in assetvalues.keys():
                            #         if assetvalues[j[5]] < j[6]:
                            #             assetvalues[j[5]] = int(j[6])
                            #         else:
                            #             assetvalues[j[5]] = int(j[6])
                elif j[7] == 'LEN:HIGHER OR EQUAL' and j[8] == 'LEN:EQUAL' and int(j[2]) >= len(e_profile2[i]) and j[
                    4] == len(e_profile2[j[3]]):
                    if j[5] in assetvalues.keys():
                        if assetvalues[j[5]] < j[6]:
                            assetvalues[j[5]] = int(j[6])
                    else:
                        assetvalues[j[5]] = int(j[6])
                elif j[7] == 'LEN:HIGHER OR EQUAL' and int(j[2]) >= len(e_profile2[i]) and j[8] == 'NULL OR NOT':
                    if j[4] is None and e_profile2[j[3]] is None:
                        if j[5] in assetvalues.keys():
                            if assetvalues[j[5]] < j[6]:
                                assetvalues[j[5]] = int(j[6])
                            else:
                                assetvalues[j[5]] = int(j[6])
                    elif j[4] is not None and e_profile2[j[3]] is not None:
                        if j[5] in assetvalues.keys():
                            if assetvalues[j[5]] < j[6]:
                                assetvalues[j[5]] = int(j[6])
                            else:
                                assetvalues[j[5]] = int(j[6])
                elif j[7] == 'LEN:EQUAL' and int(j[2]) == len(e_profile2[i]) and int(j[8]) == 'LEN:HIGHER OR EQUAL' and j[
                    4] >= len(e_profile2[j[3]]):
                    if j[5] in assetvalues.keys():
                        if assetvalues[j[5]] < j[6]:
                            assetvalues[j[5]] = int(j[6])
                    else:
                        assetvalues[j[5]] = int(j[6])
                elif j[7] == 'LEN:EQUAL' and int(j[2]) == len(e_profile2[i]) and j[8] == 'INCLUDE':
                    for k in range(len(e_profile2[j[3]])):
                        if k in j[4]:
                            if j[2] is None and e_profile2[i] is None:
                                # if j[5] in assetvalues.keys():
                                if assetvalues[j[5]] < j[6]:
                                    assetvalues[j[5]] = int(j[6])
                                else:
                                    assetvalues[j[5]] = int(j[6])
                            # elif j[2] is not None and e_profile2[i] is not None:
                            #     if j[5] in assetvalues.keys():
                            #         if assetvalues[j[5]] < j[6]:
                            #             assetvalues[j[5]] = int(j[6])
                            #         else:
                            #             assetvalues[j[5]] = int(j[6])
                elif j[7] == 'LEN:EQUAL' and int(j[2]) == len(e_profile2[i]) and j[4] == e_profile2[j[3]] and j[
                    8] == 'EQUAL':
                    if j[5] in assetvalues.keys():
                        if assetvalues[j[5]] < j[6]:
                            assetvalues[j[5]] = int(j[6])
                    else:
                        assetvalues[j[5]] = int(j[6])
                elif j[7] == 'LEN:EQUAL' and int(j[2]) == len(e_profile2[i]) and j[8] == 'NULL OR NOT':
                    if j[4] is None and e_profile2[j[3]] is None:
                        if j[5] in assetvalues.keys():
                            if assetvalues[j[5]] < j[6]:
                                assetvalues[j[5]] = int(j[6])
                            else:
                                assetvalues[j[5]] = int(j[6])
                    elif j[4] is not None and e_profile2[j[3]] is not None:
                        if j[5] in assetvalues.keys():
                            if assetvalues[j[5]] < j[6]:
                                assetvalues[j[5]] = int(j[6])
                            else:
                                assetvalues[j[5]] = int(j[6])
    return assetvalues


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


def risk_calc(vulns, risks, a_values):
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
        impact_value = max(a_values.values())
        # calculating the factor of the probability , the pourcentage of the probab
        pv = (len(preleminary_risks[i]['vul']) / len(preleminary_risks[i]['risk'][6]))
        # calculating the new probability value depending on the number of vulnerabilities discovered
        probability_value = (preleminary_risks[i]['risk'][4]) * pv
        risk_value = impact_value * probability_value
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

    assetvalues = asset_mapping(requestdata['user1'])
    risks = risk_calc(vulns=vulnerbilities, risks=Risks, a_values=assetvalues)
    for i in risks:
        report['Risks'].append(i.get_risk())
    for i in vulnerbilities:
        report['Vulnerabilities'].append({'vulnerability_id': i, 'title': Crud_functions.get_vulnerability(i)[0][0]})
    # infos = es.index(index="risk",
    #                  document=report)
    return json.dumps(report, sort_keys=False), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4001)
    # asset_mapping(1)
