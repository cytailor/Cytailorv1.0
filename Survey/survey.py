import datetime

from flask import Flask, request, json
from flask_restful import Api
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
from CRUD import Crud
import os
from flask_cors import CORS, cross_origin

load_dotenv()

organizationprofile = Crud(
    table='organization_profile',
    primarykey='id'
)
question_weakness = Crud(
    table='question_weakness',
    primarykey='id'
)
uc_weakness = Crud(

    table='uc_weakness',
    primarykey='id'
)
choice = Crud(
    table='choice',
    primarykey='id'
)
quiz = Crud(
    table='quiz',
    primarykey='id'
)


def get_all_vquestion():
    question_weakness.connect()
    q = question_weakness.select_all()
    question_weakness.close()
    return q


def get_uc_weaknesses():
    uc_weakness.connect()
    uc = uc_weakness.select_all()
    uc_weakness.close()
    return uc


def addentrepriseprofile(profile):
    organizationprofile.connect()
    organizationprofile.insert2(profile)
    organizationprofile.commit()


def get_choice(ch_id):
    choice.connect()
    ch = choice.select_all(primaryKey_value=ch_id)
    choice.close()
    return ch


def len_questions(quiz_id):
    quiz.connect()
    ch = quiz.select_all(primaryKey_value=quiz_id)[0]
    quiz.close()
    return ch[3]


def get_quizzes():
    quiz.connect()
    qu = quiz.select_all()
    quiz.close()
    return qu


def get_quiz(id_quiz):
    quiz.connect()
    qu = quiz.select_all(primaryKey_value=id_quiz)
    quiz.close()
    return qu


def get_question(question_id):
    question_weakness.connect()
    q = question_weakness.select_all(primaryKey_value=question_id)
    question_weakness.close()
    return q


app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"*": {"origins": ["http://localhost:3000", "https://app.cytailor.io"]}})

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
    basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD)
)


@app.route('/', methods=['GET'])
@cross_origin()
def first_app():
    print(1)
    e_profile = organizationprofile.organization_names()
    print(2)
    return json.dumps(e_profile, sort_keys=False), 200


@app.route('/survey/previous_survey', methods=['GET'])
@cross_origin()
def get_previous_surveys():
    entreprise_id = request.args.get('entreprise_id')
    user_id = request.args.get('user_id')
    old_quizzes = []
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
    old_quizzes_search = es.search(index="history",
                                   query=query)['hits'][
        'hits']
    print(old_quizzes_search)
    for i in old_quizzes_search:
        old_quizzes.append(i["_source"])
    return json.dumps(old_quizzes, sort_keys=False), 200


@app.route('/survey/incomplete_surveys', methods=['GET'])
@cross_origin()
def get_incomplete_survey():
    entreprise_id = request.args.get('entreprise_id')
    user_id = request.args.get('user_id')
    incomplete_quizzes = []
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
                {
                    "match": {
                        "is completed": False,
                    }
                },
            ]
        }
    }
    incomplete_quizzes_search = es.search(index="history",
                                          query=query)['hits']['hits']
    for i in incomplete_quizzes_search:
        incomplete_quizzes.append(i["_source"])
    return json.dumps(incomplete_quizzes, sort_keys=False), 200


@app.route('/survey/addanswers', methods=['PUT'])
@cross_origin()
def addanswers():
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
    delete_query = {
        "terms": {
            "_id":
                []
        }
    }
    # old_quizzes = es.search(index="history",
    #                         query={"match": {"user_id": data["user_id"], "enntreprise_id": data["enntreprise_id"],
    #                                          "quiz_id": data["quiz_id"], }})['hits']['hits'][0]
    old_quizzes = es.search(index="history", query=search_query)['hits']['hits']

    ucweakness = sorted(get_uc_weaknesses(), key=lambda x: x[0])
    u_answers = {}
    questions_number = len(data["answers"])
    questions_number_database = len(len_questions(data["quiz_id"]))
    if old_quizzes:
        print('test1')
        print(old_quizzes)
        if not bool(old_quizzes[0]["_source"]["is completed"]):
            delete_query["terms"]["_id"].append(old_quizzes[0]["_id"])
            print(delete_query)
            inf = es.delete_by_query(index="history", query=delete_query)
            # inf = es.delete_by_query(index="history", id=old_quizzes[0]["_id"], )
            print('hey')
            print(inf)
            if questions_number == questions_number_database:
                history = es.index(index="history",
                                   document={"user_id": data["user_id"], "entreprise_id": data["entreprise_id"],
                                             "quiz_id": data["quiz_id"], "timestamp": datetime.datetime.now(),
                                             "is completed": True, "answers": data["answers"], })
            else:
                history = es.index(index="history",
                                   document={"user_id": data["user_id"], "entreprise_id": data["entreprise_id"],
                                             "quiz_id": data["quiz_id"], "timestamp": datetime.datetime.now(),
                                             "is completed": False, "answers": data["answers"], })
    else:
        print(3)
        if questions_number == questions_number_database:
            print(4)
            history = es.index(index="history",
                               document={"user_id": data["user_id"], "entreprise_id": data["entreprise_id"],
                                         "quiz_id": data["quiz_id"], "timestamp": datetime.datetime.now(),
                                         "is completed": True, "answers": data["answers"], })
        else:
            print(5)
            history = es.index(index="history",
                               document={"user_id": data["user_id"], "entreprise_id": data["entreprise_id"],
                                         "quiz_id": data["quiz_id"], "timestamp": datetime.datetime.now(),
                                         "is completed": False, "answers": data["answers"], })
    if questions_number == questions_number_database:
        for i in data["answers"].keys():
            for j in ucweakness:
                if j[3]:
                    if int(i) in j[3]:
                        if "usecase {}".format(j[0]) not in u_answers.keys():
                            u_answers["usecase {}".format(j[0])] = {}
                            u_answers["usecase {}".format(j[0])][int(i)] = data["answers"][i]
                        else:
                            u_answers["usecase {}".format(j[0])][int(i)] = data["answers"][i]
        print(u_answers)
        infos = es.index(index="answers",
                         document={"user_id": data["user_id"], "entreprise_id": data["entreprise_id"],
                                   "quiz_id": data["quiz_id"], "timestamp": datetime.datetime.now(),
                                   "answers": u_answers, })
        print(infos)
        return 'Answers added to the database', 200
    return 'Answers have been added to History', 200


if __name__ == '__main__':
    port = int(os.getenv('RUN_PORT'))
    host = os.getenv('RUN_HOST')
    app.run(debug=False, host=host, port=port)
