import os

import Crud_functions
from flask import Flask, jsonify, request, json
from flask_restful import Api
from elasticsearch import Elasticsearch

# load_dotenv('/home/boudors6/Desktop/Cytailorv1.0/Cytailorv1.0/pyvenv.cfg')

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
@app.route('/asset/', methods=['GET', 'PUT', 'POST', 'DELETE'])
def crud_assets():
    if request.method == 'GET':
        assets1 = Crud_functions.get_assets()
        assets = []
        for i in assets1:
            assets.append({'ida': i[0], 'title': i[1], 'value': i[2], 'description': i[3]})
        return json.dumps({"assets": assets}, sort_keys=False), 200
    elif request.method == 'POST':
        data = request.get_json()
        owner = data['asset']['owner']
        owners = Crud_functions.get_owners()
        ido = 0
        test = True
        for i in owners:
            if i[1] == owner:
                ido = i[0]
                test = False
        if test:
            ido = Crud_functions.add_owners(owner)
        Crud_functions.insertasset(title=data['asset']['title'], description=data['asset']['description'], ido=ido,
                                   value=data['asset']['value'])
        return 'asset added successfully', 200
    elif request.method == 'PUT':
        data = request.get_json()
        Crud_functions.modifyasset(data=data)
        return 'asset updated successfully', 200
    elif request.method == 'DELETE':
        data = request.get_json()
        Crud_functions.deleteasset(a_id=data['asset_id'])
        return 'asset deleted successfully', 200


# ###################################vulnerabilities#######################################
@app.route('/vulnerabilities/', methods=['GET', 'PUT', 'POST', 'DELETE'])
def crud_vulnerabilities():
    if request.method == 'GET':
        vulnerabilities1 = Crud_functions.get_vulnerabilities()
        vulnerabilities = []
        for i in vulnerabilities1:
            vulnerabilities.append({'idv': i[0], 'title': i[1], 'description': i[2]})
        return json.dumps({"vulnerabilities": vulnerabilities}, sort_keys=False), 200
    elif request.method == 'POST':
        data = request.get_json()
        Crud_functions.insertvulnerability(title=data['vulnerability']['title'],
                                           description=data['vulnerability']['description'], )
        return 'vulnerability added successfully', 200
    elif request.method == 'PUT':
        data = request.get_json()
        Crud_functions.modifyvulnerability(data=data)
        return 'vulnerability updated successfully', 200
    elif request.method == 'DELETE':
        data = request.get_json()
        Crud_functions.deletevulnerability(idv=data['vulnerability']['idv'])
        return 'vulnerability deleted successfully', 200


# ###################################profile#######################################
@app.route('/profile/', methods=['GET', 'PUT', 'DELETE'])
def crud__profile():
    if request.method == 'GET':
        data = request.get_json()
        return json.dumps(Crud_functions.get_organizationprofile(data["id"]), sort_keys=False), 200
    elif request.method == 'PUT':
        data = request.get_json()
        columns = []
        values = []
        pk = data['id']
        for i in data['update']:
            columns.append(i[0])
            values.append(i[1])
        Crud_functions.modifyentrepriseprofile(columns=columns, values=values, pk=pk)
        return jsonify('profile updated successfully'), 200
    elif request.method == 'DELETE':
        data = request.get_json()
        Crud_functions.delete_organization_profile(org_id=data['id'])
        return 'profile deleted successfully', 200


# ###################################mapping#######################################
@app.route('/mapping/', methods=['GET', 'PUT', 'POST', 'DELETE'])
def crud_asset_mapping():
    if request.method == 'GET':
        mapping = []
        maping1 = Crud_functions.getassetmapping()
        names = list(Crud_functions.asset_mapping.mapping_names().values())
        for i in maping1:
            mapping.append(
                {'map_id': i[0], 'field1': i[1], 'field_value1': i[2], 'field2': i[3], 'field_value2': i[4],
                 'asset_id': i[5],
                 'asset_value': i[6], 'operator1': i[7], 'operator2': i[8]})
        return json.dumps(mapping, sort_keys=False)
    elif request.method == 'POST':
        data = request.get_json()
        Crud_functions.addassetmapping(data['mapping'])
        return jsonify("asset mapping added"), 200
    elif request.method == 'PUT':
        data = request.get_json()
        Crud_functions.modify_asset_value(mapping=data['mapping'], mapid=data['id'])
        return 'asset mapping updated', 200
    elif request.method == 'DELETE':
        data = request.get_json()
        Crud_functions.deleteassetmapping(data['id'])
        return 'asset mapping deleted successfully', 200


