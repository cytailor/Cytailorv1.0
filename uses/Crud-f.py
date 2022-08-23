#!/usr/bin/python
from CRUD import Crud

vulnerability = Crud(
    table='vulnerability',
    primarykey='idv'
)
asset = Crud(
    table='asset',
    primarykey='ida'
)
risk = Crud(
    table='risk',
    primarykey='idr'
)
uc_vulnerability = Crud(

    table='uc_vulnerability',
    primarykey='iduv'
)
uc_asset = Crud(
    table='uc_asset',
    primarykey='idua'
)
question_vulnerability = Crud(
    table='question_vulnerability',
    primarykey='idqv'
)
question_asset = Crud(
    table='question_asset',
    primarykey='idqa'
)
organizationprofile = Crud(
    table='organization_profile',
    primarykey='entreprise_id'
)
asset_mapping = Crud(
    table='asset_mapping',
    primarykey='map_id'
)
choice = Crud(
    table='choice',
    primarykey='id'
)
owner = Crud(
    table='asset_owner',
    primarykey='id'
)


def get_all_vquestion(prob=False):
    question_vulnerability.connect()
    questions = question_vulnerability.select_all()
    question_vulnerability.close()
    return questions


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
    return vulnerability.select_all(primaryKey_value=vid)


def get_risk(r_id):
    risk.connect()
    r = risk.select_all(primaryKey_value=r_id)
    risk.close()
    return r


def get_uc_vulnerabilities():
    uc_vulnerability.connect()
    uc = uc_vulnerability.select_all()
    uc_vulnerability.close()
    return uc


def get_uc_vulnerability(uc_id):
    uc_vulnerability.connect()
    uc = uc_vulnerability.select_all(uc_id)
    uc_vulnerability.close()
    return uc


def get_choices():
    choice.connect()
    return choice.select_all()


def get_question(qid):
    question_vulnerability.connect()
    return question_vulnerability.select_all(primaryKey_value=qid)


def update_threshold(uc_id, threshold):
    uc_vulnerability.connect()
    uc_vulnerability.update(column='threshold', column_value=threshold, primaryKey_value=uc_id)
    uc_vulnerability.commit()
    uc_vulnerability.close()


def insertasset(title, description, ido, value):
    asset.connect()
    ida = asset.insert(title=title, description=description, ido=ido, value=value)
    asset.commit()
    asset.close()


def updateuc(data):
    uc_vulnerability.connect()
    uc_keys = list(data.keys())
    uc_keys.remove('iduv')
    uc_values = list(data.values())
    uc_values.remove(data['iduv'])
    print(uc_values)
    print(uc_keys)
    if len(uc_keys) > 1:
        uc_vulnerability.update_multiple_columns(columns=uc_keys,
                                                 columns_value=uc_values,
                                                 primaryKey_value=data['iduv'])
    else:
        uc_vulnerability.update(column=uc_keys[0],
                                column_value=uc_values[0],
                                primaryKey_value=data['iduv'])
    uc_vulnerability.commit()
    uc_vulnerability.close()


def insertvulnerability(title, description, ):
    vulnerability.connect()
    idv = vulnerability.insert(title=title, description=description, )
    vulnerability.commit()
    vulnerability.close()
    uc_vulnerability.connect()
    uc_vulnerability.insert(idv=idv, choices=[])
    uc_vulnerability.commit()
    uc_vulnerability.close()


def insertrisk(title, description, impact_value, probability_value, risk_value, vulnerabilities, assets):
    risk.connect()
    risk.insert(title=title, description=description, impact_value=impact_value, probability_value=probability_value,
                risk_value=risk_value, vulnerabilities=vulnerabilities, assets=assets)
    risk.commit()
    risk.close()


def get_owners():
    owner.connect()
    owners = owner.select_all()
    owner.close()
    return owners


def add_owners(ow):
    owner.connect()
    ido = owner.insert3(owner_description=ow)
    owner.close()
    return ido


