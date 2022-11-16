### GitHub Actions workflows for caseologue

`build_docs.yml` : will run when a modification occurs in the docs/ directpry of the caseologye.py script. It will trigger the update and deployment of the github page documentation of caseologue. 

`caseologue_python.yml`: Is a callable workflow to run the caseologue.py script, running custom SPARQL queries. It cannot be run on it's own, it needs to be called by another workflow. It requires as input the ontology path and optionnaly severity level. 

`caseologue_robot_reason.yml`: Is a callable workflow to run the ELK reasonner using the robot reason tool. It cannot be run on it's own, it needs to be called by another workflow. It requires as input the ontology path.

`caseologue_robot_report.yml`: Is a callable workflow to run the generic and adapted robot SPARQL queries using the robot report tool. It cannot be run on it's own, it needs to be called by another workflow. It requires as input the ontology path.

`caseologue_all_tests.yml`: Calls the 3 workflows above (caseologue_python.yml, caseologue_robot_reason.yml, caseologue_robot_report.yml) and run them on the current dev version of EDAM. It can only be run mannualy on the GitHub Actions interface. It runs all test including the one with a "curation" level in caseologue python. 

`caseologue_error_essential.yml`: Calls the 3 workflows above (caseologue_python.yml, caseologue_robot_reason.yml, caseologue_robot_report.yml) and run them on the current dev version of EDAM. It is triggered by every push on the caseologue repository and can be run manually on the GitHub Actions interface. For caseologue python, it only runs the test with a "error" and "essential" level. 