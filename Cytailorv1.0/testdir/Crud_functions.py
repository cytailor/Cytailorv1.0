#!/usr/bin/python
import psycopg2

from CRUD import Crud


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            host="localhost",
            database="riskbase",
            user="Postges",
            password="123456789")

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        # cur.execute('SELECT version()')
        cur.execute('''SELECT * FROM vulnerability  ;''')
        cur.execute()

        # display the PostgreSQL database server version
        # db_version = cur.fetchone()
        test = cur.fetchall()
        # print(db_version)
        print(test)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


vulnerability = Crud(
    user='postgres',
    password='123456789',
    host='localhost',
    port='5432',
    dbname='riskbase',
    table='vulnerability',
    primarykey='idv'
)
asset = Crud(
    user='postgres',
    password='123456789',
    host='localhost',
    port='5432',
    dbname='riskbase',
    table='asset',
    primarykey='ida'
)
risk = Crud(
    user='postgres',
    password='123456789',
    host='localhost',
    port='5432',
    dbname='riskbase',
    table='risk',
    primarykey='idr'
)
uc_vulnerability = Crud(
    user='postgres',
    password='123456789',
    host='localhost',
    port='5432',
    dbname='riskbase',
    table='uc_vulnerability',
    primarykey='iduv'
)
uc_asset = Crud(
    user='postgres',
    password='123456789',
    host='localhost',
    port='5432',
    dbname='riskbase',
    table='uc_asset',
    primarykey='idua'
)
question_vulnerability = Crud(
    user='postgres',
    password='123456789',
    host='localhost',
    port='5432',
    dbname='riskbase',
    table='question_vulnerability',
    primarykey='idqv'
)
question_asset = Crud(
    user='postgres',
    password='123456789',
    host='localhost',
    port='5432',
    dbname='riskbase',
    table='question_asset',
    primarykey='idqa'
)
organizationprofile = Crud(
    user='postgres',
    password='123456789',
    host='localhost',
    port='5432',
    dbname='riskbase',
    table='organization_profile',
    primarykey='entreprise_id'
)
asset_mapping = Crud(
    user='postgres',
    password='123456789',
    host='localhost',
    port='5432',
    dbname='riskbase',
    table='asset_mapping',
    primarykey='map_id'
)
choice = Crud(
    user='postgres',
    password='123456789',
    host='localhost',
    port='5432',
    dbname='riskbase',
    table='choice',
    primarykey='id'
)


def get_all_vquestion(prob=False):
    question_vulnerability.connect()
    questions = question_vulnerability.select_all()
    choice.connect()
    choices = choice.select_all()
    questions_list = []
    for i in questions:
        questionmodel = [i[0], i[1], []]
        for j in choices:
            if j[2] == i[0]:
                if prob:
                    questionmodel[2].append({'choiceid': j[0], 'choice title': j[1], 'weight': j[3]})
                else:
                    questionmodel[2].append({'choice_id': j[0], 'choice_title': j[1]})
        questions_list.append(questionmodel)
    print(tuple(questions_list))
    print(len(questions_list))
    return questions_list


def get_all_aquestion():
    question_asset.connect()
    return question_asset.select_all()


def get_risks():
    risk.connect()
    return risk.select_all()


def get_assets():
    asset.connect()
    return asset.select_all()


def get_vulnerabilities():
    vulnerability.connect()
    return vulnerability.select_all()


def get_vulnerability(vid):
    vulnerability.connect()
    return vulnerability.select(columns=['title'], primaryKey_value=vid)


def get_uc_vulnerabilities():
    uc_vulnerability.connect()
    return uc_vulnerability.select_all()


def get_choices():
    choice.connect()
    return choice.select_all()


def get_question(qid):
    question_vulnerability.connect()
    return question_vulnerability.select_all(primaryKey_value=qid)


def update_threshold(uc_id, threshold):
    uc_vulnerability.connect()
    uc_vulnerability.update(column='threshold', column_value=threshold, primaryKey_value=uc_id)
    # uc_vulnerability.commit()


