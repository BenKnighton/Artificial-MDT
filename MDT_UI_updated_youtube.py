#input memory DIR which contains memory folders

defultLocation =  "Artificial_Memory"

from PyQt5 import QtCore, QtGui, QtWidgets
import itertools
import spacy
import time
import os
from spacy_wordnet.wordnet_annotator import WordnetAnnotator
from nltk.tokenize import sent_tokenize, word_tokenize
import subprocess
import webbrowser
import shutil

nlp = spacy.load('en_core_web_sm')
nlp.add_pipe("spacy_wordnet", after='tagger')


from spellchecker import SpellChecker
spell = SpellChecker()

def correct_sentence_spelling(sentence):
    misspelled = spell.unknown(word_tokenize(sentence))
    for word in misspelled:
        if len(word) >= 5:
            # Get the one `most likely` answer
            # print("lickly", word, spell.correction(word))
            # Get a list of `likely` options
            options = spell.candidates(word)
            if options is not None:
                all_options = "("+ ", ".join(list(spell.candidates(word)))+")"
                sentence = sentence.replace(word, all_options)
                # print("likley2", word, all_options)

    return sentence



#new func after observations to subsequent update
from nltk import ngrams
from difflib import SequenceMatcher

def difflib_dot(text, s_object):
    return SequenceMatcher(None, text, s_object).ratio()

def difflib_sim(phrase, text):
    phrase = phrase.lower()
    sentence = text.lower()

    n = len(word_tokenize(phrase))
    sixgrams = ngrams(sentence.split(), n)

    scores = []
    for grams in sixgrams:
        # print(grams)
        full_gram = " ".join(list(grams))
        dot_vec_score = difflib_dot(phrase, full_gram)
        scores.append((full_gram, dot_vec_score))

    most_simmilar = sorted(scores, key=lambda x: x[1], reverse=True)

    # print(most_simmilar)
    # print(time.time()-start)
    try:
        if 0.9 < most_simmilar[0][1] <= 1.0:
            # print(most_simmilar[0][1])
            # print(most_simmilar[0][0])
            return True
    except IndexError:
        pass
    
    return False









def dot(phrase, economy_domains):
    # start = time.time()
    sentence = nlp(phrase)
    enriched_sentence = []
    for token in sentence:
        synsets = token._.wordnet.wordnet_synsets_for_domain(economy_domains)
        if not synsets:
            enriched_sentence.append(token.text)
        else:
            lemmas_for_synset = [lemma.replace("_", " ") for s in synsets for lemma in s.lemma_names()]
            enriched_sentence.append('{}'.format(' <break> '.join(set(lemmas_for_synset))))

    combination = []
    for i in enriched_sentence:
        combination.append(i.split(" <break> "))

    combinations = list(itertools.product(*combination))
    results = []
    for phrase in combinations:
        print(" ".join(phrase))
        results.append(" ".join(phrase))

    # print(time.time()-start)
    return results



















