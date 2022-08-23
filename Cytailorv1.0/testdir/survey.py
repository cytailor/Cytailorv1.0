from flask import Flask, jsonify, request, json
from flask_restful import Api
from elasticsearch import Elasticsearch
from typing import List

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

question = [(1, 'Quel est votre modéle ?', ['B2B', 'B2C', 'B2B et B2C'], 2, 0, False),
            (2, 'Indiquez le nombre de vos clients?', ['0 - 10', '10 - 100', '100 - 1000', 'sup à 1000'], 2, 1, False),
            (3, "lister des propriétés intellectuel dont vous disposez dans l'entreprise : (checklist)",
             ['brevets', 'algorithme ou code source', 'création artistique', 'marque', 'logiciel'], 4, 0, True),
            (4, 'selectionner le types de données personnelles stockés sur vos bases de données:',
             ['nom', 'prénom', 'pseudonyme', 'date de naissance', 'photos', 'enregistrements sonores de voix',
              'numéro de téléphone fixe ou portable', 'adresse postale', 'adresse e-mail', 'adresse IP',
              'identifiant de connexion informatique ou identifiant de cookie', 'empreinte digitale',
              'réseau veineux ou palmaire de la main', 'empreinte rétinienne', 'numéro de plaque d’immatriculation',
              'numéro de sécurité sociale', 'numéro d’une pièce d’identité', 'cookies', 'orientattion sexuelle',
              'données relatives à la santé', 'orientation sexuelles', 'origine génalogique', 'orientation politique',
              'orientation religieuse'], 5, 0, True),
            (5, 'indiquer le nombre de salariée?', ['0 - 10', '10 - 100', '100 - 500', 'plus que 500'], 8, 0, False),
            (6, 'etes vous un fournisseur de service?', ['oui', 'non'], 9, 0, False),
            (7, 'si oui, quel est niveau de SLA du service que vous délivrez ?',
             ['24/7 en temps réel et niveau dedisponibilité prioche de 100%',
              'durant les horaire de travail',
              'à la demande', 'sans temps réel'],
             9, 1, False),
            (8, 'Quel sont les fournisseurs Cloud que vous utilisez pour votre business ? ',
             ['Azure', 'GCP', 'AWS', 'SAP', 'autre', 'mentionnez'], 10, 0, False),
            (9, "est ce que vous avez un siége d'entreprise ?", ['oui', 'non'], 18, 0, False),
            (10, 'est ce que vous avez un data center dédié ?', ['oui', 'non'], 18, 1, False),
            (11, 'disposez vous de certifications ISO ? si oui les spécifier', None, 20, 0, False),
            (
                12, 'est ce que vous maintenez une tableau de bord de vos indicateurs de performence ?', ['oui', 'non'],
                21,
                0, False),
            (13, 'si oui, comment est il généré ?',
             ['via un outil de reporting natif', 'en regroupant des données issue des application',
              'en utilisant des logs et un SIEM', 'manuellement remonté par les  opérationnelles'],
             21, 1, None)]


# @app.route('/api/entrepriseprofile/', methods=['GET'])
# def profile():

@app.route('/api/asset_survey/', methods=['GET', 'POST'])
def profilecreation():
    aquestions = sorted(Crud_functions.get_all_aquestion(), key=lambda x: x[0])
    schema = {
        0: 'entreprise_id',
        1: 'model',
        2: 'clients_number',
        3: 'intellectual_property',
        4: 'personal_data',
        5: 'number_of_employees',
        6: 'service_delivery',
        7: 'service_delivery_sla',
        8: 'cloud_proviider',
        9: 'physical_bulding',
        10: 'data_center',
        11: 'certifications',
        12: 'kpi',
        13: 'kpi_generation',
        14: 'personal_critical_data'
    }
    schema2 = Crud_functions.organizationprofile.columns_names()

    if request.method == 'GET':
        dictionnairea = {}

        dictionnairea = {"Assets survey": []}
        for i in aquestions:
            # key in the dictionary is a tuple(id usecase asset,title of  the asset)
            # making the question in format that will be easy readable from json file ,
            # creating list of questions for each use case as the value of the dictionary
            question_model = {'idq': i[0], 'title': i[1],
                              'choices': i[2], "asset id": i[3], 'question number': i[4], 'multiple choices ': i[5],
                              }
            dictionnairea["Assets survey"].append(question_model)
        return json.dumps(dictionnairea, sort_keys=False)
    if request.method == 'POST':
        data = requestdata = request.get_json()
        e_profile = {schema2[0]: data['entreprise_id']}
        # profile = []
        # assets = sorted(Crud_functions.get_assets(), key=lambda x: x[0])
        # sortedquestions = {}
        # for i in aquestions:
        #     if i[3] in sortedquestions.keys():
        #         sortedquestions[i[3]].append(i[0])
        #     else:
        #         sortedquestions[i[3]] = [i[0]]
        #
        # for i in assets:
        #     if i[0] in sortedquestions.keys():
        #         for j in sortedquestions[i[0]]:
        #             profile.append(data['answers'][str(j)])
        #     else:
        #         profile.append(['default'])
        # profile2 = {'entreprise_id': data['entreprise_id']}
        # for i in range(len(schema)):
        #     profile2[schema[i]] = profile[i]
        # Crud_functions.addentrepriseprofile(profile2)
        for i in data['answers'].keys():
            e_profile[schema2[int(i)]] = data['answers'][i]
        Crud_functions.addentrepriseprofile(e_profile)
        return "answers added Sucessfully", 200


