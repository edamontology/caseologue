import inspect
import unittest
from rdflib import OWL, ConjunctiveGraph, Namespace
import os
import pandas as pd
import argparse
import sys
from collections import Counter
from rdflib.namespace import RDF, RDFS, _OWL
from tabulate import tabulate
from rich_dataframe import prettify
from queries.edamxpath_id_unique import check_unique_id

def parsing () :

    parser = argparse.ArgumentParser(description="Level of tests, by default all levels are ran")
    parser.add_argument('-e','--error', action='store_true',  help='runs all error tests')
    parser.add_argument('-E','--essential' , action='store_true', help='runs all essential tests')
    parser.add_argument('-c','--curation',  action='store_true', help='runs all curation tests')
    parser.add_argument('unittest_args', nargs='*')

    args = parser.parse_args()

    #print("args argparse",args.error,args.essential,args.curation)

    if (args.error!=False or args.essential!=False or args.curation!=False) :
        run_error = args.error
        run_essential = args.essential
        run_curation = args.curation
        

    else: 
        run_error = True
        run_essential = True
        run_curation = True

    #print("def parsing",run_error,run_essential,run_curation)

    sys.argv[1:] = args.unittest_args 


    return(run_error,run_essential,run_curation)

def suite ():
    suite = unittest.TestSuite()
    if run_curation == True :
        suite.addTest(EdamQueryTest('test_deprecated_replacement_obsolete'))
    if run_essential == True :
        suite.addTest(EdamQueryTest('test_super_class_refers_to_self'))
    if run_essential == True :
        suite.addTest(EdamQueryTest('test_bad_uri'))
    if run_error == True :
        suite.addTest(EdamQueryTest('test_mandatory_property_missing'))
    if run_curation == True :
        suite.addTest(EdamQueryTest('test_formating'))
    if run_error == True :
        suite.addTest(EdamQueryTest('test_deprecated_replacement'))
    if run_essential == True :
        suite.addTest(EdamQueryTest('test_concept_id_inferior_to_next_id'))
    if run_essential == True :
        suite.addTest(EdamQueryTest('test_bad_uri_reference'))
    if run_error == True :
        suite.addTest(EdamQueryTest('test_missing_deprecated_property'))
    if run_curation == True :
        suite.addTest(EdamQueryTest('test_check_wikipedia_link'))
    if run_curation == True :
        suite.addTest(EdamQueryTest('test_identifier_property_missing'))
    if run_error == True :
        suite.addTest(EdamQueryTest('test_id_unique'))
    return suite



# each test is added in function of the boolean input (error essential curation), to change level category, change tested variable (+ change level error when adding new_error in data frame)