def insert_vquestion(title, choices):
    question_vulnerability.connect()
    choice.connect()
    idq = question_vulnerability.insert(title=title,
                                        choices=[], )
    question_vulnerability.commit()
    ids = []
    for i in choices:
        idc = choice.insert(title=i["title"], id_q=idq, weight=i["weight"])
        ids.append(idc)
    choice.commit()
    choice.close()
    question_vulnerability.update(column='choices', column_value=ids, primaryKey_value=idq)
    question_vulnerability.commit()
    question_vulnerability.close()
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
    choice.connect()
    uc = uc_vulnerability.select_all()
    for i in uc:
        changed = False
        questions = i[3]
        if questions:
            if idqv in questions:
                questions.remove(idqv)
                changed = True
        if changed:
            uc_vulnerability.update(column=['choices'], column_value=questions, primaryKey_value=i[0])
    ch = question_vulnerability.select(columns=['choices'], primaryKey_value=idqv)[0][0]
    print(ch)
    for i in ch:
        choice.delete(primaryKey_value=i)
    choice.commit()
    choice.close()
    question_vulnerability.delete(idqv)
    uc_vulnerability.commit()
    question_vulnerability.commit()
    uc_vulnerability.close()
    question_vulnerability.close()


def addentrepriseprofile(profile):
    organizationprofile.connect()
    organizationprofile.insert2(profile)
    organizationprofile.commit()


def modifyentrepriseprofile(columns, values, pk):
    organizationprofile.connect()
    organizationprofile.update_multiple_columns(columns=columns, columns_value=values, primaryKey_value=pk)
    organizationprofile.commit()


def get_organizationprofile(ide):
    organizationprofile.connect()
    return organizationprofile.select_all(primaryKey_value=ide)


def getassetmapping():
    asset_mapping.connect()
    assetmap = asset_mapping.select_all()
    asset_mapping.close()
    return assetmap


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


def modify_asset_value(mapping, mapid):
    asset_mapping.connect()
    asset_mapping.update_multiple_columns(columns=list(mapping.keys()), columns_value=list(mapping.values()),
                                          primaryKey_value=mapid)
    asset_mapping.commit()
    asset_mapping.close()


def addnewchoice(data):
    question_vulnerability.connect()
    choices = question_vulnerability.select(columns=['choices', ], primaryKey_value=data['question_id'])[0][0]
    if data['oldchoice'] is None:
        choices.append(data['new_choice'])
        question_vulnerability.update(column='choices', column_value=choices, primaryKey_value=data['question_id'])
    else:
        print(data['oldchoice'])
        print(choices)
        choices.remove(data['oldchoice'])
        choices.append(data['new_choice'])
        question_vulnerability.update(column='choices', column_value=choices, primaryKey_value=data['question_id'])
    question_vulnerability.commit()
    question_vulnerability.close()


def get_choice(ch_id):
    choice.connect()
    ch = choice.select_all(primaryKey_value=ch_id)
    choice.close()
    return ch


def addchoice(data, qid):
    choice.connect()
    question_vulnerability.connect()
    choices_ids = question_vulnerability.select(columns=['choices', ], primaryKey_value=qid)[0][0]
    choiceid = choice.insert2(data)
    choice.commit()
    choices_ids.append(choiceid)
    question_vulnerability.update(column='choices', column_value=choices_ids, primaryKey_value=qid)
    question_vulnerability.commit()
    question_vulnerability.close()
    choice.close()


def deletechoice(data):
    choice.connect()
    question_vulnerability.connect()
    choices_ids = question_vulnerability.select(columns=['choices', ], primaryKey_value=16)[0][0]
    choices_ids.remove(data['choice']['id'])
    question_vulnerability.update(column='choices', column_value=choices_ids, primaryKey_value=data['choice']['id_q'])
    choice.commit()
    question_vulnerability.commit()
    choice.close()
    question_vulnerability.close()


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


