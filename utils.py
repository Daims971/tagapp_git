
# Importation générale

import joblib

import os
import sys
print(os.getcwd(), file=sys.stdout)


# Import des modèles entrainés


estimator = joblib.load(os.getcwd() + '\\tagapp\\tfidf_input_pipe_pac_cv.pkl')