class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1168, 771)
        Form.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.OCRlineEdit = QtWidgets.QLineEdit(Form)
        self.OCRlineEdit.setGeometry(QtCore.QRect(50, 355, 501, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        self.OCRlineEdit.setFont(font)
        self.OCRlineEdit.setStyleSheet("background-color:  rgb(244, 238, 229);\n"
"border :2px solid rgb(244, 238, 229);\n"
"color: rgb(0, 0, 0);")
        self.OCRlineEdit.setObjectName("OCRlineEdit")
        self.YOLOlineEdit = QtWidgets.QLineEdit(Form)
        self.YOLOlineEdit.setGeometry(QtCore.QRect(620, 57, 501, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        self.YOLOlineEdit.setFont(font)
        self.YOLOlineEdit.setStyleSheet("background-color:  rgb(244, 238, 229);\n"
"border :2px solid rgb(244, 238, 229);\n"
"color: rgb(0, 0, 0);")
        self.YOLOlineEdit.setObjectName("YOLOlineEdit")
        self.YOLO = QtWidgets.QLabel(Form)
        self.YOLO.setGeometry(QtCore.QRect(620, 30, 501, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        self.YOLO.setFont(font)
        self.YOLO.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.YOLO.setObjectName("YOLO")
        self.OCR = QtWidgets.QLabel(Form)
        self.OCR.setGeometry(QtCore.QRect(50, 330, 501, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        self.OCR.setFont(font)
        self.OCR.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.OCR.setObjectName("OCR")
        self.SEARCH_1 = QtWidgets.QPushButton(Form)
        self.SEARCH_1.setGeometry(QtCore.QRect(220, 390, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        self.SEARCH_1.setFont(font)
        self.SEARCH_1.setStyleSheet("QPushButton\n"
"                             {\n"
"                             background-color : rgb(244, 238, 229);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }\n"
"                             QPushButton::pressed\n"
"                             {\n"
"                             background-color : rgb(241, 234, 222);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }")
        self.SEARCH_1.setObjectName("SEARCH_1")
        self.CLEAR_1 = QtWidgets.QPushButton(Form)
        self.CLEAR_1.setGeometry(QtCore.QRect(459, 390, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        self.CLEAR_1.setFont(font)
        self.CLEAR_1.setStyleSheet("QPushButton\n"
"                             {\n"
"                             background-color : rgb(244, 238, 229);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }\n"
"                             QPushButton::pressed\n"
"                             {\n"
"                             background-color : rgb(241, 234, 222);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }")
        self.CLEAR_1.setObjectName("CLEAR_1")
        self.SEARCH_2 = QtWidgets.QPushButton(Form)
        self.SEARCH_2.setGeometry(QtCore.QRect(790, 92, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        self.SEARCH_2.setFont(font)
        self.SEARCH_2.setStyleSheet("QPushButton\n"
"                             {\n"
"                             background-color : rgb(244, 238, 229);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }\n"
"                             QPushButton::pressed\n"
"                             {\n"
"                             background-color : rgb(241, 234, 222);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }")
        self.SEARCH_2.setObjectName("SEARCH_2")
        self.CLEAR_2 = QtWidgets.QPushButton(Form)
        self.CLEAR_2.setGeometry(QtCore.QRect(1030, 92, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        self.CLEAR_2.setFont(font)
        self.CLEAR_2.setStyleSheet("QPushButton\n"
"                             {\n"
"                             background-color : rgb(244, 238, 229);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }\n"
"                             QPushButton::pressed\n"
"                             {\n"
"                             background-color : rgb(241, 234, 222);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }")
        self.CLEAR_2.setObjectName("CLEAR_2")
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setGeometry(QtCore.QRect(620, 350, 501, 151))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        self.scrollArea.setFont(font)
        self.scrollArea.setStyleSheet("background-color: rgb(255, 225, 108);\n"
"border-radius: 3px;\n"
"color: rgb(0, 0, 0);\n"
"")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        # self.scrollAreaWidgetContents = QtWidgets.QWidget()
        # self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 501, 151))
        # self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        # self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.DOMAINS_IN_USE = QtWidgets.QLabel(Form)
        self.DOMAINS_IN_USE.setGeometry(QtCore.QRect(620, 330, 501, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        self.DOMAINS_IN_USE.setFont(font)
        self.DOMAINS_IN_USE.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.DOMAINS_IN_USE.setObjectName("DOMAINS_IN_USE")
        self.GET_DOMAINS = QtWidgets.QPushButton(Form)
        self.GET_DOMAINS.setGeometry(QtCore.QRect(790, 696, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        self.GET_DOMAINS.setFont(font)
        self.GET_DOMAINS.setStyleSheet("QPushButton\n"
"                             {\n"
"                             background-color : rgb(244, 238, 229);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }\n"
"                             QPushButton::pressed\n"
"                             {\n"
"                             background-color : rgb(241, 234, 222);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }")
        self.GET_DOMAINS.setObjectName("GET_DOMAINS")
        self.scrollArea_2 = QtWidgets.QScrollArea(Form)
        self.scrollArea_2.setGeometry(QtCore.QRect(620, 530, 501, 161))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        self.scrollArea_2.setFont(font)
        self.scrollArea_2.setStyleSheet("background-color: rgb(255, 225, 108);\n"
"border-radius: 3px;\n"
"color: rgb(0, 0, 0);")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        # self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        # self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 501, 161))
        # self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        # self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.scrollArea_3 = QtWidgets.QScrollArea(Form)
        self.scrollArea_3.setGeometry(QtCore.QRect(50, 425, 501, 111))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        self.scrollArea_3.setFont(font)
        self.scrollArea_3.setStyleSheet("background-color:   rgb(255, 184, 62);\n"
"border :1px solid  rgb(255, 184, 62);\n"
"border-radius: 3px;\n"
"color: rgb(0, 0, 0);")
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollArea_3.setObjectName("scrollArea_3")
        # self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        # self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 499, 109))
        # self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        # self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)
        self.scrollArea_4 = QtWidgets.QScrollArea(Form)
        self.scrollArea_4.setGeometry(QtCore.QRect(620, 127, 501, 111))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        self.scrollArea_4.setFont(font)
        self.scrollArea_4.setStyleSheet("background-color:  rgb(129, 222, 145);\n"
"border :1px solid rgb(129, 222, 145);\n"
"border-radius: 3px;\n"
"color: rgb(0, 0, 0);")
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollArea_4.setObjectName("scrollArea_4")
        # self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        # self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 499, 109))
        # self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")
        # self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_4)
        self.OCR_RESULTS = QtWidgets.QLabel(Form)
        self.OCR_RESULTS.setGeometry(QtCore.QRect(50, 398, 111, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        self.OCR_RESULTS.setFont(font)
        self.OCR_RESULTS.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.OCR_RESULTS.setObjectName("OCR_RESULTS")
        self.YOLO_RESULTS = QtWidgets.QLabel(Form)
        self.YOLO_RESULTS.setGeometry(QtCore.QRect(620, 98, 121, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        self.YOLO_RESULTS.setFont(font)
        self.YOLO_RESULTS.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.YOLO_RESULTS.setObjectName("YOLO_RESULTS")
        self.DOMAINS_AVALIABLE = QtWidgets.QLabel(Form)
        self.DOMAINS_AVALIABLE.setGeometry(QtCore.QRect(620, 510, 491, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        self.DOMAINS_AVALIABLE.setFont(font)
        self.DOMAINS_AVALIABLE.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.DOMAINS_AVALIABLE.setObjectName("DOMAINS_AVALIABLE")
        self.MDT = QtWidgets.QLabel(Form)
        self.MDT.setGeometry(QtCore.QRect(50, 640, 501, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        self.MDT.setFont(font)
        self.MDT.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.MDT.setObjectName("MDT")
        self.OPEN_1 = QtWidgets.QPushButton(Form)
        self.OPEN_1.setGeometry(QtCore.QRect(110, 540, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        self.OPEN_1.setFont(font)
        self.OPEN_1.setStyleSheet("QPushButton\n"
"                             {\n"
"                             background-color : rgb(255, 239, 212);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }\n"
"                             QPushButton::pressed\n"
"                             {\n"
"                             background-color : rgb(255, 236, 203);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }")
        self.OPEN_1.setObjectName("OPEN_1")
        self.OPEN_2 = QtWidgets.QPushButton(Form)
        self.OPEN_2.setGeometry(QtCore.QRect(680, 242, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        self.OPEN_2.setFont(font)
        self.OPEN_2.setStyleSheet("QPushButton\n"
"                             {\n"
"                             background-color : rgb(230, 248, 233);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }\n"
"                             QPushButton::pressed\n"
"                             {\n"
"                             background-color : rgb(223, 246, 226);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }")
        self.OPEN_2.setObjectName("OPEN_2")
        self.CLEAR_RES_1 = QtWidgets.QPushButton(Form)
        self.CLEAR_RES_1.setGeometry(QtCore.QRect(240, 540, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        self.CLEAR_RES_1.setFont(font)
        self.CLEAR_RES_1.setStyleSheet("QPushButton\n"
"                             {\n"
"                             background-color : rgb(255, 239, 212);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }\n"
"                             QPushButton::pressed\n"
"                             {\n"
"                             background-color : rgb(255, 236, 203);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }")
        self.CLEAR_RES_1.setObjectName("CLEAR_RES_1")
        self.CLEAR_RES_2 = QtWidgets.QPushButton(Form)
        self.CLEAR_RES_2.setGeometry(QtCore.QRect(810, 242, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        self.CLEAR_RES_2.setFont(font)
        self.CLEAR_RES_2.setStyleSheet("QPushButton\n"
"                             {\n"
"                             background-color : rgb(230, 248, 233);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }\n"
"                             QPushButton::pressed\n"
"                             {\n"
"                             background-color : rgb(223, 246, 226);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }")
        self.CLEAR_RES_2.setObjectName("CLEAR_RES_2")
        self.CHOOSE_FOLDER = QtWidgets.QLineEdit(Form)
        self.CHOOSE_FOLDER.setGeometry(QtCore.QRect(50, 660, 501, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        self.CHOOSE_FOLDER.setFont(font)
        self.CHOOSE_FOLDER.setStyleSheet("background-color:  rgb(207, 207, 207);\n"
"border :2px solid rgb(207, 207, 207);\n"
"color: rgb(0, 0, 0);")
        self.CHOOSE_FOLDER.setObjectName("CHOOSE_FOLDER")
        self.GET_FOLDER = QtWidgets.QPushButton(Form)
        self.GET_FOLDER.setGeometry(QtCore.QRect(50, 696, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        self.GET_FOLDER.setFont(font)
        self.GET_FOLDER.setStyleSheet("QPushButton\n"
"                             {\n"
"                             background-color : rgb(244, 238, 229);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }\n"
"                             QPushButton::pressed\n"
"                             {\n"
"                             background-color : rgb(241, 234, 222);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }")
        self.GET_FOLDER.setObjectName("GET_FOLDER")
        self.GENERATE_VAR = QtWidgets.QPushButton(Form)
        self.GENERATE_VAR.setGeometry(QtCore.QRect(160, 696, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        self.GENERATE_VAR.setFont(font)
        self.GENERATE_VAR.setStyleSheet("QPushButton\n"
"                             {\n"
"                             background-color : rgb(244, 238, 229);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }\n"
"                             QPushButton::pressed\n"
"                             {\n"
"                             background-color : rgb(241, 234, 222);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }")
        self.GENERATE_VAR.setObjectName("GENERATE_VAR")
        self.CLEAR_PATH = QtWidgets.QPushButton(Form)
        self.CLEAR_PATH.setGeometry(QtCore.QRect(310, 696, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        self.CLEAR_PATH.setFont(font)
        self.CLEAR_PATH.setStyleSheet("QPushButton\n"
"                             {\n"
"                             background-color : rgb(244, 238, 229);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }\n"
"                             QPushButton::pressed\n"
"                             {\n"
"                             background-color : rgb(241, 234, 222);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }")
        self.CLEAR_PATH.setObjectName("CLEAR_PATH")
        self.YOUTUBElineEdit = QtWidgets.QLineEdit(Form)
        self.YOUTUBElineEdit.setGeometry(QtCore.QRect(50, 57, 501, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        self.YOUTUBElineEdit.setFont(font)
        self.YOUTUBElineEdit.setStyleSheet("background-color:  rgb(244, 238, 229);\n"
"border :2px solid rgb(244, 238, 229);\n"
"color: rgb(0, 0, 0);")
        self.YOUTUBElineEdit.setObjectName("YOUTUBElineEdit")
        self.SEARCH_3 = QtWidgets.QPushButton(Form)
        self.SEARCH_3.setGeometry(QtCore.QRect(220, 92, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        self.SEARCH_3.setFont(font)
        self.SEARCH_3.setStyleSheet("QPushButton\n"
"                             {\n"
"                             background-color : rgb(244, 238, 229);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }\n"
"                             QPushButton::pressed\n"
"                             {\n"
"                             background-color : rgb(241, 234, 222);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }")
        self.SEARCH_3.setObjectName("SEARCH_3")
        self.CLEAR_3 = QtWidgets.QPushButton(Form)
        self.CLEAR_3.setGeometry(QtCore.QRect(460, 92, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        self.CLEAR_3.setFont(font)
        self.CLEAR_3.setStyleSheet("QPushButton\n"
"                             {\n"
"                             background-color : rgb(244, 238, 229);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }\n"
"                             QPushButton::pressed\n"
"                             {\n"
"                             background-color : rgb(241, 234, 222);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }")
        self.CLEAR_3.setObjectName("CLEAR_3")
        self.scrollArea_5 = QtWidgets.QScrollArea(Form)
        self.scrollArea_5.setGeometry(QtCore.QRect(50, 127, 501, 111))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        self.scrollArea_5.setFont(font)
        self.scrollArea_5.setStyleSheet("background-color:  rgb(99, 219, 255);\n"
"border :1px solid rgb(99, 219, 255);\n"
"border-radius: 3px;\n"
"color: rgb(0, 0, 0);")
        self.scrollArea_5.setWidgetResizable(True)
        self.scrollArea_5.setObjectName("scrollArea_5")
        # self.scrollAreaWidgetContents_5 = QtWidgets.QWidget()
        # self.scrollAreaWidgetContents_5.setGeometry(QtCore.QRect(0, 0, 499, 109))
        # self.scrollAreaWidgetContents_5.setObjectName("scrollAreaWidgetContents_5")
        # self.scrollArea_5.setWidget(self.scrollAreaWidgetContents_5)
        self.YOUTUBE = QtWidgets.QLabel(Form)
        self.YOUTUBE.setGeometry(QtCore.QRect(50, 30, 501, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        self.YOUTUBE.setFont(font)
        self.YOUTUBE.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.YOUTUBE.setObjectName("YOUTUBE")
        self.OPEN_3 = QtWidgets.QPushButton(Form)
        self.OPEN_3.setGeometry(QtCore.QRect(120, 242, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        self.OPEN_3.setFont(font)
        self.OPEN_3.setStyleSheet("QPushButton\n"
"                             {\n"
"                             background-color : rgb(224, 248, 255);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }\n"
"                             QPushButton::pressed\n"
"                             {\n"
"                             background-color : rgb(214, 246, 255);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }")
        self.OPEN_3.setObjectName("OPEN_3")
        self.CLEAR_RES_3 = QtWidgets.QPushButton(Form)
        self.CLEAR_RES_3.setGeometry(QtCore.QRect(250, 242, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        self.CLEAR_RES_3.setFont(font)
        self.CLEAR_RES_3.setStyleSheet("QPushButton\n"
"                             {\n"
"                             background-color : rgb(224, 248, 255);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }\n"
"                             QPushButton::pressed\n"
"                             {\n"
"                             background-color : rgb(214, 246, 255);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }")
        self.CLEAR_RES_3.setObjectName("CLEAR_RES_3")
        self.YOUTUBE_SPELL_CHECK = QtWidgets.QPushButton(Form)
        self.YOUTUBE_SPELL_CHECK.setGeometry(QtCore.QRect(317, 92, 137, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        self.YOUTUBE_SPELL_CHECK.setFont(font)
        self.YOUTUBE_SPELL_CHECK.setStyleSheet("QPushButton\n"
"                             {\n"
"                             background-color : rgb(244, 238, 229);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }\n"
"                             QPushButton::pressed\n"
"                             {\n"
"                             background-color : rgb(241, 234, 222);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }")
        self.YOUTUBE_SPELL_CHECK.setObjectName("YOUTUBE_SPELL_CHECK")
        self.YOLO_SPELL_CHECK = QtWidgets.QPushButton(Form)
        self.YOLO_SPELL_CHECK.setGeometry(QtCore.QRect(887, 92, 137, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        self.YOLO_SPELL_CHECK.setFont(font)
        self.YOLO_SPELL_CHECK.setStyleSheet("QPushButton\n"
"                             {\n"
"                             background-color : rgb(244, 238, 229);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }\n"
"                             QPushButton::pressed\n"
"                             {\n"
"                             background-color : rgb(241, 234, 222);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }")
        self.YOLO_SPELL_CHECK.setObjectName("YOLO_SPELL_CHECK")
        self.OCR_SPELL_CHECK = QtWidgets.QPushButton(Form)
        self.OCR_SPELL_CHECK.setGeometry(QtCore.QRect(317, 390, 137, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        self.OCR_SPELL_CHECK.setFont(font)
        self.OCR_SPELL_CHECK.setStyleSheet("QPushButton\n"
"                             {\n"
"                             background-color : rgb(244, 238, 229);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }\n"
"                             QPushButton::pressed\n"
"                             {\n"
"                             background-color : rgb(241, 234, 222);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }")
        self.OCR_SPELL_CHECK.setObjectName("OCR_SPELL_CHECK")
        self.YOUTUBE_RESULTS = QtWidgets.QLabel(Form)
        self.YOUTUBE_RESULTS.setGeometry(QtCore.QRect(50, 100, 141, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        self.YOUTUBE_RESULTS.setFont(font)
        self.YOUTUBE_RESULTS.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.YOUTUBE_RESULTS.setObjectName("YOUTUBE_RESULTS")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(40, 20, 521, 261))
        self.label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 3px;")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(610, 20, 521, 261))
        self.label_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 3px;")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(40, 320, 521, 261))
        self.label_3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 3px;")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(610, 320, 521, 417))
        self.label_4.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 3px;")
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(40, 630, 521, 107))
        self.label_5.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 3px;")
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(0, 0, 1168, 771))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("90.webp"))
        self.label_6.setScaledContents(True)
        self.label_6.setObjectName("label_6")
        self.spinBox = QtWidgets.QSpinBox(Form)
        self.spinBox.setGeometry(QtCore.QRect(50, 240, 51, 31))
        self.spinBox.setObjectName("spinBox")
        self.spinBox_2 = QtWidgets.QSpinBox(Form)
        self.spinBox_2.setGeometry(QtCore.QRect(50, 540, 51, 31))
        self.spinBox_2.setObjectName("spinBox_2")
        self.spinBox_3 = QtWidgets.QSpinBox(Form)
        self.spinBox_3.setGeometry(QtCore.QRect(620, 240, 51, 31))
        self.spinBox_3.setObjectName("spinBox_3")
        self.gallery_YOUTUBE_button = QtWidgets.QPushButton(Form)
        self.gallery_YOUTUBE_button.setGeometry(QtCore.QRect(380, 242, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.gallery_YOUTUBE_button.setFont(font)
        self.gallery_YOUTUBE_button.setStyleSheet("QPushButton\n"
"                             {\n"
"                             background-color : rgb(224, 248, 255);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }\n"
"                             QPushButton::pressed\n"
"                             {\n"
"                             background-color : rgb(214, 246, 255);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }")
        self.gallery_YOUTUBE_button.setObjectName("gallery_YOUTUBE_button")
        self.gallery_OCR_button = QtWidgets.QPushButton(Form)
        self.gallery_OCR_button.setGeometry(QtCore.QRect(370, 540, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.gallery_OCR_button.setFont(font)
        self.gallery_OCR_button.setStyleSheet("QPushButton\n"
"                             {\n"
"                             background-color : rgb(255, 239, 212);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }\n"
"                             QPushButton::pressed\n"
"                             {\n"
"                             background-color : rgb(255, 236, 203);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }")
        self.gallery_OCR_button.setObjectName("gallery_OCR_button")
        self.gallery_YOLO_button = QtWidgets.QPushButton(Form)
        self.gallery_YOLO_button.setGeometry(QtCore.QRect(940, 242, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.gallery_YOLO_button.setFont(font)
        self.gallery_YOLO_button.setStyleSheet("QPushButton\n"
"                             {\n"
"                             background-color : rgb(230, 248, 233);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }\n"
"                             QPushButton::pressed\n"
"                             {\n"
"                             background-color : rgb(223, 246, 226);\n"
"                        color: rgb(0, 0, 0);\n"
"                             }")
        self.gallery_YOLO_button.setObjectName("gallery_YOLO_button")
        self.label_6.raise_()
        self.label_5.raise_()
        self.label_4.raise_()
        self.label_3.raise_()
        self.label_2.raise_()
        self.label.raise_()
        self.OCRlineEdit.raise_()
        self.YOLOlineEdit.raise_()
        self.YOLO.raise_()
        self.OCR.raise_()
        self.SEARCH_1.raise_()
        self.CLEAR_1.raise_()
        self.SEARCH_2.raise_()
        self.CLEAR_2.raise_()
        self.scrollArea.raise_()
        self.DOMAINS_IN_USE.raise_()
        self.GET_DOMAINS.raise_()
        self.scrollArea_2.raise_()
        self.scrollArea_3.raise_()
        self.scrollArea_4.raise_()
        self.OCR_RESULTS.raise_()
        self.YOLO_RESULTS.raise_()
        self.DOMAINS_AVALIABLE.raise_()
        self.MDT.raise_()
        self.OPEN_1.raise_()
        self.OPEN_2.raise_()
        self.CLEAR_RES_1.raise_()
        self.CLEAR_RES_2.raise_()
        self.CHOOSE_FOLDER.raise_()
        self.GET_FOLDER.raise_()
        self.GENERATE_VAR.raise_()
        self.CLEAR_PATH.raise_()
        self.YOUTUBElineEdit.raise_()
        self.SEARCH_3.raise_()
        self.CLEAR_3.raise_()
        self.scrollArea_5.raise_()
        self.YOUTUBE.raise_()
        self.OPEN_3.raise_()
        self.CLEAR_RES_3.raise_()
        self.YOUTUBE_SPELL_CHECK.raise_()
        self.YOLO_SPELL_CHECK.raise_()
        self.OCR_SPELL_CHECK.raise_()
        self.YOUTUBE_RESULTS.raise_()
        self.spinBox.raise_()
        self.spinBox_2.raise_()
        self.spinBox_3.raise_()
        self.gallery_YOUTUBE_button.raise_()
        self.gallery_OCR_button.raise_()
        self.gallery_YOLO_button.raise_()






        # self.scrollAreaWidgetContents = QtWidgets.QTextEdit(Form)
        # self.scrollAreaWidgetContents.setFont(font)
        # self.scrollAreaWidgetContents.setStyleSheet("background-color: transparent;")
        # self.scrollAreaWidgetContents.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        # self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 269, 139))
        # self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        # self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # self.scrollAreaWidgetContents_2 = QtWidgets.QTextEdit(Form)
        # self.scrollAreaWidgetContents_2.setFont(font)
        # self.scrollAreaWidgetContents_2.setStyleSheet("background-color: transparent;")
        # self.scrollAreaWidgetContents_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        # self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 449, 139))
        # self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        # self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        # self.scrollAreaWidgetContents_3 = QtWidgets.QTextEdit(Form)
        # self.scrollAreaWidgetContents_3.setFont(font)
        # self.scrollAreaWidgetContents_3.setStyleSheet("background-color: transparent;")
        # self.scrollAreaWidgetContents_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        # self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 359, 129))
        # self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        # self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)

        # self.scrollAreaWidgetContents_4 = QtWidgets.QTextEdit(Form)
        # self.scrollAreaWidgetContents_4.setFont(font)
        # self.scrollAreaWidgetContents_4.setStyleSheet("background-color: transparent;")
        # self.scrollAreaWidgetContents_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        # self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 359, 129))
        # self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")
        # self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_4)





        Form.setFixedSize(1168, 771)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)

        self.scrollAreaWidgetContents =  QtWidgets.QTextEdit(Form)
        self.scrollAreaWidgetContents.setFont(font)
        self.scrollAreaWidgetContents.setStyleSheet("background-color: transparent;")
        self.scrollAreaWidgetContents.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 501, 151))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
 
        self.scrollAreaWidgetContents_2 =  QtWidgets.QTextEdit(Form)
        self.scrollAreaWidgetContents_2.setFont(font)
        self.scrollAreaWidgetContents_2.setStyleSheet("background-color: transparent;")
        self.scrollAreaWidgetContents_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 501, 161))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.scrollAreaWidgetContents_3 =  QtWidgets.QTextEdit(Form)
        self.scrollAreaWidgetContents_3.setStyleSheet("background-color: transparent;")
        self.scrollAreaWidgetContents_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 499, 109))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)

        self.scrollAreaWidgetContents_4 =  QtWidgets.QTextEdit(Form)
        self.scrollAreaWidgetContents_4.setStyleSheet("background-color: transparent;")
        self.scrollAreaWidgetContents_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 499, 109))
        self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")
        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_4)

        self.scrollAreaWidgetContents_5 =  QtWidgets.QTextEdit(Form)
        self.scrollAreaWidgetContents_5.setStyleSheet("background-color: transparent;")
        self.scrollAreaWidgetContents_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.scrollAreaWidgetContents_5.setGeometry(QtCore.QRect(0, 0, 499, 109))
        self.scrollAreaWidgetContents_5.setObjectName("scrollAreaWidgetContents_5")
        self.scrollArea_5.setWidget(self.scrollAreaWidgetContents_5)


        # self.spinBox.valueChanged.connect(self.valuechange)
        # self.spinBox_2.valueChanged.connect(self.valuechange_2)
        # self.spinBox_3.valueChanged.connect(self.valuechange_3)





        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.scrollAreaWidgetContents.setText("physics, metrology, electronics, mathematics, astronomy, electricity, electrotechnology, acoustics, mechanics, oceanography, chemistry, geology, number")
        self.OCRlineEdit.returnPressed.connect(self.ocr_mdt)
        self.YOLOlineEdit.returnPressed.connect(self.yolo_mdt)
        self.CHOOSE_FOLDER.returnPressed.connect(self.create_variables)
        self.SEARCH_1.clicked.connect(self.ocr_mdt)
        self.SEARCH_2.clicked.connect(self.yolo_mdt)
        self.SEARCH_3.clicked.connect(self.youtube_mdt)
        self.CLEAR_1.clicked.connect(self.clear_ocr)
        self.CLEAR_2.clicked.connect(self.clear_yolo)
        self.CLEAR_3.clicked.connect(self.clear_youtube)
        self.GET_DOMAINS.clicked.connect(self.get_domains)
        self.OPEN_1.clicked.connect(self.open_ocr)
        self.OPEN_2.clicked.connect(self.open_yolo)
        self.OPEN_3.clicked.connect(self.open_youtube)
        self.CLEAR_RES_1.clicked.connect(self.clear_ocr_res)
        self.CLEAR_RES_2.clicked.connect(self.clear_yolo_res)
        self.CLEAR_RES_3.clicked.connect(self.clear_youtube_res)
        self.GET_FOLDER.clicked.connect(self.get_main_folder)
        self.GENERATE_VAR.clicked.connect(self.create_variables)
        self.CLEAR_PATH.clicked.connect(self.clear_folder_path)
        self.YOUTUBE_SPELL_CHECK.clicked.connect(self.youtube_spell_check)
        self.OCR_SPELL_CHECK.clicked.connect(self.ocr_spell_check)
        self.YOLO_SPELL_CHECK.clicked.connect(self.yolo_spell_check)

        self.gallery_OCR_button.clicked.connect(self.open_ocr_gallery_folder)
        self.gallery_YOLO_button.clicked.connect(self.open_yolo_gallery_folder)
        self.gallery_YOUTUBE_button.clicked.connect(self.open_youtube_gallery_folder)

        #this is the initial state so that an error doesnt occur
        MemoryTerminus = defultLocation
        ArtificialMemory = []
        rootdir = MemoryTerminus
        for file in os.listdir(rootdir):
            d = os.path.join(rootdir, file)
            if os.path.isdir(d):
                print(d)
                ArtificialMemory.append(d)

        ArtificialMemory.sort()
        self.YOLO_Dirs = []
        self.OCR_Dirs = []
        self.YOUTUBE_Dirs = []
        for folder in ArtificialMemory:
            print("folder", folder)
            files = os.listdir(folder)
            files.sort()
            for file in files:
                if file.endswith(".DS_Store"):
                    files.remove(file)

            variable = ", ".join(map(str, files))
            if "YOLO.txt" in variable:
                self.YOLO_Dirs.append(folder)

            if "OCR.txt" in variable:
                self.OCR_Dirs.append(folder)

            #updated to influde youtube folders
            if "YOUTUBE.txt" in variable:
                self.YOUTUBE_Dirs.append(folder)
        #end of initial values



    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Artificial MDT"))
        self.YOLO.setText(_translate("Form", "Object Detection Keywords"))
        self.OCR.setText(_translate("Form", "Optical Charater Recognition Keywords"))
        self.SEARCH_1.setText(_translate("Form", "Search"))
        self.CLEAR_1.setText(_translate("Form", "Clear"))
        self.SEARCH_2.setText(_translate("Form", "Search"))
        self.CLEAR_2.setText(_translate("Form", "Clear"))
        self.DOMAINS_IN_USE.setText(_translate("Form", "OCR Domains In Use"))
        self.GET_DOMAINS.setText(_translate("Form", "Get OCR Domains"))
        self.OCR_RESULTS.setText(_translate("Form", "OCR Results ▼"))
        self.YOLO_RESULTS.setText(_translate("Form", "OD Results ▼"))
        self.DOMAINS_AVALIABLE.setText(_translate("Form", "OCR Domains Avaliable"))
        self.MDT.setText(_translate("Form", "Memory Location Directory"))
        self.OPEN_1.setText(_translate("Form", "Open Files"))
        self.OPEN_2.setText(_translate("Form", "Open Files"))
        self.CLEAR_RES_1.setText(_translate("Form", "Clear Results"))
        self.CLEAR_RES_2.setText(_translate("Form", "Clear Results"))
        self.GET_FOLDER.setText(_translate("Form", "Get DIR"))
        self.GENERATE_VAR.setText(_translate("Form", "Use Location"))
        self.CLEAR_PATH.setText(_translate("Form", "Clear"))
        self.SEARCH_3.setText(_translate("Form", "Search"))
        self.CLEAR_3.setText(_translate("Form", "Clear"))
        self.YOUTUBE.setText(_translate("Form", "Video Transcript Keywords"))
        self.OPEN_3.setText(_translate("Form", "Open Links"))
        self.CLEAR_RES_3.setText(_translate("Form", "Clear Results"))
        self.YOUTUBE_SPELL_CHECK.setText(_translate("Form", "Spell Check"))
        self.YOLO_SPELL_CHECK.setText(_translate("Form", "Spell Check"))
        self.OCR_SPELL_CHECK.setText(_translate("Form", "Spell Check"))
        self.YOUTUBE_RESULTS.setText(_translate("Form", "Video Results ▼"))
        self.gallery_YOUTUBE_button.setText(_translate("Form", "Create Folder"))
        self.gallery_OCR_button.setText(_translate("Form", "Create Folder"))
        self.gallery_YOLO_button.setText(_translate("Form", "Create Folder"))


    # def valuechange(self):
    #     results = self.scrollAreaWidgetContents_5.toPlainText()
    #     # print(results)
    #     length = len(results.split("\n"))
    #     # self.spinBox.setMaximum(length)
    #     print(self.spinBox.value())

    # def valuechange_2(self):
    #     results = self.scrollAreaWidgetContents_3.toPlainText()
    #     # print(results)
    #     length = len(results.split("\n"))
    #     # self.spinBox_2.setMaximum(length)
    #     print(self.spinBox_2.value())

    # def valuechange_3(self):
    #     results = self.scrollAreaWidgetContents_4.toPlainText()
    #     # print(results)
    #     length = len(results.split("\n"))
    #     # self.spinBox_3.setMaximum(length)
    #     print(self.spinBox_3.value())




    def open_ocr_gallery_folder(self):
        folder_name = "ocr gallery"

        if os.path.isdir(folder_name):
            shutil.rmtree(folder_name)

        os.mkdir(folder_name)
        results = self.scrollAreaWidgetContents_3.toPlainText()
        top_ten = results.split("\n")[:-1]
        for i in top_ten:
            x, y, z = i.partition(" rate: ")
            print(x)
            shutil.copy2(x, folder_name)

        print(f"created {folder_name} folder")
        subprocess.call(["open", folder_name])



    def open_yolo_gallery_folder(self):
        folder_name = "yolo gallery"

        if os.path.isdir(folder_name):
            shutil.rmtree(folder_name)
            
        os.mkdir(folder_name)
        results = self.scrollAreaWidgetContents_4.toPlainText()
        top_ten = results.split("\n")[:-1]
        for i in top_ten:
            x, y, z = i.partition(" rate: ")
            print("file", x)
            shutil.copy2(x, folder_name)

        print(f"created {folder_name} folder")
        subprocess.call(["open", folder_name])





    def open_youtube_gallery_folder(self):
        print("need to think of what to do here")
        pass










    def youtube_spell_check(self):
        text = self.YOUTUBElineEdit.text()
        corrected = str(correct_sentence_spelling(text))
        self.YOUTUBElineEdit.setText(corrected)


    def ocr_spell_check(self):
        text = self.OCRlineEdit.text()
        corrected = str(correct_sentence_spelling(text))
        self.OCRlineEdit.setText(corrected)


    def yolo_spell_check(self):
        text = self.YOLOlineEdit.text()
        corrected = str(correct_sentence_spelling(text))
        print(corrected)
        self.YOLOlineEdit.setText(corrected)





    def youtube_mdt(self):
        input_search = self.YOUTUBElineEdit.text()
        # print(input_search)
        # pass


        # input_search = self.OCRlineEdit.text()
        print(input_search)
        # input_search = "Maxwell velocity distribution, maxwell, velocity, speed,  Maxwellian speed, W boson"
        # economy_domains = ['mathematics', 'physics', "computing"]  mathematics, physics, computing
        economy_domains = word_tokenize(self.scrollAreaWidgetContents.toPlainText().replace(",", " "))
        print(economy_domains)



        #list of keywords and phrases
        keywords = []
        phrases = []
        extended_phrases = []
        extended_keywords = []
        for i in input_search.split(","):
            pills = word_tokenize(i)
            token = " ".join(map(str, pills))
            if len(pills) > 1:
                phrases.append(token)
            else:
                keywords.append(token)

        for phrase in phrases:
            simmilar_results = dot(phrase, economy_domains)
            extended_phrases.append(simmilar_results)

        for keyword in keywords:
            simmilar_results = dot(keyword, economy_domains)
            extended_keywords.append(simmilar_results)

        extended_phrases  = [i for sub in extended_phrases  for i in sub]
        extended_keywords = [i for sub in extended_keywords for i in sub]
        extended_keywords = list(dict.fromkeys(extended_keywords))
        extended_phrases = list(dict.fromkeys(extended_phrases))

        print("phrases", phrases)
        print("keywords", keywords)

        #remove phrases and keywords form extended_phrases and extended_keywords if i want to make faster
        print("extended_phrases", extended_phrases)
        print("extended_keywords", extended_keywords)

        #creating the Corpus

        print("self.YOUTUBE_Dirs", self.YOUTUBE_Dirs)


        #creaing YOUTUBE the corpus
        YOUTUBE_Corpuc = []
        print(len(self.YOUTUBE_Dirs))
        for i in self.YOUTUBE_Dirs:
            print("reading:", f"{i}/YOUTUBE.txt")
            with open(f"{i}/YOUTUBE.txt", "r") as file:
                data = file.readlines()
            
            for j in data:
                x = j.split(" <break> ")
                YOUTUBE_Corpuc.append((x[0], x[1].replace("\n", "")))

            file.close()

        # print("\n"+str(len(YOUTUBE_Corpuc))+"\n")
        # searchable_OCR_sentences
        def removeDuplicates(lst):
            return [[a, b] for i, [a, b] in enumerate(lst)
            if not any(c == b for _, c in lst[:i])]
            
        YOUTUBE_Corpuc = removeDuplicates(YOUTUBE_Corpuc)
        # print(f"\nUpdated: \n{YOUTUBE_Corpuc}")
        # print("\n"+str(len(YOUTUBE_Corpuc))+"\n")
        # print(YOUTUBE_Corpuc)


        #finding the results in OCR
        OCR_results = []
        for i in YOUTUBE_Corpuc:
            paragrpah = i[1].lower()
            print(paragrpah)

            for phrase in phrases:
                if phrase.lower() in paragrpah:
                    OCR_results.append(i[0])
                    pass

            #implamented after update
            for phrase in phrases:
                if difflib_sim(phrase, paragrpah):
                    OCR_results.append(i[0])
                    print("there was a result", phrase, paragrpah)
                    pass


            for keyword in keywords:
                if keyword.lower() in paragrpah:
                    OCR_results.append(i[0])
                    pass

            for extended_phrase in extended_phrases:
                if extended_phrase.lower() in paragrpah:
                    OCR_results.append(i[0])
                    pass

            for extended_keyword in extended_keywords:
                if extended_keyword.lower() in paragrpah:
                    OCR_results.append(i[0])
                    pass

        OCR_removed = list(dict.fromkeys(OCR_results))
        OCR_sorted_results = []
        for i in OCR_removed:
            x = OCR_results.count(i)
            # print(i, x)
            OCR_sorted_results.append((i, x))


        print("YOUTUBE Results")
        x = sorted(OCR_sorted_results, key=lambda x: x[1], reverse=True)
        y = ""
        for i in x:
            y += f"{i[0]} rate: {i[1]}\n"
            print(i)

        self.scrollAreaWidgetContents_5.setText(y)
        self.spinBox.setValue(len(x))
        self.spinBox.setMaximum(len(x))






























    def clear_youtube(self):
        self.YOUTUBElineEdit.clear()



    # def open_youtube(self):
    #     results = self.scrollAreaWidgetContents_5.toPlainText()
        
    #     print(results)
    #     top_ten = results.split("\n")[:10]
    #     for i in top_ten:
    #         x, y, z = i.partition(" rate: ")
    #         print(x)
    #         print("opening youtube results")
    #         webbrowser.open_new_tab(x)
            



    def clear_youtube_res(self):
        self.scrollAreaWidgetContents_5.clear()





    def clear_folder_path(self):
        self.CHOOSE_FOLDER.clear()

    def get_main_folder(self):
        folderpath = QtWidgets.QFileDialog.getExistingDirectory(Form, 'Select a directory')
        print(folderpath)
        self.CHOOSE_FOLDER.setText(folderpath)


    def create_variables(self):
        try:
            MemoryTerminus = self.CHOOSE_FOLDER.text()

            ArtificialMemory = []
            rootdir = MemoryTerminus
            for file in os.listdir(rootdir):
                d = os.path.join(rootdir, file)
                if os.path.isdir(d):
                    print(d)
                    ArtificialMemory.append(d)

            ArtificialMemory.sort()
            self.YOLO_Dirs = []
            self.OCR_Dirs = []
            self.YOUTUBE_Dirs = []
            for folder in ArtificialMemory:
                print("folder", folder)
                files = os.listdir(folder)
                files.sort()
                for file in files:
                    if file.endswith(".DS_Store"):
                        files.remove(file)

                variable = ", ".join(map(str, files))
                if "YOLO.txt" in variable:
                    self.YOLO_Dirs.append(folder)

                if "OCR.txt" in variable:
                    self.OCR_Dirs.append(folder)

                #updated to influde youtube folders
                if "YOUTUBE.txt" in variable:
                    self.YOUTUBE_Dirs.append(folder)
        except Exception as e:
            print(f"not a path {e}")








    def open_ocr(self):
        results = self.scrollAreaWidgetContents_3.toPlainText()
        # length = len(results.split("\n"))
        # self.spinBox_2.setMaximum(length)
        # print(self.spinBox_2.value())
        # print(results)
        top_ten = results.split("\n")[:self.spinBox_2.value()]
        for i in top_ten:
            x, y, z = i.partition(" rate: ")
            print(x)
            subprocess.call(["open", x])
            # print(i)

        print("opening ocr results")


    def open_yolo(self):
        results = self.scrollAreaWidgetContents_4.toPlainText()
        # length = len(results.split("\n"))
        # self.spinBox_3.setMaximum(length)
        # print(self.spinBox_3.value())
        # print(results)
        top_ten = results.split("\n")[:self.spinBox_3.value()]
        for i in top_ten:
            x, y, z = i.partition(" rate: ")
            print(x)
            subprocess.call(["open", x])

        print("opening yolo results")


    def open_youtube(self):
        results = self.scrollAreaWidgetContents_5.toPlainText()
        # length = len(results.split("\n"))
        # self.spinBox.setMaximum(length)
        # print(self.spinBox.value())
        # print(results)
        top_ten = results.split("\n")[:self.spinBox.value()]
        print(top_ten)
        for i in top_ten:
            x, y, z = i.partition(" rate: ")
            print(x)
            print("opening youtube results")
            webbrowser.open_new_tab(x)









    def clear_yolo_res(self):
        print("clearing results from yolo")
        # print(self.scrollAreaWidgetContents_4.toPlainText())
        self.scrollAreaWidgetContents_4.clear()


    def clear_ocr_res(self):
        self.scrollAreaWidgetContents_3.clear()



    def clear_yolo(self):
        self.YOLOlineEdit.clear()


    def clear_ocr(self):
        self.OCRlineEdit.clear()


    def get_domains(self):
        # sentence = 'Maxwell velocity distribution'
        sentence = self.OCRlineEdit.text()
        # token = nlp(sentence)[0]
        # And automatically tags with wordnet domains
        # domains = token._.wordnet.wordnet_domains()
        possible_domains = []
        for word in word_tokenize(sentence.replace(",", " ")):
            # print(word)
            token = nlp(word)[0]
            # print(token._.wordnet.wordnet_domains())
            possible_domains += token._.wordnet.wordnet_domains()

        possible_domains = list(dict.fromkeys(possible_domains))
        # print(possible_domains)
        # print("domains", possible_domains )
        self.scrollAreaWidgetContents_2.setText(", ".join(map(str, possible_domains )))


    def ocr_mdt(self):
        input_search = self.OCRlineEdit.text()
        print(input_search)
        # input_search = "Maxwell velocity distribution, maxwell, velocity, speed,  Maxwellian speed, W boson"
        # economy_domains = ['mathematics', 'physics', "computing"]  mathematics, physics, computing
        economy_domains = word_tokenize(self.scrollAreaWidgetContents.toPlainText().replace(",", " "))
        print(economy_domains)



        #list of keywords and phrases
        keywords = []
        phrases = []
        extended_phrases = []
        extended_keywords = []
        for i in input_search.split(","):
            pills = word_tokenize(i)
            token = " ".join(map(str, pills))
            if len(pills) > 1:
                phrases.append(token)
            else:
                keywords.append(token)

        for phrase in phrases:
            simmilar_results = dot(phrase, economy_domains)
            extended_phrases.append(simmilar_results)

        for keyword in keywords:
            simmilar_results = dot(keyword, economy_domains)
            extended_keywords.append(simmilar_results)

        extended_phrases  = [i for sub in extended_phrases  for i in sub]
        extended_keywords = [i for sub in extended_keywords for i in sub]
        extended_keywords = list(dict.fromkeys(extended_keywords))
        extended_phrases = list(dict.fromkeys(extended_phrases))

        print("phrases", phrases)
        print("keywords", keywords)

        #remove phrases and keywords form extended_phrases and extended_keywords if i want to make faster
        print("extended_phrases", extended_phrases)
        print("extended_keywords", extended_keywords)

        #creating the Corpus




        #creaing OCR the corpus
        OCR_Corpuc = []
        print(len(self.OCR_Dirs))
        for i in self.OCR_Dirs:
            print("reading:", f"{i}/OCR.txt")
            with open(f"{i}/OCR.txt", "r") as file:
                data = file.readlines()
            
            for j in data:
                x = j.split(" <break> ")
                OCR_Corpuc.append((x[0], x[1].replace("\n", "")))

            file.close()

        # print("\n"+str(len(OCR_Corpuc))+"\n")
        # searchable_OCR_sentences
        def removeDuplicates(lst):
            return [[a, b] for i, [a, b] in enumerate(lst)
            if not any(c == b for _, c in lst[:i])]
            
        OCR_Corpuc = removeDuplicates(OCR_Corpuc)
        # print(f"\nUpdated: \n{OCR_Corpuc}")
        # print("\n"+str(len(OCR_Corpuc))+"\n")
        # print(OCR_Corpuc)


        #finding the results in OCR
        OCR_results = []
        for i in OCR_Corpuc:
            paragrpah = i[1].lower()

            for phrase in phrases:
                if phrase.lower() in paragrpah:
                    OCR_results.append(i[0])
                    pass

            #implamented after update
            for phrase in phrases:
                if difflib_sim(phrase, paragrpah):
                    OCR_results.append(i[0])
                    print("there was a result", phrase, paragrpah)
                    pass


            for keyword in keywords:
                if keyword.lower() in paragrpah:
                    OCR_results.append(i[0])
                    pass

            for extended_phrase in extended_phrases:
                if extended_phrase.lower() in paragrpah:
                    OCR_results.append(i[0])
                    pass

            for extended_keyword in extended_keywords:
                if extended_keyword.lower() in paragrpah:
                    OCR_results.append(i[0])
                    pass

        OCR_removed = list(dict.fromkeys(OCR_results))
        OCR_sorted_results = []
        for i in OCR_removed:
            x = OCR_results.count(i)
            # print(i, x)
            OCR_sorted_results.append((i, x))


        print("OCR Results")
        x = sorted(OCR_sorted_results, key=lambda x: x[1], reverse=True)
        y = ""
        for i in x:
            y += f"{i[0]} rate: {i[1]}\n"
            print(i)

        self.scrollAreaWidgetContents_3.setText(y)
        self.spinBox_2.setValue(len(x))
        self.spinBox_2.setMaximum(len(x))









    def yolo_mdt(self):
        # input_search = "Book, baseball bat" #books doesnot work
        input_search = self.YOLOlineEdit.text()


        #creaing YOLO the corpus
        YOLO_Corpuc = []
        # print(len(YOLO_Dirs))
        for i in self.YOLO_Dirs:
            # print("reading:", f"{{i}/YOLO.txt")
            with open(f"{i}/YOLO.txt", "r") as file:
                data = file.readlines()
            
            for j in data:
                x = j.split(" <break> ")
                YOLO_Corpuc.append((x[0], x[1].replace("\n", "")))

            file.close()

        # print("\n"+str(len(YOLO_Corpuc))+"\n")
        # searchable_OCR_sentences
        def removeDuplicates(lst):
            return [[a, b] for i, [a, b] in enumerate(lst)
            if not any(c == b for _, c in lst[:i])]
            
        YOLO_Corpuc = removeDuplicates(YOLO_Corpuc)
        # print(YOLO_Corpuc)


        #list of keywords and phrases
        keywords = []
        phrases = []
        # extended_phrases = []
        # extended_keywords = []

        for i in input_search.split(","):
            pills = word_tokenize(i)
            token = " ".join(map(str, pills))
            if len(pills) > 1:
                phrases.append(token)
            else:
                keywords.append(token)


        #finding the results in YOLO
        YOLO_results = []
        for i in YOLO_Corpuc:
            paragrpah = i[1].lower()

            for phrase in phrases:
                if phrase.lower() in paragrpah:
                    YOLO_results.append(i[0])
                    pass

            for keyword in keywords:
                if keyword.lower() in paragrpah:
                    YOLO_results.append(i[0])
                    pass

        print("\n\n")


        YOLO_removed = list(dict.fromkeys(YOLO_results))
        YOLO_sorted_results = []
        for i in YOLO_removed:
            x = YOLO_results.count(i)
            # print(i, x)
            YOLO_sorted_results.append((i, x))


        print("YOLO Results")
        x = sorted(YOLO_sorted_results, key=lambda x: x[1], reverse=True)
        y = ""
        for i in x:
            y += f"{i[0]} rate: {i[1]}\n"
            print(i)

        self.scrollAreaWidgetContents_4.setText(y)
        self.spinBox_3.setValue(len(x))
        self.spinBox_3.setMaximum(len(x))


    


# Maxwell velocity distribution, maxwell, velocity, speed,  Maxwellian speed, W boson


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
