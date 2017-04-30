
firsts = dict()


def construct_first(production_rules):
    '''get the LHS and if first one is a terminal add to the first of the current
    Variable (non terminal) if it's a non terminal get the '''
    for rule in reversed(production_rules):
        for or_rules in rule['LHS']:
            if or_rules[0] == '\'':
                '''getting a terminal'''
                firsts[rule['RHS']].append(or_rules[1])
            else:
                '''getting a non terminal'''
                firsts[rule['RHS']].append(firsts[or_rules.split()[0].strip()])
    

follows = dict()
def construct_follows(production_rules):
    '''get the follow of every non terminal variable by checking LHS rules,
    if a terimnal added to the follow, if it's also a variable get the firsts of it'''

    for rules in production_rules:
        for or_rule in rules['LHS']:
            '''get all terimnals and search after them for'''
            for search_term in firsts.keys():
                if search_term in or_rule:
                    '''found a varuiable'''
                    if(or_rule.find(search_term) is not -1):
                        start_index = or_rule.find(search_term)
                        end_index = start_index + search_term.__len__()
                        test_next_string = or_rule[end_index].split()
                        test_next_thing = test_next_string[0].strip()
                        if test_next_thing[0]=='\'':
                            '''found a follow terminal'''
                            follows[rules['RHS']].append(test_next_thing[1])
                        else:
                            '''found a variable follow'''
                            follows[rules['RHS']].append(firsts[test_next_string[0].strip()])
            #TODO: if elipsone add to as an object