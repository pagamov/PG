class TOKENS:
    pass

class OPERATORS:
    pass


class Reader:
    # read file and separates it apart 
    text = []
    def read(self, file = 'index.pg'):
        import sys
        if len(sys.argv) == 2:
            file = sys.argv[1]
        with open(file, 'r') as f:
            data = f.read()
        for line in data.splitlines():
            self.text = self.text + line.split()
        return self.text

    def log(self, file='Reader.log.txt'):
        f = open(file, 'w')
        for word in self.text:
            f.write(word)
            f.write(' ')
            if word in [';', ':', ';;']:
                f.write('\n')
        f.close()
    
    def formTree(self, file='Reader.tree.txt'):








if __name__ == "__main__":
    # read code and split in apart
    reader = Reader()
    text = reader.read()
    reader.log()
    print('\033[92mReading stage complete\033[0m')
