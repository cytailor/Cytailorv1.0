import os

from flask import Flask, jsonify, request, json
from flask_restful import Api
from elasticsearch import Elasticsearch
from psycopg2._json import Json

from CRUD import Crud
from flask_cors import CORS, cross_origin

weakness = Crud(
    table='weakness',
    primarykey='id'
)
asset = Crud(
    table='asset',
    primarykey='id'
)
risk = Crud(
    table='risk',
    primarykey='id'
)
uc_weakness = Crud(

    table='uc_weakness',
    primarykey='id'
)
question_weakness = Crud(
    table='question_weakness',
    primarykey='id'
)

organizationprofile = Crud(
    table='organization_profile',
    primarykey='id'
)
asset_mapping = Crud(
    table='asset_mapping',
    primarykey='id'
)
choice = Crud(
    table='choice',
    primarykey='id'
)
owner = Crud(
    table='asset_owner',
    primarykey='id'
)
quiz = Crud(
    table='quiz',
    primarykey='id'
)


def get_owners():
    owner.connect()
    owners = owner.select_all()
    owner.close()
    return owners


def get_assets():
    asset.connect()
    a = asset.select_all()
    asset.close()
    return a


def get_asset(asset_id):
    asset.connect()
    a = asset.select_all(primaryKey_value=asset_id)
    asset.close()
    return a


def add_owners(ow):
    owner.connect()
    ido = owner.insert(owner_description=ow)
    owner.close()
    return ido


def insertasset(title, description, id_owner, value, source):
    asset.connect()
    asset.insert(title=title, description=description, id_owner=id_owner, value=value, source=source)
    asset.commit()
    asset.close()


def modifyasset(data):
    asset.connect()
    asset_keys = list(data['asset'].keys())
    asset_keys.remove('id')
    asset_values = list(data['asset'].values())
    asset_values.remove(data['asset']['id'])
    asset.update_multiple_columns(columns=asset_keys,
                                  columns_value=asset_values,
                                  primaryKey_value=data['asset']['id'])
    asset.commit()
    asset.close()


def deleteasset(id_asset):
    asset.connect()
    asset.delete(primaryKey_value=id_asset)
    asset.commit()
    asset.close()


def get_weaknesses():
    weakness.connect()
    v = weakness.select_all()
    weakness.close()
    return v


def insertweakness(title, description):
    weakness.connect()
    id_weakness = weakness.insert(title=title, description=description)
    weakness.commit()
    weakness.close()
    uc_weakness.connect()
    uc_weakness.insert(id=id_weakness, choices=[])
    uc_weakness.commit()
    uc_weakness.close()


def modifyweakness(data):
    weakness.connect()
    weakness_keys = list(data['weakness'].keys())
    weakness_keys.remove('idw')
    weakness_values = list(data['weakness'].values())
    weakness_values.remove(data['weakness']['id'])
    if len(weakness_keys) > 1:
        weakness.update_multiple_columns(columns=weakness_keys,
                                         columns_value=weakness_values,
                                         primaryKey_value=data['weakness']['id'])
    else:
        weakness.update(column=weakness_keys[0],
                        column_value=weakness_values[0],
                        primaryKey_value=data['weakness']['id'])
    weakness.commit()
    weakness.close()


def deleteweakness(id_weakness):
    weakness.connect()
    uc_weakness.connect()

    uc_weakness.delete2(column='idw', column_value=[id_weakness], primaryKey_value=id_weakness)
    uc_weakness.commit()
    weakness.delete(primaryKey_value=id_weakness)
    weakness.commit()
    uc_weakness.close()
    weakness.close()


def add_organizationprofile(profile):
    organizationprofile.connect()
    ido = organizationprofile.insert2(profile)
    organizationprofile.commit()
    organizationprofile.close()
    return ido


def get_organizationprofile(id_organization):
    organizationprofile.connect()
    pro = organizationprofile.select_all2(primaryKey_value=id_organization)
    organizationprofile.close()
    return pro


