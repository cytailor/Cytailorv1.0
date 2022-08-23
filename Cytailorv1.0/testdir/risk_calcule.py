User_answers = {'username': 'Mohamed', 'userid': '01', 'date': '20/03/2022',
                'answersv': {'1': '2', '2': '2', '3': '1', '5': '1', '6': '3', '7': '1'},
                'answersa': {'1': '1', '2': '2', '3': '1', '4': '1', '5': '2', '6': '1', }}

Vulner = sorted([{'idv': '1', 'title': 'lack of security knowledge',
                  'description': 'the responsible of the security is not qualified to be the position'},
                 {'idv': '2', 'title': 'intrusion point',
                  'description': 'website is not secured'}
                 ],
                key=lambda i: i['idv'])
Assets = sorted([{'ida': '1', 'title': 'Physical buildings', 'description': 'None', 'ido': '3', 'value': 'HIGH'},
                 {'ida': '2', 'title': 'security logs',
                  'description': 'Useful as evidence of security breaches and ' 'forensics',
                  'ido': '3', 'value': 'MEDIUM'}, {'ida': '3', 'title': 'operational logs',
                                                   'description': 'Those logs used to sustain and optimisebusiness ' 'processesand for auditing purposes',
                                                   'ido': '1', 'value': 'MEDIUM'}, {'ida': '4',
                                                                                    'title': 'Intellectual property',
                                                                                    'description': 'None', 'ido': '1',
                                                                                    'value': 'HIGH'}, {'ida': '5',
                                                                                                       'title': 'Personal sensitive data',
                                                                                                       'description': '(as defined in European Data Protection ' 'Directive)',
                                                                                                       'ido': '3',
                                                                                                       'value': 'VERY ' 'HIGH'},
                 {'ida': '6', 'title': 'Service delivery –real time services', 'description':
                     'All those services that ' 'aretime critical and that ' 'need a level of availability ' 'close to 100%',
                  'ido': '1', 'value': 'VERY HIGH'}], key=lambda i: i['ida'])
Ucv = sorted([{'iduv': '1', 'idv': '1', 'questions': ['1', '2', '3', '4', ], 'threshold': '0.5'},
              {'iduv': '2', 'idv': '2', 'questions': ['5', '6', '7'], 'threshold': '0.6'}], key=lambda i: i['iduv'])
Uca = []
QV = sorted([{'idqv': '1', 'title': 'who is responsible for your security?', 'choices': [('you', '0'),
                                                                                         ('third party', '0'),
                                                                                         ('security team', '0')],
              'iduv': '1'},
             {'idqv': '2', 'title': 'if it is a secrity team ,How  many employee do you have in your security team?',
              'choices': [('1', '0.7'), ('2', '0.5'), ('3 or more', '0')],
              'iduv': '1'}, {'idqv': '3', 'title': 'how many one of them is certified ?', 'choices': [('0', '0.6'),
                                                                                                      ('most of them',
                                                                                                       '0.3'), (
                                                                                                          'all of them',
                                                                                                          '0')],
                             'iduv': '1'},
             {'idqv': '4', 'title': '	if it is you ,are you certified ?', 'choices': [('yes', '0.5'), ('no', '0')],
              'iduv': '1'},
             {'idqv': '5', 'title': 'Do you have awebsite ?', 'choices': [('yes', '0.5'), ('no', '0')], 'iduv': '2'},
             {'idqv': '6', 'title': 'where is it hosted ?',
              'choices': [('on the  server of the same cloud provider ', '0.6'), ('on another dedicated server', '0.1'),
                          ('i have no idea', '0.8')], 'iduv': '2'},
             {'idqv': '7', 'title': 'How much is your web presence important?',
              'choices': [('very important ', '0.5'), ('normal', '0.3'), ('not too much important', '0.2')],
              'iduv': '2'}, ],
            key=lambda i: i['iduv'])
QA = sorted([{'idqa': '1', 'title': 'do you have Physical buildings?', 'choices': ['yes', 'no', ], 'ida': '1 '},
             {'idqa': '2', 'title': 'do you keep your security logs?', 'choices': ['yes', 'no', ], 'ida': '2'},
             {'idqa': '3', 'title': 'do you keep your operational logs?', 'choices': ['yes', 'no', ], 'ida': '3'},
             {'idqa': '4', 'title': 'do you own Intellectual property?', 'choices': ['yes', 'no', ], 'ida': '4'},
             {'idqa': '5', 'title': 'do you have some data that is considered sensitive?', 'choices': ['yes', 'no', ],
              'ida': '5'},
             {'idqa': '6', 'title': 'do you have a real time Service delivery ?', 'choices': ['yes', 'no', ],
              'ida': '6'},
             ], key=lambda i: i['idqa'])


