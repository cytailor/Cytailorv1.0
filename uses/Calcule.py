import Crud_functions
from itertools import chain, combinations

ELASTIC_PASSWORD = "H*j6eoznPUYhmvmcz8LR"
# Entrprise_id: integer
# Company reputation: varchar[]
# Customer trust: varchar[]
# Employee loyalty and experience: varchar[]
# Intellectual property: varchar[]
# Personal sensitive data: varchar[]
# Personal data: varchar[]
# Personal data - critical: varchar[]
# HR data: varchar[]
# Service delivery – real time services: varchar[]
# Service delivery: varchar[]
# Access control / authentication / authorization (root/admin v others): varchar[]
# Credentials: varchar[]
# User directory (data): varchar[]
# Cloud service management interface: varchar[]
# Management interface APIs: varchar[]
# Network (connections, etc): varchar[]
# Physical hardware: varchar[]
# Physical buildings: varchar[]
# CP Application (source code): varchar[]
# Certification: varchar[]
# Operational logs (customer and cloud provider): varchar[]
# Security logs: varchar[]
# Backup or archive data: varchar[]
# Entrprise=[1,['exist'],['B2C','100-1000'],['marque','logiciel'],[],['nom','prénom','date de naissance'],[],['100-500'],
#            ['oui','24/7 en temps réel et niveau de disponibilité proche de 100%'],['exist'],['exist'],['exist'],
#            ['exist'],['exist'],['azure'],[],['exist'],['exist'],['oui','oui'],['exist'],['oui','iso27001'],
#            ['oui','via un outil de reporting natif'],['exist'],['exist'],]

Entrprise = [1, (1, ['exist']), (2, ['B2C', '100-1000'], ['marque', 'logiciel']), ...]

assetmap = [(1, 1, 1, 'high'), (2, 1, 3, 'very high')]

# Create the client instance
# es = Elasticsearch(
#     "https://localhost:9200",
#     # ca_certs="C:/Users/Public/certs/http_ca.crt",
#     verify_certs=False,
#     basic_auth=("elastic", ELASTIC_PASSWORD)
# )
# User_answers = {'username': 'Mohamed', 'userid': '01', 'date': '20/03/2022',
#                 'answersv': {'1': '2', '2': '2', '3': '1', '5': '1', '6': '3', '7': '1'},
#                 'answersa': {'1': '1', '2': '2', '3': '1', '4': '1', '5': '2', '6': '1', },
#                 'answersv_uc': {'1': [('1', '2'), ('2', '2'), ('3', '1'), ], '2': [('5', '1'), ('6', '3'), ('7', '1')]}}

User_answers = {'question1': 4, 'question2': 7, 'question3': 10, 'question4': 14, 'question5': 18, 'question6': 22,
                'question7': 25, 'question8': 32, 'question9': 35, 'question10': 38, 'question11': 42, 'question12': 48,
                'question13': 50, 'question14': 54, 'question15': 60}

# answers = es.search(index="answer001", query={"match": {"user": "userid"}})
# Vulner = sorted([{'idv': '1', 'title': 'lack of security knowledge',
#                   'description': 'the responsible of the security is not qualified to be the position'},
#                  {'idv': '2', 'title': 'intrusion point',
#                   'description': 'website is not secured'}
#                  ],
#                 key=lambda i: i['idv'])
Vulner = sorted(Crud_functions.get_vulnerabilities())
testqa = [(1, 'do you have Physical buildings?', ['yes', 'no', ], 1),
          (1, 'do you have Physical buildings?', ['yes', 'no', ], 1, [1]),
          (1, 'do you have Physical buildings?', ['yes', 'no', ], 1),
          (1, 'do you have Physical buildings?', ['yes', 'no', ], 1, [1])]

