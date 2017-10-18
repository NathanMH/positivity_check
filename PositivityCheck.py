####################
# Author: Nathan Mador-House
# Title: PositivityCheck
####################

####################
# Index:
#     1. Imports and Readme
#     2. Functions
#     3. Main
#     4. Testing
####################

###################################################################
# 1. IMPORTS AND README
###################################################################

import math
import string
import os

###################################################################
# 2. CLASSES & FUNCTIONS
###################################################################

class Afinn:
    """ A class to hold all of the afinn information. """
    def __init__(self):
        self.afinn_dict = {}
        self.afinn_set = set()

        #
        self.setup_afinn_structs()

    def setup_afinn_structs(self):
        """ Create a set and dictionary of the afinn word list. """
        try:
            afinn_file = os.path.dirname(__file__) + '/resources/AFINN-111.txt'
            self.afinn_dict = dict(line.split('\t') for line in open(afinn_file))
        except FileNotFoundError:
            afinn_file = os.path.dirname(__file__) + 'resources/AFINN-111.txt'
            self.afinn_dict = dict(line.split('\t') for line in open(afinn_file))

        #  Setup a dictionary with words as keys and integers for values.
        #  Setup a set of just the words from AFINN for quicker membership lookup.
        for word in self.afinn_dict:
            self.afinn_set.add(word)

class UserText:
    """ An object of the text that the user provides. """
    def __init__(self, text):
        self.afinn = Afinn()
        self.text = "".join(l for l in text if l not in string.punctuation)
        self.word_list = [x.lower() for x in self.text.split()]
        self.word_total = len(self.word_list)

        # Word counts, totals and percents set to 0
        self.matching_word_list = []
        self.neg_count, self.pos_count, self.neutral_count, \
        self.percent_neg, percent_pos, self.percent_neutral, \
        self.neg_total, self.pos_total = (0, 0, 0, 0, 0, 0, 0, 0)
        self.sentiment = 0

        # User generated word lists
        self.neg_word_list = []
        self.pos_word_list = []

        # Run functions
        self.find_matching_words()
        self.get_word_vals()
        self.eval_percentages()
        self.eval_sentiment()

    def find_matching_words(self):
        """ Find matching words from user text and assign vals using afinn object. """
        for word in self.word_list:
            if word in self.afinn.afinn_set:
                self.matching_word_list.append(word)

    def get_word_vals(self):
        """ Find the associate values of the words and add them to the totals. """
        for word in self.matching_word_list:
            val = self.afinn.afinn_dict[word]
            if int(val) < 0:
                self.neg_count += 1
                self.neg_total += int(val)
                self.neg_word_list.append(word)
            elif int(val) > 0:
                self.pos_count += 1
                self.pos_total += int(val)
                self.pos_word_list.append(word)
            else:
                self.neutral_count += 1

    def eval_percentages(self):
        """ Calculate the percentages of words. """
        try:
            self.percent_neg = round((self.neg_count / self.word_total) * 100, 2)
            self.percent_pos = round((self.pos_count / self.word_total) * 100, 2)
            self.percent_neutral = round((self.neutral_count / self.word_total) * 100, 2)
        except ZeroDivisionError:
            print("Uh oh, there was some division by zero.")

    def eval_sentiment(self):
        """ Calculate the final sentiment number. """
        try:
            self.sentiment = round((self.neg_total +
                                    self.pos_total) / math.sqrt(self.word_total), 3)
        except ZeroDivisionError:
            print("Uh oh, there was some division by zero.")

    def print_stats(self):
        """ Print the stats in the terminal. """
        print("Total words: " + str(self.word_total))
        print("Negative words: " + str(self.neg_count))
        print("Negative sum: " + str(self.neg_total))
        print("Positive words: " + str(self.pos_count))
        print("Positive sum: " + str(self.pos_total))
        print("Percent Negative Words: " + str(self.percent_neg))
        print("Percent Positive Words: " + str(self.percent_pos))
        print("Normalized Sentiments: " + str(self.sentiment))

    def print_word_lists(self):
        """ Print the entirety of the user generated word lists """
        print("Positive Words Used:")
        print(self.pos_word_list)
        print("Negative Words Used:")
        print(self.neg_word_list)

###################################################################
# 3. MAIN
###################################################################

if __name__ == "__main__":
    POS_CHECK_OBJ = UserText(input("Text for analysis: "))
    POS_CHECK_OBJ.print_stats()
    POS_CHECK_OBJ.print_word_lists()

###################################################################
# 4. TESTING
###################################################################


