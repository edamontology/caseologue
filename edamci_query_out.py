import unittest
from rdflib import ConjunctiveGraph, Namespace
import json
import os

class edamQueryTest(unittest.TestCase):
      
    def parse_edam(self, edam_file):
        g = ConjunctiveGraph()
        g.parse(os.environ.get('EDAM_PATH', edam_file), format='xml')
        return (g)
    
    # def test_initialize_output(self):
    #     with open("edamci.out", 'w') as f:
    #         f.write("Level\tTest Name\tEntity\tLabel\tDebug Message\n")
    #     f.close()
    #     print("workiiing")


    def test_deprecated_replacement_obsolete(self):
        
        g = self.parse_edam(edam_file="/home/llamothe/work/edamontology/EDAM_dev.owl")
        
        query = "/home/llamothe/work/ci_query/deprecated_replacement_obsolete.rq"
        with open(query,'r') as f:
            query_term = f.read()
        results = g.query(query_term)
        nb_err = len(results)
        f.close()

        with open("edamci.out", 'a') as f:

            for r in results:
                f.write(f"ERROR\tdeprecated_replacement_obsolete\t{r['entity']}\t'{r['label']}'\tconcept is replaced by ({r['property']}) an obsolete concept: {r['replacement']}'\n")
        f.close()
        
        self.assertEqual(nb_err, 0)

    def test_super_class_refers_to_self(self):
        
        g = self.parse_edam(edam_file="/home/llamothe/work/edamontology/EDAM_dev.owl")

        query = "/home/llamothe/work/ci_query/super_class_refers_to_self.rq"
        with open(query,'r') as f:
            query_term = f.read()

        results = g.query(query_term)
        nb_err = len(results)

        for r in results:
            print(f"{r['entity']} , super declared as superclass of itself ")
        self.assertEqual(nb_err, 0)

if __name__ == '__main__':
    with open("edamci.out", 'w') as f:
        f.write("Level\tTest Name\tEntity\tLabel\tDebug Message\n")
    f.close()
    unittest.main()