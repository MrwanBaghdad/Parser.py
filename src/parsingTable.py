import logging
logging.basicConfig(level=logging.DEBUG)
class Table(object):
    def __init__(self, cfg, firsts, follows):
        self.cfg = cfg
        self.temp_input = ['h', '+', 'h']
        # self.temp_input = ['b', 'a', 'a']
        # self.temp_input = ['}', ';', '0', 'assign', 'id', '{', ')', 'num', 'relop', 'id', '(', 'if', ';', 'num', 'assign', 'id', ';', 'id', 'int']
        self.table = dict()
        for non_terminal in cfg.non_terminals:
            if '$' in follows[non_terminal]:
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
        stack = ['$', self.cfg.non_terminals[0]]
        terminal = self.nextInput()
        stack_peek = stack[-1]
        while stack_peek != '$':
            if terminal == '$':
                if self.table.get((stack_peek, terminal)) is not None:
                    print(stack_peek + " => " + self.table.get((stack_peek, terminal)))
                stack.pop()
            elif stack_peek in self.cfg.non_terminals:
                data = self.table.get((stack_peek, terminal))
                if data is None:
                    print("Error: (illegal " + stack_peek + ")")
                    terminal = self.nextInput()
                elif data == 'sync':  # Done popping from the stack.
                    print("Error: sync was found")
                    stack.pop()
                else:
                    stack.pop()
                    for element in reversed(data.split()):  # Done Pushing elements to stack and output the production
                        if element.strip() != "None":
                            stack.append(element.strip())
                    print(stack_peek+" => "+data)
            elif stack_peek in self.cfg.terminals:
                if stack_peek != terminal:  # Done Matching
                    print("Error: missing " + stack_peek)
                else:
                    terminal = self.nextInput()
                stack.pop()

            else:
                print("Unknown Symbol => " + terminal)
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

if __name__ == "__main__":
    import construct_first_follows as ff 
    ff.reader.terminals = [terminal.replace("'", "") for terminal in ff.reader.terminals]
    Table(ff.reader, ff.firsts, ff.follows)
