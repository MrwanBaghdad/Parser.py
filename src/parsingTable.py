import logging
logging.basicConfig(level=logging.DEBUG)
class Table(object):
    def __init__(self, cfg, firsts, follows):
        self.cfg = cfg
        seen = set()
        seen_add = seen.add
        cfg.terminals = [x for x in cfg.terminals if not (x in seen or seen_add(x))]
        seen = set()
        seen_add = seen.add
        cfg.non_terminals = [x for x in cfg.non_terminals if not (x in seen or seen_add(x))]
        # self.temp_input = ['h', '+', 'h']
        # self.temp_input = ['b', 'a', 'a']
        self.temp_input = ['}', ';', '0', 'assign', 'id', '{', ')', 'num', 'relop', 'id', '(', 'if', ';', 'num', 'assign', 'id', ';', 'id', 'int']
        self.table = dict()
        for non_terminal in cfg.non_terminals:
            if '$' in follows[non_terminal] and 'None' in firsts[non_terminal]:
                self.table[(non_terminal, '$')] = "None"
            else:
                self.table[(non_terminal, '$')] = None
            for terminal in cfg.terminals:
                terminal = terminal.replace("'", '')
                if terminal in firsts.get(non_terminal):
                    productionsList = cfg.productions2.get(non_terminal)
                    for production in productionsList:
                        production = production.replace("'", "")
                        s = production.find(' ')
                        if s > 0:
                            first = production[:s]
                        else:
                            first = production
                        if first in cfg.non_terminals:
                            if first == terminal or terminal in firsts.get(first):
                                self.table[(non_terminal, terminal)] = production
                                break
                        elif first in cfg.terminals:
                            if first == terminal:
                                self.table[(non_terminal, terminal)] = production
                                break
                elif terminal in follows[non_terminal]:
                    if "None" in cfg.productions.get(non_terminal):
                        self.table[(non_terminal, terminal)] = "None"
                    else:
                        self.table[(non_terminal, terminal)] = "sync"
                else:
                    self.table[(non_terminal, terminal)] = None
        # from tabulate import tabulate
        self.trace()

    def trace(self):
        string = "" + self.cfg.non_terminals[0]
        print(string)
        stack = ['$', self.cfg.non_terminals[0]]
        terminal = self.nextInput()
        stack_peek = stack[-1]
        while stack_peek != '$':
            if terminal == '$':
                if self.table.get((stack_peek, terminal)) is not None:
                    string = self.replaceString(string, stack_peek, self.table.get((stack_peek, terminal)))
                    print(string + " || " + stack_peek + " => " + self.table.get((stack_peek, terminal)))
                stack.pop()
            elif stack_peek in self.cfg.non_terminals:
                data = self.table.get((stack_peek, terminal))
                if data is None:
                    string = self.replaceString(string, stack_peek, '')
                    print(string + " || " + "Error: (illegal " + stack_peek + ")")
                    terminal = self.nextInput()
                elif data == 'sync':  # Done popping from the stack.
                    print("Error: sync was found")
                    stack.pop()
                else:
                    stack.pop()
                    for element in reversed(data.split()):  # Done Pushing elements to stack and output the production
                        if element.strip() != "None":
                            stack.append(element.strip())
                    string = self.replaceString(string, stack_peek, data)
                    print(string + " || " + stack_peek + " => " + data)
            elif stack_peek in self.cfg.terminals:
                if stack_peek != terminal:  # Done Matching
                    string = self.replaceString(string, stack_peek, '')
                    print(string + " || " + "Error: missing " + stack_peek)
                else:
                    terminal = self.nextInput()
                stack.pop()

            else:
                print(string + "Unknown Symbol => " + terminal)
                terminal = self.nextInput()
            stack_peek = stack[-1]
        print("accept")

    def nextInput(self):
        # temp = lexical_analyzer.next()
        # if temp is None:
        #     return '$';
        # return temp
        if len(self.temp_input) > 0:
            return self.temp_input.pop()
        return '$'

    def replaceString(self, string, to_be_replaced, replacement):
        if to_be_replaced == string:
            return replacement
        s = string.find(to_be_replaced, 0)
        if s > 0:
            if s + len(to_be_replaced) == len(string):
                return string.replace(" " + to_be_replaced, " " + replacement)
            else:
                return string.replace(" " + to_be_replaced + " ", " " + replacement + " ")
        return string.replace(to_be_replaced + " ", replacement + " ")

if __name__ == "__main__":
    import construct_first_follows as ff 
    ff.reader.terminals = [terminal.replace("'", "") for terminal in ff.reader.terminals]
    Table(ff.reader, ff.firsts, ff.follows)
