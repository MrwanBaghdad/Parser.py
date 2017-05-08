# from CFGReader import Reader
# from parsingTable import *
# from construct_first_follows import *
import CFGReader
import parsingTable
import construct_first_follows

parsingTable = parsingTable.Table(construct_first_follows.reader, construct_first_follows.firsts, construct_first_follows.follows)
# parsingTable = Table(reader, firsts, follows)
print("done")