@app.route('/api/take_survey/', methods=['GET'])
def uc_questions():
    vquestions = sorted(Crud_functions.get_all_vquestion(prob=True), key=lambda x: x[0])
    # if requestdata['type'] == 'assets':
    #     dictionnairea = {"Questions related to": "assets", "Questions": []}
    #     for i in aquestions:
    #         # key in the dictionary is a tuple(id usecase asset,title of  the asset)
    #         # making the question in format that will be easy readable from json file ,
    #         # creating list of questions for each use case as the value of the dictionary
    #         question_model = {'idq': i[0], 'title': i[1],
    #                           'choices': i[2], "asset id": assets[ucasset[i[3] - 1][1] - 1][0], 'multiple choices '
    #                                                                                             'question': True}
    #         dictionnairea[i[0]]["Questions"].append(question_model)
    #     return jsonify(dictionnairea)
    # if requestdata['type'] == 'Vulnerabilities':
    dictionnairev = {"Questions related to": "vulnerabilities", "Questions": []}
    for i in vquestions:
        # key in the dictionary is a tuple(id usecase asset,title of  the asset)
        question_model = {'idq': i[0], 'title': i[1], 'choices': i[2]}
        dictionnairev["Questions"].append(question_model)
    return json.dumps(dictionnairev, sort_keys=False)


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
    # assets = {}
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


@app.route('/assetmapping', methods=['GET'])
def readmappings():
    mappings = Crud_functions.getassetmapping()
    newmapping = {"Asset values": []}
    for i in mappings:
        model = {'map_id': i[0], 'asset': i[1], 'question_value': i[2], 'asset_value': i[3]}
        newmapping["Asset values"].append(model)
    return json.dumps(newmapping, sort_keys=False)


@app.route('/assetmapping/updatevalue', methods=['POST'])
def updatemappings():
    data = request.get_json()
    mappings = Crud_functions.getassetmapping()
    for i in mappings:
        if data["asset"] == i[1] and data["question_value"] == i[2]:
            data['idmap'] = i[0]
            print('done')
    Crud_functions.updateassetvalue(mapid=data['idmap'], value=data['new_asset_value'])
    return "value updated successfully", 200


@app.route('/assetmapping/add_asset_mapping', methods=['POST'])
def addmappings():
    data = request.get_json()
    Crud_functions.addassetmapping(data)
    return "asset mapping added successfully", 200


# @app.route('/assetmapping/addchoice', methods=['POST'])
# def addchoice():
#     data = request.get_json()
#     if data['update']:
#         mappings = Crud_functions.getassetmapping()
#         for i in mappings:
#             if data["mapping"]["asset"] == i[1] and data["oldchoice"] == i[2]:
#                 data['idmap'] = i[0]
#         Crud_functions.updateassetvalue(data["idmap"], data['oldchoice'])
#         Crud_functions.addnewchoice(data)
#         return 200, "choice updated successfully"
#     else:
#         Crud_functions.addassetmapping({'asset': data["asset"], 'question_value': data["new_choice"],
#                                         'asset_value': data["asset_value"]})
#         Crud_functions.addnewchoice(data)
#         return 200, "choice added successfully"

@app.route('/assetmapping/addchoice', methods=['POST'])
def addchoice():
    data = request.get_json()
    # if data['update']:
    #     mappings = Crud_functions.getassetmapping()
    #     for i in mappings:
    #         if data["mapping"]["asset"] == i[1] and data["oldchoice"] in i[2]:
    #             data['idmap'] = i[0]
    #     Crud_functions.updateassetvalue(data["idmap"], data['oldchoice'])
    #     Crud_functions.addnewchoice(data)
    #     return 200, "choice updated successfully"
    # else:
    #     Crud_functions.addassetmapping({'asset': data["asset"], 'question_value': data["new_choice"],
    #                                     'asset_value': data["asset_value"]})
    Crud_functions.addnewchoice(data)
    return "choice added successfully", 200




if __name__ == '__main__':
    # questionsinsert()
    # print(choices)
    # app.run(debug=True)
    print(Crud_functions.organizationprofile.columns_names())
    # Crud_functions.get_all_vquestion()
    # print(len(test))
