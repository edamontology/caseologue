import os
import sys
if os.path.dirname(os.getcwd()) not in sys.path:
    sys.path.insert(0, os.path.dirname(os.getcwd()))
from caseologue import EdamQueryTest

dir_path=os.path.dirname(os.path.realpath(__file__))

class NoErrorFound(Exception):
    """Raised when the test_test function doesn't catch the errors in the test data or the test data is not right.
    
    Attributes:
        nb_expected_error -- number of error expected to be caught by the test in the test data. 
        message -- explanation of the error
    """

    def __init__(self, nb_expected_error, message="No error caught by the test instead of the expected "):
        self.message = message + str(nb_expected_error)
        super().__init__(self.message)

class IncorrectNumberError(Exception):
    """Raised when the test_test function doesn't catch the errors in the test data or the test data is not right.

    Attributes:
        nb_detected_errors -- number of error detected by the test in the test data. 
        nb_expected_error -- number of error expected to be caught by the test in the test data. 
        message_start -- explanation of the error
        message_end -- explanation of the error
    """

    def __init__(self, nb_expected_error, nb_detected_errors, message_start="Incorrect number of errors caught by the test: ", message_end=" instead of "):
        self.message = message_start + str(nb_detected_errors) + message_end + str(nb_expected_error)
        super().__init__(self.message)



def test_caseologue(name,nb_expected_error):
    
    os.environ['EDAM_PATH'] = dir_path + "/data/" + name +"_test_data.owl" #get the test data from the name using the full path based on the directory path

    test_object=EdamQueryTest()

    test_object.setUpClass()  #run setupclass before calling each test, load edam_graph and the report data frame
    
    function = getattr(test_object, "test_"+ name) #function will call the corresponding caseologue test function

    try:
        
        function()

    except AssertionError as e:
        nb_detected_errors=int(str(e).rsplit('!')[0]) # checks that the number or found error is the expected one
        if nb_detected_errors == nb_expected_error : 
            print(f"\n=====================\n\ntest_{name} caught {nb_detected_errors} errors in the test data {name}_test_data.owl\n")
        else:
            raise IncorrectNumberError(nb_expected_error,nb_detected_errors) 

    else: 
        raise NoErrorFound(nb_expected_error)

    test_object.tearDownClass()
    
    return()


if __name__ == "__main__":

    test_caseologue(name= "deprecated_replacement_obsolete", nb_expected_error=1)
    test_caseologue(name= "super_class_refers_to_self", nb_expected_error=1)
    test_caseologue(name= "bad_uri", nb_expected_error=2)
    # test_caseologue(name= "mandatory_property_missing", nb_expected_error=5)
    test_caseologue(name= "formatting", nb_expected_error=5)
    test_caseologue(name= "deprecated_replacement", nb_expected_error=1)
    # test_caseologue(name= "bad_uri_reference", nb_expected_error=6)
    test_caseologue(name= "missing_deprecated_property", nb_expected_error=3)
    test_caseologue(name= "check_wikipedia_link", nb_expected_error=2)
    test_caseologue(name= "identifier_property_missing", nb_expected_error=1)
    test_caseologue(name= "id_unique", nb_expected_error=2)
    test_caseologue(name= "relation_too_broad", nb_expected_error=1)
    # test_caseologue(name= "duplicate_in_concept", nb_expected_error=2)
    # test_caseologue(name= "duplicate_all", nb_expected_error=1)
    test_caseologue(name= "literal_links", nb_expected_error=1)
    test_caseologue(name= "next_id_modif", nb_expected_error=1)
    test_caseologue(name= "subset_id", nb_expected_error=1)
    test_caseologue(name= "object_relation_obsolete", nb_expected_error=1)
    test_caseologue(name= "format_property_missing", nb_expected_error=3)
    test_caseologue(name= "empty_property", nb_expected_error=1)
    test_caseologue(name= "spelling_check", nb_expected_error=2)