def insertasset(title, description, ido, value):
    asset.connect()
    ida = asset.insert(title=title, description=description, ido=ido, value=value)
    uc_asset.connect()
    uc_asset.insert(ida=ida, choices=None)
    uc_asset.commit()
    uc_asset.close()
    asset.commit()
    asset.close()


def updateuc(iduc, idq):
    uc_vulnerability.connect()
    u_case = uc_vulnerability.select(['choices'], primaryKey_value=iduc)
    if u_case[0][0] is None:
        uc_vulnerability.update(column='choices', column_value=[idq], primaryKey_value=iduc)
    else:
        choices = u_case[0][0]
        choices.append(idq)
        uc_vulnerability.update(column='choices', column_value=choices, primaryKey_value=iduc)
    uc_vulnerability.commit()
    uc_vulnerability.close()


def insertvulnerability(title, description, ido, value):
    vulnerability.connect()
    idv = vulnerability.insert(title=title, description=description, value=value, threshold=0.0)
    uc_vulnerability.connect()
    uc_vulnerability.insert(idv=idv, choices=None)
    uc_vulnerability.commit()
    uc_vulnerability.close()
    vulnerability.commit()
    vulnerability.close()


def insert_vquestion(title, choices, id_uc=None):
    question_vulnerability.connect()
    choice.connect()
    idq = question_vulnerability.insert(title=title,
                                        choices=[], )
    question_vulnerability.commit()
    ids = []
    for i in choices:
        idc = choice.insert(title=i[0], id_q=idq, weight=i[1])
        choice.commit()
        choice.close()
        ids.append(idc)
    if id_uc is not None:
        uc_vulnerability.connect()
        uc_vulnerability.update(column='choices', column_value=[idq], primaryKey_value=id_uc)
        uc_vulnerability.commit()
        uc_vulnerability.close()
    question_vulnerability.update(column='choices', column_value=ids, primaryKey_value=idq)
    question_vulnerability.commit()
    # {'idqv': '1', 'title': 'who is responsible for your security?',
    # 'choices': [('you', '0'), ('third party', '0'), ('security team', '0')], 'iduv': '1'}


def insert_aquestion(title, choices, id_uc):
    question_asset.connect()
    idq = question_asset.insert(title=title,
                                choices=choices, id_uc=id_uc)
    print(idq)
    question_asset.select_all()
    uc_asset.connect()
    uc_asset.updateuca(column_value=idq, primaryKey_value=id_uc)
    question_asset.commit()
    uc_asset.commit()
    question_asset.close()
    uc_asset.close()
    # {'idqv': '1', 'title': 'who is responsible for your security?',
    # 'choices': [('you', '0'), ('third party', '0'), ('security team', '0')], 'iduv': '1'}


def updatequestiona(data):
    question_asset.connect()
    uc_asset.connect()
    for i in data.keys():
        if i == 'title':
            question_asset.update(column='title', column_value=data[i], primaryKey_value=data['idqa'])
        elif i == 'choices':
            question_asset.update(column='choices', column_value=data[i], primaryKey_value=data['idqa'])
        elif i == 'id_uc':
            question_asset.update(column='id_uc', column_value=data[i], primaryKey_value=data['idqa'])
            ucasset = question_asset.select(columns=['id_uc'], primaryKey_value=data['idqa'])
            choices = list(uc_asset.select(columns=['choices'], primaryKey_value=ucasset[0])[0][0])
            print(choices)
            choices.remove(data['idqa'])
            question_asset.update(column='id_uc', column_value=data['id_uc'], primaryKey_value=data['idqa'])
            uc_asset.updateucaall(choices, primaryKey_value=data['id_uc'])
    question_asset.commit()
    uc_asset.commit()


