# edamci
CI python tool for the Edam Ontology

EDAM_PATH=../edamontology/EDAM_dev.owl python3 -m unittest edamci.py

error=False EDAM_PATH=../edamontology/EDAM_dev.owl python3 -m unittest edamci_envarg.py


EDAM_PATH=../edamontology/EDAM_dev.owl python3 edamci_testsuite.py

Pour ne lancer qu'un seul test contenu dans la classe EdamQueryTest
EDAM_PATH=../edamontology/EDAM_dev.owl python3 -m unittest edamci.EdamQueryTest.test_deprecated_replacement_obsolete
