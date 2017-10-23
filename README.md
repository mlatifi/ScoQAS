# Semantic-based closed and open domain Question Answering System (ScoQAS) Architecture [Beta]:

In the ScoQAS architecure, there are common and specific components, modules, and KBs.
This is the repository of the Ontology Based Question Answering System which process the NL questions. The ScoQA system is based on NLP techniques combining semantic-based structure-feature patterns (Ss-fP) for question classification and creating a question syntactic-semantic information structure (QSiS). The ScoQA system performs over ontologies not over free text and operates on two scenarios, one Closed-domain, where the domain is restricted by an ontology, which using a human-made ontology and the other is Open domain where the answers are retrieved from a LOD knowledge base.

There are common and specific components, modules, and KBs. 
Some of these components are  such as  Question Preprocessing, Question Representation, Question Classifier, Building Constraints, Graph Construction, SPARQL Query Construction and Answer Extraction.

You can use these samples as a reference or as a starting point for creating your own apps. The focus here is on code structure, architecture, testing and maintainability. However, bear in mind that there are many ways to build apps with these architectures and tools, depending on your priorities, so these shouldn't be considered canonical examples.

Each components are released in their own branch. Check each componets's README for more information.
# Component samples:
- [NSIF](https://github.com/mlatifi/OntoQAS/tree/NSIF) - Building NSIF

- [Q-Preprocessing](https://github.com/mlatifi/OntoQAS/tree/Q-Preprocessing) - Question Preprocessing

- [QC](https://github.com/mlatifi/OntoQAS/tree/QC) - Question Classifier

- [Constraints](https://github.com/mlatifi/OntoQAS/tree/Constraints) - Building Constraints

- [Graph-Construction](https://github.com/mlatifi/OntoQAS/blob/Graph-Construction) - Graph Construction

This project is built by **Majid Latifi** .
I developed ScoQAS for modeling and gathering data when following a certain theory/methodology in Articial Intelligence. Plesae cite these papers when you are using this code:

1- Latifi, M., Rodríguez, H., & Sànchez-Marrè, M. (2017). [ScoQAS: A Semantic-based Closed and Open Domain Question Answering System](http://journal.sepln.org/sepln/ojs/ojs/index.php/pln/article/view/5495). Procesamiento del Lenguaje Natural, 59, 73-80.

2- Latifi, M., & Sànchez-Marrè, M. (2013, October). [The Use of NLP Interchange Format for Question Answering in Organizations](http://ebooks.iospress.nl/publication/35253). In CCIA (pp. 235-244).

# License:

- See [LICENSE](https://github.com/mlatifi/OntoQAS/tree/LICENSE)