# Assets = sorted([{'ida': '1', 'title': 'Physical buildings', 'description': 'None', 'ido': '3', 'value': 'HIGH'},
# {'ida': '2', 'title': 'security logs', 'description': 'Useful as evidence of security breaches and ' 'forensics',
# 'ido': '3', 'value': 'MEDIUM'}, {'ida': '3', 'title': 'operational logs', 'description': 'Those logs used to
# sustain and optimisebusiness ' 'processesand for auditing purposes', 'ido': '1', 'value': 'MEDIUM'}, {'ida': '4',
# 'title': 'Intellectual property', 'description': 'None', 'ido': '1', 'value': 'HIGH'}, {'ida': '5',
# 'title': 'Personal sensitive data', 'description': '(as defined in European Data Protection ' 'Directive)',
# 'ido': '3', 'value': 'VERY ' 'HIGH'}, {'ida': '6', 'title': 'Service delivery –real time services', 'description':
# 'All those services that ' 'aretime critical and that ' 'need a level of availability ' 'close to 100%',
# 'ido': '1', 'value': 'VERY HIGH'}], key=lambda i: i['ida'])
Assets = sorted(Crud_functions.get_assets(), key=lambda x: x[0])
# Ucv = sorted([{'iduv': '1', 'idv': '1', 'questions': ['1', '2', '3', '4', ], 'threshold': '0.5'},
#               {'iduv': '2', 'idv': '2', 'questions': ['5', '6', '7'], 'threshold': '0.6'}], key=lambda i: i['iduv'])
Ucv = sorted(Crud_functions.get_uc_vulnerabilities(), key=lambda x: x[0])
# Uca = sorted(Crud_functions.get_uc_assets(), key=lambda x: x[0])

# Uca = [] QV = sorted([{'idqv': '1', 'title': 'who is responsible for your security?', 'choices': [('you', '0'),
# ('third party', '0'), ('security team', '0')], 'iduv': '1'}, {'idqv': '2', 'title': 'if it is a secrity team ,
# How  many employee do you have in your security team?', 'choices': [('1', '0.7'), ('2', '0.5'), ('3 or more', '0')],
# 'iduv': '1'}, {'idqv': '3', 'title': 'how many one of them is certified ?', 'choices': [('0', '0.6'),
# ('most of them', '0.3'), ('all of them', '0')], 'iduv': '1'}, {'idqv': '4', 'title': '	if it is you ,
# are you certified ?', 'choices': [('yes', '0.5'), ('no', '0')], 'iduv': '1'}, {'idqv': '5', 'title': 'Do you have a
# website ?', 'choices': [('yes', '0.5'), ('no', '0')], 'iduv': '2'}, {'idqv': '6', 'title': 'where is it hosted ?',
# 'choices': [('on the  server of the same cloud provider ', '0.6'), ('on another dedicated server', '0.1'),
# ('i have no idea', '0.8')], 'iduv': '2'}, {'idqv': '7', 'title': 'How much is your web presence important?',
# 'choices': [('very important ', '0.5'), ('normal', '0.3'), ('not too much important', '0.2')], 'iduv': '2'}, ],
# key=lambda i: i['iduv'])
QV = sorted(Crud_functions.get_all_vquestion(), key=lambda x: x[0])


# QA = sorted([{'idqa': '1', 'title': 'do you have Physical buildings?', 'choices': ['yes', 'no', ], 'ida': '1 '},
#              {'idqa': '2', 'title': 'do you keep your security logs?', 'choices': ['yes', 'no', ], 'ida': '2'},
#              {'idqa': '3', 'title': 'do you keep your operational logs?', 'choices': ['yes', 'no', ], 'ida': '3'},
#              {'idqa': '4', 'title': 'do you own Intellectual property?', 'choices': ['yes', 'no', ], 'ida': '4'},
#              {'idqa': '5', 'title': 'do you have some data that is considered sensitive?', 'choices': ['yes', 'no', ],
#               'ida': '5'},
#              {'idqa': '6', 'title': 'do you have a real time Service delivery ?', 'choices': ['yes', 'no', ],
#               'ida': '6'},
#              ], key=lambda i: i['idqa'])
# QA = sorted(Crud_functions.get_all_aquestion(), key=lambda x: x[0])


