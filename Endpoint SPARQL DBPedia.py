__author__ = 'majid'

from SPARQLWrapper import SPARQLWrapper, SPARQLExceptions, JSON
import string
import re
import rdflib
from rdflib import Literal,XSD,plugin,BNode, URIRef


def EU_Countries():
    cnt={}
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)

    sparql.setQuery("""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX yago: <http://dbpedia.org/class/yago/>
    PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>

    SELECT ?place WHERE {
        ?place rdf:type yago:EuropeanCountries .
        ?place rdf:type dbpedia-owl:Country
    }
    """)

    results = sparql.query().convert()
    print "European Countries are:","\n",results
    i=0
    for row in results:
        if i==0:
            print "European Countries are:","\n",

        cnt[i]=str(row)
        cnt[i]=cnt[i].split()
        cnt[i][0]=cnt[i][0].rsplit('/resource/')[-1]
        # classTemp[itk,intji][1]=classTemp[itk,intji][1].rsplit('/rdf')[-1]


def  artcilefromdbpedia():
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)

    sparql.setQuery("""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX yago: <http://dbpedia.org/class/yago/>
    PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>

    SELECT ?place WHERE {
            ?place rdf:type yago:EuropeanCountries .
            ?place rdf:type dbpedia-owl:Country
    }
    """)
    results = sparql.query().convert()
    print "Result for article", results


def Property_Domain_Range():
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)
    sparql.setQuery("""
    PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
    SELECT distinct ?property ?domain ?range
    where {?property ?p rdf:Property.
                ?property <http://www.w3.org/2000/01/rdf-schema#domain> ?domain.
                ?property <http://www.w3.org/2000/01/rdf-schema#range> ?range

    }
    limit 10
    """)
    results = sparql.query().convert()
    print "Result for Property_Domain_Range over DBpedia", results

EU_Countries()
Property_Domain_Range()
artcilefromdbpedia()
