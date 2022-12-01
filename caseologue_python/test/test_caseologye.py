import os
from caseologue import EdamQueryTest


class NoErrorFound(Exception):
    """Raised when the test_test function doesn't catch the errors in the test data or the test data is not right.
    
    Attributes:
        nb_expected_error -- number of error expected to be caught by the test in the test data. 
        message -- explanation of the error
    """

    def __init__(self, nb_expected_error, message="No error caugtht by the test instead of the expected "):
        self.message = message + str(nb_expected_error)
        super().__init__(self.message)

class UncorrectNumberError(Exception):
    """Raised when the test_test function doesn't catch the errors in the test data or the test data is not right.

    Attributes:
        nb_detected_errors -- number of error detected by the test in the test data. 
        nb_expected_error -- number of error expected to be caught by the test in the test data. 
        message_start -- explanation of the error
        message_end -- explanation of the error
    """

    def __init__(self, nb_expected_error, nb_detected_errors, message_start="Uncorrect number of errors caught by the test: ", message_end=" instead of "):
        self.message = message_start + str(nb_detected_errors) + message_end + str(nb_expected_error)
        super().__init__(self.message)

################# DEPRECATED REPLACEMENT OBSOLETE ###########################


def test_test_deprecated_replacement_obsolete():
    
    os.environ['EDAM_PATH'] = "data/deprecated_replacement_obsolete_test_data.owl"

    nb_expected_error = 1

    test_object=EdamQueryTest()

    test_object.setUpClass()

    try:
        
        test_object.test_deprecated_replacement_obsolete(query = "../queries/deprecated_replacement_obsolete.rq")

    except AssertionError as e:
        nb_detected_errors=int(str(e).rsplit('!')[0])
        if nb_detected_errors == nb_expected_error : 
            print(f"\n=====================\n\ntest_deprecated_replacement_obsolete caught {nb_detected_errors} errors in the test data {os.environ['EDAM_PATH']}\n")
        else:
            raise UncorrectNumberError(nb_expected_error,nb_detected_errors)

    else: 
        raise NoErrorFound(nb_expected_error)

    test_object.tearDownClass()
    
    return()

################# SUPERCLASS REFERS TO SELF ###########################

def test_test_super_class_refers_to_self():
    
    os.environ['EDAM_PATH'] = "data/super_class_refers_to_self_test_data.owl"

    nb_expected_error = 1

    test_object=EdamQueryTest()

    test_object.setUpClass()

    try:
        test_object.test_super_class_refers_to_self(query = "../queries/super_class_refers_to_self.rq")
    except AssertionError as e:
        nb_detected_errors=int(str(e).rsplit('!')[0])
        if nb_detected_errors == nb_expected_error : 
            print(f"\n=====================\n\ntest_class_refers_to_self caught {nb_detected_errors} errors in the test data {os.environ['EDAM_PATH']}\n")
        else:
            raise UncorrectNumberError(nb_expected_error,nb_detected_errors)

    else: 
        raise NoErrorFound(nb_expected_error)

    test_object.tearDownClass()
    
    return()

################# BAD URI ###########################


def test_test_bad_uri():
    
    os.environ['EDAM_PATH'] = "data/bad_uri_test_data.owl"

    nb_expected_error = 2

    test_object=EdamQueryTest()

    test_object.setUpClass()

    try:
        test_object.test_bad_uri(query = "../queries/bad_uri.rq")
    except AssertionError as e:
        nb_detected_errors=int(str(e).rsplit('!')[0])
        if nb_detected_errors == nb_expected_error : 
            print(f"\n=====================\n\ntest_bad_uri caught {nb_detected_errors} errors in the test data {os.environ['EDAM_PATH']}\n")
        else:
            raise UncorrectNumberError(nb_expected_error,nb_detected_errors)

    else: 
        raise NoErrorFound(nb_expected_error)

    test_object.tearDownClass()
    
    return()

################# MANDATORY PROPERTY MISSING ###########################

