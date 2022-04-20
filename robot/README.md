# dowlload .jar file 
wget https://github.com/ontodev/robot/releases/download/v1.8.1/robot.jar
-P /usr/local/bin
# download shell script wrapper 
curl https://raw.githubusercontent.com/ontodev/robot/master/bin/robot >
/usr/local/bin/robot

# Launch reasonner 
robot reason --reasoner ELK   --input <_path to EDAM_>


# Launch custom robot report (sparql queries)
robot report --input <_path to EDAM_> --output report_profile.tsv --profile report_queries.txt


# Queries ducumentation 

http://robot.obolibrary.org/report_queries/ 