def vul_finder(u_answers, qv, ucv, vul):
    vul_list = []
    # answreed questons serted by the uc id
    uc_answered_question = {}
    # sorting the answererd question by use case
    for i in u_answers.keys():
        if qv[int(i) - 1]['iduv'] in uc_answered_question.keys():
            uc_answered_question[qv[int(i) - 1]['iduv']].append(int(i))
        else:
            uc_answered_question[qv[int(i)]['iduv']] = [int(i)]
    # finding vulnerabilities by comparing each one to the seuil of the uscase
    for i in uc_answered_question.keys():
        # print(uc_answered_question[i])
        threshold = 0
        for j in uc_answered_question[i]:
            if float(qv[j - 1]['choices'][int(u_answers[str(j)]) - 1][1]) > threshold:
                # print(float(qv[j - 1]['choices'][int(u_answers[str(j)]) - 1][1]))
                threshold = float(qv[j - 1]['choices'][int(u_answers[str(j)]) - 1][1])
        if threshold >= float(ucv[int(i) - 1]['threshold']):
            vul_list.append(vul[int(ucv[int(i) - 1]['idv']) - 1]['idv'])
            print(vul[int(ucv[int(i) - 1]['idv']) - 1])
    return vul_list


def uc_vul_finder(answer_ucv, qv, ucv, vuln):
    vul_list = []
    for i in answer_ucv.keys():
        threshold = 0
        for j in answer_ucv[i]:
            if float(qv[int(j[0]) - 1]['choices'][int(j[1]) - 1][1]) > threshold:
                threshold = float(qv[int(j[0]) - 1]['choices'][int(j[1]) - 1][1])
        if threshold >= float(ucv[int(i) - 1]['threshold']):
            vul_list.append(vuln[int(ucv[int(i) - 1]['idv']) - 1])
    return vul_list


def asset_finder(u_answers, qa, ass):
    assets = []
    for i in u_answers.keys():
        if u_answers[i] == '1':
            assets.append(ass[int(qa[int(i) - 1]['ida']) - 1]['ida'])
            print(ass[int(qa[int(i) - 1]['ida']) - 1])
    return assets


class Risk:
    def __init__(self, idr, impact_value, probability_value, risk_value, vulnerabilities, assets):
        self.idr = idr
        self.impact_value = impact_value
        self.probability_value = probability_value
        self.risk_value = risk_value
        self.vulnerabilities = vulnerabilities
        self.assets = assets

    def get_idr(self):
        return self.idr

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
        return {'idr': self.idr, 'impact_value': self.impact_value, 'probability_value': self.probability_value,
                'risk_value': self.risk_value, 'vulnerabilities': self.vulnerabilities, 'assets': self.assets}


Risks = [Risk(idr=1, impact_value=2, probability_value=3, risk_value=5, vulnerabilities=['4', '2'], assets=['1', '3',
                                                                                                            '4', '5'])]


def risk_calc(assets, vulns, risks, ):
    preleminary_risks = {}
    user_risks = []
    for i in risks:
        print(i.get_risk())
        for j in i.get_vulnerabilities():
            if str(j) in vulns:
                if i.get_idr() not in preleminary_risks:
                    preleminary_risks[i.get_idr()] = {'vul': [j], 'asset': [], 'risk': i.get_risk()}
                else:
                    preleminary_risks[i.get_idr()]['vul'].append(j)
        for j in i.get_assets():
            if str(j) in assets:
                if i.get_idr() not in preleminary_risks:
                    preleminary_risks[i.get_idr()] = {'vul': [], 'asset': [j], 'risk': i.get_risk()}
                else:
                    preleminary_risks[i.get_idr()]['asset'].append(j)
    for i in preleminary_risks.keys():
        risk_value = 0.0
        impact_value = 0.0
        probability_value = 0.0
        pv = (len(preleminary_risks[i]['vul']) / len(preleminary_risks[i]['risk']['vulnerabilities']))
        # pa = (len(preleminary_risks[i]['asset']) / len(preleminary_risks[i]['risk']['assets']))
        # impact_value = (preleminary_risks[i]['risk']['impact_value']) * pa
        probability_value = (preleminary_risks[i]['risk']['probability_value']) * pv
        risk_value = impact_value + probability_value
        user_risks.append(Risk(preleminary_risks[i]['risk']['idr'], impact_value, probability_value, risk_value,
                               preleminary_risks[i]['vul'], preleminary_risks[i]['asset']))
    return user_risks


if __name__ == '__main__':
    vul = vul_finder(User_answers['answersv'], QV, Ucv, Vulner)
    asset = asset_finder(u_answers=User_answers['answersa'], ass=Assets, qa=QA)
    # uc_vul = uc_vul_finder(answer_ucv=User_answers['answersv_uc'], qv=QV, ucv=Ucv, vuln=Vulner)
    print('the vulnerabilities that could affect you have  ids: ')
    print(vul)
    # print(uc_vul)
    print('your assets that could be affected are have ids:')
    print(asset)
    risks = risk_calc(assets=asset, vulns=vul, risks=Risks)
    print('your risks are : ')
    for i in risks:
        print(i.get_risk())
