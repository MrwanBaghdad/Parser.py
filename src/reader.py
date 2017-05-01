class reader:
    def __init__(self,filename):
        self.f = open(filename, "r+")
    def readRules(self):
        inputText = self.f.read()
        inputText = inputText.split()
        inputText = ''.join(inputText)
        inputText = inputText.split("#")
        text = []
        for x in inputText:
            if x == '' or x == None:
                continue
            text.append(x)
        first = []
        second = []
        rules={}
        for x in text:
            x = x.split("=")
            # first.append(x[0])
            # second.append(x[1])
            rules[x[0]]=x[1]
            # print(first)
        return rules
    def removeOr(self,Rules):
        text=Rules.values()
        x=[]
        finalRules={}
        for i in text:
            x.append(i.split('|'))
        j=0
        for i in Rules.keys():
            finalRules[i]=x[j]
            j+=1
        return finalRules
    def getRules(self):
        Rules = self.readRules()
        self.finalRules = self.removeOr(Rules)
        return self.finalRules
        # print('\n\n\n\nafter no or',finalRules)

def main():
    r = reader('input.txt')
    print(r.getRules())


if __name__ == '__main__':
    main()


