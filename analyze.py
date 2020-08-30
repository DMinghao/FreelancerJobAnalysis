import pandas as pd
import numpy as np
import nltk
nltk.download('punkt')
import os
import nltk.corpus
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize

# read result 
result = pd.read_csv("result.csv") 

Tags = result["Tag"]
print(Tags)

allTag = ""
for row in result.index: 
    allTag = allTag + " " + result['Tag'][row]

token = word_tokenize(allTag)

# find most popular 20tag 
fdist = FreqDist(token)

fdist20 = fdist.most_common(20)

print(fdist20)