def modifyorganizationprofile(columns, values, id_organization):
    organizationprofile.connect()
    organizationprofile.update_multiple_columns(columns=columns, columns_value=values, primaryKey_value=id_organization)
    organizationprofile.commit()
    organizationprofile.close()


def delete_organization_profile(id_organization):
    organizationprofile.connect()
    organizationprofile.delete(primaryKey_value=id_organization)
    organizationprofile.commit()
    organizationprofile.close()


def get_organization_names():
    organizationprofile.connect()
    names = organizationprofile.select(columns=["name_A"])
    organizationprofile.close()
    return (names)


def addassetmapping(maping):
    asset_mapping.connect()
    asset_mapping.insert2(maping)
    asset_mapping.commit()
    asset_mapping.close()


def modify_asset_value(mapping, id_asset_mapping):
    asset_mapping.connect()
    asset_mapping.update_multiple_columns(columns=list(mapping.keys()), columns_value=list(mapping.values()),
                                          primaryKey_value=id_asset_mapping)
    asset_mapping.commit()
    asset_mapping.close()


def getassetmapping():
    asset_mapping.connect()
    assetmap = asset_mapping.select_all()
    asset_mapping.close()
    return assetmap


def deleteassetmapping(id_asset_mapping):
    asset_mapping.connect()
    asset_mapping.delete(primaryKey_value=id_asset_mapping)
    asset_mapping.commit()
    asset_mapping.close()


def get_uc_weakness(id_uc_weakness):
    uc_weakness.connect()
    uc = uc_weakness.select_all(id_uc_weakness)
    uc_weakness.close()
    return uc


def get_uc_weaknesses():
    uc_weakness.connect()
    uc = uc_weakness.select_all()
    uc_weakness.close()
    return uc


def get_question(question_id):
    question_weakness.connect()
    q = question_weakness.select_all(primaryKey_value=question_id)
    question_weakness.close()
    return q


def get_choice(id_choice):
    choice.connect()
    ch = choice.select_all(primaryKey_value=id_choice)
    choice.close()
    return ch


def get_weakness(id_weakness):
    weakness.connect()
    v = weakness.select_all(primaryKey_value=id_weakness)
    weakness.close()
    return v


def update_threshold(id_uc_weakness, threshold):
    uc_weakness.connect()
    uc_weakness.update(column='threshold', column_value=threshold, primaryKey_value=id_uc_weakness)
    uc_weakness.commit()
    uc_weakness.close()


def adduc(data):
    uc_weakness.connect()
    uc_weakness.insert(idw=data["usecase"]["idw"], threshold=data["usecase"]["threshold"],
                       choices=data["usecase"]["choices"], weakness_value=data["usecase"]["weakness_value"])
    uc_weakness.commit()
    uc_weakness.close()


def updateuc(data):
    uc_weakness.connect()
    uc_keys = list(data.keys())
    uc_keys.remove('id')
    uc_values = list(data.values())
    uc_values.remove(data['id'])
    print(uc_values)
    print(uc_keys)
    if len(uc_keys) > 1:
        uc_weakness.update_multiple_columns(columns=uc_keys,
                                            columns_value=uc_values,
                                            primaryKey_value=data['id'])
    else:
        uc_weakness.update(column=uc_keys[0],
                           column_value=uc_values[0],
                           primaryKey_value=data['id'])
    uc_weakness.commit()
    uc_weakness.close()


def deleteuc(ucid):
    risk.connect()
    risk.delete(primaryKey_value=ucid)
    risk.commit()
    risk.close()


def get_choices():
    choice.connect()
    ch = choice.select_all()
    choice.close()
    return ch


def addchoice(data, id_question):
    choice.connect()
    question_weakness.connect()
    choices_ids = question_weakness.select(columns=['choices', ], primaryKey_value=id_question)[0][0]
    choiceid = choice.insert2(data)
    choice.commit()
    choices_ids.append(choiceid)
    question_weakness.update(column='choices', column_value=choices_ids, primaryKey_value=id_question)
    question_weakness.commit()
    question_weakness.close()
    choice.close()


