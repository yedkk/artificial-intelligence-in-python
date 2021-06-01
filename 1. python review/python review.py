############################################################
# CMPSC 442: Homework 1
############################################################

student_name = "Kangdong Yuan"

############################################################
# Section 1: Working with Lists
############################################################

def extract_and_apply(l, p, f):
    return [f(i) for i in l if p(i)]

def concatenate(seqs):
    return [j for i in seqs for j in i]

def transpose(matrix):
    return [[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]

############################################################
# Section 2: Sequence Slicing
############################################################

def copy(seq):
    return seq[:]

def all_but_last(seq):
    return seq[:-1]

def every_other(seq):
    return seq[::2]

############################################################
# Section 3: Combinatorial Algorithms
############################################################

def prefixes(seq):
    for i in range(len(seq)+1):
        yield seq[:i]

def suffixes(seq):
    for i in range(len(seq)+1):
        yield seq[i:len(seq)]

def slices(seq):
    for i in range(len(seq)):
        for j in range(len(seq)):
            if seq[i:j + 1]:
                yield seq[i:j + 1]

############################################################
# Section 4: Text Processing
############################################################

def normalize(text):
    return " ".join(str.split(text)).lower()

def no_vowels(text):
    v = ["a", "e", "i", "o", "u", "A", "E", "I", "O", "U"]
    return ''.join([i for i in text if i not in v])

def digits_to_words(text):
    convert = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    return " ".join([convert[int(i)] for i in text if i.isdigit()])

def to_mixed_case(name):
    return "".join(str.split(name.replace("_", " ").title()))[0].lower()+"".join(str.split(name.replace("_", " ").title()))[1:]

############################################################
# Section 5: Polynomials
############################################################

class Polynomial(object):

    def __init__(self, polynomial):
        self.poly = tuple(polynomial)

    def get_polynomial(self):
        return self.poly

    def __neg__(self):
        return Polynomial([(-x, y) for (x, y) in list(self.poly)])

    def __add__(self, other):
        return Polynomial(list(self.poly+other.poly))

    def __sub__(self, other):
        negative = -other
        return Polynomial(self.poly+negative.get_polynomial())

    def __mul__(self, other):
        x, y = list(self.poly), list(other.poly)
        return Polynomial([(i[0]*j[0], i[1]+j[1])  for i in x for j in y])


    def __call__(self, x):
        return sum([i[0]*(x**i[1]) for i in list(self.poly) if i[1] != 0]+[i[0] for i in list(self.poly) if i[1] == 0])

    def simplify(self):
        record={}
        sim=[]
        for i in list(self.poly):
            if i[1] not in record:
                record[i[1]]=i[0]
            else:
                record[i[1]]+=i[0]

        for k in sorted(record):
            if record[k]!=0:
                sim.append((record[k], k))
        if sim:
            sim.reverse()
        else:
            sim=[(0, 0),]
        self.poly=tuple(sim)

    def __str__(self):
        record=""
        li = list(self.poly)
        for i in li:
            if i[1] == 0:
                if i[0] > 0:
                    record += "+"+str(i[0])
                else:
                    record += str(i[0])
            elif i[1] == 1:
                if i[0] < 0:
                    if i[0] == -1:
                        record += "-x"
                    else:
                        record += str(i[0])+"x"
                elif i[0] == 1:
                    record += "+x"
                else:
                    record += "+"+str(i[0])+"x"
            else:
                if i[0] < 0:
                    if i[0] == -1:
                        record += "-x^"+str(i[1])
                    else:
                        record += str(i[0]) + "x^"+str(i[1])
                elif i[0] == 1:
                    record += "x^"+str(i[1])
                else:
                    record += "+"+str(i[0]) + "x^"+str(i[1])
        if record[0] == "+":
            return record[1:]
        else:
            return record









