import Crud_functions
from flask import Flask, jsonify, request, json
from flask_restful import Api
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv('/Cytailorv1.0/pyvenv.cfg')

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


# ###################################asset#######################################
@app.route('/asset/', methods=['GET,PUT,POST,DELETE'])
def assets():
    if request.method == 'GET':
        assets1 = Crud_functions.get_assets()
        assets = []
        for i in assets1:
            assets.append({'ida': i[0], 'title': i[1], 'value': i[2], 'description': i[3]})
        return jsonify({"assets": assets}), 200


@app.route('/asset/', methods=['GET'])
def add_asset():
    data = request.get_json()
    owner = data['asset']['owner']
    Crud_functions.insertasset(title=data['asset']['title'], description=data['asset']['description'], ido=data,
                               value=data['asset']['value'])
    return 'asset added successfully', 200


@app.route('/asset/', methods=['GET'])
def modify_asset():
    data = request.get_json()
    Crud_functions.modify_asset(data=data)
    return 'asset updated successfully', 200


def delete_asset():
    data = request.get_json()
    Crud_functions.deleteasset(a_id=data['a_id'])
    return 'asset deleted successfully', 200


# ###################################vulnerabilities#######################################
@app.route('/vulnerabilities/', methods=['GET'])
def get_vulnerabilities():
    vulnerabilities1 = Crud_functions.get_vulnerabilities()
    vulnerabilities = []
    for i in vulnerabilities1:
        vulnerabilities.append({'idv': i[0], 'title': i[1], 'description': i[2]})
    return jsonify({"vulnerabilities": vulnerabilities}), 200


@app.route('/vulnerability/', methods=['GET'])
def add_vulnerability():
    data = request.get_json()
    Crud_functions.insertvulnerability(title=data['vulnerability']['title'],
                                       description=data['vulnerability']['description'], )
    return 'asset added successfully', 200


@app.route('/vulnerability/', methods=['GET'])
def modify_vulnerability():
    data = request.get_json()
    Crud_functions.modifyvulnerability(data=data)
    return 'vulnerability updated successfully', 200


def delete_vulnerability():
    data = request.get_json()
    Crud_functions.deletevulnerability(v_id=data['v_id'])
    return 'vulnerability deleted successfully', 200


# ###################################profile#######################################
@app.route('/profile/', methods=['GET'])
def get_org_profile():
    data = request.get_json()
    return jsonify(Crud_functions.get_organizationprofile(data["id"])), 200


@app.route('/profile/', methods=['PATCH'])
def modify_org_profile():
    data = request.get_json()
    columns = []
    values = []
    pk = data['id']
    for i in data['update']:
        columns.append(i[0])
        values.append(i[1])
    Crud_functions.modifyentrepriseprofile(columns=columns, values=values, pk=pk)
    return jsonify('profile updated successfully'), 200


def delete_org_profile():
    data = request.get_json()
    Crud_functions.delete_organization_profile(org_id=data['org_id'])
    return 'profile deleted successfully', 200


# ###################################mapping#######################################
@app.route('/mapping/', methods=['GET'])
def add_asset_mapping():
    data = request.get_json()
    Crud_functions.addassetmapping(data['mapping'])
    return jsonify("asset mapping added"), 200


@app.route('/mapping', methods=['GET'])
def get_asset_mapping():
    mapping = []
    maping1 = Crud_functions.getassetmapping()
    for i in maping1:
        mapping.append(
            {'id': i[0], 'parameter1': i[1], 'value1': i[2], 'parameter2': i[3], 'value2': i[4], 'assetid': i[5],
             'asset_value': i[6], 'operator1': i[7], 'operator2': i[8]})
    return jsonify(mapping)


@app.route('/mapping/', methods=['GET'])
def modify_asset_mapping():
    data = request.get_json()
    Crud_functions.modify_asset_value(mapping=data['mapping'], mapid=data['id'])
    return 'asset mapping updated', 200


@app.route('/mapping/', methods=['GET'])
def delete_asset_mapping():
    data = request.get_json()
    Crud_functions.deleteassetmapping(data['id'])
    return 'asset mapping deleted successfully', 200


