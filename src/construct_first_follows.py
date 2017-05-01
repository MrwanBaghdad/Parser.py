
firsts = dict()

from CFGReader import Reader

def construct_first(production_rules):
    '''get the LHS and if first one is a terminal add to the first of the current
    Variable (non terminal) if it's a non terminal get the '''
    for rule in reversed(production_rules):
        if firsts.get(rule['LHS']) is None:
            firsts[rule['LHS']] = list()
        for or_rules in rule['RHS']:
            if or_rules[0] == '\'':
                '''getting a terminal'''
                firsts[rule['LHS']].append(or_rules[1])
            else:
                '''getting a non terminal'''
                firsts[rule['LHS']].append(firsts[or_rules.split()[0].strip()])

follows = dict()
def construct_follows(production_rules):
    '''get the follow of every non terminal variable by checking LHS rules,
    if a terimnal added to the follow, if it's also a variable get the firsts of it'''

#     for rules in production_rules:
#         for or_rule in rules['LHS']:
#             '''get all terimnals and search after them for'''
#             for search_term in firsts.keys():
#                 if search_term in or_rule:
#                     '''found a varuiable'''
#                     if(or_rule.find(search_term) is not -1):
#                         start_index = or_rule.find(search_term)
#                         end_index = start_index + search_term.__len__()
#                         test_next_string = or_rule[end_index].split()
#                         test_next_thing = test_next_string[0].strip()
#                         if test_next_thing[0]=='\'':
#                             '''found a follow terminal'''
#                             follows[rules['RHS']].append(test_next_thing[1])
#                         else:
#                             '''found a variable follow'''
#                             follows[rules['RHS']].append(firsts[test_next_string[0].strip()])

    VARIABLES = [ rule['LHS'] for rule in production_rules]
    ALL_RHS_RULES = [rule['RHS'] for rule in production_rules]
    ELIPSON = "None"
    for v in VARIABLES:
        '''loop on all variables checking RHS rules for getting follows'''
        if follows.get(v) is None:
            follows[v] = list()
        if v == production_rules[0].get("LHS"):
            if '$' not in follows[v]:
                follows[v].append('$')
        for rule in ALL_RHS_RULES:
            for or_rule in rule:
                if v in or_rule:
                    start_index = or_rule.index(v)
                    end_index = start_index + v.__len__()
                    testing_string = or_rule[end_index:]
                    testing_next = testing_string.split().strip()
                    if testing_next[0] =='\'':
                        '''found a follow terminal'''
                        follows[v].append(testing_next[1])
                    else:
                        '''found another variable'''

                        for vv in testing_string.split():
                            vv = vv.strip()
                            if ELIPSON in firsts.get(vv):
                                follows[v].append(firsts.get(vv).remove(ELIPSON))
                            else:
                                break

            #TODO: if ELIPSONe add to as an object

reader = Reader()
production_rules = list()

def translate():
    for non_terminal in reader.non_terminals:
        temp_dict = dict()
        temp_dict['LHS'] = non_terminal
        temp_dict['RHS'] = reader.productions.get(non_terminal).split('|')
        production_rules.append(temp_dict)
