
# Importation générale

import pandas as pd
# pd.set_option('display.max_columns', None)
import numpy as np
import joblib

# Importation des librairies pour la prédiction

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PowerTransformer

from sklearn.pipeline import Pipeline
from sklearn import linear_model
from sklearn.metrics import jaccard_score, make_scorer

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


import re 

import os
import sys
print(os.getcwd(), file=sys.stdout)


# -------------- Define scoring functions
def jaccard_func(y_true, y_pred):
    result_score = jaccard_score(y_true, y_pred, average='samples',zero_division=0)
    return result_score

# -------------- Score and error functions
score_jaccard_func = make_scorer(jaccard_func, greater_is_better=True)
scoring_model = {'score_jaccard_func':score_jaccard_func, 'accuracy':'accuracy'}

# Import des modèles entrainés


estimator = joblib.load(os.getcwd() + '\\tagapp\\tfidf_input_pipe_pac_cv.pkl')



# ---------------------- Fonction de Nettoyage -------------------

# Tokenizer
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

def tokenizer_fct(sentence) :
    # remove or replace by empty or space char a specific symbol
    sentence_clean = sentence.replace('-', ' ').replace('/', ' ').replace('_', ' ').replace('<', ' ') \
    .replace('>', ' ').replace(':', ' ').replace('=', ' ').replace('.', ' ').replace("'", ' ').replace("\\", ' ')
    # Ajout de _, <, >, ', :, =, .
    word_tokens = word_tokenize(sentence_clean)
    return word_tokens

def digit_clean(list_words):
    # remove or replace by '' a char word from list_words only composed by digits
    filtered_w = [re.sub("^[0-9]+[0-9]$", "", w) for w in list_words] 
    return filtered_w
    
def body_html_tag_out(sentence):
    # remove or replace by empty or space char only < or >
    filtered_sentence = re.sub("<.+?>", " ", sentence)
    return filtered_sentence
    
def non_latin_char_clean(list_words):
    # replace all non latin char by empty char
    filtered_w = [re.sub("([^\x00-\x7F])+", "", w) for w in list_words]
    return filtered_w

    
# Stop words
from nltk.corpus import stopwords
stop_w = list(set(stopwords.words('english'))) + ['[', ']', ',', '.', ':', '?', '(', ')','','=',"'"]

def stop_word_filter_fct(list_words) :
    filtered_w = [w for w in list_words if not w in stop_w]
    filtered_w2 = [w for w in filtered_w if len(w) > 2]
    return filtered_w2

# lower case et alpha
def lower_start_fct(list_words) :
    lw = [w.lower() for w in list_words if (not w.startswith("@")) 
    #                                   and (not w.startswith("#"))
                                       and (not w.startswith("http"))]
    return lw



# Fonction de préparation du texte pour le bag of words (Countvectorizer et Tf_idf, Word2Vec)
def transform_bow_fct(desc_text) :
    word_tokens = tokenizer_fct(desc_text)
    word_tokens_bis = non_latin_char_clean(word_tokens)
    lw = lower_start_fct(word_tokens_bis)
    sw = stop_word_filter_fct(lw)
    sw_bis = digit_clean(sw)
#     lw = lower_start_fct(sw_bis)
    # lem_w = lemma_fct(lw)    
    transf_desc_text = ' '.join(sw_bis)
    return transf_desc_text



# Tokenizer
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

def tokenizer_tags(sentence) :
    # print(sentence)
    sentence_clean = sentence.replace('<', ' ').replace('>', ' ').replace('-', ' ').replace(':', ' ')
    word_tokens = word_tokenize(sentence_clean.lower())
    word_tokens_bis = non_latin_char_clean(word_tokens)
    lw = lower_start_fct(word_tokens_bis)
    sw = stop_word_filter_fct(lw)
    sw_bis = digit_clean(sw)
#     lw = lower_start_fct(sw_bis)
    transf_desc_text = ' '.join(sw_bis)
    transf_desc_text_2 = transform_bow_fct(transf_desc_text)
    lw_bis = tokenizer_fct(transf_desc_text_2)
    word_tokens_sorted = sorted(set(lw_bis))
    return word_tokens_sorted


# ---------------------------- Nettoyage Question & predictions

def pred_tags(user_question):
    user_question_cleaned = transform_bow_fct(user_question)
    
    y_pred = estimator.best_estimator_.fit_transform([user_question_cleaned])
    
    
    return y_pred

