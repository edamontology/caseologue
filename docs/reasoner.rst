.. _reasonner:

Reasoner - ELK
=================

A **reasonner** is run on EDAM using the ROBOT `reason command <http://robot.obolibrary.org/reason>`_, calling the `ELK <http://liveontologies.github.io/elk-reasoner/>`_ reasonner.

By running ELK we ensure the of **semantic consistency** the EDAM ontology by infering logical consequences from the ontology axioms. 

Installation & Usage
---------------------

You can check out robot installation documentation  `here <http://robot.obolibrary.org/>`_. 

Once robot is installed you can run ELK with robot reason on EDAM using this command
::
    robot reason --reasoner ELK  --input <path to EDAM> -v 