# ###################################use_case vulnerabilities#######################################
@app.route('/usecase/', methods=['GET', 'PUT'])
def usecase():
    if request.method == 'GET':
        data = request.get_json()
        uc = Crud_functions.get_uc_vulnerability(data['iduv'])[0]
        questions = []
        for i in uc[3]:
            q = Crud_functions.get_question(i)[0]
            choices = []
            for j in q[2]:
                ch = Crud_functions.get_choice(ch_id=j)[0]
                choices.append({'choice_id': ch[0], 'title': ch[1], 'weight': ch[3]})
            questions.append({'question_id': q[0], 'title': q[1], 'choices': choices})
        vul = Crud_functions.get_vulnerability(uc[1])
        return json.dumps({'iduv': uc[0], 'vulnerability': vul, 'threshold': uc[2], 'questions': questions},
                          sort_keys=False)
    elif request.method == 'PUT':
        data = request.get_json()
        usecase1 = Crud_functions.get_uc_vulnerability(data['use_case']['iduv'])
        if set(data['use_case']['choices']) == set(usecase1[0][3]):
            Crud_functions.update_threshold(uc_id=data['use_case']['iduv'], threshold=data['use_case']['threshold'])
        else:
            print('test')
            Crud_functions.updateuc(data=data['use_case'])
        return 'use case updated successfully', 200


# ###################################choice#######################################
@app.route('/choice/', methods=['GET', 'PUT', 'POST', 'DELETE'])
def crud_choice():
    if request.method == 'GET':
        choices_list = Crud_functions.get_choices()
        choices = []
        for i in choices_list:
            choices.append({'Choice_id': i[0], 'Title': i[1], 'Question_id': i[2], 'Weight': i[3]})
        return json.dumps(choices, sort_keys=False), 200

    elif request.method == 'POST':
        data = request.get_json()
        Crud_functions.addchoice(data=data['choice'], qid=data['choice']['id_q'])
        return 'choice added successfully', 200
    elif request.method == 'PUT':
        data = request.get_json()
        Crud_functions.modifychoice(data)
        return 'choice updated successfully'
    elif request.method == 'DELETE':
        data = request.get_json()
        Crud_functions.deletechoice(data)
        return 'choice deleted successfully', 200


# ###################################question#######################################
@app.route('/question/', methods=['GET', 'PUT', 'POST', 'DELETE'])
def crud_question():
    if request.method == 'GET':
        data = request.get_json()
        if data == {}:
            question = Crud_functions.get_all_vquestion()
            questions = []
            for i in question:
                choices = []
                for j in i[2]:
                    ch = Crud_functions.get_choice(ch_id=j)
                    print(ch)
                    choices.append({'choice_id': ch[0][0], 'title': ch[0][1], 'weight': ch[0][3]})
                questions.append({'question_id': i[0], 'title': i[1], 'choices': sorted(choices, key=lambda k: k['choice_id'])})
            return json.dumps(sorted(questions, key=lambda k: k['question_id']), sort_keys=False), 200

        else:
            question = Crud_functions.get_question(data['id_qv'])[0]
            choices = []
            for j in question[2]:
                ch = Crud_functions.get_choice(ch_id=j)
                choices.append({'choice_id': ch[0][0], 'title': ch[0][1], 'weight': ch[0][3]})
            return json.dumps({'question_id': question[0], 'title': question[1], 'choices': choices},
                              sort_keys=False), 200
    elif request.method == 'POST':
        data = request.get_json()
        Crud_functions.insert_vquestion(title=data['title'], choices=data['choices'], )
        return 'question added successfully'
    elif request.method == 'PUT':
        data = request.get_json()
        Crud_functions.modifyquestion(data=data)
        return 'question updated successfully', 200
    elif request.method == 'DELETE':
        data = request.get_json()
        Crud_functions.deletequestionv(data['question']['id'])
        return 'question deleted successfully', 200


# ###################################risk#######################################
@app.route('/risk/', methods=['GET', 'PUT', 'POST', 'DELETE'])
def crud_risk():
    if request.method == 'GET':
        data = request.get_json()
        if data == {}:
            risks = []
            risk = Crud_functions.get_risks()
            for i in risk:
                risks.append({'risk_id': i[0], 'title': i[1], 'description': i[2], 'impact_value': i[3],
                              'probability_value': i[4], 'risk_value': i[5], 'vulnerabilities': i[6],
                              'assets': i[7]})
            return json.dumps(risks, sort_keys=False), 200
        else:
            risk = Crud_functions.get_risk(data['idr'])[0]
            return json.dumps({'risk_id': risk[0], 'title': risk[1], 'description': risk[2], 'impact_value': risk[3],
                               'probability_value': risk[4], 'risk_value': risk[5], 'vulnerabilities': risk[6],
                               'assets': risk[7]}, sort_keys=False), 200
    elif request.method == 'POST':
        data = request.get_json()
        Crud_functions.insertrisk(title=data['risk']['title'], description=data['risk']['description'],
                                  impact_value=data['risk']['impact_value'],
                                  probability_value=data['risk']['probability_value'],
                                  risk_value=data['risk']['risk_value'],
                                  vulnerabilities=data['risk']['vulnerabilities'],
                                  assets=data['risk']['assets'])
        return 'risk added successfully', 200
    elif request.method == 'PUT':
        data = request.get_json()
        Crud_functions.modifyrisk(data=data)
        return 'risk updated successfully', 200
    elif request.method == 'DELETE':
        data = request.get_json()
        Crud_functions.deleterisk(r_id=data['idr'])
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
    report= es.search(index="answers", query={"match": {"user": data['user']}})
    return jsonify(report)


if __name__ == '__main__':
    port = int(os.getenv('RUN_PORT'))
    host = os.getenv('RUN_HOST')
    app.run(debug=False, host=host, port=port)