# ###################################threshold#######################################
@app.route('/threshold/', methods=['GET'])
def modify_threshold():
    data = request.get_json()
    Crud_functions.update_threshold(uc_id=data['id'], threshold=data['threshold'])
    return 'threshold updated successfully', 200


# ###################################choice#######################################
@app.route('/choice/', methods=['GET'])
def add_choice():
    data = request.get_json()
    Crud_functions.addchoice(data=data['choice'], qid=data['question_id'])
    return 'choice added successfully', 200


@app.route('/choice/', methods=['GET'])
def get_choices():
    choices_list = Crud_functions.get_choices()
    choices = []
    for i in choices_list:
        choices.append({'Choice_id': i[0], 'Title': i[1], 'Question_id': i[2], 'Weight': i[3]})
    return json.dumps(choices, sort_keys=False), 200


@app.route('/choice/', methods=['GET'])
def modify_choice():
    data = request.get_json()
    Crud_functions.choice(data)
    return 'choice updated successfully'


@app.route('/choice/', methods=['GET'])
def delete_choice():
    data = request.get_json()
    Crud_functions.deletechoice(data)
    return 'question deleted successfully', 200


# ###################################question#######################################
@app.route('/question/', methods=['GET'])
def add_question():
    data = request.get_json()
    Crud_functions.insert_vquestion(title=data['title'], choices=data['choices'], id_uc=data['id_uc'])
    return 'question added successfully'


@app.route('/question/', methods=['GET'])
def get_question():
    data = request.get_json()
    question = Crud_functions.get_question(data['question_id'])[0]
    choices = []
    for i in question[0][3]:
        ch = Crud_functions.choice.select_all(primaryKey_value=i)[0]
        choices.append({'choice_id': ch[0], 'title': ch[1], 'weight': ch[3]})
    return json.dumps({{'choice_id': question[0], 'title': question[1], 'choices': choices}}, sort_keys=False), 200


@app.route('/question/', methods=['GET'])
def modify_question():
    data = request.get_json()
    Crud_functions.modifyquestion(data=data)
    return 'question updated successfully', 200


@app.route('/question/', methods=['GET'])
def delete_question():
    data = request.get_json()
    Crud_functions.deletequestionv(data['id'])
    return 'question deleted successfully', 200


# ###################################risk#######################################
@app.route('/risk/', methods=['GET'])
def add_risk():
    data = request.get_json()
    Crud_functions.insertrisk(title=data['risk']['title'], description=data['risk']['description'],
                              impact_value=data['risk']['impact_value'],
                              probability_value=data['risk']['probability_value'],
                              risk_value=data['risk']['risk_value'], vulnerabilities=data['risk']['vulnerabilities'],
                              assets=data['risk']['assets'])
    return 'asset added successfully', 200


@app.route('/risk/', methods=['GET'])
def get_risk():
    data = request.get_json()
    risk = Crud_functions.get_risk(data['risk_id'])[0]
    return json.dumps({{'risk_id': risk[0], 'title': risk[1], 'description': risk[2], 'impact_value': risk[3],
                        'probability_value': risk[4], 'risk_value': risk[5], 'vulnerabilities': risk[6],
                        'assets': risk[7]}}, sort_keys=False), 200


@app.route('/risk/', methods=['GET'])
def modify_risk():
    data = request.get_json()
    Crud_functions.modifyrisk(data=data)
    return 'risk updated successfully', 200


@app.route('/risk/', methods=['GET'])
def delete_risk():
    data = request.get_json()
    Crud_functions.deleterisk(r_id=data['r_id'])
    return 'risk deleted successfully', 200


# @app.route('/admin/', methods=['GET'])
# def get_previous_surveys():
#     i = 0
#
#
# @app.route('/admin/', methods=['GET'])
# def get_incomplete_survey():
#     i = 0
#
#
# @app.route('/admin/', methods=['GET'])
# def get_delegated_survey():
#     i = 0
#
#
# @app.route('/admin/', methods=['GET'])
# def delegate_survey():
#     i = 0


@app.route('/report/', methods=['GET'])
def get_report():
    data = request.get_json()
    es.search(index="answers", query={"match": {"user": data['user']}})
