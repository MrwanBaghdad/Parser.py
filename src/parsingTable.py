class Table(object):
    def __init__(self, cfg, firsts, follows):
        self.table = dict()
        for non_terminal in cfg.non_terminals:
            for terminal in cfg.terminals:
                if terminal in firsts.get(non_terminal):
                    self.table[(non_terminal, terminal)] = cfg.getProduction(non_terminal, terminal)
                elif terminal in follows[non_terminal]:
                    self.table[(non_terminal, terminal)] = "sync"
                else:
                    self.table[(non_terminal, terminal)] = None
        print(self.table)

    def trace(self):
        # TODO Implement the trace function
        return None
