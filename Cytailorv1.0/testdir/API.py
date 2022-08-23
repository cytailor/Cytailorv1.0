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


# @app.route('/api/take_survey/', methods=['GET'])
# def uc_questions():
#     requestdata = request.get_json()
#     aquestions = sorted(Crud_functions.get_all_aquestion(), key=lambda x: x[0])
#     vquestions = sorted(Crud_functions.get_all_vquestion(), key=lambda x: x[0])
#     vulnerabilities = sorted(Crud_functions.get_vulnerabilities(), key=lambda x: x[0])
#     assets = sorted(Crud_functions.get_assets(), key=lambda x: x[0])
#     ucasset = sorted(Crud_functions.get_uc_assets(), key=lambda x: x[0])
#     ucvulnerability = sorted(Crud_functions.get_uc_vulnerabilities(), key=lambda x: x[0])
#     dictionnairea = {}
#     dictionnairev = {}
#     if requestdata['type'] == 'assets':
#         for i in ucasset:
#             # key in the dictionary is a tuple(id usecase asset,title of  the asset)
#             dictionnairea[i[0]] = {"Asset id": assets[i[1] - 1][0], "Questions": []}
#             if i[2]:
#                 for j in i[2]:
#                     # making the question in format that will be easy readable from json file ,
#                     # creating list of questions for each use case as the value of the dictionary
#                     question_model = {'idq': aquestions[j - 1][0], 'title': aquestions[j - 1][1],
#                                       'choices': aquestions[j - 1][2]}
#                     dictionnairea[i[0]]["Questions"].append(question_model)
#         return jsonify(dictionnairea)
#     if requestdata['type'] == 'Vulnerabilities':
#         for i in ucvulnerability:
#             # key in the dictionary is a tuple(id usecase asset,title of  the asset)
#             dictionnairev = {"Questions related to ": "vulnerabilities", "Questions": []}
#             if i[3]:
#                 for j in i[3]:
#                     # making the question in format that will be easy readable from json file ,
#                     # creating list of questions for each use case as the value of the dictionary
#                     question_model = {
#                         'choices': vquestions[j - 1][2], 'idq': vquestions[j - 1][0], 'title': vquestions[j - 1][1],
#                         "Vulnerability id": vulnerabilities[i[1] - 1][0]}
#                     dictionnairev["Questions"].append(question_model)
#         print(jsonify(dictionnairev))
#         return jsonify(dictionnairev)

@app.route('/api/take_survey/', methods=['GET'])
def uc_questions():
    requestdata = request.get_json()
    aquestions = sorted(Crud_functions.get_all_aquestion(), key=lambda x: x[0])
    vquestions = sorted(Crud_functions.get_all_vquestion(), key=lambda x: x[0])
    vulnerabilities = sorted(Crud_functions.get_vulnerabilities(), key=lambda x: x[0])
    assets = sorted(Crud_functions.get_assets(), key=lambda x: x[0])
    ucasset = sorted(Crud_functions.get_uc_assets(), key=lambda x: x[0])
    ucvulnerability = sorted(Crud_functions.get_uc_vulnerabilities(), key=lambda x: x[0])
    dictionnairea = {}
    dictionnairev = {}
    if requestdata['type'] == 'assets':
        dictionnairea = {"Questions related to": "assets", "Questions": []}
        for i in aquestions:
            # key in the dictionary is a tuple(id usecase asset,title of  the asset)
            # making the question in format that will be easy readable from json file ,
            # creating list of questions for each use case as the value of the dictionary
            question_model = {'idq': i[0], 'title': i[1],
                              'choices': i[2], "asset id": assets[ucasset[i[3] - 1][1] - 1][0], 'multiple choices '
                                                                                                'question': True}
            dictionnairea[i[0]]["Questions"].append(question_model)
        return jsonify(dictionnairea)
    if requestdata['type'] == 'Vulnerabilities':
        dictionnairev = {"Questions related to": "vulnerabilities", "Questions": []}
        for i in vquestions:
            # key in the dictionary is a tuple(id usecase asset,title of  the asset)
            question_model = {
                'idq': i[0], 'title': i[1], "Vulnerability id": vulnerabilities[ucvulnerability[i[3] - 1][1] - 1][0],
                'choices': i[2], 'multiple choices question': True}
            dictionnairev["Questions"].append(question_model)
        return json.dumps(dictionnairev, sort_keys=False)


#    dictionnaire = {'Questions for assets': dictionnairea, 'Questions for vulnerabilities': dictionnairev}


