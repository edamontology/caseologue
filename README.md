# edamci
CI python tool for the Edam Ontology. Test for continuous integration (inmplemented in GitHub Actions, triggered pu Pull Requests) and curation.

run edamci (replace the edampath):
```
EDAM_PATH=../edamontology/EDAM_dev.owl python3 edamci.py 
```

Options:\
  -e, --error      runs all error tests\
  -E, --essential  runs all essential tests\
  -c, --curation   runs all curation tests


> Documentation using docstrinf for each tests: xxxxxxxxxxx\

Install requirements:\
pip install -r requirements.txt