def test_test_mandatory_property_missing():
    
    os.environ['EDAM_PATH'] = "data/mandatory_property_missing_test_data.owl"

    nb_expected_error = 5

    test_object=EdamQueryTest()

    test_object.setUpClass()

    try:
        test_object.test_mandatory_property_missing(query = "../queries/mandatory_property_missing.rq")
    except AssertionError as e:
        nb_detected_errors=int(str(e).rsplit('!')[0])
        if nb_detected_errors == nb_expected_error : 
            print(f"\n=====================\n\ntest_mandatory_property_missing caught {nb_detected_errors} errors in the test data {os.environ['EDAM_PATH']}\n")
        else:
            raise UncorrectNumberError(nb_expected_error,nb_detected_errors)

    else: 
        raise NoErrorFound(nb_expected_error)

    test_object.tearDownClass()
    
    return()

################# FORMATTING ###########################

def test_test_formatting():
    
    os.environ['EDAM_PATH'] = "data/formatting_test_data.owl"

    nb_expected_error = 5

    test_object=EdamQueryTest()

    test_object.setUpClass()

    try:
        test_object.test_formatting(query_dot_def = "../queries/end_dot_def_missing.rq", query_dot_label = "../queries/end_dot_label.rq", query_end_space = "../queries/end_space_annotation.rq", query_eol = "../queries/eol_in_annotation.rq", query_start_space = "../queries/start_space_annotation.rq", query_tab = "../queries/tab_in_annotation.rq")
    except AssertionError as e:
        nb_detected_errors=int(str(e).rsplit('!')[0])
        if nb_detected_errors == nb_expected_error : 
            print(f"\n=====================\n\ntest_formatting caught {nb_detected_errors} errors in the test data {os.environ['EDAM_PATH']}\n")
        else:
            raise UncorrectNumberError(nb_expected_error,nb_detected_errors)

    else: 
        raise NoErrorFound(nb_expected_error)

    test_object.tearDownClass()
    
    return()

################# DEPRECATED REPLACEMENT ###########################

def test_test_deprecated_replacement():
    
    os.environ['EDAM_PATH'] = "data/deprecated_replacement_test_data.owl"

    nb_expected_error = 1

    test_object=EdamQueryTest()

    test_object.setUpClass()

    try:
        test_object.test_deprecated_replacement(query = "../queries/deprecated_replacement.rq")
    except AssertionError as e:
        nb_detected_errors=int(str(e).rsplit('!')[0])
        if nb_detected_errors == nb_expected_error : 
            print(f"\n=====================\n\ntest_deprecated_replacement caught {nb_detected_errors} errors in the test data {os.environ['EDAM_PATH']}\n")
        else:
            raise UncorrectNumberError(nb_expected_error,nb_detected_errors)

    else: 
        raise NoErrorFound(nb_expected_error)

    test_object.tearDownClass()
    
    return()

################# BAD URI REFERENCE ###########################

def test_test_bad_uri_reference():
    
    os.environ['EDAM_PATH'] = "data/bad_uri_reference_test_data.owl"

    nb_expected_error = 6

    test_object=EdamQueryTest()

    test_object.setUpClass()

    try:
        test_object.test_bad_uri_reference(query_get_uri = "../queries/get_uri.rq", query_uri_reference = "../queries/uri_reference.rq")
    except AssertionError as e:
        nb_detected_errors=int(str(e).rsplit('!')[0])
        if nb_detected_errors == nb_expected_error : 
            print(f"\n=====================\n\ntest_bad_uri_reference caught {nb_detected_errors} errors in the test data {os.environ['EDAM_PATH']}\n")
        else:
            raise UncorrectNumberError(nb_expected_error,nb_detected_errors)

    else: 
        raise NoErrorFound(nb_expected_error)

    test_object.tearDownClass()
    
    return()

################# MISSING DEPRECATED PROPERTY ###########################

def test_test_missing_deprecated_property():
    
    os.environ['EDAM_PATH'] = "data/missing_deprecated_property_test_data.owl"

    nb_expected_error = 3

    test_object=EdamQueryTest()

    test_object.setUpClass()

    try:
        test_object.test_missing_deprecated_property(query = "../queries/missing_deprecated_property.rq")
    except AssertionError as e:
        nb_detected_errors=int(str(e).rsplit('!')[0])
        if nb_detected_errors == nb_expected_error : 
            print(f"\n=====================\n\ntest_missing_deprecated_property caught {nb_detected_errors} errors in the test data {os.environ['EDAM_PATH']}\n")
        else:
            raise UncorrectNumberError(nb_expected_error,nb_detected_errors)

    else: 
        raise NoErrorFound(nb_expected_error)

    test_object.tearDownClass()
    
    return()