@app.route('/api/CRUD/AddQ', methods=['POST'])
def addquestion():
    vulnerabilities = sorted(Crud_functions.get_vulnerabilities(), key=lambda x: x[0])
    assets = sorted(Crud_functions.get_assets(), key=lambda x: x[0])
    ucasset = sorted(Crud_functions.get_uc_assets(), key=lambda x: x[0])
    ucvulnerability = sorted(Crud_functions.get_uc_vulnerabilities(), key=lambda x: x[0])
    # getting the json file
    requestdata = request.get_json()
    # asset or a vlnerability question
    qtype = requestdata['question_type']
    if qtype == 'asset':
        asset_title = requestdata['asset_title']
        title = requestdata['title']
        choices = requestdata['choices']
        ida = 0
        iduc = 0
        for i in assets:
            # finding the id of the asset for which we have a title
            if i[1] == asset_title:
                ida = i[0]
        for i in ucasset:
            if i[1] == ida:
                iduc = i[0]
        Crud_functions.insert_aquestion(title=title, choices=choices, id_uc=iduc)
    else:
        vulnerability_title = requestdata['vulnerability_title']
        title = requestdata['title']
        choices = requestdata['choices']
        idv = 0
        iduc = 0
        for i in vulnerabilities:
            # finding the id of the asset for which we have a title
            if i[1] == vulnerability_title:
                idv = i[0]
        for i in ucvulnerability:
            if i[1] == idv:
                iduc = i[0]
        Crud_functions.insert_vquestion(title=title, choices=choices, id_uc=iduc)
    return 'Question added sucessfully', 200


@app.route('/api/CRUD/AddUC', methods=['POST'])
def adduc():
    vulnerabilities = sorted(Crud_functions.get_vulnerabilities(), key=lambda x: x[0])
    assets = sorted(Crud_functions.get_assets(), key=lambda x: x[0])
    ucasset = sorted(Crud_functions.get_uc_assets(), key=lambda x: x[0])
    ucvulnerability = sorted(Crud_functions.get_uc_vulnerabilities(), key=lambda x: x[0])
    # getting the json file
    requestdata = request.get_json()
    # asset or a vlnerability question
    uctype = requestdata['uc_type']
    if uctype == 'asset':
        asset_title = requestdata['asset_title']
        ida = 0
        iduc = 0
        for j in assets:
            # finding the id of the asset for which we have a title
            if j[1] == asset_title:
                ida = j[0]
        for j in ucasset:
            if j[1] == ida:
                iduc = j[0]
        for i in requestdata['questions']:
            title = i['title']
            choices = i['choices']
            Crud_functions.insert_aquestion(title=title, choices=choices, id_uc=iduc)
    else:
        vulnerability_title = requestdata['vulnerability_title']
        idv = 0
        iduc = 0
        for j in vulnerabilities:
            # finding the id of the asset for which we have a title
            if j[1] == vulnerability_title:
                idv = j[0]
        for j in ucvulnerability:
            if j[1] == idv:
                iduc = j[0]
        for i in requestdata['questions']:
            title = i['title']
            choices = i['choices']
            Crud_functions.insert_vquestion(title=title, choices=choices, id_uc=iduc)
    return 'Use Case added sucessfully', 200


@app.route('/api/CRUD/Adda', methods=['POST'])
def add_asset():
    ido = 0
    requestdata = request.get_json()
    owners = []
    for i in owners:
        if i[1] == requestdata['owner']:
            ido = i[0]
    Crud_functions.insertasset(description=requestdata['description'], title=requestdata['title'],
                               ido=ido,
                               value=requestdata['value'])
    return 'asset added sucessfully', 200


@app.route('/api/CRUD/Addv', methods=['POST'])
def add_vulnerability():
    requestdata = request.get_json()
    Crud_functions.insertvulnerability(description=requestdata['description'], title=requestdata['title'],
                                       ido=requestdata[''],
                                       value=requestdata['value'])
    return 'vulnerability added sucessfully', 200


@app.route('/api/CRUD/ModifyQa', methods=['POST'])
def modify_questiona():
    requestdata = request.get_json()
    if requestdata["type"] == "asset":
        Crud_functions.updatequestiona(requestdata)
    else:
        Crud_functions.updatequestionv(requestdata)
    return 'question modified sucessfully', 200


# @app.route('/api/CRUD/ModifyQv', methods=['POST'])
# def modify_questionv():
#     requestdata = request.get_json()
#     if requestdata["type"] == "asset":
#         Crud_functions.updatequestionv(requestdata)
#     else:
#
#     return 'question modified sucessfully', 200


@app.route('/api/CRUD/deleteQ', methods=['POST'])
def delete_questiona():
    requestdata = request.get_json()
    if requestdata["type"] == "asset":
        Crud_functions.deletequestiona(requestdata['idqa'])
    else:
        Crud_functions.deletequestionv(requestdata['idqv'])

    return 'question deleted sucessfully', 200


@app.route('/api/CRUD/deleteQv', methods=['POST'])
def delete_questionv():
    requestdata = request.get_json()
    Crud_functions.deletequestionv(requestdata['idqv'])
    return 'question deleted sucessfully', 200