def modifychoice(data):
    choice.connect()
    choice_keys = list(data['choice'].keys())
    choice_keys.remove('id')
    choice_values = list(data['choice'].values())
    choice_values.remove(data['choice']['id'])
    choice.update_multiple_columns(columns=choice_keys,
                                   columns_value=choice_values,
                                   primaryKey_value=data['choice']['id'])
    choice.commit()
    choice.close()


def deletechoice(data):
    choice.connect()
    question_weakness.connect()
    choices_ids = question_weakness.select(columns=['choices', ], primaryKey_value=data['choice']['id_q'])[0][0]
    choices_ids.remove(data['choice']['id'])
    question_weakness.update(column='choices', column_value=choices_ids, primaryKey_value=data['choice']['id_q'])
    choice.commit()
    question_weakness.commit()
    choice.close()
    question_weakness.close()


def get_all_vquestion():
    question_weakness.connect()
    questions = question_weakness.select_all()
    question_weakness.close()
    return questions


def insert_vquestion(title, choices):
    question_weakness.connect()
    choice.connect()
    idq = question_weakness.insert(title=title,
                                   choices=[], )
    question_weakness.commit()
    ids = []
    for i in choices:
        idc = choice.insert(title=i["title"], id_q=idq, weight=i["weight"])
        ids.append(idc)
    choice.commit()
    choice.close()
    question_weakness.update(column='choices', column_value=ids, primaryKey_value=idq)
    question_weakness.commit()
    question_weakness.close()
    return idq


def modifyquestion(data):
    question_weakness.connect()
    choice.connect()
    ids = []
    choices1 = []
    ch = question_weakness.select(columns=['choices'], primaryKey_value=data['question']['id'])[0]
    for i in ch[0]:
        choices1.append(choice.select_all(primaryKey_value=i)[0])
    for i in data['question']['choices']:
        lk = list(i.keys())
        if choices1:
            for j in choices1:
                if 'id' not in lk:
                    idc = choice.insert3(title=i['title'], id_q=data['question']['id'], weight=i['weight'])
                    ids.append(idc)
                    break
                elif i['id'] == j[0] and (i['title'] != j[1] or j[3] != i['weight']):
                    choice.update_multiple_columns(columns=['title', 'weight'],
                                                   columns_value=[i['title'], i['weight']],
                                                   primaryKey_value=i['id'])
                    ids.append(i['id'])
                    break
                elif i["id"] == j[0] and i['title'] == j[1] and j[3] == i['weight']:
                    ids.append(i["id"])
                    break
        else:
            idc = choice.insert3(title=i['title'], id_q=data['question']['id'], weight=i['weight'])
            ids.append(idc)
    q_keys = list(data['question'].keys())
    q_keys.remove('id')
    print(ids)
    data['question']['choices'] = list(set(ids))
    q_values = list(data['question'].values())
    q_values.remove(data['question']['id'])
    question_weakness.update_multiple_columns(columns=q_keys,
                                              columns_value=q_values,
                                              primaryKey_value=data['question']['id'])
    choice.commit()
    choice.close()
    question_weakness.commit()
    question_weakness.close()


def deletequestionv(id_question_weakness):
    question_weakness.connect()
    uc_weakness.connect()
    choice.connect()
    uc = uc_weakness.select_all()
    for i in uc:
        changed = False
        questions = i[3]
        if questions:
            if id_question_weakness in questions:
                questions.remove(id)
                changed = True
        if changed:
            uc_weakness.update(column=['choices'], column_value=questions, primaryKey_value=i[0])
    ch = question_weakness.select(columns=['choices'], primaryKey_value=id_question_weakness)[0][0]
    for i in ch:
        choice.delete(primaryKey_value=i)
    choice.commit()
    choice.close()
    question_weakness.delete(id_question_weakness)
    uc_weakness.commit()
    question_weakness.commit()
    uc_weakness.close()
    question_weakness.close()


