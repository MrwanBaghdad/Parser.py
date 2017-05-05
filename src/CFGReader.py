import re

import os
CWD = os.getcwd()
cfg_file_path = os.path.join(CWD,"src/cfg")
class Reader(object):
    def __init__(self, file_name=cfg_file_path):
        self.terminals = []
        self.non_terminals = []
        self.file_lines = []
        self.productions = {}
        self.productions2 = {}
        f = open(file_name, 'r')
        self.data = f.readlines()
        f.close()
        self.prepareData()
        # print(self.productions)
        # for k in self.non_terminals:
        #     print(k + " => " + self.productions[k])
        self.eliminateLeftRecusion()
        for non_terminal in self.non_terminals:
            array = self.productions[non_terminal].split("|")
            temp = []
            for element in array:
                temp.append(element.strip())
            self.productions2[non_terminal] = temp
        # print(self.file_lines)
        # print(self.terminals)
        # print(self.non_terminals)
        print(self.productions)
        for k in self.non_terminals:
            print(k + " => " + self.productions[k])

    def prepareData(self):
        # Read Productions From the given file and analyze data into terminals and non-terminals
        temp = []
        for line in self.data:
            temp.append(re.sub(r'[#\n]', '', line))
        self.file_lines.append(temp[0])
        j = 0
        for i in range(1, len(temp)):
            if '=' not in temp[i]:
                self.file_lines[j] += (temp[i])
            else:
                j += 1
                self.file_lines.append(temp[i])
        for line in self.file_lines:
            temp = line.split('=')
            self.productions[temp[0].strip()] = temp[1].strip()
            self.non_terminals.append(temp[0].strip())
            terminals_list = re.findall(r'(\'[\w+*\-(),;{}=_]*\')', temp[1])
            for terminal in terminals_list:
                self.terminals.append(terminal)

    def eliminateLeftRecusion(self):
        # Eleminate left recursions from the productions
        length = len(self.non_terminals)
        for i in range(0, length):
            for j in range(0, i):
                s = 0
                while s < len(self.productions[self.non_terminals[i]]):
                    s = self.productions[self.non_terminals[i]].find(self.non_terminals[j], s)
                    if s == -1:
                        break
                    if s + len(self.non_terminals[j]) < len(self.productions[self.non_terminals[i]]):
                        if s == 0:
                            if self.productions[self.non_terminals[i]][s + len(self.non_terminals[j])] == ' ':
                                self.replaceString(self.non_terminals[i], self.non_terminals[j], s)
                            else:
                                s += 1
                        else:
                            if self.productions[self.non_terminals[i]][s - 1] == ' ' and \
                                            self.productions[self.non_terminals[i]][
                                                        s + len(self.non_terminals[j])] == ' ':
                                self.replaceString(self.non_terminals[i], self.non_terminals[j], s)
                            else:
                                s += 1
            self.eliminateImmediateLeftRecusion(self.non_terminals[i])

    def replaceString(self, key, value, s):
        # Replace a non-terminal with it's corresponding value in the production dictionary
        end = s + len(value)
        beginning = s
        while beginning > 0:
            if self.productions[key][beginning] == '|':
                break;
            beginning -= 1
        previous = self.productions[key][beginning:s]
        following = ""
        while end < len(self.productions[key]):
            if self.productions[key][end] == '|':
                break
            following += self.productions[key][end]
            end += 1
        if previous in ['| ', '|'] and following in [' |', '|']:
            self.productions[key] = self.productions[key].replace(value.strip(), self.productions[value], 1)
        elif previous in ['| ', '|']:
            new_string = ""
            splitted_productions = self.productions[value].split('|')
            for production in splitted_productions:
                new_string += production.strip() + " " + following.strip() + " | "
            new_string = new_string[:len(new_string) - 3]
            self.productions[key] = self.productions[key].replace((value + following).strip(), new_string, 1)
        elif following in [' |', '|']:
            new_string = ""
            splitted_productions = self.productions[value].split('|')
            for production in splitted_productions:
                new_string += previous.strip() + " " + production.strip() + " | "
            new_string = new_string[:len(new_string) - 3]
            self.productions[key] = self.productions[key].replace((previous + value).strip(), new_string, 1)
        else:
            new_string = ""
            splitted_productions = self.productions[value].split('|')
            for production in splitted_productions:
                new_string += previous.strip() + " " + production.strip() + " " + following.strip() + " | "
            new_string = new_string[:len(new_string) - 3]
            self.productions[key] = self.productions[key].replace((previous + value + following).strip(), new_string,
                                                                  1).replace("| |", "|")
        print(self.productions[key])

    def eliminateImmediateLeftRecusion(self, key):
        # This function eliminate immediate Left Recursion => A = AB|Aa|A
        productions = self.productions[key].split('|')
        recursive = []
        non_recursive = []
        for production in productions:
            i = 0
            while production[i] == ' ':
                i += 1
            if production.find(key) == i:
                recursive.append(production)
            else:
                non_recursive.append(production)
        if len(recursive) > 0:
            new_non_terminal = key + "`"
            string = ""
            for non in non_recursive:
                string += non.strip() + " " + new_non_terminal + " | "
            string = string[:len(string) - 3]
            self.productions[key] = string
            new_non_terminal_value = ""
            for production in recursive:
                new_non_terminal_value += production.replace(key, "").strip() + " " + new_non_terminal + " | "
            new_non_terminal_value += "None"
            self.non_terminals.append(new_non_terminal)
            self.productions[new_non_terminal] = new_non_terminal_value

    def getProduction(self, non_terminal, terminal):
        for production in self.productions2[non_terminal]:
            if production.find(terminal) == 0:
                return production
        return None

    def nonTerminaleName(self, non_terminal):
        new_name = non_terminal + "`"
        while new_name in self.non_terminals:
            new_name += "`"
        return new_name

    def leftFactoring(self):
        temp_productions = list()
        sep_productions = dict() #FIXME: assign sep_productions
        for non_terimnal in self.non_terminals:
            for prod in sep_productions.get(non_terimnal):
                temp_productions.append(tuple((non_terimnal, prod)))
        prod_sorted = sorted(temp_productions, key=lambda x: x[1].split()[0])
        start_prod = [i for i in prod_sorted[1].split()[0].strip()]
        start_prod = set(start_prod)
        for unique in start_prod:
                for i in range(0, len(prod_sorted)):
                    temp_tuple = prod_sorted[i]
                    temp_first = temp_tuple[1].split()[0]
                    if temp_first == unique:
                        continue
                    else:
                        break
                same_unique = [prod_sorted[tt] for tt in range(0,i)]
                #remove the unique from prod sorted
                for t in same_unique:
                    prod_sorted.remove(t)
                new_non_terminal = get_new_nonterminal() #TODO:
                #assign 
                for i in same_unique:
                    rhs_string = i[1]
                    if unique != i[0]:
                        raise RuntimeError
                    rhs_string.sub(unique, new_non_terminal)
                sep_productions[new_non_terminal] = unique
                    

    def lf(self, non_terminal):
        prods = []
        prods.append(self.productions[non_terminal])
 #       yy = lambda rhs_array:
        def yy(rhs_array):
            dict1 = {}
            for i in range(0, len(rhs_array)):
                #Construct dict1 with key as first word and value of index of OR PROD
                first_char = rhs_array[i].split()[0]
                if dict1.get(first_char) is None:
                    #init 
                    dict1[first_char] = list()
                dict1[first_char].append(i)
            for key in dict1:
                if dict1.get(key).__len__() ==1:
                    continue
                #found a factor
                A = self.get_new_nonterminal()
                rhs_new_prod =list() 
                for p_index in dict1.get(key):
                    p = p_index
                    non_factor = ''.join(rhs_array[p][1:])
                    if non_factor == '':
                        non_factor = "None"
                    rhs_new_prod.append(non_factor)
                    #changed ^ the production
                    del(rhs_array[p])
                #finished factoring for current factor key
                #add the new production in the productions table
                #first remove dublicates 
                prods.append(list(set(rhs_new_prod)))
                #FIXME: do we need to reference RHS?
                #NO WE DONT!!
#                self.prods[non_terminal_input]
                self.productions[A] = rhs_new_prod
                rhs_array.append(key+' '+A)
        for rhs in prods:
            yy(rhs)

    def get_new_nonterminal(self):
        import string
        import random
        yy = lambda _: string.ascii_letters[random.randint(0,len(string.ascii_letters))]
        while True:
             temp_str = ''.join(list(map(yy, range(3))))
             if temp_str not in self.non_terminals:
                 return temp_str