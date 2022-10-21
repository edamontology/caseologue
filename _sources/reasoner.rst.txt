.. _reasoner:

Reasoner - ELK
=================

A **reasoner** is run on EDAM using the ROBOT `reason command <http://robot.obolibrary.org/reason>`_, which calls the `ELK reasoner <http://liveontologies.github.io/elk-reasoner/>`_.

By running ELK we validate the **semantic consistency** of the EDAM ontology by inferring logical consequences from the ontology axioms. 

Installation & Usage
---------------------

You can check out robot installation documentation  `here <http://robot.obolibrary.org/>`_. 

Once robot is installed you can run ELK with robot reason on EDAM using this command
::
    robot reason --reasoner ELK  --input <path to EDAM> -v 
