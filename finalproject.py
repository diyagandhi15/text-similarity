import math


def clean_text(txt):
    """ takes a string of text txt as a parameter and returns a list 
        containing the words in txt after it has been “cleaned."
    """

    for character in txt:
        for symbol in """.,?"'!;:""":
           if character == symbol:
               txt = txt.replace(symbol, '')
    
    txt = txt.lower().split()
    
    return txt

def stem(s):
    """function should then return the stem of s. The stem of a word is 
       the root part of the word, which excludes any prefixes and suffixes
    """
    
    if s[-1] == 'y':
        s = s[:-1] + 'i'

    if s[-1] == 's':
        if s[-2] == 's':
            if s[-4:] == 'ness':
                s = s[:-4]  
            else:
                s = s[:-2]
        else: 
            s = s[:-1]
    
    if s[-2:] == 'er':
        if len(s) < 6:
            s = s
        else:
            s = s[:-2]    
    elif s[-1] == 'e':
        if len(s) < 4:
            s = s
        elif s[-2] == 'e':
            s = s
        else:
            s = s[:-1]
    elif s[-3:] == 'ing':
        if len(s) < 6:
            s = s
        elif s[-4] in 'bdgkmnprt':
            if s[-5] == s[-4]:
                s = s[:-4]
            else:
                s = s[:-3]
        else:
            s = s[:-3]

    return s

def punctuation(s):
    """returns a list of the number of punctuation marks (.?!:;,) in a string
    """
    
    period = 0
    question = 0 
    exclamation = 0
    colon = 0
    semicolon = 0
    comma = 0
    for c in s:
        if c == '.':
            period += 1
        elif c == '?':
            question += 1
        elif c == '!':
            exclamation += 1
        elif c == ':':
            colon += 1
        elif c ==';':
            semicolon += 1
        elif c == ',':
            comma += 1
    return [period, question, exclamation, colon, semicolon, comma]

def compare_dictionaries(d1, d2):
    """compute and returns the dictionaries' log similarity score
       inputs: dictionaries d1 and d2
    """
    
    total = 0
    if d1 == {}:
        return -50
    else:
        for words in d1:
            total += d1[words]
    
    score = 0
    for words2 in d2:
        if words2 in d1:
            if d1[words2] == 0:
                score += 0
            else:
                score += d2[words2] * math.log(d1[words2]/total)
        else:
            score += d2[words2] * math.log(0.5/total)
            
            
    return score
   