# def vul_finder(u_answers, qv, ucv, vul):
#     vul_list = []
#     # answreed questons serted by the uc id
#     uc_answered_question = {}
#     # sorting the answererd question by use case
#     for i in u_answers.keys():
#         if qv[int(i) - 1]['iduv'] in uc_answered_question.keys():
#             uc_answered_question[qv[int(i) - 1]['iduv']].append(int(i))
#         else:
#             uc_answered_question[qv[int(i)]['iduv']] = [int(i)]
#     # finding vulnerabilities by comparing each one to the seuil of the uscase
#     for i in uc_answered_question.keys():
#         # print(uc_answered_question[i])
#         threshold = 0
#         for j in uc_answered_question[i]:
#             if float(qv[j - 1]['choices'][int(u_answers[str(j)]) - 1][1]) > seuil:
#                 # print(float(qv[j - 1]['choices'][int(u_answers[str(j)]) - 1][1]))
#                 threshold = float(qv[j - 1]['choices'][int(u_answers[str(j)]) - 1][1])
#         if threshold >= float(ucv[int(i) - 1]['threshold']):
#             vul_list.append(vul[int(ucv[int(i) - 1]['idv']) - 1]['idv'])
#     return vul_list
def findvul(u_answers, ucv, vul):
    vul_list = []
    qv = sorted(Crud_functions.get_all_vquestion(), key=lambda x: x[0])
    # answreed questons sorted by the uc id
    uc_answered_question = {}
    for i in u_answers.keys():
        for j in ucv:
            if j[3] is not None:
                if int(i[8:]) in j[3]:
                    if j[0] in uc_answered_question.keys():
                        uc_answered_question[j[0]].append(int(i[8:]))
                    else:
                        uc_answered_question[j[0]] = [int(i[8:])]
    for i in uc_answered_question.keys():
        threshold = 0
        for j in uc_answered_question[i]:
            answers = Crud_functions.get_choices()
            for k in answers:
                if u_answers["question" + str(j)] == k[0]:
                    threshold = k[2]
        if threshold > ucv[i - 1][2]:
            vul_list.append(vul[ucv[i - 1][1] - 1][0])
    print(len(vul_list))
    return vul_list


def vul_finder(u_answers, qv, ucv, vul):
    vul_list = []
    # answreed questons serted by the uc id
    uc_answered_question = {}
    # sorting the answererd question by use case
    for i in u_answers.keys():
        index = 0
        for j in range(0, len(qv)):
            if qv[j][0] == int(i):
                index = j

        if qv[index][3] in uc_answered_question.keys():
            uc_answered_question[qv[index][3]].append(int(i))
        else:
            uc_answered_question[qv[index][3]] = [int(i)]
    # finding vulnerabilities by comparing each one to the threshold of the usecase
    for i in uc_answered_question.keys():
        index1 = 0
        index2 = 0
        for j in range(0, len(ucv)):
            if ucv[j][0] == int(i):
                index2 = j
        # print(uc_answered_question[i])
        threshold = 0
        for j in uc_answered_question[i]:
            index1 = 0
            for k in range(0, len(qv)):
                if qv[k][0] == int(j):
                    index1 = k
            if float(qv[index1][2][int(u_answers[str(j)]) - 1][1:-1].split(',')[1]) > threshold:
                # print(float(qv[j - 1]['choices'][int(u_answers[str(j)]) - 1][1]))
                threshold = float(qv[index1][2][int(u_answers[str(j)]) - 1][1:-1].split(',')[1])
        if threshold >= float(ucv[index2][2]):
            vul_list.append(vul[int(ucv[index2][1]) - 1][0])
            print(vul[int(ucv[index2][1]) - 1])
    return vul_list


# Functions that finds the vulnerabilities related to the user considering his answers to the questions as an input
def findvul(u_answers, ucv, vul):
    # A blank list in which we will insert the different vulnerabilities discovered
    vul_list = []
    # answreed questons sorted by the uc id
    uc_answered_question = {}
    # throught this loop we will sort the answers of the user depending on the use case to which they are related
    for i in u_answers.keys():
        for j in ucv:
            if j[3] is not None:
                # checking if the id of the question in the list of the questions related to the usecase
                if int(i[8:]) in j[3]:
                    # if the id of the usecase already exists as a key we add the question to the list of the questions,
                    # if it does not we add the usecase id as a new key
                    if j[0] in uc_answered_question.keys():
                        uc_answered_question[j[0]].append(int(i[8:]))
                    else:
                        uc_answered_question[j[0]] = [int(i[8:])]
    # we check if one of the answers weight overpass the threshold so that we know if the vulnerability exists or not
    for i in uc_answered_question.keys():
        # the threshold is defined null in the beginning
        threshold = 0
        for j in uc_answered_question[i]:
            # we extract the list of  choices from the database
            answers = Crud_functions.get_choices()
            for k in answers:
                # if the weight of the answer overpass the previous threshold ,then its weight is the new threshold
                if u_answers["question" + str(j)] == k[0]:
                    threshold = k[2]
        # if the final value of the threshold overpass the one of the usecase,then the vulnerability exists
        if threshold > ucv[i - 1][2]:
            vul_list.append(vul[ucv[i - 1][1] - 1][0])
    return vul_list


