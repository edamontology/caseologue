import unittest
from rdflib import ConjunctiveGraph, Namespace
import json
import os

class edamQueryTest(unittest.TestCase):
      
    def parse_edam(self, edam_file):
        g = ConjunctiveGraph()
        g.parse(os.environ.get('EDAM_PATH', edam_file), format='xml')
        return (g)


    def test_deprecated_replacement_obsolete(self):
        
        g = self.parse_edam(edam_file="/home/llamothe/work/edamontology/EDAM_dev.owl")

        query_term = """
        PREFIX obo: <http://purl.obolibrary.org/obo/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>
        PREFIX edam:<http://edamontology.org/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        SELECT DISTINCT ?entity ?label ?property ?replacement WHERE {
            VALUES ?property { oboInOwl:replacedBy
                            oboInOwl:consider      }
            ?entity  ?property ?replacement .
            ?entity rdfs:label ?label .
            ?replacement owl:deprecated true .
            
        }
        ORDER BY ?entity
        """

        results = g.query(query_term)
        nb_err = len(results)

        for r in results:
            print(f"{r['entity']},'{r['label']}', is replaced by ({r['property']}) an obsolete concept: {r['replacement']}'")

        self.assertEqual(nb_err, 0)

    def test_super_class_refers_to_self(self):
        
        g = self.parse_edam(edam_file="/home/llamothe/work/edamontology/EDAM_dev.owl")

        query_term = """
        PREFIX obo: <http://purl.obolibrary.org/obo/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>
        PREFIX edam:<http://edamontology.org/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        SELECT DISTINCT ?entity ?property ?value WHERE {
                 VALUES ?property { rdfs:subClassOf }
                 ?entity ?property ?value
                 FILTER (?entity = ?value)

        }
        ORDER BY ?entity
        """

        results = g.query(query_term)
        nb_err = len(results)

        for r in results:
            print(f"{r['entity']} , super declared as superclass of itself ")
        self.assertEqual(nb_err, 0)

if __name__ == '__main__':
    unittest.main()