################# MISSING WIKIPEDIA LINK ###########################

def test_test_check_wikipedia_link():
    
    os.environ['EDAM_PATH'] = "data/check_wikipedia_link_test_data.owl"

    nb_expected_error = 2

    test_object=EdamQueryTest()

    test_object.setUpClass()

    try:
        test_object.test_check_wikipedia_link(query = "../queries/check_wikipedia_link.rq")
    except AssertionError as e:
        nb_detected_errors=int(str(e).rsplit('!')[0])
        if nb_detected_errors == nb_expected_error : 
            print(f"\n=====================\n\ntest_check_wikipedia_link caught {nb_detected_errors} errors in the test data {os.environ['EDAM_PATH']}\n")
        else:
            raise UncorrectNumberError(nb_expected_error,nb_detected_errors)

    else: 
        raise NoErrorFound(nb_expected_error)

    test_object.tearDownClass()
    
    return()

################# IDENTIFIER PROPERTY MISSING ###########################

def test_test_identifier_property_missing():
    
    os.environ['EDAM_PATH'] = "data/identifier_property_missing_test_data.owl"

    nb_expected_error = 1

    test_object=EdamQueryTest()

    test_object.setUpClass()

    try:
        test_object.test_identifier_property_missing(query = "../queries/identifier_property_missing.rq")
    except AssertionError as e:
        nb_detected_errors=int(str(e).rsplit('!')[0])
        if nb_detected_errors == nb_expected_error : 
            print(f"\n=====================\n\ntest_identifier_property_missing caught {nb_detected_errors} errors in the test data {os.environ['EDAM_PATH']}\n")
        else:
            raise UncorrectNumberError(nb_expected_error,nb_detected_errors)

    else: 
        raise NoErrorFound(nb_expected_error)

    test_object.tearDownClass()
    
    return()

################# ID UNIQUE ###########################

def test_test_id_unique():
    
    os.environ['EDAM_PATH'] = "data/id_unique_test_data.owl"

    nb_expected_error = 4

    test_object=EdamQueryTest()

    test_object.setUpClass()

    try:
        test_object.test_id_unique(query = "../queries/get_uri.rq")
    except AssertionError as e:
        nb_detected_errors=int(str(e).rsplit('!')[0])
        if nb_detected_errors == nb_expected_error : 
            print(f"\n=====================\n\ntest_id_unique caught {nb_detected_errors} errors in the test data {os.environ['EDAM_PATH']}\n")
        else:
            raise UncorrectNumberError(nb_expected_error,nb_detected_errors)

    else: 
        raise NoErrorFound(nb_expected_error)

    test_object.tearDownClass()
    
    return()

################# RELATION TOO BROAD ###########################

def test_test_relation_too_broad():
    
    os.environ['EDAM_PATH'] = "data/relation_too_broad_test_data.owl"

    nb_expected_error = 1

    test_object=EdamQueryTest()

    test_object.setUpClass()

    try:
        test_object.test_relation_too_broad(query = "../queries/relation_too_broad.rq")
    except AssertionError as e:
        nb_detected_errors=int(str(e).rsplit('!')[0])
        if nb_detected_errors == nb_expected_error : 
            print(f"\n=====================\n\ntest_relation_too_broad caught {nb_detected_errors} errors in the test data {os.environ['EDAM_PATH']}\n")
        else:
            raise UncorrectNumberError(nb_expected_error,nb_detected_errors)

    else: 
        raise NoErrorFound(nb_expected_error)

    test_object.tearDownClass()
    
    return()

################# DUPLICATE IN CONCEPT ###########################

