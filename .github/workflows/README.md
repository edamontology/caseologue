### GitHub Actions workflows for caseologue

`build_docs.yml` : This workflow will run when a modification occurs in the docs/ folder of the caseologue.py script. A run of this workflow will trigger the update and deployment of the caseologue GitHub page documentation. 

`caseologue_python.yml`: This is a callable workflow to run the caseologue.py script, running custom SPARQL queries. This workflow cannot be run on its own as it needs to be called by another workflow. The workflow requires an ontology path as input, with optional severity levels.

`caseologue_robot_reason.yml`: This is a callable workflow to run the ELK reasoner using the ROBOT reason tool. This workflow cannot be run on its own as it needs to be called by another workflow. The workflow requires an ontology path as input.

`caseologue_robot_report.yml`: This is a callable workflow to run the generic and adapted ROBOT SPARQL queries using the ROBOT report tool. This workflow cannot be run on its own as it needs to be called by another workflow. The workflow requires an ontology path as input.

`caseologue_all_tests.yml`: This workflow runs "error", "essential" and "curation" tests. The workflow calls caseologue_python.yml, caseologue_robot_reason.yml, and caseologue_robot_report.yml and runs them on the current dev version of EDAM. The workflow can only be run manually on the GitHub Actions interface.

`caseologue_error_essential.yml`: This workflow runs "error" and "essential" level tests. The workflow calls caseologue_python.yml, caseologue_robot_reason.yml, and caseologue_robot_report.yml and runs them on the current dev version of EDAM. The workflow calls the same three workflows as caseologue_all_tests and runs them on the current dev version of EDAM. The workflow is triggered by every push on the caseologue repository, but can also be run manually on the GitHub Actions interface. 

`caseologue_curation.yml`: This workflow runs "curation" level tests. The workflow calls caseologue_python.yml, caseologue_robot_reason.yml, and caseologue_robot_report.yml and runs them on the current dev version of EDAM. The workflow can only be run manually on the GitHub Actions interface. 

`test_caseologue.yml`: This workflow runs the test_caseologue.py script in the caseologue_python/test/ folder and checks that caseologue tests catch the correct number of errors in the test data owl files. 