def get_risks():
    risk.connect()
    r = risk.select_all()
    risk.close()
    return r


def get_risk(r_id):
    risk.connect()
    r = risk.select_all(primaryKey_value=r_id)
    risk.close()
    return r


def insertrisk(title, description, impact_value, probability_value, risk_value, weaknesses, assets):
    risk.connect()
    risk.insert(title=title, description=description, impact_value=impact_value, probability_value=probability_value,
                risk_value=risk_value, weaknesses=weaknesses, assets=assets)
    risk.commit()
    risk.close()


def deleterisk(r_id):
    risk.connect()
    risk.delete(primaryKey_value=r_id)
    risk.commit()
    risk.close()


def modifyrisk(data):
    risk.connect()
    risk_keys = list(data['risk'].keys())
    risk_keys.remove('id')
    risk_values = list(data['risk'].values())
    risk_values.remove(data['risk']['id'])
    risk.update_multiple_columns(columns=risk_keys,
                                 columns_value=risk_values,
                                 primaryKey_value=data['risk']['id'])
    risk.commit()
    risk.close()


def get_quiz(quiz_id):
    quiz.connect()
    qu = quiz.select_all(primaryKey_value=quiz_id)
    quiz.close()
    return qu


def get_quizzes():
    quiz.connect()
    qu = quiz.select_all()
    quiz.close()
    return qu


def add_quiz(data):
    quiz.connect()
    quiz_questions = []
    for i in data['questions']:
        if isinstance(i, int):
            quiz_questions.append(i)
        else:
            id_question = insert_vquestion(title=i['title'], choices=i['choices'])
            quiz_questions.append(id_question)
    data['questions'] = quiz_questions
    quiz.insert2(data)
    quiz.commit()
    quiz.close()


def update_quiz(data):
    quiz.connect()
    quiz_questions = []
    for i in data['questions']:
        if isinstance(i, int):
            quiz_questions.append(i)
        else:
            id_question = insert_vquestion(title=i['title'], choices=i['choices'])
            quiz_questions.append(id_question)
    data['questions'] = quiz_questions,
    quiz_keys = list(data.keys())
    quiz_keys.remove('id')
    quiz_values = list(data.values())
    quiz_values.remove(data['id'])
    quiz.update_multiple_columns(columns=quiz_keys,
                                 columns_value=quiz_values,
                                 primaryKey_value=data['id'])
    quiz.commit()
    quiz.close()


def deletequiz(quiz_id):
    quiz.connect()
    quiz.delete(primaryKey_value=quiz_id)
    quiz.commit()
    quiz.close()


app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"*": {"origins": ["http://localhost:3000", "https://app.cytailor.io"]}})


# Create the client instance
# ELASTIC_PASSWORD = os.getenv('ELASTIC_PASSWORD')
# ELASTIC_USER = os.getenv('ELASTIC_USERNAME')
# ELASTIC_HOST = os.environ['ELASTICSEARCH_MASTER_SERVICE_HOST']
# ELASTIC_PORT = os.environ['ELASTICSEARCH_MASTER_SERVICE_PORT']
# ELASTIC_URL = 'https://' + ELASTIC_HOST + ':' + ELASTIC_PORT
#
# es = Elasticsearch(
#     ELASTIC_URL,
#     # ca_certs=os.getenv('CERT_PATH'),
#     verify_certs=bool(int(os.getenv('VERIFY_CERTS'))),
#     basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD)
# )

@app.route('/', methods=['GET'])
@cross_origin()
def first_app():
    return jsonify('this is a test')