def modifyrisk(data):
    risk.connect()
    risk_keys = list(data['risk'].keys())
    risk_keys.remove('idr')
    risk_values = list(data['risk'].values())
    risk_values.remove(data['risk']['idr'])
    risk.update_multiple_columns(columns=risk_keys,
                                 columns_value=risk_values,
                                 primaryKey_value=data['risk']['idr'])
    risk.commit()
    risk.close()


def modifyasset(data):
    asset.connect()
    asset_keys = list(data['asset'].keys())
    asset_keys.remove('ida')
    asset_values = list(data['asset'].values())
    asset_values.remove(data['asset']['ida'])
    asset.update_multiple_columns(columns=asset_keys,
                                  columns_value=asset_values,
                                  primaryKey_value=data['asset']['ida'])
    asset.commit()
    asset.close()


def modifyvulnerability(data):
    vulnerability.connect()
    vulnerability_keys = list(data['vulnerability'].keys())
    vulnerability_keys.remove('idv')
    vulnerability_values = list(data['vulnerability'].values())
    vulnerability_values.remove(data['vulnerability']['idv'])
    if len(vulnerability_keys) > 1:
        vulnerability.update_multiple_columns(columns=vulnerability_keys,
                                              columns_value=vulnerability_values,
                                              primaryKey_value=data['vulnerability']['idv'])
    else:
        vulnerability.update(column=vulnerability_keys[0],
                             column_value=vulnerability_values[0],
                             primaryKey_value=data['vulnerability']['idv'])
    vulnerability.commit()
    vulnerability.close()


def modifyquestion(data):
    question_vulnerability.connect()
    choice.connect()
    ids = []
    choices1 = []
    ch = question_vulnerability.select(columns=['choices'], primaryKey_value=data['question']['idqv'])[0]
    for i in ch[0]:
        choices1.append(choice.select_all(primaryKey_value=i)[0])
    for i in data['question']['choices']:
        l = list(i.keys())
        if choices1:
            for j in choices1:
                if 'id' not in l:
                    idc = choice.insert3(title=i['title'], id_q=data['question']['idqv'], weight=i['weight'])
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
            idc = choice.insert3(title=i['title'], id_q=data['question']['idqv'], weight=i['weight'])
            ids.append(idc)
    q_keys = list(data['question'].keys())
    q_keys.remove('idqv')
    print(ids)
    data['question']['choices'] = list(set(ids))
    q_values = list(data['question'].values())
    q_values.remove(data['question']['idqv'])
    question_vulnerability.update_multiple_columns(columns=q_keys,
                                                   columns_value=q_values,
                                                   primaryKey_value=data['question']['idqv'])
    choice.commit()
    choice.close()
    question_vulnerability.commit()
    question_vulnerability.close()


def deleterisk(r_id):
    risk.connect()
    risk.delete(primaryKey_value=r_id)
    risk.commit()
    risk.close()


def deleteasset(a_id):
    asset.connect()
    asset.delete(primaryKey_value=a_id)
    asset.commit()
    asset.close()


def deletevulnerability(idv):
    vulnerability.connect()
    uc_vulnerability.connect()
    uc_vulnerability.delete(primaryKey_value=idv)
    uc_vulnerability.commit()
    vulnerability.delete(primaryKey_value=idv)
    vulnerability.commit()
    uc_vulnerability.close()
    vulnerability.close()


def delete_organization_profile(org_id):
    organizationprofile.connect()
    organizationprofile.delete(primaryKey_value=org_id)
    organizationprofile.commit()
    organizationprofile.close()


if __name__ == '__main__':
    # get_all_vquestion()
    get_all_aquestion()
    # get_risks()
    # get_assets()
    # get_vulnerabilities()
    # get_uc_assets()
    # updatequestiona({'idqa': 1, 'title': 'do you have  any HR data?', 'id_uc': 7})
    # deletequestionv(4)
    # updateuc(41, 15)
    # insert_aquestion(title='do you have HR data?', choices="{'yes','no'}", id_uc=8)
    # get_uc_vulnerabilities()
    # get_risks()
    # get_question()
    # update_threshold(uc_id=1,threshold=0.9)
    # insert_vquestion()
    #   connect()
