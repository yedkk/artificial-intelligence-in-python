############################################################
# CMPSC442: Homework 5
############################################################

student_name = "Kangdong Yuan"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import email
import math
from collections import defaultdict
import os

############################################################
# Section 1: Spam Filter
############################################################

def def_value():
    return 0

def load_tokens(email_path):
    text = []
    try:
        f = open(email_path, encoding='utf-8')
        message = email.message_from_file(f)
        f.close()
    except:
        f = open(email_path, encoding='ISO-8859-1')
        message = email.message_from_file(f)
        f.close()
    lines = email.iterators.body_line_iterator(message)
    for line in lines:
        text += line.split()
    return text

def log_helper(email_paths):
    vocabulary = defaultdict(def_value)
    total_count = 0
    for path in email_paths:
        text = load_tokens(path)
        total_count += len(text)
        for w in text:
            vocabulary[w] += 1
    return vocabulary, total_count

def log_probs(email_paths, smoothing):
    prob = {}
    total_count = 0
    vocabulary, total_count = log_helper(email_paths)
    for v in vocabulary.keys():
        prob[v] = math.log((vocabulary[v] + smoothing) / (total_count + smoothing * (len(vocabulary) + 1)))
    prob["<UNK>"] = math.log(smoothing / (total_count + smoothing * (len(vocabulary) + 1)))
    return prob



class SpamFilter(object):

    def __init__(self, spam_dir, ham_dir, smoothing):
        self.smoothing = smoothing
        self.spam_dir = spam_dir
        self.ham_dir = ham_dir

        self.spamtext = next(os.walk(spam_dir))[2]
        self.hamtext = next(os.walk(ham_dir))[2]
        self.spamloc = [self.spam_dir + "/" + f for f in self.spamtext]
        self.hamloc = [self.ham_dir + "/" + f for f in self.hamtext]
        self.spamlog = log_probs(self.spamloc, self.smoothing)
        self.hamlog = log_probs(self.hamloc, self.smoothing)
        self.logprob = log_probs(self.spamloc + self.hamloc, self.smoothing)

        self.spamnum = len(self.spamtext)
        self.hamnum = len(self.hamtext)
        self.filenum = self.spamnum + self.hamnum
        self.spampro = self.spamnum / self.filenum
        self.hampro = self.hamnum / self.filenum
        
    def is_spam(self, email_path):
        spam_num, ham_num, all = 1, 1, log_helper([email_path])[0]
        for w in all:
            if w in self.spamlog:
                spam_num += self.spamlog[w] * math.log(all[w])
            else:
                spam_num += self.spamlog["<UNK>"] * math.log(all[w])
            if w in self.hamlog:
                ham_num += self.hamlog[w] * math.log(all[w])
            else:
                ham_num += self.hamlog["<UNK>"] * math.log(all[w])
        return (math.log(self.spampro) + spam_num) > (math.log(self.hampro) + ham_num)

    def most_indicative_spam(self, n):
        value_store = {}
        all_words = set(list(self.spamlog.keys()) + list(self.hamlog.keys()))
        for w in all_words:
            if w in self.spamlog and w in self.hamlog:
                value_store[w] = self.spamlog[w] - math.log(math.exp(self.spamlog[w]) + math.exp(self.hamlog[w]))
        sorted_value = sorted(value_store.items(), key = lambda v: v[1], reverse = True)
        return [sorted_value[i][0] for i in range(n)]

    def most_indicative_ham(self, n):
        value_store = {}
        all_words = set(list(self.spamlog.keys()) + list(self.hamlog.keys()))
        for w in all_words:
            if w in self.spamlog and w in self.hamlog:
                value_store[w] = self.hamlog[w] - math.log(math.exp(self.spamlog[w]) + math.exp(self.hamlog[w]))
        sorted_value = sorted(value_store.items(), key = lambda v: v[1], reverse = True)
        return [sorted_value[i][0] for i in range(n)]