# ###################################asset#######################################
@app.route('/model/assets', methods=['GET', 'PUT', 'POST', 'DELETE'])
@cross_origin()
# class profile(Resource:)
def crud_assets():
    if request.method == 'GET':
        assets1 = get_assets()
        assets = []
        for i in assets1:
            assets.append(
                {'id': i[0], 'title': i[1], 'description': i[2], "id_owner": i[3], 'value': i[4], 'title_fr': i[5],
                 'description_fr': i[6], 'source': i[7]})
        return jsonify({"assets": assets}), 200
    elif request.method == 'POST':
        data = request.get_json()
        owner_a = data['asset']['owner']
        owners = get_owners()
        id_owner = 0
        test = True
        for i in owners:
            if i[1] == owner_a:
                id_owner = i[0]
                test = False
        if test:
            id_owner = add_owners(owner_a)
        insertasset(title=data['asset']['title'],
                    description=data['asset']['description'],
                    id_owner=id_owner,
                    value=data['asset']['value'], source=data['asset']['source'])
        return jsonify('asset added successfully'), 200
    elif request.method == 'PUT':
        data = request.get_json()
        owners = get_owners()
        owner1 = 0
        if 'owner' in data['asset'].keys():
            for i in owners:
                if i[1] == data['asset']['owner']:
                    owner1 = i[0]
            del (data['asset']['owner'])
            data['asset']['ido'] = owner1
        modifyasset(data=data)
        return jsonify('asset updated successfully'), 200
    elif request.method == 'DELETE':
        data = request.get_json()
        deleteasset(id_asset=data['asset']['id'])
        return jsonify('asset deleted successfully'), 200


@app.route('/model/assets/<int:id_a>', methods=['GET'])
@cross_origin()
def get_asset_id(id_a):
    asset1 = get_asset(id_a)[0]
    return jsonify(
        {'id': asset1[0], 'title': asset1[1], 'value': asset1[4], 'description': asset1[2],
         "id_owner": asset1[3]},
        sort_keys=False), 200


# ###################################weaknesses#######################################
@app.route('/model/weaknesses', methods=['GET', 'PUT', 'POST', 'DELETE'])
@cross_origin()
def crud_weaknesses():
    if request.method == 'GET':
        weaknesses1 = get_weaknesses()
        weaknesses = []
        for i in weaknesses1:
            weaknesses.append(
                {'id': i[0], 'title': i[1], 'description': i[2], 'title_fr': i[3], 'description_fr': i[4]})
        return jsonify({"weaknesses": weaknesses}), 200
    elif request.method == 'POST':
        data = request.get_json()
        insertweakness(title=data['weakness']['title'],
                       description=data['weakness']['description'], )
        return jsonify('weakness added successfully'), 200
    elif request.method == 'PUT':
        data = request.get_json()
        modifyweakness(data=data)
        return jsonify('weakness updated successfully'), 200
    elif request.method == 'DELETE':
        data = request.get_json()
        deleteweakness(id_weakness=data['weakness']['id'])
        return jsonify('weakness deleted successfully'), 200


# ###################################profile#######################################
@app.route('/model/profiles', methods=['PUT', 'POST', 'DELETE'])
@cross_origin()
def crud__profile():
    if request.method == 'PUT':
        data = request.get_json()
        for i in data.keys():
            if type(data[i]) is dict:
                data[i] = Json(data[i])
            if i == 'security_team_employees_number_B' and i == 'it_department_employees_number_B':
                if data['security_team_employees_number_B'] is not None and data[
                    'it_department_employees_number_B'] is not None:
                    data['security_team_pourcentage_B'] = data['security_team_employees_number_B'] / \
                                                          data['it_department_employees_number_B']

        columns = data.keys()
        values = data.values()
        id_organization = data['id']
        modifyorganizationprofile(columns=columns, values=values, id_organization=id_organization)
        profile_updated = get_organizationprofile(id_organization)
        return jsonify(profile_updated), 200
    elif request.method == 'POST':
        data = request.get_json()
        for i in data['answers'].keys():
            if type(data['answers'][i]) is dict:
                data['answers'][i] = Json(data['answers'][i])
        if data['answers']['security_team_employees_number_B'] is not None and data['answers'][
            'it_department_employees_number_B'] is not None:
            data['answers']['security_team_pourcentage_B'] = data['answers']['security_team_employees_number_B'] / \
                                                             data['answers']['it_department_employees_number_B']
        ido = add_organizationprofile(data['answers'])
        profile_added = get_organizationprofile(ido)
        return jsonify(profile_added), 200


