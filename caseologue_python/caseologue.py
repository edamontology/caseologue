import unittest
from rdflib import OWL, ConjunctiveGraph, Namespace
import os
import pandas as pd
import argparse
import sys
from collections import Counter
from rdflib.namespace import RDF, RDFS, _OWL
from tabulate import tabulate

# from rich_dataframe import prettify
from queries.edamxpath_id_unique import check_unique_id


def parsing():

    parser = argparse.ArgumentParser(
        description="Level of tests, by default all levels are ran"
    )
    parser.add_argument(
        "-e", "--error", action="store_true", help="runs all error tests"
    )
    parser.add_argument(
        "-E", "--essential", action="store_true", help="runs all essential tests"
    )
    parser.add_argument(
        "-c", "--curation", action="store_true", help="runs all curation tests"
    )
    parser.add_argument("unittest_args", nargs="*")

    args = parser.parse_args()

    # print("args argparse",args.error,args.essential,args.curation)

    if args.error != False or args.essential != False or args.curation != False:
        run_error = args.error
        run_essential = args.essential
        run_curation = args.curation

    else:
        run_error = True
        run_essential = True
        run_curation = True

    # print("def parsing",run_error,run_essential,run_curation)

    sys.argv[1:] = args.unittest_args

    return (run_error, run_essential, run_curation)


def suite():
    """
    Defines the level of error of each test.
    """
    suite = unittest.TestSuite()

    if run_curation == True:
        suite.addTest(EdamQueryTest("test_deprecated_replacement_obsolete"))
        suite.addTest(EdamQueryTest("test_formatting"))
        suite.addTest(EdamQueryTest("test_check_wikipedia_link"))
        suite.addTest(EdamQueryTest("test_identifier_property_missing"))
        suite.addTest(EdamQueryTest("test_relation_too_broad"))
        suite.addTest(EdamQueryTest("test_duplicate_in_concept"))
        suite.addTest(EdamQueryTest("test_literal_links"))
        #        suite.addTest(EdamQueryTest('test_duplicate_all'))   too long computing time for now 
        suite.addTest(EdamQueryTest("test_format_property_missing"))

    if run_essential == True:
        suite.addTest(EdamQueryTest("test_super_class_refers_to_self"))
        suite.addTest(EdamQueryTest("test_bad_uri_reference"))
        suite.addTest(EdamQueryTest("test_empty_property"))
        suite.addTest(EdamQueryTest("test_id_unique"))
        suite.addTest(EdamQueryTest("test_spelling_check"))

    if run_error == True:
        suite.addTest(EdamQueryTest("test_mandatory_property_missing"))
        suite.addTest(EdamQueryTest("test_deprecated_replacement"))
        suite.addTest(EdamQueryTest("test_missing_deprecated_property"))
        suite.addTest(EdamQueryTest("test_next_id_modif"))
        suite.addTest(EdamQueryTest("test_subset_id"))
        suite.addTest(EdamQueryTest("test_object_relation_obsolete"))
        suite.addTest(EdamQueryTest("test_bad_uri"))

    return suite


# each test is added in function of the boolean input (error essential curation), to change level category, change tested variable (+ change level error when adding new_error in data frame)


class EdamQueryTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        """
        :meta private:
        docstring set to private to avoid automatic default docstring in documentation
        """
        cls.dir_path=os.path.dirname(os.path.realpath(__file__))
        cls.edam_graph = ConjunctiveGraph()
        cls.edam_graph.parse(os.environ.get("EDAM_PATH"), format="xml")
        cls.report = pd.DataFrame(
            columns=["Level", "Test Name", "Entity", "Label", "Debug Message"]
        )
        # print(cls.report)

    ################# DEPRECATED REPLACEMENT OBSOLETE ###########################

    def test_deprecated_replacement_obsolete(self):

        """
        Checks that the suggested replacement (replacedBy/consider) for a deprecated term is not obsolete.

            > SPARQL query available `here  <https://github.com/edamontology/edam-validation/blob/main/caseologue/queries/deprecated_replacement_obsolete.rq>`_
        
        Severity level: curation

        """
        
        query=self.dir_path + "/queries/deprecated_replacement_obsolete.rq"

        with open(query, "r") as f:
            query_term = f.read()
        results = self.edam_graph.query(query_term)
        nb_err = len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame(
                [
                    [
                        "CURATION",
                        "deprecated_replacement_obsolete",
                        r["entity"],
                        (f"'{r['label']}'"),
                        (
                            f"concept is replaced by ({r['property']}) an obsolete concept: {r['replacement']}"
                        ),
                    ]
                ],
                columns=["Level", "Test Name", "Entity", "Label", "Debug Message"],
            )
            self.__class__.report = pd.concat(
                [self.report, new_error], ignore_index=True
            )

        self.assertEqual(nb_err, 0)

    ################# SUPERCLASS REFERS TO SELF ###########################

    def test_super_class_refers_to_self(self):

        """
        Checks if a given concept doesn't refers to itself as superclass.

            > SPARQL query available `here  <https://github.com/edamontology/edam-validation/blob/main/caseologue/queries/super_class_refers_to_self.rq>`_
        
        Severity level: essential

        """
        query =self.dir_path + "/queries/super_class_refers_to_self.rq"
        
        with open(query, "r") as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err = len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame(
                [
                    [
                        "ESSENTIAL",
                        "super_class_refers_to_self",
                        r["entity"],
                        (f"'{r['label']}'"),
                        "concept declared as superclass of itself",
                    ]
                ],
                columns=["Level", "Test Name", "Entity", "Label", "Debug Message"],
            )
            self.__class__.report = pd.concat(
                [self.report, new_error], ignore_index=True
            )

        self.assertEqual(nb_err, 0)

    ################# BAD URI ###########################

    def test_bad_uri(self):

        """
        Checks that the concepts URI matches the regex ^http://edamontology.org/(data|topic|operation|format)_[0-9]{4}$.

           > SPARQL query available `here  <https://github.com/edamontology/edam-validation/blob/main/caseologue/queries/bad_uri.rq>`_

        
        Severity level: essential

        """
        query =self.dir_path + "/queries/bad_uri.rq"

        with open(query, "r") as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err = len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame(
                [
                    [
                        "ESSENTIAL",
                        "bad_rui",
                        r["entity"],
                        (f"'{r['label']}'"),
                        "has a bad URI (entity) (regex :^http://edamontology.org/(data|topic|operation|format)_[0-9]\{4\}$)",
                    ]
                ],
                columns=["Level", "Test Name", "Entity", "Label", "Debug Message"],
            )
            self.__class__.report = pd.concat(
                [self.report, new_error], ignore_index=True
            )

        self.assertEqual(nb_err, 0)

    ################# MANDATORY PROPERTY MISSING ###########################

    def test_mandatory_property_missing(self):

        """
        Checks that no mandatory property for all concepts are missing (oboInOwl:hasDefinition, rdfs:subClassOf, created_in, oboInOwl:inSubset, rdfs:label).

            > SPARQL query available `here  <https://github.com/edamontology/edam-validation/blob/main/caseologue/queries/mandatory_property_missing.rq>`_
        
        Severity level: error

        """
        query =self.dir_path + "/queries/mandatory_property_missing.rq"

        with open(query, "r") as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err = len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame(
                [
                    [
                        "ERROR",
                        "mandatory_property_missing",
                        r["entity"],
                        (f"'{r['label']}'"),
                        (f"is missing mandatory property: {r['property']} "),
                    ]
                ],
                columns=["Level", "Test Name", "Entity", "Label", "Debug Message"],
            )
            self.__class__.report = pd.concat(
                [self.report, new_error], ignore_index=True
            )

        self.assertEqual(nb_err, 0)

    ################# FORMATTING ###########################

    def test_formatting(self):

        """
        Checks the formatting of the properties. Properties should not have a space neither at the start nor the end, no tab and no end of line.
        Checks that label have no dot at the end and that definition do have a dot at the end.

            > SPARQL query available here:

                * `Definition dot  <https://github.com/edamontology/edam-validation/blob/main/caseologue/queries/end_dot_def_missing.rq.rq>`_
                * `Label dot  <https://github.com/edamontology/edam-validation/blob/main/caseologue/queries/end_dot_label.rq>`_
                * `End space  <https://github.com/edamontology/edam-validation/blob/main/caseologue/queries/end_space_annotation.rq>`_
                * `Start space  <https://github.com/edamontology/edam-validation/blob/main/caseologue/queries/start_space_annotation.rq>`_
                * `Tab  <https://github.com/edamontology/edam-validation/blob/main/caseologue/queries/tab_in_annotation.rq>`_
                * `End of line  <https://github.com/edamontology/edam-validation/blob/main/caseologue/queries/eol_in_annotation.rq>`_

        
        Severity level: curation

        """
        query_dot_def =self.dir_path + "/queries/end_dot_def_missing.rq"
        query_dot_label =self.dir_path + "/queries/end_dot_label.rq"
        query_end_space =self.dir_path + "/queries/end_space_annotation.rq"
        query_eol =self.dir_path + "/queries/eol_in_annotation.rq"
        query_start_space =self.dir_path + "/queries/start_space_annotation.rq"
        query_tab =self.dir_path + "/queries/tab_in_annotation.rq"

        with open(query_dot_def, "r") as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err = len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame(
                [
                    [
                        "CURATION",
                        "end_dot_def_missing",
                        r["entity"],
                        (f"'{r['label']}'"),
                        "A dot is missing at the end of the definition.",
                    ]
                ],
                columns=["Level", "Test Name", "Entity", "Label", "Debug Message"],
            )
            self.__class__.report = pd.concat(
                [self.report, new_error], ignore_index=True
            )

        with open(query_dot_label, "r") as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err += len(results)  # add to same counter for the test
        f.close()

        for r in results:
            new_error = pd.DataFrame(
                [
                    [
                        "CURATION",
                        "end_dot_label",
                        r["entity"],
                        (f"'{r['label']}'"),
                        "There is an unwanted dot at the end of the label.",
                    ]
                ],
                columns=["Level", "Test Name", "Entity", "Label", "Debug Message"],
            )
            self.__class__.report = pd.concat(
                [self.report, new_error], ignore_index=True
            )

        with open(query_end_space, "r") as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err += len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame(
                [
                    [
                        "CURATION",
                        "end_space_annotation",
                        r["entity"],
                        (f"'{r['label']}'"),
                        (
                            f"There is an unwanted space at the end of {r['property']} : {r['value']}."
                        ),
                    ]
                ],
                columns=["Level", "Test Name", "Entity", "Label", "Debug Message"],
            )
            self.__class__.report = pd.concat(
                [self.report, new_error], ignore_index=True
            )

        with open(query_eol, "r") as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err += len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame(
                [
                    [
                        "CURATION",
                        "eol_in_annotation",
                        r["entity"],
                        (f"'{r['label']}'"),
                        (
                            f"There is an unwanted end-of-line in {r['property']} : {r['value']}."
                        ),
                    ]
                ],
                columns=["Level", "Test Name", "Entity", "Label", "Debug Message"],
            )
            self.__class__.report = pd.concat(
                [self.report, new_error], ignore_index=True
            )

        with open(query_start_space, "r") as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err += len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame(
                [
                    [
                        "CURATION",
                        "start_space_annotation",
                        r["entity"],
                        (f"'{r['label']}'"),
                        (
                            f"There is an unwanted space at the start of {r['property']} : {r['value']}."
                        ),
                    ]
                ],
                columns=["Level", "Test Name", "Entity", "Label", "Debug Message"],
            )
            self.__class__.report = pd.concat(
                [self.report, new_error], ignore_index=True
            )

        with open(query_tab, "r") as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err += len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame(
                [
                    [
                        "CURATION",
                        "tab_in_annotation",
                        r["entity"],
                        (f"'{r['label']}'"),
                        (
                            f"There is an unwanted tabulation in {r['property']} : {r['value']}."
                        ),
                    ]
                ],
                columns=["Level", "Test Name", "Entity", "Label", "Debug Message"],
            )
            self.__class__.report = pd.concat(
                [self.report, new_error], ignore_index=True
            )

        self.assertEqual(nb_err, 0)

    ################# DEPRECATED REPLACEMENT ###########################

    def test_deprecated_replacement(self):

        """
        Checks that every deprecated concept has a replacement suggested (replaced_by or consider).

            > SPARQL query available `here  <https://github.com/edamontology/edam-validation/blob/main/caseologue/queries/deprecated_replacement.rq>`_
        
        Severity level: error

        """

        query =self.dir_path + "/queries/deprecated_replacement.rq"

        with open(query, "r") as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err = len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame(
                [
                    [
                        "ERROR",
                        "deprecated_replacement",
                        r["entity"],
                        (f"'{r['label']}'"),
                        "is deprecated and is missing either a replacedBy property or a consider property",
                    ]
                ],
                columns=["Level", "Test Name", "Entity", "Label", "Debug Message"],
            )
            self.__class__.report = pd.concat(
                [self.report, new_error], ignore_index=True
            )

        self.assertEqual(nb_err, 0)

    ################# BAD URI REFERENCE ###########################

    def test_bad_uri_reference(self):

        """
        Check that a reference (e.g. superclass) to another concept is actually declared in EDAM.

        "get_uri.rq" retrieves all URI. "uri_reference.rq" retrieves all referenced URI. Then check if the references URIs are in the declared concept URIs.

            > SPARQL query available here :

                * `get uri  <https://github.com/edamontology/edam-validation/blob/main/caseologue/queries/get_uri.rq>`_
                * `uri reference <https://github.com/edamontology/edam-validation/blob/main/caseologue/queries/uri_reference.rq>`_
        
        Severity level: essential

        """

        query_get_uri =self.dir_path + "/queries/get_uri.rq"
        query_uri_reference =self.dir_path + "/queries/uri_reference.rq"

        
        uri = []
        with open(query_get_uri, "r") as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        f.close()

        for r in results:
            uri.append(r["entity"])

        
        with open(query_uri_reference, "r") as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        f.close()

        nb_err = 0
        for r in results:
            if r["reference"] not in uri:
                nb_err += 1
                new_error = pd.DataFrame(
                    [
                        [
                            "ESSENTIAL",
                            "bad_uri_reference",
                            r["entity"],
                            (f"'{r['label']}'"),
                            (
                                f"The property {r['property']} refers not an undeclared URI: '{r['reference']}'"
                            ),
                        ]
                    ],
                    columns=["Level", "Test Name", "Entity", "Label", "Debug Message"],
                )
                self.__class__.report = pd.concat(
                    [self.report, new_error], ignore_index=True
                )

        self.assertEqual(nb_err, 0)

    ################# MISSING DEPRECATED PROPERTY ###########################

    def test_missing_deprecated_property(self):

        """
        Checks that no mandatory property for deprecated concept are missing (edam:obsolete_since, edam:oldParent, oboInOwl:inSubset <http://purl.obolibrary.org/obo/edam#obsolete>, rdfs:subClassOf <http://www.w3.org/2002/07/owl#DeprecatedClass>).

            > SPARQL query available `here  <https://github.com/edamontology/edam-validation/blob/main/caseologue/queries/missing_deprecated_property.rq>`_
        
        Severity level: error 

        """

        query =self.dir_path + "/queries/missing_deprecated_property.rq"

        
        with open(query, "r") as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err = len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame(
                [
                    [
                        "ERROR",
                        "missing_deprecated_property",
                        r["entity"],
                        (f"'{r['label']}'"),
                        (f"is missing mandatory deprecated property: {r['property']}"),
                    ]
                ],
                columns=["Level", "Test Name", "Entity", "Label", "Debug Message"],
            )
            self.__class__.report = pd.concat(
                [self.report, new_error], ignore_index=True
            )

        self.assertEqual(nb_err, 0)

    ################# CHECK WIKIPEDIA LINK ###########################

    def test_check_wikipedia_link(self):

        """
        Checks that every topic has a wikipedia link filled in the seeAlso property.

            > SPARQL query available `here  <https://github.com/edamontology/edam-validation/blob/main/caseologue/queries/check_wikipedia_link.rq>`_
        
        Severity level: curation

        """

        query =self.dir_path + "/queries/check_wikipedia_link.rq"
        
        with open(query, "r") as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err = len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame(
                [
                    [
                        "CURATION",
                        "check_wikipedia_link",
                        r["entity"],
                        (f"'{r['label']}'"),
                        "Topic concept missing a wikipedia link",
                    ]
                ],
                columns=["Level", "Test Name", "Entity", "Label", "Debug Message"],
            )
            self.__class__.report = pd.concat(
                [self.report, new_error], ignore_index=True
            )

        self.assertEqual(nb_err, 0)

    ################# IDENTIFIER PROPERTY MISSING ###########################

    def test_identifier_property_missing(self):

        """
        Checks the no mandatory property for identifier (subclass of accession) are missing (regex).

            > SPARQL query available `here  <https://github.com/edamontology/edam-validation/blob/main/caseologue/queries/identifier_property_missing.rq>`_
        
        Severity level: curation

        """

        query =self.dir_path + "/queries/identifier_property_missing.rq"

        with open(query, "r") as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err = len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame(
                [
                    [
                        "CURATION",
                        "identifier_property_missing",
                        r["entity"],
                        (f"'{r['label']}'"),
                        "is missing regex property",
                    ]
                ],
                columns=["Level", "Test Name", "Entity", "Label", "Debug Message"],
            )
            self.__class__.report = pd.concat(
                [self.report, new_error], ignore_index=True
            )

        self.assertEqual(nb_err, 0)

    ################# ID UNIQUE ###########################

    def test_id_unique(self):

        """
        Checks that the numerical part of the URI is not duplicated.

        Uses a small python script to retrieve all duplicated id available `here  <https://github.com/edamontology/edam-validation/blob/main/caseologue/queries/edamxpath_id_unique.py>`_
        
        Severity level: error

        """

        query =self.dir_path + "/queries/get_uri.rq"

        duplicate_id = check_unique_id(os.environ.get("EDAM_PATH"))  #  this function only returns the second of the duplicated id. If the id are not strictly identical and their subontology is different, only one line will be visible in the report table for this error (ex format_1234 is duplicate of data_1234).
        nb_err = len(duplicate_id)


        with open(query, "r") as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        f.close()


        for id in duplicate_id:
            for r in results:
                if id in str(r["entity"]):
                    new_error = pd.DataFrame(
                        [
                            [
                                "ERROR",
                                "id_unique",
                                r["entity"],
                                (f"'{r['label']}'"),
                                (f"numerical id is used several times"),
                            ]
                        ],
                        columns=[
                            "Level",
                            "Test Name",
                            "Entity",
                            "Label",
                            "Debug Message",
                        ],
                    )
                    self.__class__.report = pd.concat(
                        [self.report, new_error], ignore_index=True
                    )

        self.assertEqual(nb_err, 0)

    ################# RELATION TOO BROAD ###########################

    def test_relation_too_broad(self):

        """
        Checks that a concept is not in relation (restriction) with a concept "not recommended for annotation".

            > SPARQL query available `here  <https://github.com/edamontology/edam-validation/blob/main/caseologue/queries/relation_too_broad.rq>`_
        
        Severity level: curation

        """

        query =self.dir_path + "/queries/relation_too_broad.rq"

        
        with open(query, "r") as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err = len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame(
                [
                    [
                        "CURATION",
                        "relation_too_broad",
                        r["entity"],
                        (f"'{r['label']}'"),
                        (
                            f"linked ({r['property']}) with a concept not recommended for annotation : '{r['value']}'"
                        ),
                    ]
                ],
                columns=["Level", "Test Name", "Entity", "Label", "Debug Message"],
            )
            self.__class__.report = pd.concat(
                [self.report, new_error], ignore_index=True
            )

        self.assertEqual(nb_err, 0)

    ################# DUPLICATE IN CONCEPT ###########################

    def test_duplicate_in_concept(self):

        """
        Checks that there is no duplicate content (case insensitive) within a concept on given properties.

            > SPARQL query available `here  <https://github.com/edamontology/edam-validation/blob/main/caseologue/queries/duplicate_in_concept.rq>`_
        
        Severity level: curation

        """

        query =self.dir_path + "/queries/duplicate_in_concept.rq"

        
        with open(query, "r") as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err = len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame(
                [
                    [
                        "CURATION",
                        "duplicate_in_concept",
                        r["entity"],
                        (f"'{r['label']}'"),
                        (
                            f"{r['property']} and {r['property2']} have the same content: '{r['value']}'"
                        ),
                    ]
                ],
                columns=["Level", "Test Name", "Entity", "Label", "Debug Message"],
            )
            self.__class__.report = pd.concat(
                [self.report, new_error], ignore_index=True
            )

        # here for each duplicate there will be 2 line in the table but this is mandatory if there is 3 time the same content.

        self.assertEqual(nb_err, 0)

    ################# DUPLICATE ALL ###########################

    def test_duplicate_all(self):

        """
        Checks that there is no duplicate content (case sensitive, for computational reasons) across all the ontology on given properties.

            > SPARQL query available `here  <https://github.com/edamontology/edam-validation/blob/main/caseologue/queries/duplicate_all.rq>`_
        
        Severity level: curation

        """
        # this is case sensitive for computational time reasons

        query =self.dir_path + "/queries/duplicate_all.rq"
        
        with open(query, "r") as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err = len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame(
                [
                    [
                        "CURATION",
                        "duplicate_all",
                        r["entity"],
                        (f"'{r['label']}'"),
                        (
                            f"have the same content on {r['property']} as {r['entity2']} '{r['label2']}' on {r['property2']}: '{r['value']}'"
                        ),
                    ]
                ],
                columns=["Level", "Test Name", "Entity", "Label", "Debug Message"],
            )
            self.__class__.report = pd.concat(
                [self.report, new_error], ignore_index=True
            )

        # here for each duplicate there will be 2 line in the table but this is mandatory if there is 3 time the same content.

        self.assertEqual(nb_err, 0)

    ################# LITERAL LINKS ###########################

    def test_literal_links(self):

        """
        Checks that all webpage and doi are declared as literal links.

            > SPARQL query available `here  <https://github.com/edamontology/edam-validation/blob/main/caseologue/queries/literal_links.rq>`_
        
        Severity level: curation

        """

        query =self.dir_path + "/queries/literal_links.rq"
        
        with open(query, "r") as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err = len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame(
                [
                    [
                        "CURATION",
                        "literal_links",
                        r["entity"],
                        (f"'{r['label']}'"),
                        (
                            f"{r['property']} value is not declared as a literal: '{r['value']}'"
                        ),
                    ]
                ],
                columns=["Level", "Test Name", "Entity", "Label", "Debug Message"],
            )
            self.__class__.report = pd.concat(
                [self.report, new_error], ignore_index=True
            )

        self.assertEqual(nb_err, 0)

    ################# NEXT ID MODIF ###########################

    def test_next_id_modif(self):

        """
        Checks that the "next id" property is equal to "the maximal concept id numerical part" +1.

            > SPARQL query available `here  <https://github.com/edamontology/edam-validation/blob/main/caseologue/queries/get_id_and_next_id.rq>`_
        
        Severity level: error

        """

        query =self.dir_path + "/queries/get_id_and_next_id.rq"
        
        with open(query, "r") as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        f.close()
        nb_err = 0
        ids = []
        for r in results:
            ids.append(int(r["id"]))
            next_id = int(r["value"])
        max_ids = max(ids)
        if next_id != (max_ids + 1):
            nb_err = 1
            new_error = pd.DataFrame(
                [
                    [
                        "ERROR",
                        "next_id_modif",
                        "None",
                        "None",
                        (
                            f"The 'next_id' property has not been updated, it is not equal to the max id +1"
                        ),
                    ]
                ],
                columns=["Level", "Test Name", "Entity", "Label", "Debug Message"],
            )
            self.__class__.report = pd.concat(
                [self.report, new_error], ignore_index=True
            )

        self.assertEqual(nb_err, 0)

    ################# SUBSET ID ###########################

    def test_subset_id(self):

        """
        Checks that the "subset" part of a concept id is the same as its superclass (e.g. data concept only subclass of another data concept).

            > SPARQL query available `here  <https://github.com/edamontology/edam-validation/blob/main/caseologue/queries/subset_id.rq>`_
        
        Severity level: error

        """

        query =self.dir_path + "/queries/subset_id.rq"

        with open(query, "r") as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err = len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame(
                [
                    [
                        "ERROR",
                        "subset_id",
                        r["entity"],
                        (f"'{r['label']}'"),
                        (
                            f"Concept subset id ({r['subset']}) is different from its subclass {r['superclass']} '{r['label_sc']}'"
                        ),
                    ]
                ],
                columns=["Level", "Test Name", "Entity", "Label", "Debug Message"],
            )
            self.__class__.report = pd.concat(
                [self.report, new_error], ignore_index=True
            )

        self.assertEqual(nb_err, 0)

    ################# OBJECT RELATION OBSOLETE ###########################

    def test_object_relation_obsolete(self):

        """
        Checks that a relation between concepts is not pointing towards obsolete concepts (is_format_of, has_input, has_output, is_identifier_of, has_topic ...)

            > SPARQL query available `here  <https://github.com/edamontology/edam-validation/blob/main/caseologue/queries/object_relation_obsolete.rq>`_
        
        Severity level: error

        """

        query =self.dir_path + "/queries/object_relation_obsolete.rq"

        with open(query, "r") as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err = len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame(
                [
                    [
                        "ERROR",
                        "object_relation_obsolete",
                        r["entity"],
                        (f"'{r['label']}'"),
                        (
                            f"is related ({r['property']}) with {r['target']}, which is a deprecated concept"
                        ),
                    ]
                ],
                columns=["Level", "Test Name", "Entity", "Label", "Debug Message"],
            )
            self.__class__.report = pd.concat(
                [self.report, new_error], ignore_index=True
            )

        self.assertEqual(nb_err, 0)

    ################# FORMAT PROPERTY MISSING ###########################

    def test_format_property_missing(self):

        """
        Checks the no mandatory property for format are missing (documentation,is_format_of). To make sure not to miss the inherited "is_format_of" property from parent concept, a CONSTRUCT query is used to add the missing triplets to the graph. 

            > SPARQL query available `here  <https://github.com/edamontology/edam-validation/blob/main/caseologue/queries/format_property_missing.rq>`_
        
        Severity level: curation

        """

        construct =self.dir_path + "/queries/is_format_of_construct.rq"
        query =self.dir_path + "/queries/format_property_missing.rq"
        
        with open(construct, "r") as f:
            construct_term = f.read()
        
        results_update = self.edam_graph.query(construct_term)
        for r in results_update:
            update_edam=self.edam_graph.add((r[0],r[1],r[2]))

        f.close()
        
        with open(query, "r") as f:
            query_term = f.read()
        if len(results_update)!=0:
            results = update_edam.query(query_term)
        else:
            results = self.edam_graph.query(query_term)

        nb_err = len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame(
                [
                    [
                        "CURATION",
                        "format_property_missing",
                        r["entity"],
                        (f"'{r['label']}'"),
                        (f"is missing mandatory format property: {r['property']}"),
                    ]
                ],
                columns=["Level", "Test Name", "Entity", "Label", "Debug Message"],
            )
            self.__class__.report = pd.concat(
                [self.report, new_error], ignore_index=True
            )

        self.assertEqual(nb_err, 0)

    ################# EMPTY PROPERTY ###########################

    def test_empty_property(self):

        """
        Checks that no property is empty.

            > SPARQL query available `here  <https://github.com/edamontology/edam-validation/blob/main/caseologue/queries/empty_property.rq>`_
        
        Severity level: error

        """

        query =self.dir_path + "/queries/empty_property.rq"

        
        with open(query, "r") as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err = len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame(
                [
                    [
                        "ERROR",
                        "empty_property",
                        r["entity"],
                        (f"'{r['label']}'"),
                        (f"{r['property']} is empty"),
                    ]
                ],
                columns=["Level", "Test Name", "Entity", "Label", "Debug Message"],
            )
            self.__class__.report = pd.concat(
                [self.report, new_error], ignore_index=True
            )

        self.assertEqual(nb_err, 0)

    ################# SPELLING CHECK ###########################

    def test_spelling_check(self):

        """
        Uses unix codespell command and custom spelling dictionary to check spelling errors in EDAM.

            > GitHub page of codespell available `here  <https://github.com/codespell-project/codespell>`_
        
        Severity level: curation

        """
        spelling_ignore = self.dir_path + "/spelling_ignore.txt"
        edam_path = str(os.environ.get("EDAM_PATH"))
        cmd = "codespell -I " + spelling_ignore + " " + edam_path

        output = os.popen(cmd).read()
        spelling_err = output.rsplit("\n")
        spelling_err.remove("")

        for e in spelling_err:
            line = e.rsplit(":")[1]
            err = e.rsplit(": ")[1].rsplit(" ==>")[0]
            suggest = e.rsplit("==> ")[1]
            new_error = pd.DataFrame(
                [
                    [
                        "CURATION",
                        "spelling_check",
                        "Unknown",
                        "Unknown",
                        (
                            f'in your EDAM file, line {line}, "{err}" is suspected to be a spelling error. Could it be "{suggest}" instead? (if exception needed comment in PR ... )'
                        ),
                    ]
                ],
                columns=["Level", "Test Name", "Entity", "Label", "Debug Message"],
            )
            self.__class__.report = pd.concat(
                [self.report, new_error], ignore_index=True
            )

        nb_err = len(spelling_err)
        self.assertEqual(nb_err, 0)

    # ################# XXXXXTEMPLATE TO COPY-PASTEXXXXX ###########################

    # def XXXtest_nameXXX(self, query =self.dir_path + "/queries/XXXQUERY_FILEXXX.rq"):

    #     """
    #     XXXXDocstring documentation.XXXX

    #         > SPARQL query available `here  <https://github.com/edamontology/edam-validation/blob/main/caseologue/queries/XXXXXX.rq>`_
    #     """

    #     
    #     with open(query, "r") as f:
    #         query_term = f.read()

    #     results = self.edam_graph.query(query_term)
    #     nb_err = len(results)
    #     f.close()

    #     for r in results:
    #         new_error = pd.DataFrame(
    #             [
    #                 [
    #                     "XXXLEVELXXX",
    #                     "XXXTEST_NAMEXXX",
    #                     r["entity"],
    #                     (f"'{r['label']}'"),
    #                     (f" XXXDEBUG_MESSAGEXXX {r['property']}: '{r['value']}'"),
    #                 ]
    #             ],
    #             columns=["Level", "Test Name", "Entity", "Label", "Debug Message"],
    #         )
    #         self.__class__.report = pd.concat(
    #             [self.report, new_error], ignore_index=True
    #         )

    #     self.assertEqual(nb_err, 0)

    @classmethod
    def tearDownClass(cls):

        """
        :meta private:
        docstring set to private to avoid automatic default docstring in documentation
        
        Severity level: XXXX

        """

        # output = cls.report.sort('Level',)
        if cls.report.empty == False:
            pd.set_option(
                "display.max_rows",
                None,
                "display.max_colwidth",
                5000,
                "display.width",
                5000,
            )
            print(
                tabulate(
                    cls.report[["Test Name", "Entity", "Label", "Debug Message"]],
                    headers=["Test Name", "Entity", "Label", "Debug Message"],
                )
            )
            # prettify(cls.report[['Entity','Label','Debug Message']])
        cls.report.to_csv("./output_caseologue.tsv", sep="\t")
        return super().tearDownClass()


if __name__ == "__main__":

    run_error, run_essential, run_curation = parsing()
    print(
        f"error = {run_error}, essential = {run_essential}, curation = {run_curation}"
    )

    runner = unittest.TextTestRunner()
    # sys.exit(runner.run(suite()))
    cmd = runner.run(suite())
    print(cmd)
    if (len(cmd.failures) != 0) or (len(cmd.errors) != 0):
        exit(1)
