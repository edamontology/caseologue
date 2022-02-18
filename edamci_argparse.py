import unittest
from rdflib import ConjunctiveGraph, Namespace
import json
import os
import pandas as pd
import argparse
import sys



run_error = False
run_essential = False
run_curation = False
print('corps',run_error,run_essential,run_curation)


def parsing () :

    parser = argparse.ArgumentParser(description="Level of tests")
    parser.add_argument('-e','--error', action='store_true',  help='True/False, if true, runs all error tests')
    parser.add_argument('-E','--essential' , action='store_true', help='True/False, if true, runs all essential tests')
    parser.add_argument('-c','--curation',  action='store_true', help='True/False, if true, runs all curation tests')
    parser.add_argument('unittest_args', nargs='*')

    args = parser.parse_args()

    print("args argparse",args.error,args.essential,args.curation)

    # global run_error
    # global run_essential
    # global run_curation

    run_error = args.error
    run_essential = args.essential
    run_curation = args.curation
    print("def parsing",run_error,run_essential,run_curation)

    sys.argv[1:] = args.unittest_args 


    # run_all == aucune 3 variabem (not xx and ...) 
    #     esle if  not args_error && not run_all = run_error = False

    return(run_error,run_essential,run_curation)

class EdamQueryTest(unittest.TestCase):

    @classmethod  
    def setUpClass(cls): 
        print("run setupclass") 
        cls.edam_graph = ConjunctiveGraph()
        cls.edam_graph.parse(os.environ.get('EDAM_PATH'), format='xml')
        cls.report = pd.DataFrame(columns = ['Level','Test Name','Entity','Label','Debug Message'])
        #print(cls.report)
    

    @unittest.skipUnless(run_error == True, reason="requires parse argument")
    def test_deprecated_replacement_obsolete(self):
        
        print("run test 1")
        query = "queries/deprecated_replacement_obsolete.rq"
        with open(query,'r') as f:
            query_term = f.read()
        results = self.edam_graph.query(query_term)
        nb_err = len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame([['ERROR','deprecated_replacement_obsolete',r['entity'],r['label'],(f"concept is replaced by ({r['property']}) an obsolete concept: {r['replacement']}")]], columns=['Level','Test Name','Entity','Label','Debug Message'])
            self.__class__.report = pd.concat([self.report, new_error],  ignore_index=True) 
            #self.report = self.report.append({'Level':'ERROR','Test Name':'deprecated_replacement_obsolete','Entity':r['entity'],'Label':r['label'],'Debug Message':(f"concept is replaced by ({r['property']}) an obsolete concept: {r['replacement']}")}, ignore_index=True)
        
        #print(self.__class__.report)
        
        self.assertEqual(nb_err, 0)


    @unittest.skipUnless(run_essential == True, reason="requires parse argument" ,)
    def test_super_class_refers_to_self(self):
        
        print("run test 2")
        query = "queries/super_class_refers_to_self.rq"
        with open(query,'r') as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err = len(results)

        for r in results:
            new_error = pd.DataFrame([['ERROR','super_class_refers_to_self',r['entity'],r['label'],'concept declared as superclass of itself']], columns=['Level','Test Name','Entity','Label','Debug Message'])
            self.__class__.report = pd.concat([self.report, new_error],  ignore_index=True) 
        
        #print(self.__class__.report)

        self.assertEqual(nb_err, 0)
    
    @classmethod
    def tearDownClass(cls):
        print("run teardownclass")
        print(cls.report)
        cls.report.to_csv("./output_edamci.tsv", sep='\t')
        return super().tearDownClass()

if __name__ == '__main__':
    print("run main 1")
    run_error,run_essential,run_curation = parsing()
    print("run main2")
    print('main',run_error,run_essential,run_curation)

    unittest.main()

    print("done")
    