@app.route('/model/profiles/<int:id>', methods=['GET', 'DELETE'])
@cross_origin()
def get_profile(id):
    if request.method == 'GET':
        o_profile = get_organizationprofile(int(id))
        return jsonify(o_profile), 200
    elif request.method == 'DELETE':
        delete_organization_profile(int(id))
        return jsonify(f'profile with id {id} deleted successfully'), 200


# ###################################static_data#######################################
@app.route('/model/static_data', methods=['GET'])
@cross_origin()
def getdata():
    if request.method == 'GET':
        data = {}
        f = open('activity_domaine.json')
        data["activity_domaine"] = json.load(f)
        f.close()
        f = open('cloud_model.json')
        data["cloud_model"] = json.load(f)
        f.close()
        f = open('cloud_providers.json')
        data["cloud_providers"] = json.load(f)
        f.close()
        f = open('system_equipments.json')
        data["system_equipments"] = json.load(f)
        f.close()
        return jsonify(data)


# ###################################mapping#######################################
@app.route('/model/mappings', methods=['GET', 'PUT', 'POST', 'DELETE'])
@cross_origin()
def crud_asset_mapping():
    if request.method == 'GET':
        mapping = []
        maping1 = getassetmapping()
        for i in maping1:
            mapping.append(
                {'id': i[0], 'field1': i[1], 'field_value1': i[2], 'field2': i[3], 'field_value2': i[4],
                 'asset_id': i[5],
                 'asset_value': i[6], 'operator1': i[7], 'operator2': i[8]})
        return jsonify(mapping)
    elif request.method == 'POST':
        data = request.get_json()
        addassetmapping(data['mapping'])
        return jsonify("asset mapping added"), 200
    elif request.method == 'PUT':
        data = request.get_json()
        modify_asset_value(mapping=data['mapping'], id_asset_mapping=data['id'])
        return jsonify('asset mapping updated'), 200
    elif request.method == 'DELETE':
        data = request.get_json()
        deleteassetmapping(data['mapping']['id'])
        return jsonify('asset mapping deleted successfully'), 200


# ###################################use_case_weaknesses#######################################
@app.route('/model/usecases', methods=['GET', 'PUT', 'DELETE', 'POST'])
@cross_origin()
def usecase():
    if request.method == 'GET':
        uc = get_uc_weaknesses()
        usecases = []
        for i in uc:
            questions = []
            if i[3]:
                for j in i[3]:
                    q = get_question(j)[0]
                    choices = []
                    for k in q[2]:
                        ch = get_choice(id_choice=k)[0]
                        choices.append({'id': ch[0], 'title': ch[1], 'weight': ch[3]})
                    questions.append({'id': q[0], 'title': q[1], 'choices': choices})
            weak = get_weakness(i[1])[0]
            weaknesse1 = {'idw': weak[0], 'title': weak[1], 'description': weak[2]}
            usecases.append({'id': i[0], 'weakness': weaknesse1, 'threshold': i[2], 'questions': questions}),

        return jsonify(usecases)
    elif request.method == 'POST':
        data = request.get_json()
        adduc(data)
        return jsonify('use case added successfully'), 200
    elif request.method == 'PUT':
        data = request.get_json()
        updateuc(data['usecase'])
        return jsonify('use case updated successfully'), 200
    elif request.method == 'DELETE':
        data = request.get_json()
        deleteuc(data['usecase']['id'])
        return jsonify('use case deleted successfully'), 200


