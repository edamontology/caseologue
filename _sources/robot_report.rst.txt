.. _robot_report:

ROBOT report 
=============

**A generic ontology quality control** is run on EDAM using the ROBOT `report command <http://robot.obolibrary.org/report>`_. 
ROBOT report is a **command line tool** calling a **customizable list** of `SPARQL queries <http://robot.obolibrary.org/report_queries/>`_  that ensure **basic requirements** for all ontologies following the OBO guidelines (e.g. presence of a licence, more than one label in a entity) 
Some of these queries were modified to fit the EDAM properties declaration. 

You can check out our custom selection of the robot SPARQL queries in our caseologue repository  `here <https://github.com/edamontology/caseologue/tree/main/robot/report_queries.txt>`_.

Installation & Usage
---------------------

You can access the ROBOT installation documentation  `here <http://robot.obolibrary.org/>`_. 

Once ROBOT is installed, you can run ROBOT report on EDAM using this command
::
    ROBOT report --input <path to EDAM> --output <output tsv file> --profile report_queries.txt

This tool returns in the output tsv file a table of all the detected errors.
