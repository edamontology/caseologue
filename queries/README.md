# Run tests individually with their test data

template : 
EDAM_PATH=<path to test data> python3 -m unittest edamci.EdamQueryTest.<name of test>


example:
EDAM_PATH=bad_uri_test_data.owl python3 -m unittest edamci.EdamQueryTest.test_bad_uri
