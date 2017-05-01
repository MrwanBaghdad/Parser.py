class Table(object):
    def __init__(self, terminals, non_terminals, follows, starts):
        self.table = dict()
        for non_terminal in non_terminals:
            for terminal in terminals:
                if terminal in starts[non_terminal]:
                    # TODO replace the None with the required production
                    self.table[(non_terminal, terminal)] = None
                elif terminal in follows[non_terminal]:
                    # TODO replace the None with the required production
                    self.table[(non_terminal, terminal)] = None
                else:
                    self.table[(non_terminal, terminal)] = None

    def trace(self):
        # TODO Implement the trace function
        return None
