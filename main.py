#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 21:16:15 2018

@author: mythrebi
"""
'''libraries'''
from tika import parser
from sklearn import preprocessing 
import pandas as pa
import nltk
from nltk.corpus import stopwords#
from sklearn.ensemble import RandomForestClassifier#
from sklearn.feature_extraction.text import CountVectorizer#
from bs4 import BeautifulSoup#
import numpy as np#
import re#
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, XMLConverter, HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


'''
Convert pdf to text
'''

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text
    
def clean(rawData):
    if len(rawData)>13:
        rawData=rawData[0:13]
    rawData=re.sub("[^a-zA-Z]", "",rawData)# 

    letterList=[]
    asciiList=[]
    letterList=list(rawData)
    for i in xrange(0,len(letterList)):
        asciiList.append(str(ord(letterList[i])))
    return long("".join(asciiList))


'''Change the path to the path of the pdf file in your system'''
pdfDir = "/Users/mythrebi/Desktop/PDFParsing/resumes/1531012.pdf"
text = convert(pdfDir)

    
'''load the manually curated training data which consists of compilation of data of different names, qualifications 
   and other names'''
trainData=pa.read_csv("/Users/mythrebi/Desktop/PDFParsing/qualifications.csv",delimiter=",",header=0)



'''Preprocessing the test data to remove bad chars'''
stop=stopwords.words("english")
for i in xrange(0,len(stop)):
    stop[i]=stop[i].upper()
noStopWords=None
words=None
letters_only=None
text=text.replace("\n",'')
noTags=BeautifulSoup(text).get_text()#
data=noTags.replace("\r"," ")
letters_only=re.sub("[^.a-zA-Z]", " ",data)# 
letters_only=re.sub("[.]","",letters_only)
words=letters_only.upper().split()
noStopWords=[w for w in words if not w in stop]
noStopWords=[w[0:13] for w in noStopWords if len(w)<13]


'''Clean and ENCODE the data to fit the model'''
cleanTrain=[]
for i in xrange(0,len(trainData["qualification"])):
    cleanTrain.append(clean(trainData["qualification"][i]))
    
atrain=np.asarray(cleanTrain)
atrain=atrain

cleanT=[]
for i in xrange(0,len(noStopWords)):
    cleanT.append(clean(noStopWords[i]))
atest=np.asarray(cleanT)

   
'''Train and predict using random forest classifier'''
forest = RandomForestClassifier(n_estimators = 2)
result=forest.fit(atrain.reshape(-1,1),trainData["result"])
result=forest.predict(atest.reshape(-1,1))

noDF=pa.DataFrame(data={"words":noStopWords,"qualification":result})

'''Display Results'''
name=[]
qual=[]
other=[]
for i in xrange(0,len(noDF)):
    if noDF["qualification"][i]==1:
        qual.append(noDF["words"][i])
    elif noDF["qualification"][i]==2:
        name.append(noDF["words"][i])
        
print "Qualifications:", set(qual), "\n"
print "Names:",set(name),"\n"