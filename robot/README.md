## dowlload .jar file 
wget https://github.com/ontodev/robot/releases/download/v1.8.1/robot.jar
-P /usr/local/bin
## download shell script wrapper 
curl https://raw.githubusercontent.com/ontodev/robot/master/bin/robot >
/usr/local/bin/robot

## Launch reasonner 
```
robot reason --reasoner ELK   --input <_path to EDAM_>
```
or
```
java -jar robot.jar reason --reasoner ELK   --input <_path to EDAM_>
```

## Launch custom robot report (sparql queries)
```
robot report --input <_path to EDAM_> --output report_profile.tsv --profile report_queries.txt
```
or
```
java -jar robot.jar report --input <_path to EDAM_> --output report_profile.tsv --profile report_queries.txt
```
## Queries documentation 

http://robot.obolibrary.org/report_queries/ 

## Report configuration files:

 - report_queries_old.txt = initial configuration file with all tests available in robot useful for EDAM (some bein quickly modified to fit EDAM property deifnitions)
 - report_queries_no_redundancy.txt = configuration file where only the tests that are not redundant with caseologue.py custom tool are kept. 
 - report_queries.txt = curent used file (as of 18th may 2022) with some redundancy with caseologue.py (while some of the tests are still in "curation" mode due to too many raised errors). 