@app.route('/model/usecases/<int:id_uc>', methods=['GET'])
@cross_origin()
def one_usecase(id_uc):
    if request.method == 'GET':
        uc = get_uc_weakness(id_uc)[0]
        questions = []
        if uc[3]:
            for i in uc[3]:
                q = get_question(i)[0]
                choices = []
                for j in q[2]:
                    ch = get_choice(id_choice=j)[0]
                    choices.append({'id': ch[0], 'title': ch[1], 'weight': ch[3]})
                questions.append({'id': q[0], 'title': q[1], 'choices': choices})
        weak = get_weakness(uc[1])[0]
        weaknesse1 = {'idw': weak[0], 'title': weak[1], 'description': weak[2]}
        return jsonify({'id': uc[0], 'weakness': weaknesse1, 'threshold': uc[2], 'questions': questions},
                       sort_keys=False)


# ###################################choice#######################################
@app.route('/model/choices', methods=['GET', 'PUT', 'POST', 'DELETE'])
@cross_origin()
def crud_choice():
    if request.method == 'GET':
        choices_list = get_choices()
        choices = []
        for i in choices_list:
            choices.append({'id': i[0], 'Title': i[1], 'Question_id': i[2], 'Weight': i[3], 'Title_fr': i[4]})
        return jsonify(choices), 200

    elif request.method == 'POST':
        data = request.get_json()
        addchoice(data=data['choice'], id_question=data['choice']['id_q'])
        return jsonify('choice added successfully'), 200
    elif request.method == 'PUT':
        data = request.get_json()
        modifychoice(data)
        return jsonify('choice updated successfully'), 200
    elif request.method == 'DELETE':
        data = request.get_json()
        deletechoice(data)
        return jsonify('choice deleted successfully'), 200


# ###################################question#######################################
@app.route('/model/questions', methods=['GET', 'PUT', 'POST', 'DELETE'])
@cross_origin()
def crud_question():
    if request.method == 'GET':
        question = get_all_vquestion()
        questions = []
        for i in question:
            choices = []
            for j in i[2]:
                ch = get_choice(id_choice=j)[0]
                print(ch)
                choices.append({'id': ch[0], 'title': ch[1], 'weight': ch[3], 'title_fr': ch[4]})
            questions.append(
                {'id': i[0], 'title': i[1], 'choices': sorted(choices, key=lambda k: k['id']), 'title_fr': i[3]})
        return jsonify(sorted(questions, key=lambda k: k['id'])), 200
    elif request.method == 'POST':
        data = request.get_json()
        insert_vquestion(title=data['title'], choices=data['choices'], )
        return jsonify('question added successfully'), 200
    elif request.method == 'PUT':
        data = request.get_json()
        modifyquestion(data=data)
        return jsonify('question updated successfully'), 200
    elif request.method == 'DELETE':
        data = request.get_json()
        deletequestionv(data['question']['id'])
        return jsonify('question deleted successfully'), 200


@app.route('/model/questions/<int:id_q>', methods=['GET'])
@cross_origin()
def get_question_id(id_q):
    question = get_question(id_q)[0]
    choices = []
    for j in question[2]:
        ch = get_choice(id_choice=j)
        choices.append({'id': ch[0][0], 'title': ch[0][1], 'weight': ch[0][3]})
    return jsonify({'id': question[0], 'title': question[1], 'choices': choices},
                   sort_keys=False), 200


# ###################################risk#######################################
@app.route('/model/risks', methods=['GET', 'PUT', 'POST', 'DELETE'])
@cross_origin()
def crud_risk():
    if request.method == 'GET':
        risks = []
        risk_list = get_risks()
        for i in risk_list:
            risks.append({'id': i[0], 'title': i[1], 'description': i[2], 'impact_value': i[3],
                          'probability_value': i[4], 'risk_value': i[5], 'weaknesses': i[6],
                          'assets': i[7], 'title_fr': i[8], 'description_fr': i[9], "source": i[10]})
        return jsonify(risks), 200
    elif request.method == 'POST':
        data = request.get_json()
        insertrisk(title=data['risk']['title'], description=data['risk']['description'],
                   impact_value=data['risk']['impact_value'],
                   probability_value=data['risk']['probability_value'],
                   risk_value=data['risk']['risk_value'],
                   weaknesses=data['risk']['weaknesses'],
                   assets=data['risk']['assets'])
        return jsonify('risk added successfully'), 200
    elif request.method == 'PUT':
        data = request.get_json()
        modifyrisk(data=data)
        return jsonify('risk updated successfully'), 200
    elif request.method == 'DELETE':
        data = request.get_json()
        deleterisk(r_id=data["risk"]['id'])
        return jsonify('risk deleted successfully'), 200


