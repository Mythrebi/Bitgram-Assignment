# Bitgram-Assignment
Created a machine learning system that learns from PDF of resumes and identifies the name and qualifications from the resume.

# To Run 
To run the file, open main.py edit the path of your resume in 
pdfDir = "/Users/mythrebi/Desktop/PDFParsing/resumes/1531012.pdf".
(line 69) 

Load the path of qualifications.csv in trainData=pa.read_csv("/Users/mythrebi/Desktop/PDFParsing/qualifications.csv",delimiter=",",header=0).
(line 75)

# Notes
The model is trained with list of names, qualifications and other words. The system uses a dataset which I created on my own by compiling lots of sources of data from web and writing some manually.

The System can predict Qualifications and Names with approximately about 85% and 67% for train data.

The System can perform much more better if it is fed with more data. 

