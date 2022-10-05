.. caseologue documentation master file, created by
   sphinx-quickstart on Tue Sep  6 15:51:08 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Caseologue documentation
====================================================================

This tool suite tests the `EDAM ontology  <http://edamontology.org/page>`_ source code for semantic and syntactic consistancy.
`Caseologue <https://github.com/edamontology/caseologue>`_ comprises:
   * A custom version of the `ROBOT <http://robot.obolibrary.org/>`_ report query tool. 
   * ELK ontology reasoner called using the robot reson command.
   * A in house developped pyhton script to complement the above tools and further test the EDAM ontology with tailored quality checks. 

Caseologue is primarly used for continuous integration purposes in GitHub Actions worflows in our `GitHub repository <https://github.com/edamontology/edamontology>`_ and for curation purposes by the maintainer team of EDAM. 


.. image:: _static/Figure_front_page.png
  :width: 800

To understand EDAM and discover more about it's structure go and check out it's `documentation <https://edamontologydocs.readthedocs.io/en/latest/what_is_edam.html>`_. 


Summary
--------
The tools and there usage in CI workflow are further described in the pages bellow: 

.. toctree::
   :maxdepth: 1
   :numbered:
   
   caseologue_python
   reasoner
   robot_report
   workflow