def test_test_duplicate_in_concept():
    
    os.environ['EDAM_PATH'] = "data/duplicate_in_concept_test_data.owl"

    nb_expected_error = 2

    test_object=EdamQueryTest()

    test_object.setUpClass()

    try:
        test_object.test_duplicate_in_concept(query = "../queries/duplicate_in_concept.rq")
    except AssertionError as e:
        nb_detected_errors=int(str(e).rsplit('!')[0])
        if nb_detected_errors == nb_expected_error : 
            print(f"\n=====================\n\ntest_duplicate_in_concept caught {nb_detected_errors} errors in the test data {os.environ['EDAM_PATH']}\n")
        else:
            raise UncorrectNumberError(nb_expected_error,nb_detected_errors)

    else: 
        raise NoErrorFound(nb_expected_error)

    test_object.tearDownClass()
    
    return()

################# DUPLICATE ALL ###########################

def test_test_duplicate_all():
    
    os.environ['EDAM_PATH'] = "data/duplicate_all_test_data.owl"

    nb_expected_error = 1

    test_object=EdamQueryTest()

    test_object.setUpClass()

    try:
        test_object.test_duplicate_all(query = "../queries/duplicate_all.rq")
    except AssertionError as e:
        nb_detected_errors=int(str(e).rsplit('!')[0])
        if nb_detected_errors == nb_expected_error : 
            print(f"\n=====================\n\ntest_duplicate_all caught {nb_detected_errors} errors in the test data {os.environ['EDAM_PATH']}\n")
        else:
            raise UncorrectNumberError(nb_expected_error,nb_detected_errors)

    else: 
        raise NoErrorFound(nb_expected_error)

    test_object.tearDownClass()
    
    return()

################# LITERAL LINKS ###########################

def test_test_literal_links():
    
    os.environ['EDAM_PATH'] = "data/literal_links_test_data.owl"

    nb_expected_error = 1

    test_object=EdamQueryTest()

    test_object.setUpClass()

    try:
        test_object.test_literal_links(query = "../queries/literal_links.rq")
    except AssertionError as e:
        nb_detected_errors=int(str(e).rsplit('!')[0])
        if nb_detected_errors == nb_expected_error : 
            print(f"\n=====================\n\ntest_literal_links caught {nb_detected_errors} errors in the test data {os.environ['EDAM_PATH']}\n")
        else:
            raise UncorrectNumberError(nb_expected_error,nb_detected_errors)

    else: 
        raise NoErrorFound(nb_expected_error)

    test_object.tearDownClass()
    
    return()

################# NEXT ID MODIF ###########################

def test_test_next_id_modif():
    
    os.environ['EDAM_PATH'] = "data/next_id_modif_test_data.owl"

    nb_expected_error = 1

    test_object=EdamQueryTest()

    test_object.setUpClass()

    try:
        test_object.test_next_id_modif(query = "../queries/get_id_and_next_id.rq")
    except AssertionError as e:
        nb_detected_errors=int(str(e).rsplit('!')[0])
        if nb_detected_errors == nb_expected_error : 
            print(f"\n=====================\n\ntest_next_id_modif caught {nb_detected_errors} errors in the test data {os.environ['EDAM_PATH']}\n")
        else:
            raise UncorrectNumberError(nb_expected_error,nb_detected_errors)

    else: 
        raise NoErrorFound(nb_expected_error)

    test_object.tearDownClass()
    
    return()

################# SUBSET ID ###########################

def test_test_subset_id():
    
    os.environ['EDAM_PATH'] = "data/subset_id_test_data.owl"

    nb_expected_error = 1

    test_object=EdamQueryTest()

    test_object.setUpClass()

    try:
        test_object.test_subset_id(query = "../queries/subset_id.rq")
    except AssertionError as e:
        nb_detected_errors=int(str(e).rsplit('!')[0])
        if nb_detected_errors == nb_expected_error : 
            print(f"\n=====================\n\ntest_subset_id caught {nb_detected_errors} errors in the test data {os.environ['EDAM_PATH']}\n")
        else:
            raise UncorrectNumberError(nb_expected_error,nb_detected_errors)

    else: 
        raise NoErrorFound(nb_expected_error)

    test_object.tearDownClass()
    
    return()

################# OBJECT RELATION OBSOLETE ###########################

