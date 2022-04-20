# Run tests individually with their test data

template :\
EDAM_PATH=<_path to test data_> python3 -m unittest edamci.EdamQueryTest.<_name of test_> 


example:\
EDAM_PATH=bad_uri_test_data.owl python3 -m unittest edamci.EdamQueryTest.test_bad_uri

For description of queries, see linked tests in the documentation of edamci.py