import re


class Reader(object):
    def __init__(self, file_name='cfg.txt'):
        self.terminals = []
        self.non_terminals = []
        self.file_lines = []
        self.productions = {}
        f = open(file_name, 'r')
        self.data = f.readlines()
        f.close()
        self.prepareData()
        self.eliminateLeftRecusion()


    def prepareData(self):
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
            list = re.findall(r'‘\w+’|‘[\W\w]*’', temp[1])
            for value in list:
                self.terminals.append(value)
        print(self.file_lines)
        print(self.terminals)
        print(self.non_terminals)
        print(self.productions)
        return None

    def eliminateLeftRecusion(self):
        length = len(self.non_terminals)
        for i in range(0, length):
            for j in range(0, i):
                s = 0
                while s < len(self.productions[self.non_terminals[i]]):
                    s = self.productions[self.non_terminals[i]].find(self.non_terminals[j], s)
                    if s == -1:
                        break
                    if s != 0 and (self.productions[self.non_terminals[i]][s-1] != ' ' or self.productions[self.non_terminals[i]][s+len(self.non_terminals[j])] != ' '):
                        s += 1
                    else:
                        self.replaceString(self.non_terminals[i], self.non_terminals[j], s)
            self.eliminateImmediateLeftRecusion(self.non_terminals[i])
        for k in self.non_terminals:
            print(k+" => "+self.productions[k])

    def replaceString(self, key, value, s):
        trace = s + len(value)
        following = ""
        while trace < len(self.productions[key]):
            if self.productions[key][trace] == '|':
                break
            following += self.productions[key][trace]
            trace += 1
        new_string = ""
        temp = self.productions[value].split('|')
        for tempaya in temp:
            new_string += tempaya.strip() + " " + following.strip() + " | "
        new_string = new_string[:len(new_string) - 3]
        self.productions[key] = self.productions[key].replace((value+following).strip(), new_string, 1)

    def eliminateImmediateLeftRecusion(self, key):
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
                string += non.strip()+" "+new_non_terminal+" | "
            string = string[:len(string)-3]
            self.productions[key] = string
            new_non_terminal_value = ""
            for production in recursive:
                new_non_terminal_value += production.replace(key, "").strip() + " " + new_non_terminal + " | "
            new_non_terminal_value += "None"
            self.non_terminals.append(new_non_terminal)
            self.productions[new_non_terminal] = new_non_terminal_value