@app.route('/model/risks/<int:id_r>', methods=['GET'])
@cross_origin()
def get_risk_id(id_r):
    risk_list = get_risk(id_r)[0]
    return jsonify({'risk_id': risk_list[0], 'title': risk_list[1], 'description': risk_list[2],
                    'impact_value': risk_list[3],
                    'probability_value': risk_list[4], 'risk_value': risk_list[5],
                    'weaknesses': risk_list[6],
                    'assets': risk_list[7], 'title_fr': risk_list[8], 'description_fr': risk_list[9],
                    "source": risk_list[10]}), 200


# ###################################quizzes#######################################
@app.route('/model/quizzes', methods=['GET', 'PUT', 'POST', 'DELETE'])
@cross_origin()
def crud_quiz_get():
    if request.method == 'GET':
        entreprise_id = '"cytail1'
        user_id = "user1"
        poucentage = 0
        query = {
            "bool": {
                "must": [
                    {
                        "match": {
                            "user_id": user_id,
                        }
                    },
                    {
                        "match": {
                            "entreprise_id": entreprise_id,
                        }
                    },
                ]
            }
        }
        # quizzes_history_search = es.search(index="history",
        #                                    query=query)['hits']['hits']
        quizzes_history_search = []
        quiz_list = sorted(get_quizzes(), key=lambda x: x[0])
        all_quizzes = []
        for i in quiz_list:
            single_quiz = {'id': i[0], 'title': i[1], 'description': i[2], 'question_number': len(i[3]),
                           'duration': int(len(i[3]) * 45 / 60),
                           'title_fr': i[4],
                           'description_fr': i[5], }
            for j in quizzes_history_search:
                if i[0] == j['_source']['quiz_id']:
                    poucentage = (len(j['_source']['answers'].keys()) / len(i[3])) * 100
                    single_quiz['poucentage'] = poucentage
            all_quizzes.append(single_quiz)
        return jsonify(all_quizzes)
    if request.method == 'POST':
        data = request.get_json()
        add_quiz(data)
        return jsonify('Quiz added successfully')
    if request.method == 'PUT':
        data = request.get_json()
        update_quiz(data)
        return jsonify('Quiz updated successfully')
    if request.method == 'DELETE':
        data = request.get_json()
        deletequiz(data['quiz']['id'])
        return jsonify('Quiz deleted successfully')


@app.route('/model/quizzes/<int:id_quiz>', methods=['GET'])
@cross_origin()
def quizzes_id(id_quiz):
    qu = get_quiz(id_quiz)[0]
    one_quiz = {'id': qu[0], 'title': qu[1], 'description': qu[2], 'questions': [], 'title_fr': qu[4],
                'description_fr': qu[5]}
    for i in qu[3]:
        question = get_question(i)[0]
        choices = []
        for k in question[2]:
            ch = get_choice(int(k))[0]
            choices.append({"id": ch[0], "title": ch[1], "title_fr": ch[4]})
        question_model = {'id': question[0], 'title': question[1], 'choices': choices, "title_fr": question[3]}
        one_quiz["questions"].append(question_model)
    return jsonify(one_quiz, )


# ###################################Profilenames#######################################
@app.route('/model/profilenames', methods=['GET'])
@cross_origin()
def profile_names():
    names = get_organization_names()
    return jsonify(names), 200


if __name__ == '__main__':
    port = int(os.getenv('RUN_PORT'))
    host = os.getenv('RUN_HOST')
    app.run(debug=False, host=host, port=port)