def updatequestionv(data):
    question_vulnerability.connect()
    uc_vulnerability.connect()
    for i in data.keys():
        if i == 'title':
            question_vulnerability.update(column='title', column_value=data[i], primaryKey_value=data['idqv'])
        elif i == 'choices':
            question_vulnerability.update(column='choices', column_value=data[i], primaryKey_value=data['idqv'])
        elif i == 'id_uc':
            question_vulnerability.update(column='id_uc', column_value=data[i], primaryKey_value=data['idqv'])
            ucvul = question_vulnerability.select(columns=['id_uc'], primaryKey_value=data['idqv'])
            choices = list(uc_vulnerability.select(columns=['choices'], primaryKey_value=ucvul[0])[0][0])
            print(choices)
            choices.remove(data['idqv'])
            question_vulnerability.update(column='id_uc', column_value=data['id_uc'], primaryKey_value=data['idqv'])
            uc_vulnerability.updateucaall(choices, primaryKey_value=data['id_uc'])
    question_asset.commit()
    uc_asset.commit()


def deletequestiona(idqa):
    question_asset.connect()
    uc_asset.connect()
    question = question_asset.select_all(primaryKey_value=idqa)
    choices = uc_asset.select(columns=['choices', ], primaryKey_value=question[0][3])[0][0]
    choices.remove(idqa)
    uc_asset.updateucaall(choices, primaryKey_value=question[0][3])
    question_asset.delete(idqa)
    uc_asset.commit()
    question_asset.commit()


def deletequestionv(idqv):
    question_vulnerability.connect()
    uc_vulnerability.connect()
    question = question_vulnerability.select_all(primaryKey_value=idqv)
    choices = uc_vulnerability.select(columns=['choices', ], primaryKey_value=question[0][3])[0][0]
    choices.remove(idqv)
    uc_vulnerability.updateucaall(choices, primaryKey_value=question[0][3])
    question_vulnerability.delete(idqv)
    uc_vulnerability.commit()
    question_vulnerability.commit()


def addentrepriseprofile(profile):
    organizationprofile.connect()
    organizationprofile.insert2(profile)
    organizationprofile.commit()

def get_entrepriseprofile(ide):
    organizationprofile.connect()
    return organizationprofile.select_all(primaryKey_value=ide)


def getassetmapping():
    asset_mapping.connect()
    return asset_mapping.select_all()


def addassetmapping(maping):
    asset_mapping.connect()
    asset_mapping.insert2(maping)
    asset_mapping.commit()
    asset_mapping.close()


def deleteassetmapping(map_id):
    asset_mapping.connect()
    asset_mapping.delete(primaryKey_value=map_id)
    asset_mapping.commit()
    asset_mapping.close()


def updateassetvalue(mapid, value):
    asset_mapping.connect()
    asset_mapping.update(column='asset_value', column_value=value, primaryKey_value=mapid)
    asset_mapping.commit()
    asset_mapping.close()


def addnewchoice(data):
    question_asset.connect()
    choices = question_asset.select(columns=['choices', ], primaryKey_value=data['question_id'])[0][0]
    if data['oldchoice'] is None:
        choices.append(data['new_choice'])
        question_asset.update(column='choices', column_value=choices, primaryKey_value=data['question_id'])
    else:
        print(data['oldchoice'])
        print(choices)
        choices.remove(data['oldchoice'])
        choices.append(data['new_choice'])
        question_asset.update(column='choices', column_value=choices, primaryKey_value=data['question_id'])
    question_asset.commit()


if __name__ == '__main__':
    # get_all_vquestion()
    # get_all_aquestion()
    # get_risks()
    # get_assets()
    # get_vulnerabilities()
    # get_uc_assets()
    # updatequestiona({'idqa': 1, 'title': 'do you have  any HR data?', 'id_uc': 7})
    # deletequestionv(4)
    updateuc(41, 15)
    # insert_aquestion(title='do you have HR data?', choices="{'yes','no'}", id_uc=8)
    # get_uc_vulnerabilities()
    # get_risks()
    # get_question()
    # update_threshold(uc_id=1,threshold=0.9)
    # insert_vquestion()
    #   connect()
