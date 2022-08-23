import os

from flask import Flask, request, json
from flask_cors import CORS, cross_origin
from flask_restful import Api
from elasticsearch import Elasticsearch
from CRUD import Crud

organizationprofile = Crud(
    table='organization_profile',
    primarykey='id'
)

asset_mapping = Crud(
    table='asset_mapping',
    primarykey='id'
)

uc_weakness = Crud(

    table='uc_weakness',
    primarykey='id'
)

weakness = Crud(
    table='weakness',
    primarykey='id'
)

choice = Crud(
    table='choice',
    primarykey='id'
)

risk = Crud(
    table='risk',
    primarykey='id'
)

asset = Crud(
    table='asset',
    primarykey='id'
)


def get_organizationprofile(ide):
    organizationprofile.connect()
    org = organizationprofile.select_all2(primaryKey_value=ide)
    organizationprofile.close()
    return org


def getassetmapping():
    asset_mapping.connect()
    assetmap = asset_mapping.select_all()
    asset_mapping.close()
    return assetmap


def get_uc_weaknesses():
    uc_weakness.connect()
    uc = uc_weakness.select_all()
    uc_weakness.close()
    return uc


def get_weaknesses():
    weakness.connect()
    weak = weakness.select_all()
    weakness.close()
    return weak


def get_choices():
    choice.connect()
    ch = choice.select_all()
    choice.close()
    return ch


def get_risks():
    risk.connect()
    r = risk.select_all()
    risk.connect()
    return r


def get_weakness(vid):
    weakness.connect()
    v = weakness.select_all(primaryKey_value=vid)
    weakness.connect()
    return v


app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"*": {"origins": ["http://localhost:3000", "https://app.cytailor.io"]}})

# Create the client instance
ELASTIC_PASSWORD = os.getenv('ELASTIC_PASSWORD')
ELASTIC_USER = os.getenv('ELASTIC_USERNAME')
ELASTIC_HOST = os.environ['ELASTICSEARCH_MASTER_SERVICE_HOST']
ELASTIC_PORT = os.environ['ELASTICSEARCH_MASTER_SERVICE_PORT']
ELASTIC_URL = 'https://' + ELASTIC_HOST + ':' + ELASTIC_PORT

# Create the client instance
es = Elasticsearch(
    ELASTIC_URL,
    # ca_certs=os.getenv('CERT_PATH'),
    verify_certs=bool(int(os.getenv('VERIFY_CERTS'))),
    basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD))


def valuation(values, value, value_id):
    if value_id in values.keys():
        if values[value_id] < value:
            values[value_id] = value
    else:
        values[value_id] = value


def equal(value1, value2):
    if value1 == value2:
        return True
    else:
        return False


def include(list_values, value):
    return_value = False
    for k in range(len(list_values)):
        if list_values[k] in value.split(','):
            return_value = True
    return return_value


def len_equal(list_values, value):
    if len(list_values) == value:
        return True
    else:
        return False


def len_higher_or_equal(list_values, value):
    if len(list_values) >= value:
        return True
    else:
        return False


def null_or_not(value1, value2):
    if value1 is None and value2 is None:
        return True
    elif value1 is not None and value2 is not None:
        return True
    else:
        return False


def assetmapping2(ide):
    # This funnction will take as input the id of the current organization to which we are processing a risk assessment
    # it will get its profile defining the different answers of the survey filled in the beggining of the process
    # it will also get the asset mapping from the database and try to map each answer with its specific usecase and
    # it will return a dictionary with the different assets with values
    # # blank dictionary in which we will insert the different vales later
    assetvalues = {}
    # # list of all the assets from the database
    # # entreprise profile from the database
    e_profile = get_organizationprofile(ide=ide)
    # # list the operators
    operators = [['EQUAL', equal], ['INCLUDE', include], ['LEN:EQUAL', len_equal],
                 ['LEN:HIGHER OR EQUAL', len_higher_or_equal], ['NULL OR NOT', null_or_not]]
    # # getting the asset mapping
    asset_mapping1 = getassetmapping()
    # running through the profile of the organization and processing the different answers in order to get the
    # different values
    for i in e_profile.keys():
        # a list to get all the asset mapping rows related to this field of the organization profile
        mapping = []
        for j in asset_mapping1:
            if j[1] == i:
                mapping.append(j)
        for j in mapping:
            if j[4] is None:
                for k in operators:
                    if j[7] == k[0]:
                        if k[1](e_profile[i], j[2]):
                            valuation(assetvalues, i[6], j[5])

            else:
                for k in operators:
                    operators2 = operators
                    operators2.remove(k)
                    for h in operators2:
                        if j[7] == k[0] and h[0] == j[8]:
                            if k[1](e_profile[i], j[2]) and h[1](e_profile[j[3]], j[4]):
                                valuation(assetvalues, i[6], j[5])


