############################################################
# CMPSC 442: Homework 6
############################################################

student_name = "Kangdong Yuan"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import re
from collections import defaultdict
import math

############################################################
# Section 1: Hidden Markov Models
############################################################

def load_corpus(path):
    result = []
    f = open(path, 'r')
    for line in f:
        temp = re.split(' |=', line.strip())
        result.append(list((temp[i], temp[i + 1]) for i in range(0, len(temp) - 1, 2)))
    f.close()
    return result

class Tagger(object):

    def __init__(self, sentences):
        self.sentences = sentences
        self.tag = {"NOUN": 0,
                    "VERB": 0,
                    "ADJ": 0,
                    "ADV": 0,
                    "PRON": 0,
                    "DET": 0,
                    "ADP": 0,
                    "NUM": 0,
                    "CONJ": 0,
                    "PRT": 0,
                    ".": 0,
                    "X": 0}
        partsofspeech=["NOUN","VERB","ADJ","ADV","PRON","DET","ADP","NUM","CONJ","PRT",".","X"]
        self.partsofspeechtransition = {}
        postrans = self.partsofspeechtransition

        for tg in partsofspeech:
            for j in partsofspeech:
                self.partsofspeechtransition[tuple([tg, j])] = 0

        self.sample, tags, pairs = {}, [], {}
        sumtotal, sumtrans, laplace, check = 0, 0, 1e-10, 0

        possibleoutcomes = len(self.tag)
        pairs = self.tag.copy()

        for line in self.sentences:
            check, pos01 = check + 1, line[0][1]

            if pos01 in self.tag:
                self.tag[pos01], sumtotal = self.tag[pos01] + 1, sumtotal + 1

            samplekeys = self.sample.keys()
            for tok in line:

                if tok not in samplekeys:
                    self.sample[tok] = 1

                elif tok in samplekeys:
                    self.sample[tok] = self.sample[tok] + 1

                t1 = tok[1]
                if t1 in pairs:
                    pairs[t1] = pairs[t1] + 1

                tags.append(t1)

        for t in self.tag:
            smtn, denom = self.tag[t] + laplace, sumtotal + possibleoutcomes*laplace
            self.tag[t] = smtn / denom

        ran = len(tags) - 1
        for tg in range(0, ran):
            tpair = tuple([tags[tg], tags[tg+1]])
            if tpair in postrans:
                postrans[tpair], sumtrans = postrans[tpair] + 1, sumtrans + 1

        for value in postrans:
            smtn, denom = laplace + postrans[value], len(postrans) * laplace + sumtrans
            postrans[value] = smtn / denom

        for k, tpair in self.sample.items():
            if k[1] in pairs:
                smtn, denom = self.sample[k] + laplace, pairs[k[1]] + (laplace * 12)
                self.sample[k] = smtn / denom
        CONSTANT = 3.14e-10

        begin = defaultdict(lambda : 0)
        default = defaultdict(lambda : 0)
        nex = defaultdict(lambda : default.copy())
        generate = defaultdict(lambda : default.copy())
        for s in sentences:
            begin[s[0][1]] += 1
            for i in range(len(s) - 1):
                j = i + 1
                nex[s[i][1]]["total"] += 1
                nex[s[i][1]][s[j][1]] += 1
                generate[s[i][0]]["total"] += 1
                generate[s[i][0]][s[i][1]] += 1
            generate[s[-1][0]]["total"] += 1
            generate[s[-1][0]][s[-1][1]] += 1

        self.emiss_probs = {}
        for w in generate:
            self.emiss_probs[w] = defaultdict(lambda : math.log((CONSTANT) / generate[w]["total"] + len(generate) * CONSTANT))
            for t in generate[w]:
                if t != "total":
                    self.emiss_probs[w][t] = math.log((generate[w][t] + CONSTANT) / generate[w]["total"] + len(generate) * CONSTANT)
        
    def most_probable_tags(self, tokens):
        tags = []
        for t in tokens:
            if t in self.emiss_probs:
                tags.append(max(self.emiss_probs[t].items(), key = lambda x : x[1])[0])
            else:
                tags.append(max(self.emiss_probs["X"].items(), key = lambda x : x[1])[0])
        return tags

    def alpha_helper(self, taglist, samplelist, laplace, tokens):
        dict_store = {}
        for v in taglist:
            start, end = (tokens[0], v),  (0, v)
            if start not in samplelist:
                dict_store[end] = laplace
            if start in samplelist:
                dict_store[end] =taglist[v]*samplelist[start]
        return dict_store

    def toptag(self, tokens, alpha_para, location, taglist):
        most_tag = []
        for i in range(0, len(tokens)):
            start, end = 0, "X"
            for val in taglist:
                if alpha_para[(i, val)] > start:
                    start, end = alpha_para[(i, val)], val
            most_tag += [end]
        for j in range(len(tokens) - 1, 0, -1):
            most_tag[j - 1] = location[(j, most_tag[j])]
        return most_tag

    def last_tag(self, taglist, finalre, alpha_para, final, i, j):
        for t in taglist:
            prob, position, pair = 0, self.partsofspeechtransition, (t, j)
            if pair in position:
                prob = alpha_para[(i - 1, t)]*position[(t, j)]
            if finalre < prob:
                finalre, final = prob, t
        return finalre, final

    def viterbi_tags(self, tokens):
        dist_para = 1e-10
        taglist = self.tag
        samplelist = self.sample
        alpha_para = self.alpha_helper(taglist, samplelist, dist_para, tokens)
        location = {}
        for i in range(1, len(tokens)):
            for j in taglist:
                finalre, final, tuple1 = 0, "X",(i, j)
                finalre, final = self.last_tag(taglist,finalre, alpha_para, final, i, j)
                if (tokens[i], j) in samplelist:
                    alpha_para[tuple1] = finalre * samplelist[(tokens[i], j)]
                else:
                    alpha_para[tuple1] = dist_para * finalre
                location[(i, j)] = final
        return self.toptag(tokens, alpha_para, location, taglist)

# c = load_corpus(r"C:\Users\yedkk\Desktop\CS442\hw6\brown-corpus.txt")
# t = Tagger(c)
# s = "I am waiting to reply".split()
# print(t.most_probable_tags(s))
# print(t.viterbi_tags(s))