import unittest
from rdflib import ConjunctiveGraph, Namespace
import json
import os
import pandas as pd
import argparse
import sys


def parsing () :

    parser = argparse.ArgumentParser(description="Level of tests, by default all levels are ran")
    parser.add_argument('-e','--error', action='store_true',  help='runs all error tests')
    parser.add_argument('-E','--essential' , action='store_true', help='runs all essential tests')
    parser.add_argument('-c','--curation',  action='store_true', help='runs all curation tests')
    parser.add_argument('unittest_args', nargs='*')

    args = parser.parse_args()

    print("args argparse",args.error,args.essential,args.curation)

    if (args.error!=False or args.essential!=False or args.curation!=False) :
        run_error = args.error
        run_essential = args.essential
        run_curation = args.curation
        

    else: 
        run_error = True
        run_essential = True
        run_curation = True

    print("def parsing",run_error,run_essential,run_curation)

    sys.argv[1:] = args.unittest_args 


    return(run_error,run_essential,run_curation)

def suite ():
    suite = unittest.TestSuite()
    if run_error == True :
        suite.addTest(EdamQueryTest('test_deprecated_replacement_obsolete'))
    if run_essential == True :
        suite.addTest(EdamQueryTest('test_super_class_refers_to_self'))
    if run_essential == True :
        suite.addTest(EdamQueryTest('test_bad_uri'))
    if run_error == True :
        suite.addTest(EdamQueryTest('test_mandatory_property_missing'))
    return suite



# each test is added in function of the boolean input (error essential curation), to change level category, change tested variable (+ change level error when adding new_error in data frame)


class EdamQueryTest(unittest.TestCase):

    @classmethod  
    def setUpClass(cls):  
        cls.edam_graph = ConjunctiveGraph()
        cls.edam_graph.parse(os.environ.get('EDAM_PATH'), format='xml')
        cls.report = pd.DataFrame(columns = ['Level','Test Name','Entity','Label','Debug Message'])
        #print(cls.report)
    

    def test_deprecated_replacement_obsolete(self):
        
        query = "queries/deprecated_replacement_obsolete.rq"
        with open(query,'r') as f:
            query_term = f.read()
        results = self.edam_graph.query(query_term)
        nb_err = len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame([['ERROR','deprecated_replacement_obsolete',r['entity'],r['label'],(f"concept is replaced by ({r['property']}) an obsolete concept: {r['replacement']}")]], columns=['Level','Test Name','Entity','Label','Debug Message'])
            self.__class__.report = pd.concat([self.report, new_error],  ignore_index=True) 

        
        self.assertEqual(nb_err, 0)

    def test_super_class_refers_to_self(self):
            
            query = "queries/super_class_refers_to_self.rq"
            with open(query,'r') as f:
                query_term = f.read()

            results = self.edam_graph.query(query_term)
            nb_err = len(results)

            for r in results:
                new_error = pd.DataFrame([['ESSENTIAL','super_class_refers_to_self',r['entity'],r['label'],'concept declared as superclass of itself']], columns=['Level','Test Name','Entity','Label','Debug Message'])
                self.__class__.report = pd.concat([self.report, new_error],  ignore_index=True) 
            

            self.assertEqual(nb_err, 0)

    def test_bad_uri(self):
            
            query = "queries/bad_uri.rq"
            with open(query,'r') as f:
                query_term = f.read()

            results = self.edam_graph.query(query_term)
            nb_err = len(results)

            for r in results:
                new_error = pd.DataFrame([['ESSENTIAL','bad_rui',r['entity'],r['label'],'has a bad URI (entity) (regex :^http://edamontology.org/(data|topic|operation|format)_[0-9]\{4\}$)']], columns=['Level','Test Name','Entity','Label','Debug Message'])
                self.__class__.report = pd.concat([self.report, new_error],  ignore_index=True) 
            

            self.assertEqual(nb_err, 0)
    
    def test_mandatory_property_missing(self):
            
            query = "queries/mandatory_property_missing.rq"
            with open(query,'r') as f:
                query_term = f.read()

            results = self.edam_graph.query(query_term)
            nb_err = len(results)

            for r in results:
                #here put a filter for root concept missing subClassOf? 
                new_error = pd.DataFrame([['ERROR','mandatory_property_missing',r['entity'],r['label'],(f"is missing mandatory property: {r['property']} ")]], columns=['Level','Test Name','Entity','Label','Debug Message'])
                self.__class__.report = pd.concat([self.report, new_error],  ignore_index=True) 
            

            self.assertEqual(nb_err, 0)

    def test_XXXTEST_NAMEXXX(self):
            
            query = "queries/XXXQUERY_FILEXXX"
            with open(query,'r') as f:
                query_term = f.read()

            results = self.edam_graph.query(query_term)
            nb_err = len(results)

            for r in results:
                new_error = pd.DataFrame([['XXXLEVELXXX','XXXTEST_NAMEXXX',r['entity'],r['label'],'XXXDEBUG_MESSAGEXXX']], columns=['Level','Test Name','Entity','Label','Debug Message'])
                self.__class__.report = pd.concat([self.report, new_error],  ignore_index=True) 
            

            self.assertEqual(nb_err, 0)
    
    @classmethod
    def tearDownClass(cls):
        print(cls.report)
        cls.report.to_csv("./output_edamci.tsv", sep='\t')
        return super().tearDownClass()

if __name__ == '__main__':

    run_error,run_essential,run_curation = parsing()
    print('main',run_error,run_essential,run_curation)

    runner = unittest.TextTestRunner()
    runner.run(suite())
