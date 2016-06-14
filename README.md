# Question Pre-Processing:

In the first step of the QA system architecture, NSIF of the question is built by applying Stanford CoreNLP Parser. The NSIF contains parsing information and dependency parsing results for corresponding question. It consists of word segmentation (tokenization), morphological analysis, lemmatization, POS tagging, and named entity recognition (NER) for every question separately. 


Each components are released in their own branch. Check each componets's README for more information.
# Component samples:
[mlatifi/OntoQAS/](https://github.com/mlatifi/OntoQAS/blob/master/representingSentences.py) - Question Preprocessing
[mlatifi/OntoQAS/](https://github.com/mlatifi/OntoQAS/blob/master/questionProcessing.py) - Question Classifier
