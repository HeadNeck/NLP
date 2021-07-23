import nltk
import numpy as np
from nltk.corpus import wordnet

t = """As we all know, the text is the most unstructured form of all
 the available data. Extracting Meaning from Text is Hard."""

class Pipe:
    def __init__(self, targets=None):
        if targets is None:
            targets = []
        self.targets = targets

    def get_targets(self):
        return self.targets

    def delete_first_target(self):
        self.targets = self.targets[1:]


class Text_to_sent(Pipe):
    def piping(self, text):
        sent = nltk.sent_tokenize(text)
        return sent

    def add_target(self, target):
        self.targets.append(target)

    def __str__(self):
        return "Text_to_sent"


class Text_to_words(Pipe):
    def piping(self, text):
        if isinstance(text, list):
            prep = []
            for t in text:
                prep.append(nltk.word_tokenize(t))
            words = []
            for sent in prep:
                for word in sent:
                    words.append(word)
        else:
            words = nltk.word_tokenize(text)
        return words

    def add_target(self, target):
        self.targets.append(target)

    def __str__(self):
        return "Text_to_words"


class Without_stop_words(Pipe):
    def piping(self, words):
        stop_words = set(nltk.corpus.stopwords.words("english"))
        without_stop_words = [word for word in words if not word in stop_words]

        return without_stop_words

    def add_target(self, target):
        self.targets.append(target)

    def __str__(self):
        return "Without_stop_words"


class Stemming(Pipe):
    def piping(self, words):
        stemmer = nltk.stem.PorterStemmer()
        stemmed_words = []
        for word in words:
            stemmed_words.append(stemmer.stem(word=word))

        return stemmed_words

    def add_target(self, target):
        self.targets.append(target)

    def __str__(self):
        return "Stemming"


class Default_lemmatizing(Pipe):
    def piping(self, words):
        lemmatizer = nltk.stem.WordNetLemmatizer()
        lemmatized_words = []
        for word in words:
            lemmatized_words.append(lemmatizer.lemmatize(word=word))

        return lemmatized_words

    def add_target(self, target):
        self.targets.append(target)

    def __str__(self):
        return "Default_lemmatizing"


class Lemmatizing_after_pos_tag(Pipe):
    def piping(self, tagged_words):
        lemmatizer = nltk.stem.WordNetLemmatizer()
        lemmatized_words = []

        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}

        for word in tagged_words:
            tag = word[1][0]
            pos = tag_dict.get(tag, wordnet.NOUN)

            lemmatized_words.append(lemmatizer.lemmatize(word=word[0], pos=pos))

        return lemmatized_words

    def add_target(self, target):
        self.targets.append(target)

    def __str__(self):
        return "Lemmatizing_after_pos_tag"


class Pos_tag(Pipe):
    def piping(self, words):
        tagged_words = nltk.pos_tag(words)

        return tagged_words

    def add_target(self, target):
        self.targets.append(target)

    def __str__(self):
        return "Pos_tag"


class Printer(Pipe):
    def piping(self, line):
        return line

    def add_target(self, target):
        self.targets.append(target)

    def __str__(self):
        return "Printer"


class Pipeline:
    pipes = [Text_to_sent, Text_to_words, Without_stop_words, Stemming, Default_lemmatizing,
             Lemmatizing_after_pos_tag, Pos_tag, Printer]

    def __init__(self, list):
        self.final_res = []
        self.structure = []
        list = list.reshape(list.shape[0]*2, list.shape[1]//2)
        ulist = np.unique(list, axis=0)

        for i in range(len(list)):
            for ui in range(len(ulist)):
                if all(list[i] == ulist[ui]):
                    list[i][0] = ui

        ulist = np.unique(list, axis=0)
        list = list.reshape(list.shape[0]//2, list.shape[1]*2)

        self.line = []
        for i in ulist:
            self.line.append(self.pipes[i[1]]())

        for i in list:
            self.line[i[0]].add_target(self.line[i[2]])


    def piping(self, text, current = None):
        if current == None:
            current = self.line[0]
        child_count = 0
        while len(current.get_targets())>0:
            child_count+=1
            temp = current.get_targets()[0]
            current.delete_first_target()
            self.piping(text = current.piping(text), current = temp)
        if child_count==0:
            self.final_res.append(current.piping(text))

    def get_structure(self, current = None, level=0):
        if current == None:
            current = self.line[0]
        if(len(current.get_targets())>0):
            self.structure.append(str(level)+ " " + str(current))
        for i in current.get_targets():
            self.structure.append(str(i))
        while len(current.get_targets())>0:
            temp = current.get_targets()[0]
            current.delete_first_target()
            self.get_structure(current = temp, level=level+1)

    def get_structure(self, current = None, first = 1):
        if first == 1:
            current = self.line[0]
            first = 0
        if len(current.get_targets())>0:
            self.structure.append(str(current))
            self.get_structure(current = current.get_targets()[0], first = 0)
        else:
            self.structure.append(str(current))
            return self.structure




    def start(self, text):
        current = self.line[0]
        res = current.piping(text=text)
        while len(current.get_targets())>0:
            current = current.get_targets()[0]
            res = current.piping(res)
        return res

#    For create "pipeline" tree, we create matrix with 2 field for every function
#    id_parent, type_parent, id_child, type_child
#    below K is sequnce of that functions
#    [Text_to_sent, Text_to_words, Without_stop_words, Pos_tag, Output]

K = np.array([
    [1, 0, 1, 1],
    [1, 1, 1, 2],
    [1, 2, 1, 7],
    [1, 1, 1, 4],
    [1, 4, 2, 7]
])

p = Pipeline(K)

p.piping(text=t)

for i in p.final_res:
    print(i)
