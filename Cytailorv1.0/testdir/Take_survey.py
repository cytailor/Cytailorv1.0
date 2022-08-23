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
    verify_certs=False,
    basic_auth=("elastic", ELASTIC_PASSWORD)
)


@app.route('/Take_survey/entreprise_profile/', methods=['GET', 'POST'])
def profilecreation():
    schema2 = Crud_functions.organizationprofile.columns_names()

    if request.method == 'GET':
        requestdata = request.get_json()
        organizationdata = Crud_functions.organizationprofile.select_all(primaryKey_value=requestdata['entreprise_id'])[
            0]
        organizationprofile = {}
        print(organizationdata)
        for i in range(len(schema2.values()) - 2):
            # key in the dictionary is a tuple(id usecase asset,title of  the asset)
            # making the question in format that will be easy readable from json file ,
            # creating list of questions for each use case as the value of the dictionary
            print(i)
            organizationprofile[schema2[i]] = organizationdata[i]
        return json.dumps(organizationprofile, sort_keys=False)
    if request.method == 'POST':
        data = request.get_json()
        e_profile = {schema2[0]: data['entreprise_id']}
        for i in data['answers'].keys():
            e_profile[schema2[int(i)]] = data['answers'][i]
            print(schema2)
        print(e_profile)
        Crud_functions.addentrepriseprofile(e_profile)
        return "Organization Profile added Sucessfully", 200


@app.route('/take_survey/get_questions', methods=['GET'])
def questions():
    vquestions = sorted(Crud_functions.get_all_vquestion(prob=True), key=lambda x: x[0])

    dictionnairev = {"Questions related to": "vulnerabilities", "Questions": []}
    for i in vquestions:
        question_model = {'idq': i[0], 'title': i[1], 'choices': i[2]}
        dictionnairev["Questions"].append(question_model)
    return json.dumps(dictionnairev, sort_keys=False)


@app.route('/take_survey/addanswers', methods=['PUT'])
def addanswers():
    data = request.get_json()
    ucvulnerability = sorted(Crud_functions.get_uc_vulnerabilities(), key=lambda x: x[0])
    vulnerabilities = {}
    # history = es.index(index="history",
    #                    document=data)
    if data['_is_completed']:
        for i in data["vulnerabilities"]:
            for j in ucvulnerability:
                if j[3]:
                    if int(i[0]) in j[3]:
                        if "usecase {}".format(j[0]) not in vulnerabilities.keys():
                            vulnerabilities["usecase {}".format(j[0])] = {}
                            # print(vulnerabilities)
                            print(vulnerabilities)
                            vulnerabilities["usecase {}".format(j[0])][i[0]] = i[1]
                            # print(vulnerabilities)
                        else:
                            vulnerabilities["usecase {}".format(j[0])][i[0]] = i[1]
        infos = es.index(index="answers",
                         document={"user": data["user"], "vulnerabilities": vulnerabilities, })
        print(vulnerabilities)
        print(infos)
        return 'Answers added to the database', 200
    return 'Answers have been added to History'


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=4000)
