class Table(object):
    def __init__(self, cfg, firsts, follows):
        self.cfg = cfg
        self.table = dict()
        for non_terminal in cfg.non_terminals:
            for terminal in cfg.terminals:
                if terminal in firsts.get(non_terminal):
                    self.table[(non_terminal, terminal)] = cfg.getProduction(non_terminal, terminal)
                elif terminal in follows[non_terminal]:
                    self.table[(non_terminal, terminal)] = "sync"
                else:
                    self.table[(non_terminal, terminal)] = None
        # self.table[(cfg.non_terminals[0], '$')] = 'sync'
        print(self.table)

    def trace(self):
        # TODO Implement the trace function
        stack = ['$', self.cfg.non_terminals[0]]
        terminal = self.nextInput()
        while stack_peek is not None:
            stack_peek = stack[-1]
            if stack_peek in self.cfg.non_terminals:
                data = self.table.get((stack_peek, terminal))
                if data is None:
                    print("Error: (illegal " + stack_peek + ")")
                    terminal = self.nextInput()
                elif data == 'sync':  # Done popping from the stack.
                    print("Error: sync was found")
                    stack.pop()
                else:
                    for element in reversed(data.split()):  # Done Pushing elements to stack and output the production
                        if element.strip != "None":
                            stack.append(element.strip())
                    print(stack_peek+" => "+data)
            elif stack_peek in self.cfg.terminals:
                if stack_peek != terminal:  # Done Matching
                    print("Error: missing " + stack_peek)
                stack.pop()
                terminal = self.nextInput()
            else:
                print("Unknown Symbol => " + stack_peek)

    def nextInput(self):
        temp = lexical_analyzer.next()
        if temp is None:
            return '$';
        return temp