# def uc_vul_finder(answer_ucv, qv, ucv, vuln):
#     vul_list = []
#     for i in answer_ucv.keys():
#         threshold = 0
#         for j in answer_ucv[i]:
#             if float(qv[int(j[0]) - 1]['choices'][int(j[1]) - 1][1]) > threshold:
#                 threshold = float(qv[int(j[0]) - 1]['choices'][int(j[1]) - 1][1])
#         if threshold >= float(ucv[int(i) - 1]['threshold']):
#             vul_list.append(vuln[int(ucv[int(i) - 1]['idv']) - 1])
#     return vul_list

def uc_vul_finder(answer_ucv, qv, ucv, vuln):
    vul_list = []
    for i in answer_ucv.keys():
        threshold = 0
        for j in answer_ucv[i]:
            if float(qv[int(j[0]) - 1][2][int(j[1]) - 1][1:-1].split(',')[1]) > threshold:
                threshold = float(qv[int(j[0]) - 1][2][int(j[1]) - 1][1:-1].split(',')[1])
        if threshold >= float(ucv[int(i) - 1][2]):
            vul_list.append(vuln[int(ucv[int(i) - 1][1]) - 1])
    return vul_list


# def asset_finder(u_answers, qa, ass):
#     assets = []
#     for i in u_answers.keys():
#         if u_answers[i] == '1':
#             assets.append(ass[int(qa[int(i) - 1]['ida']) - 1]['ida'])
#     return assets


def asset_finder(uca_answers, qa, allassets, ucasset):
    assets = []
    for i in uca_answers.keys():
        index = 0
        if ucasset:
            for j in ucasset:
                if j[0] == int(i):
                    index = j
            asset_exist = True
            for j in uca_answers[i]:
                if j[1] == '1':
                    asset_exist = False
            if asset_exist:
                assets.append(allassets[ucasset[index][1] - 1])
    return assets


# def find_asset(answersa, qa, allasset, uc_asset):
#     assets = []
#     ucanswered = {}
#     for i in uc_asset():
#         for j in answersa:
#             if j == i[0]:
#                 if i[0] in ucanswered:
#                     ucanswered[i[0]].append(j)
#                 else:
#                     ucanswered[i[0]] = [j]
#     for i in ucanswered:
#         for j in qa


class Risk:
    def __init__(self, idr, title, impact_value, probability_value, risk_value, vulnerabilities, assets):
        self.idr = idr
        self.title = title
        self.impact_value = impact_value
        self.probability_value = probability_value
        self.risk_value = risk_value
        self.vulnerabilities = vulnerabilities
        self.assets = assets

    def get_idr(self):
        return self.idr

    def get_title(self):
        return self.title

    def get_impact_value(self):
        return self.impact_value

    def get_probability_value(self):
        return self.probability_value

    def get_value_risk(self):
        return self.risk_value

    def get_vulnerabilities(self):
        return self.vulnerabilities

    def get_assets(self):
        return self.assets

    def get_risk(self):
        return {'idr': self.idr, 'title': self.title, 'impact_value': self.impact_value,
                'probability_value': self.probability_value,
                'risk_value': self.risk_value, 'vulnerabilities': self.vulnerabilities, 'assets': self.assets}


# Risks = [Risk(idr=1, impact_value=2, probability_value=3, risk_value=5, vulnerabilities=['4', '2'], assets=['1',
# '3', '4', '5'])]
Risks = Crud_functions.get_risks()


# Risk(idr,title,description, impact_value, probability_value, risk_value, vulnerabilities, assets)


