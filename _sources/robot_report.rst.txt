.. _robot_report:

ROBOT report 
=============

General quality control for ontology is run on EDAM using the ROBOT `report command <http://robot.obolibrary.org/report>`_ from the robot suite. 
Robot report is a command line tool caling a customizable list of `SPARQL queries <http://robot.obolibrary.org/report_queries/>`_. 
Some of these queries were modified to fit the EDAM properties declaration. 

You can check out our custom selection of the robot SPARQL queries in our caseologue repository  `here <https://github.com/edamontology/caseologue/tree/main/robot>`_. 

Installation & Usage
---------------------

You can check out robot installation documentation  `here <http://robot.obolibrary.org/>`_. 

Once robot is installed you can run robot report on EDAM using this command
::
robot report --input <path to EDAM> --output <output tsv file> --profile report_queries.txt
::