class TextModel:
    def __init__(self, model_name):
        """ constructs a new TextModel object by accepting a string 
            model_name as a parameter and initializing the following three 
            attributes:
        """
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.punctuation = {}
    
    
    def __repr__(self):
        """ return a string representation of the TextModel.
        """
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of distinct punctuations: ' + str(sum(self.punctuation[punct] for punct in self.punctuation))
        
        return s
    
   
    def add_string(self, s):
        """ analyzes the string txt and adds its pieces
        to all of the dictionaries in this text model.
        """
        
        count = 1
        if s[-1] in "?.!":
            for c in s: 
                if c == ' ':
                    count += 1
                elif c in '.?!':
                    if count in self.sentence_lengths:
                        self.sentence_lengths[count] += 1
                        count = 0
                    else:
                        self.sentence_lengths[count] = 1
                        count = 0
        
        else:
            for c in s: 
                if c == ' ':
                    count += 1
                elif c in '.?!':
                    if count in self.sentence_lengths:
                        self.sentence_lengths[count] += 1
                        count = 0
                    else:
                        self.sentence_lengths[count] = 1
                        count = 0
            
            if count in self.sentence_lengths:
                self.sentence_lengths[count] += 1
                count = 0
            else:
                self.sentence_lengths[count] = 1
                count = 0
        
        punct = punctuation(s)
        self.punctuation['.'] = punct[0]
        self.punctuation['?'] = punct[1]
        self.punctuation['!'] = punct[2]
        self.punctuation[':'] = punct[3]
        self.punctuation[';'] = punct[4]
        self.punctuation[','] = punct[5]
        
        word_list = clean_text(s)
        
        for w in word_list:
            if w in self.words:
                self.words[w] += 1
            else:
                self.words[w] = 1
        
        for w in word_list:
            if len(w) in self.word_lengths:
                self.word_lengths[len(w)] += 1
            else:
                self.word_lengths[len(w)] = 1    
                
        for w in word_list:
            if stem(w) in self.stems:
                self.stems[stem(w)] += 1
            else:
                self.stems[stem(w)] = 1
        
    
    def add_file(self, filename):
        """ adds all of the text in the file identified by filename to 
            the model. It should not explicitly return a value.
        """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        s = f.read()
        self.add_string(s)
        f.close()
        
   
    def save_model(self):
        """ saves the TextModel object self by writing its various feature 
            dictionaries to files. There will be one file written for each 
            feature dictionary.
        """
        words = self.words
        filename = self.name + '_words'
        f = open(filename, 'w')
        f.write(str(words))
        f.close()
        
        word_lengths = self.word_lengths
        filename = self.name + '_word_lengths'
        f = open(filename, 'w')
        f.write(str(word_lengths))
        f.close() 
        
        stems = self.stems
        filename = self.name +'_stems'
        f = open(filename, 'w')
        f.write(str(stems))
        f.close() 
        
        sentence_lengths = self.sentence_lengths
        filename = self.name + '_sentence_lengths'
        f = open(filename, 'w')
        f.write(str(sentence_lengths))
        f.close()
        
        punctuation = self.punctuation
        filename = self.name + '_punctuation'
        f = open(filename, 'w')
        f.write(str(punctuation))
        f.close()
        
        
    def read_model(self):
        """ reads the stored dictionaries for the called TextModel object 
            from their files and assigns them to the attributes of the called 
            TextModel.
        """
        f = open(self.name + '_words', 'r')
        d_str = f.read()
        f.close()
        self.words = dict(eval(d_str))
        
        f = open(self.name + '_word_lengths', 'r')
        d_str = f.read()
        f.close()
        self.word_lengths = dict(eval(d_str))
        
        f = open(self.name + '_stems', 'r')
        d_str = f.read()
        f.close()
        self.stems = dict(eval(d_str))
        
        f = open(self.name + '_sentence_lengths', 'r')
        d_str = f.read()
        f.close()
        self.sentence_lengths = dict(eval(d_str))
        
        f = open(self.name + '_punctuation', 'r')
        d_str = f.read()
        f.close()
        self.punctuation = dict(eval(d_str))
        
        
    def similarity_scores(self, other):
        """computes and returns a list of log similarity scores measuring 
           the similarity of self and other – one score for each type of 
           feature (words, word lengths, stems, sentence lengths, and your 
           additional feature).
        """
        word_score = compare_dictionaries(other.words, self.words)
        wlength_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        stem_score = compare_dictionaries(other.stems, self.stems)
        slength_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        punctuation_score = compare_dictionaries(other.punctuation, self.punctuation)
        return [word_score, wlength_score, stem_score, slength_score, punctuation_score]
    
    def classify(self, source1, source2):
        """compares the called TextModel object (self) to two other “source” 
           TextModel objects (source1 and source2) and determines which of 
           these other TextModels is the more likely source of the called TextModel
        """
        
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        s1 = 0
        for i in range(5):
            if scores1[i] > scores2[i]:
                s1 += 1
        
        if s1 >= 3:
            source = source1
        else:
            source = source2
    
        print('scores for ' + source1.name + ': ' + str(scores1))
        print('scores for ' + source2.name + ': ' + str(scores2))
        print(self.name + ' is more likely to have come from ' + source.name)

def run_tests():
    source1 = TextModel('poe_og')
    source1.add_file('poe_og_source_text.txt')

    source2 = TextModel('silverstein_og')
    source2.add_file('silverstein_og_source_text.txt')

    new1 = TextModel('drake')
    new1.add_file('drake_source_text.txt')
    new1.classify(source1, source2)
    
    new2 = TextModel('diya')
    new2.add_file('diya_source_text.txt')
    new2.classify(source1, source2)
    
    new3 = TextModel('poe')
    new3.add_file('poe_source_text.txt')
    new3.classify(source1, source2)
    
    new4 = TextModel('silverstein')
    new4.add_file('silverstein_source_text.txt')
    new4.classify(source1, source2)


                