def risk_calc(vulns, risks, ):
    preleminary_risks = {}
    user_risks = []
    for i in risks:
        print(i)
        for j in i[6]:
            if j in vulns:
                if i[0] not in preleminary_risks:
                    # preleminary_risks[i[0]] = {'vul': [j], 'asset': [], 'risk': i}
                    preleminary_risks[i[0]] = {'vul': [j], 'risk': i}

                else:
                    preleminary_risks[i[0]]['vul'].append(j)

        # for j in i[7]:
        #     if str(j) in assets:
        #         if i[0] not in preleminary_risks:
        #             preleminary_risks[i[0]] = {'vul': [], 'asset': [j], 'risk': i[0]}
        #         else:
        #             preleminary_risks[i[0]]['asset'].append(j)
    for i in preleminary_risks.keys():
        risk_value = 0.0
        impact_value = 0.0
        probability_value = 0.0
        pv = (len(preleminary_risks[i]['vul']) / len(preleminary_risks[i]['risk'][6]))
        # pa = (len(preleminary_risks[i]['asset']) / len(preleminary_risks[i]['risk']['assets']))
        # impact_value = (preleminary_risks[i]['risk']['impact_value']) * pa
        probability_value = (preleminary_risks[i]['risk'][4]) * pv
        risk_value = preleminary_risks[i]['risk'][3] + probability_value
        user_risks.append(
            Risk(preleminary_risks[i]['risk'][0], preleminary_risks[i]['risk'][1], impact_value, probability_value,
                 risk_value,
                 preleminary_risks[i]['vul'], preleminary_risks[i]['risk'][7]))

    return user_risks


# def risk_calc(assets, vulns, risks, ):
#     preleminary_risks = {}
#     user_risks = []
#     for i in risks:
#         print(i.get_risk())
#         for j in i.get_vulnerabilities():
#             if str(j) in vulns:
#                 if i.get_idr() not in preleminary_risks:
#                     preleminary_risks[i.get_idr()] = {'vul': [j], 'asset': [], 'risk': i.get_risk()}
#                 else:
#                     preleminary_risks[i.get_idr()]['vul'].append(j)
#         for j in i.get_assets():
#             if str(j) in assets:
#                 if i.get_idr() not in preleminary_risks:
#                     preleminary_risks[i.get_idr()] = {'vul': [], 'asset': [j], 'risk': i.get_risk()}
#                 else:
#                     preleminary_risks[i.get_idr()]['asset'].append(j)
#     for i in preleminary_risks.keys():
#         risk_value = 0.0
#         impact_value = 0.0
#         probability_value = 0.0
#         pv = (len(preleminary_risks[i]['vul']) / len(preleminary_risks[i]['risk']['vulnerabilities']))
#         # pa = (len(preleminary_risks[i]['asset']) / len(preleminary_risks[i]['risk']['assets']))
#         # impact_value = (preleminary_risks[i]['risk']['impact_value']) * pa
#         probability_value = (preleminary_risks[i]['risk']['probability_value']) * pv
#         risk_value = impact_value + probability_value
#         user_risks.append(Risk(preleminary_risks[i]['risk']['idr'], impact_value, probability_value, risk_value,
#                                preleminary_risks[i]['vul'], preleminary_risks[i]['asset']))
#     return user_risks
def insertaquestion(title, choices, related_asset, assets, uc_asset):
    ida = 0
    idua = 0
    for i in assets:
        if i[1] == related_asset:
            ida = i[0]
    for i in uc_asset:
        if i[1] == ida:
            idua = i[0]
    Crud_functions.insert_aquestion(title=title, choices=choices, id_uc=idua)


def insertvquestion(title, choices, related_asset, assets, uc_asset):
    idv = 0
    iduv = 0
    for i in assets:
        if i[1] == related_asset:
            idv = i[0]
    for i in uc_asset:
        if i[1] == idv:
            iduv = i[0]
    Crud_functions.insert_vquestion(title=title, choices=choices, id_uc=iduv)


def powerset(list_name):
    s = list(list_name)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


if __name__ == '__main__':
    # vul = findvul(User_answers, Ucv, Vulner)
    # asset = asset_finder(User_answers['answersa'], qa=QA, allassets=Assets, ucasset=Uca)
    # uc_vul = uc_vul_finder(answer_ucv=User_answers['answersv_uc'], qv=QV, ucv=Ucv, vuln=Vulner)
    # print('the vulnerabilities that could affect you have  ids: ')
    # print(vul)
    # print(uc_vul)
    # print('your assets that could be affected are have ids:')
    # print(asset)
    # risks = risk_calc(vulns=vul, risks=Risks)
    # print('your risks are : ')
    # for i in risks:
    #     print(i.get_risk())
    sourceFile = open('cominations.txt', 'w')
    A = ["Azure",
         "GCP",
         "AWS",
         "SAP",
         "autre, mentionnez: "]

    for x in powerset(A):
        print(x, file=sourceFile)
    sourceFile.close()
    # print(answers["hits"]["hits"][1]["_source"])