def assetmapping(ide):
    # This funnction will take as input the id of the current organization to which we are processing a risk assessment
    # it will get its profile defining the different answers of the survey filled in the beggining of the process
    # it will also get the asset mapping from the database and try to map each answer with its specific usecase and
    # it will return a dictionary with the different assets with values
    # # blank dictionary in which we will insert the different vales later
    assetvalues = {}
    # # list of all the assets from the database
    # # entreprise profile from the database
    e_profile = get_organizationprofile(ide=ide)
    # # blank dictionary where we will arrange the organization profile with the fiels and the value
    e_profile2 = {}
    # # getting the names of the different fields of the organization profile
    schema = organizationprofile.organization_names()
    # # list the operators
    operators = ['EQUAL', 'INCLUDE', 'LEN:EQUAL', 'LEN:HIGHER OR EQUAL', 'NULL OR NOT']

    # for i in operators :
    #     operators2=operators
    #     operators2.remove(i)
    #     for j in operators2:
    for i in operators:
        operators2 = operators
        operators2.remove(i)

    # # getting the asset mapping
    asset_mapping1 = getassetmapping()
    # Through this function we will organize the  different fields and the values of the organization profile
    for i in range(1, len(e_profile[0])):
        e_profile2[schema[i]] = e_profile[0][i]
    # running through the profile of the organization and processing the different answers in order to get the
    # different values
    for i in e_profile2.keys():
        print(i)
        # a list to get all the asset mapping rows related to this field of the organization profile
        mapping = []
        for j in asset_mapping1:
            if j[1] == i:
                mapping.append(j)
        for j in mapping:
            if j[4] is None:
                if j[2] == e_profile2[i] and j[7] == 'EQUAL':
                    if j[5] in assetvalues.keys():
                        if assetvalues[j[5]] < j[6]:
                            assetvalues[j[5]] = int(j[6])
                    else:
                        assetvalues[j[5]] = int(j[6])
                elif j[7] == 'INCLUDE':
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
                elif j[2] == e_profile2[i] and j[7] == 'NULL OR NOT' and j[8] == 'LEN:HIGHER OR EQUAL' and int(
                        j[4]) >= len(e_profile2[j[3]]):
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
                elif j[7] == 'LEN:HIGHER OR EQUAL' and j[8] == 'EQUAL' and int(j[2]) >= len(e_profile2[i]) and int(
                        j[4]) == \
                        e_profile2[j[3]]:
                    if j[5] in assetvalues.keys():
                        if assetvalues[j[5]] < j[6]:
                            assetvalues[j[5]] = int(j[6])
                    else:
                        assetvalues[j[5]] = int(j[6])
                elif j[7] == 'LEN:HIGHER OR EQUAL' and int(j[2]) >= len(e_profile2[i]) and j[8] == 'INCLUDE':
                    for k in range(len(e_profile2[j[3]])):
                        if k in j[4]:
                            if j[5] in assetvalues.keys():
                                if assetvalues[int(j[5])] < int(j[6]):
                                    assetvalues[j[5]] = int(j[6])
                                else:
                                    assetvalues[j[5]] = int(j[6])
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
                elif j[7] == 'LEN:EQUAL' and int(j[2]) == len(e_profile2[i]) and int(j[8]) == 'LEN:HIGHER OR EQUAL' and \
                        j[
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
                                if assetvalues[j[5]] < j[6]:
                                    assetvalues[j[5]] = int(j[6])
                                else:
                                    assetvalues[j[5]] = int(j[6])
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


# Functions that finds the weaknesses related to the user considering his answers to the questions as an input
def findweak(uc_answered_question, ucv, weak):
    # A blank list in which we will insert the different weaknesses discovered
    weak_list = []
    # we check if one of the answers weight overpass the threshold so that we know if the weakness exists or not
    for i in uc_answered_question.keys():
        # the threshold is defined null in the beginning
        threshold = 0
        for j in uc_answered_question[i].keys():
            # we extract the list of  choices from the database
            choices_list = get_choices()
            for k in choices_list:
                # if the weight of the answer overpass the previous threshold ,then its weight is the new threshold
                if uc_answered_question[i][j] == k[0]:
                    threshold += k[3]
        # if the final value of the threshold overpass the one of the usecase,then the weakness exists
        if threshold > float(ucv[int(i[7:]) - 1][2]):
            weak_list.append((weak[ucv[int(i[7:]) - 1][1] - 1][0], (threshold / ucv[int(i[7:]) - 1][4])))
    return weak_list


# we define a Risk class with getter and setter  in order to be used later in the risk calculation
class Risk:
    def __init__(self, idr, title, impact_value, probability_value, risk_value, weaknesses, assets):
        self.idr = idr
        self.title = title
        self.impact_value = impact_value
        self.probability_value = probability_value
        self.risk_value = risk_value
        self.weaknesses = weaknesses
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

    def get_weaknesses(self):
        return self.weaknesses

    def get_assets(self):
        return self.assets

    def get_risk(self):
        return {'idr': self.idr, 'title': self.title, 'impact_value': self.impact_value,
                'probability_value': self.probability_value,
                'risk_value': self.risk_value, 'weaknesses': self.weaknesses, 'assets': self.assets}


def risk_calc(weakns, risks, a_values):
    # identifying risks without adding any risk or probabilities values
    preleminary_risks = {}
    # final user risks after adding the different values
    user_risks = []
    # first loop for in order to identify the risks depending on weaknesses
    for i in risks:
        for j in i[6]:
            # if the weakness is exists in the list of weaknesses related to the risk then the risk exists
            if j in weakns:
                # if the risk already in the list we add the weakness to the weaknesses list
                # if not we add the risk o preleminary_risks
                if i[0] not in preleminary_risks:
                    preleminary_risks[i[0]] = {'weak': [j], 'risk': i}
                else:
                    preleminary_risks[i[0]]['weak'].append(j)
    # loop for to add the different values
    for i in preleminary_risks.keys():
        pv = 0
        # getting the values of the assets related to this risk
        values = []
        for j in preleminary_risks[i]['weak']:
            pv += preleminary_risks[i]['weak'][j][1]
        for k in preleminary_risks[i]['risk'][7]:
            if k in a_values.keys():
                values.append(a_values[k])
        # impact value defined as 0 and will be added later using asset_mapping
        impact_value = sum(values)
        # calculating the factor of the probability , the pourcentage of the probab
        # pv = (len(preleminary_risks[i]['weak']) / len(preleminary_risks[i]['risk'][6]))
        # calculating the new probability value depending on the number of weaknesses discovered
        probability_value = pv / len(preleminary_risks[i]['weak'])
        risk_value = impact_value * probability_value
        user_risks.append(
            Risk(preleminary_risks[i]['risk'][0], preleminary_risks[i]['risk'][1], impact_value, probability_value,
                 risk_value,
                 preleminary_risks[i]['weak'], preleminary_risks[i]['risk'][7]))
    return user_risks


@app.route('/', methods=['GET'])
@cross_origin()
def first_app():
    return json.dumps('this is a test', sort_keys=False)


@app.route('/calculator/', methods=['POST'])
@cross_origin()
def calculaterisk():
    # getting the weaknesses list from the database
    weaknesseslist = sorted(get_weaknesses(), key=lambda x: x[0])
    # Getting the list of risks from the database
    Risks = get_risks()
    # getting the  use-case weakness list from the database
    Ucv = sorted(get_uc_weaknesses(), key=lambda x: x[0])
    data = request.get_json()
    search_query = {
        "bool": {
            "must": [
                {
                    "match": {
                        "user_id": data["user_id"],
                    }
                },
                {
                    "match": {
                        "entreprise_id": data["entreprise_id"],
                    }
                },
                {
                    "match": {
                        "quiz_id": data["quiz_id"],
                    }
                },
            ]
        }
    }
    report = {'user': data["user_id"], 'entreprise': data["entreprise_id"], 'Risks': [], 'Assets': [],
              'weaknesses': [], }
    answers = es.search(index="answers", query=search_query)
    weaknesses = findweak(ucv=Ucv, weak=weaknesseslist,
                          uc_answered_question=answers['hits']['hits'][0]['_source']['answers'])
    assetvalues = assetmapping(data['entreprise_id'])
    risks = risk_calc(weakns=weaknesses, risks=Risks, a_values=assetvalues)
    for i in risks:
        report['Risks'].append(i.get_risk())
    for i in assetvalues.keys():
        asset.connect()
        report['Assets'].append({'asset_id': i, 'value': assetvalues[i],
                                 'title': asset.select(columns=['title'], primaryKey_value=i)[0][0]})
        asset.close()
    for i in weaknesses:
        report['weaknesses'].append({'weakness_id': i[0], 'title': get_weakness(i[0])[0][0]})
    infos = es.index(index="report",
                     document=report)
    return json.dumps(report, sort_keys=False), 200


if __name__ == '__main__':
    port = int(os.getenv('RUN_PORT'))
    host = os.getenv('RUN_HOST')
    app.run(debug=False, host=host, port=port)