@app.route('/api/CRUD/assets', methods=['GET'])
def assets():
    assets_list = Crud_functions.get_assets()
    dicta = []
    for i in assets_list:
        asset_model = {"id": i[0], "Title": i[1]}
        dicta.append(asset_model)
    return json.dumps(dicta, sort_keys=False), 200


@app.route('/api/CRUD/vulnerabilities', methods=['GET'])
def vulnerabilities():
    vul_list = Crud_functions.get_vulnerabilities()
    dictv = []
    for i in vul_list:
        vul_model = {"id": i[0], "Title": i[1]}
        dictv.append(vul_model)
    return json.dumps(dictv, sort_keys=False), 200


@app.route('/elastic/addanswers', methods=['PUT'])
def addanswers():
    data = request.get_json()
    # ucasset = sorted(Crud_functions.get_uc_assets(), key=lambda x: x[0])
    ucvulnerability = sorted(Crud_functions.get_uc_vulnerabilities(), key=lambda x: x[0])
    # data = {
    #     "user": "userid",
    #     "vulnerabilities": {
    #         "question1": 2,
    #         "question2": 1,
    #         "question3": 2,
    #         "question4": 1,
    #         "question5": 2,
    #         "question6": 1
    #     },
    #     "assets": {
    #         "question1": 2,
    #         "question2": 1,
    #         "question3": 2,
    #         "question4": 1,
    #         "question5": 2,
    #         "question6": 1
    #     }
    # }

    vulnerabilities = {}
    assets = {}
    # classify questions and their answers per usecase related to vulnerabilities
    for i in data["vulnerabilities"].keys():
        for j in ucvulnerability:
            if j[3]:
                if int(i[8:]) in j[3]:
                    if "usecase {}".format(j[0]) not in vulnerabilities.keys():
                        vulnerabilities["usecase {}".format(j[0])] = {}
                        print(vulnerabilities)
                        vulnerabilities["usecase {}".format(j[0])][i] = data["vulnerabilities"][i]
                        print(vulnerabilities)
                    else:
                        vulnerabilities["usecase {}".format(j[0])][i] = data["vulnerabilities"][i]
                        print(vulnerabilities)

    # classify questions and their answers per usecase related to assets
    # for i in data["assets"].keys():
    #     for j in ucasset:
    #         if j[2]:
    #             if int(i[8:]) in j[2]:
    #                 if "usecase {}".format(j[0]) not in assets.keys():
    #                     assets["usecase {}".format(j[0])] = {}
    #                     assets["usecase {}".format(j[0])][i] = data["assets"][i]
    #                 else:
    #                     assets["usecase {}".format(j[0])][i] = data["assets"][i]

   # print({"user": data["user"], "vulnerabilities": vulnerabilities, "assets": assets})
    infos = es.index(index="answers",
                     document={"user": data["user"], "vulnerabilities": vulnerabilities, })
    print(infos.raw)
    return infos.raw

User_answers = {'question1': 4, 'question2': 7, 'question3': 10, 'question4': 14, 'question5': 18, 'question6': 22,
                'question7': 25, 'question8': 32, 'question9': 35, 'question10': 38, 'question11': 42, 'question12': 48,
                'question13': 50, 'question14': 54, 'question15': 60}

@app.route('/elastic/addHistory', methods=['PUT'])
def addhistory():
    data = request.get_json()
    # data = {
    #     "user": "userid",
    #     "vulnerabilities": {
    #         "question1": 2,
    #         "question2": 1,
    #         "question3": 2,
    #         "question4": 1,
    #         "question5": 2,
    #         "question6": 1
    #     },
    #     "assets": {
    #         "question1": 2,
    #         "question2": 1,
    #         "question3": 2,
    #         "question4": 1,
    #         "question5": 2,
    #         "question6": 1
    #     }
    # "Is_completed":True
    # }

    infos = es.index(index="history",
                     document=data)
    print(infos.raw)
    return infos.raw


@app.route('/elastic/getanswers', methods=['get'])
def gethistory():
    user=request.get_json()
    resp = es.search(index="answers", query={"match": {"user": user['user']}})
    return jsonify(resp['hits']['hits'][0]['_source']), 200


@app.route('/elastic/gethistory', methods=['get'])
def getanswers():
    resp = es.search(index="history", query={"match": {"user": "userid"}})
    return jsonify(resp['hits']['hits']), 200


@app.route('/elastic/risks', methods=['put'])
def putrisks():
    data = request.get_json()

    infos = es.index(index="risk",
                     document=data)
    print(infos.raw)
    return infos.raw


@app.route('/elastic/risks', methods=['get'])
def getrisks():
    resp = es.search(index="risk", )
    return jsonify(resp['hits']['hits']), 200


if __name__ == "__main__":
    app.run(debug=True)