class EdamQueryTest(unittest.TestCase):

    @classmethod  
    def setUpClass(cls):  
        cls.edam_graph = ConjunctiveGraph()
        cls.edam_graph.parse(os.environ.get('EDAM_PATH'), format='xml')
        cls.report = pd.DataFrame(columns = ['Level','Test Name','Entity','Label','Debug Message'])
        #print(cls.report)
    
    ################# DEPRECATED REPLACEMENT OBSOLETE ###########################

    def test_deprecated_replacement_obsolete(self):

        """
        Checks that the suggested replacement (replacedBy/consider) for a deprecated term is not obsolete.
        """
        
        query = "queries/deprecated_replacement_obsolete.rq"
        with open(query,'r') as f:
            query_term = f.read()
        results = self.edam_graph.query(query_term)
        nb_err = len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame([['CURATION','deprecated_replacement_obsolete',r['entity'],(f"'{r['label']}'"),(f"concept is replaced by ({r['property']}) an obsolete concept: {r['replacement']}")]], columns=['Level','Test Name','Entity','Label','Debug Message'])
            self.__class__.report = pd.concat([self.report, new_error],  ignore_index=True) 

        
        self.assertEqual(nb_err, 0)

    ################# SUPERCLASS REFERS TO SELF ###########################

    def test_super_class_refers_to_self(self):

        """
        Checks if a given consept doesn't refers to itself as superclass.
        """
            
        query = "queries/super_class_refers_to_self.rq"
        with open(query,'r') as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err = len(results)
        f.close()        
        
        for r in results:
            new_error = pd.DataFrame([['ESSENTIAL','super_class_refers_to_self',r['entity'],(f"'{r['label']}'"),'concept declared as superclass of itself']], columns=['Level','Test Name','Entity','Label','Debug Message'])
            self.__class__.report = pd.concat([self.report, new_error],  ignore_index=True) 
        

        self.assertEqual(nb_err, 0)

    ################# BAD URI ###########################

    def test_bad_uri(self):

        """
        Checks that the concepts URI matches the regex ^http://edamontology.org/(data|topic|operation|format)_[0-9]{4}$.
        """

        query = "queries/bad_uri.rq"
        with open(query,'r') as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err = len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame([['ESSENTIAL','bad_rui',r['entity'],(f"'{r['label']}'"),'has a bad URI (entity) (regex :^http://edamontology.org/(data|topic|operation|format)_[0-9]\{4\}$)']], columns=['Level','Test Name','Entity','Label','Debug Message'])
            self.__class__.report = pd.concat([self.report, new_error],  ignore_index=True) 
        

        self.assertEqual(nb_err, 0)

    ################# MANDATORY PROPERTY MISSING ###########################

    def test_mandatory_property_missing(self):

        """
        Checks that no mandatory property for all concepts are missing (oboInOwl:hasDefinition, rdfs:subClassOf, created_in, oboInOwl:inSubset, rdfs:label).
)
        """
            
        query = "queries/mandatory_property_missing.rq"
        with open(query,'r') as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err = len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame([['ERROR','mandatory_property_missing',r['entity'],(f"'{r['label']}'"),(f"is missing mandatory property: {r['property']} ")]], columns=['Level','Test Name','Entity','Label','Debug Message'])
            self.__class__.report = pd.concat([self.report, new_error],  ignore_index=True) 
        

        self.assertEqual(nb_err, 0)

    ################# FORMATING ###########################

    def test_formating(self):

        """
        Checks that no property has a space neither at the start nor the end, no tab and no end of line. Checks that label have not dot at the end and that definition do have a dot at the end. 
        """
            
        query = "queries/end_dot_def_missing.rq"
        with open(query,'r') as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err = len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame([['CURATION','end_dot_def_missing',r['entity'],(f"'{r['label']}'"),'A dot is missing at the end of the definition.']], columns=['Level','Test Name','Entity','Label','Debug Message'])
            self.__class__.report = pd.concat([self.report, new_error],  ignore_index=True) 
        

        query = "queries/end_dot_label.rq"
        with open(query,'r') as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err += len(results)  # add to same counter for the test 
        f.close()

        for r in results:
            new_error = pd.DataFrame([['CURATION','end_dot_label',r['entity'],(f"'{r['label']}'"),'There is an unwanted dot at the end of the label.']], columns=['Level','Test Name','Entity','Label','Debug Message'])
            self.__class__.report = pd.concat([self.report, new_error],  ignore_index=True)
        
        
        query = "queries/end_space_annotation.rq"
        with open(query,'r') as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err += len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame([['CURATION','end_space_annotation',r['entity'],(f"'{r['label']}'"),(f"There is an unwanted space at the end of {r['property']} : {r['value']}.")]], columns=['Level','Test Name','Entity','Label','Debug Message'])
            self.__class__.report = pd.concat([self.report, new_error],  ignore_index=True)
        

        query = "queries/eol_in_annotation.rq"
        with open(query,'r') as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err += len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame([['CURATION','eol_in_annotation',r['entity'],(f"'{r['label']}'"),(f"There is an unwanted end-of-line in {r['property']} : {r['value']}.")]], columns=['Level','Test Name','Entity','Label','Debug Message'])
            self.__class__.report = pd.concat([self.report, new_error],  ignore_index=True)
        
        
        query = "queries/start_space_annotation.rq"
        with open(query,'r') as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err += len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame([['CURATION','start_space_annotation',r['entity'],(f"'{r['label']}'"),(f"There is an unwanted space at the start of {r['property']} : {r['value']}.")]], columns=['Level','Test Name','Entity','Label','Debug Message'])
            self.__class__.report = pd.concat([self.report, new_error],  ignore_index=True)
        

        query = "queries/tab_in_annotation.rq"
        with open(query,'r') as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err += len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame([['CURATION','tab_in_annotation',r['entity'],(f"'{r['label']}'"),(f"There is an unwanted tabulation in {r['property']} : {r['value']}.")]], columns=['Level','Test Name','Entity','Label','Debug Message'])
            self.__class__.report = pd.concat([self.report, new_error],  ignore_index=True)
        
        self.assertEqual(nb_err, 0)


    ################# DEPRECATED REPLACEMENT ###########################

    def test_deprecated_replacement(self):

        """"
        checks that every deprecated concept has a replacement suggested (replaced_by or consider).
        """
            
        query = "queries/deprecated_replacement.rq"
        with open(query,'r') as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err = len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame([['ERROR','deprecated_replacement',r['entity'],(f"'{r['label']}'"),'is deprecated and is missing either a replacedBy property or a consider property']], columns=['Level','Test Name','Entity','Label','Debug Message'])
            self.__class__.report = pd.concat([self.report, new_error],  ignore_index=True) 
        

        self.assertEqual(nb_err, 0)


    ################# CONCEPT ID INFERIOR TO NEXT ###########################

    def test_concept_id_inferior_to_next_id(self):

        """
        Checks that the numerical part of the concept URI is inferior to the "next id" variable (header).
        """
            
        query = "queries/concept_id_inferior_to_next_id.rq"
        with open(query,'r') as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err = len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame([['ESSENTIAL','concept_id_inferior_to_next_id',r['entity'],(f"'{r['label']}'"),(f"The concept URI (numerical id) is equal or superior to the next_id info--> update one or the other {r['property']}: '{r['value']}'")]], columns=['Level','Test Name','Entity','Label','Debug Message'])
            self.__class__.report = pd.concat([self.report, new_error],  ignore_index=True) 
        

        self.assertEqual(nb_err, 0)


    ################# BAD URI REFERENCE ###########################

    def test_bad_uri_reference(self):

        """
        Check that a reference (e.g. superclass) to another concept is actually declared in EDAM.

        "get_uri.rq" retrieves all URI. "uri_reference.rq" retrieves all referenced URI. Then check if the references URIs are in the declared concept URIs.
        """
            
        query = "queries/get_uri.rq"
        uri=[]
        with open(query,'r') as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term) 
        f.close()

        for r in results :
            uri.append(r['entity'])

        query = "queries/uri_reference.rq"
        with open(query,'r') as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term) 
        f.close()

        nb_err = 0
        for r in results:
            if r['reference'] not in uri : 
                nb_err += 1
                new_error = pd.DataFrame([['ESSENTIAL','bad_uri_reference',r['entity'],(f"'{r['label']}'"),(f"The property {r['property']} refers not an undeclared URI: '{r['reference']}'")]], columns=['Level','Test Name','Entity','Label','Debug Message'])
                self.__class__.report = pd.concat([self.report, new_error],  ignore_index=True) 
        
        
        self.assertEqual(nb_err, 0)


    ################# MISSING DEPRECATED PROPERTY ###########################

    def test_missing_deprecated_property(self):

        """
        Checks that no mandatory property for deprecated concept are missing (edam:obsolete_since, edam:oldParent, oboInOwl:inSubset <http://purl.obolibrary.org/obo/edam#obsolete>, rdfs:subClassOf <http://www.w3.org/2002/07/owl#DeprecatedClass>).
        """
            
        query = "queries/missing_deprecated_property.rq"
        with open(query,'r') as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err = len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame([['ERROR','missing_deprecated_property',r['entity'],(f"'{r['label']}'"),(f"is missing mandatory deprecated property: {r['property']}")]], columns=['Level','Test Name','Entity','Label','Debug Message'])
            self.__class__.report = pd.concat([self.report, new_error],  ignore_index=True) 
        

        self.assertEqual(nb_err, 0)


    ################# MISSING WIKIPEDIA LINK ###########################

    def test_check_wikipedia_link(self):

        """
        Checks that every topic has a wikipedia link filled in the seeAlso property.
        """
            
        query = "queries/check_wikipedia_link.rq"
        with open(query,'r') as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err = len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame([['CURATION','check_wikipedia_link',r['entity'],(f"'{r['label']}'"),"Topic concept missing a wikipedia link"]], columns=['Level','Test Name','Entity','Label','Debug Message'])
            self.__class__.report = pd.concat([self.report, new_error],  ignore_index=True) 
        

        self.assertEqual(nb_err, 0)


    ################# IDENTIFIER PROPERTY MISSING ###########################
    
    def test_identifier_property_missing(self):

        """
        Checks the no mandatory property for identifier (subclass of accession) are missing (regex).
        """
            
        query = "queries/identifier_property_missing.rq"
        with open(query,'r') as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err = len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame([['CURATION','identifier_property_missing',r['entity'],(f"'{r['label']}'"),"Missing regex property"]], columns=['Level','Test Name','Entity','Label','Debug Message'])
            self.__class__.report = pd.concat([self.report, new_error],  ignore_index=True) 
        

        self.assertEqual(nb_err, 0)

    ################# ID UNIQUE ###########################
    
    def test_id_unique(self):

        """
        Checks that no numeriacal part of the URI is duplicated.
        """
            
        duplicate_id = check_unique_id(os.environ.get('EDAM_PATH'))
        nb_err = len(duplicate_id)

        query = "queries/get_uri.rq"
        uri=[]
        with open(query,'r') as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        f.close()

        for id in duplicate_id:
            for r in results:
                if id in str(r['entity']):   
                    new_error = pd.DataFrame([['ERROR','id_unique',r['entity'],(f"'{r['label']}'"),(f"numerical id is used several times:{duplicate_id[0]}")]], columns=['Level','Test Name','Entity','Label','Debug Message'])
                    self.__class__.report = pd.concat([self.report, new_error],  ignore_index=True) 

        self.assertEqual(nb_err, 0)    

    ################# TEST NAME ###########################
    
    def test_XXXTEST_NAMEXXX(self):

        """
        Docstring documentation. 
        """
            
        query = "queries/XXXQUERY_FILEXXX"
        with open(query,'r') as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err = len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame([['XXXLEVELXXX','XXXTEST_NAMEXXX',r['entity'],(f"'{r['label']}'"),(f" XXXDEBUG_MESSAGEXXX {r['property']}: '{r['value']}'")]], columns=['Level','Test Name','Entity','Label','Debug Message'])
            self.__class__.report = pd.concat([self.report, new_error],  ignore_index=True) 
        

        self.assertEqual(nb_err, 0)
    
    @classmethod
    def tearDownClass(cls):
        #output = cls.report.sort('Level',)
        if cls.report.empty == False:
            print("\n_____________________________________________________________________________________________\n\nFollowing debug table can be found as a tsv file at the bottom of the summary of this job\n_____________________________________________________________________________________________")
            pd.set_option("display.max_rows",None,"display.max_colwidth", 5000,"display.width",5000)
            print(tabulate(cls.report[['Test Name','Entity','Label','Debug Message']], headers=['Test Name','Entity','Label','Debug Message']))
            # prettify(cls.report[['Entity','Label','Debug Message']])
        cls.report.to_csv("./output_edamci.tsv", sep='\t')
        return super().tearDownClass()

if __name__ == '__main__':

    run_error,run_essential,run_curation = parsing()
    print(f"error = {run_error}, essential = {run_essential}, curation = {run_curation}")

    runner = unittest.TextTestRunner()
    sys.exit(runner.run(suite()))
    


    