def test_test_object_relation_obsolete():
    
    os.environ['EDAM_PATH'] = "data/object_relation_obsolete_test_data.owl"

    nb_expected_error = 1

    test_object=EdamQueryTest()

    test_object.setUpClass()

    try:
        test_object.test_object_relation_obsolete(query = "../queries/object_relation_obsolete.rq")
    except AssertionError as e:
        nb_detected_errors=int(str(e).rsplit('!')[0])
        if nb_detected_errors == nb_expected_error : 
            print(f"\n=====================\n\ntest_object_relation_obsolete caught {nb_detected_errors} errors in the test data {os.environ['EDAM_PATH']}\n")
        else:
            raise UncorrectNumberError(nb_expected_error,nb_detected_errors)

    else: 
        raise NoErrorFound(nb_expected_error)

    test_object.tearDownClass()
    
    return()

################# FORMAT PROPERTY MISSING ###########################

def test_test_format_property_missing():
    
    os.environ['EDAM_PATH'] = "data/format_property_missing_test_data.owl"

    nb_expected_error = 3

    test_object=EdamQueryTest()

    test_object.setUpClass()

    try:
        test_object.test_format_property_missing(construct = "../queries/is_format_of_construct.rq", query = "../queries/format_property_missing.rq")
    except AssertionError as e:
        nb_detected_errors=int(str(e).rsplit('!')[0])
        if nb_detected_errors == nb_expected_error : 
            print(f"\n=====================\n\ntest_format_property_missing caught {nb_detected_errors} errors in the test data {os.environ['EDAM_PATH']}\n")
        else:
            raise UncorrectNumberError(nb_expected_error,nb_detected_errors)

    else: 
        raise NoErrorFound(nb_expected_error)

    test_object.tearDownClass()
    
    return()

################# EMPTY PROPERTY ###########################

def test_test_empty_property():
    
    os.environ['EDAM_PATH'] = "data/empty_property_test_data.owl"

    nb_expected_error = 1

    test_object=EdamQueryTest()

    test_object.setUpClass()

    try:
        test_object.test_empty_property(query = "../queries/empty_property.rq")
    except AssertionError as e:
        nb_detected_errors=int(str(e).rsplit('!')[0])
        if nb_detected_errors == nb_expected_error : 
            print(f"\n=====================\n\ntest_empty_property caught {nb_detected_errors} errors in the test data {os.environ['EDAM_PATH']}\n")
        else:
            raise UncorrectNumberError(nb_expected_error,nb_detected_errors)

    else: 
        raise NoErrorFound(nb_expected_error)

    test_object.tearDownClass()
    
    return()

################# SPELLING CHECK ###########################

def test_test_spelling_check():
    
    os.environ['EDAM_PATH'] = "data/spelling_check_test_data.owl"

    nb_expected_error = 2

    test_object=EdamQueryTest()

    test_object.setUpClass()

    try:
        test_object.test_spelling_check(spelling_ignore = "../spelling_ignore.txt")
    except AssertionError as e:
        nb_detected_errors=int(str(e).rsplit('!')[0])
        if nb_detected_errors == nb_expected_error : 
            print(f"\n=====================\n\ntest_spelling_check caught {nb_detected_errors} errors in the test data {os.environ['EDAM_PATH']}\n")
        else:
            raise UncorrectNumberError(nb_expected_error,nb_detected_errors)

    else: 
        raise NoErrorFound(nb_expected_error)

    test_object.tearDownClass()
    
    return()

if __name__ == "__main__":
    
    # test_test_deprecated_replacement_obsolete()
    # test_test_super_class_refers_to_self()
    # test_test_bad_uri()
    # test_test_mandatory_property_missing()
    # test_test_formatting()
    # test_test_deprecated_replacement()
    # test_test_bad_uri_reference()
    # test_test_missing_deprecated_property()
    # test_test_check_wikipedia_link()
    # test_test_identifier_property_missing()
    test_test_id_unique()
    # test_test_relation_too_broad()
    # test_test_duplicate_in_concept()
    # test_test_duplicate_all()
    # test_test_literal_links()
    # test_test_next_id_modif()
    # test_test_subset_id()
    # test_test_object_relation_obsolete()
    # test_test_format_property_missing()
    # test_test_empty_property()
    # test_test_spelling_check()
