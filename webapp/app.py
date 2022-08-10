import csv
from flask import Flask, redirect, url_for, request, render_template
import random
import nbformat

from rdflib import ConjunctiveGraph, Namespace

import requests    
from dotenv import load_dotenv 
from os import environ, path

app = Flask(__name__)

def load_edam():

    g = ConjunctiveGraph()
    g.load('https://raw.githubusercontent.com/edamontology/edamontology/main/EDAM_dev.owl', format='xml')
    g.bind('edam', Namespace('http://edamontology.org/'))
    print(str(len(g)) + ' triples in the EDAM triple store')

    g_last_stable = ConjunctiveGraph()
    g_last_stable.load('http://edamontology.org/EDAM.owl', format='xml')

    ## Build an index to retrieve term labels 
    idx_label = {}
    idx_uri = {}
    idx_query = """
    SELECT ?x ?label WHERE {
        ?x rdf:type owl:Class ; 
        rdfs:label ?label .
    }
    """
    results = g.query(idx_query)
    for r in results :
        #print(f"{r['label']} is identified in EDAM with concept {r['x']}") 
        idx_uri[str(r['x'])] = str(r['label'])
        idx_label[str(r['label'])] = str(r['x'])
    
    return (g,g_last_stable, idx_label,idx_uri)

def main_topic_children(g):

    query_children_topic= """
    SELECT DISTINCT ?uri ?label WHERE {
        ?uri rdfs:subClassOf <http://edamontology.org/topic_0003> .
        ?uri rdfs:label ?label.
    }
    
    """

    results = g.query(query_children_topic)
    for r in results:
        print(r)
    
    children_topic_query = {}
    for r in results:
        children_topic_query[str(r['label'])]=f"SELECT DISTINCT ?uri WHERE {{?uri rdfs:subClassOf+ <{str(r['uri'])}>.}}"
    
    print(children_topic_query)
    results_table= [["edam_topic", "number_chrildren"]]
    
    for label,query in children_topic_query.items():
        results = g.query(query)
        results_table.append([label,len(results)])
    print(results_table)
    
    return(results_table) #in curent 1.26 unstable version Biosciences have 70% of topic children, maybe filtre that if a concept have more than 50%, show its children instead. 

def get_edam_numbers(g):
    query_op = """
    SELECT DISTINCT ?x WHERE {
        ?x rdfs:subClassOf+ <http://edamontology.org/operation_0004> .
    }
    """
    results = g.query(query_op)
    nb_op = len(results)

    query_top = """
    SELECT DISTINCT ?x WHERE {
        ?x rdfs:subClassOf+ <http://edamontology.org/topic_0003> .
    }
    """
    results = g.query(query_top)
    nb_top = len(results)

    query_data = """
    SELECT DISTINCT ?x WHERE {
        ?x rdfs:subClassOf+ <http://edamontology.org/data_0006> .
    }
    """
    results = g.query(query_data)
    nb_data = len(results)

    query_formats = """
    SELECT DISTINCT ?x WHERE {
        ?x rdfs:subClassOf+ <http://edamontology.org/format_1915> .
    }
    """
    results = g.query(query_formats)
    nb_formats = len(results)

    return {'nb_topics': nb_top, 
            'nb_operations': nb_op, 
            'nb_data': nb_data, 
            'nb_formats': nb_formats}

def compute_repo_metadata ():
    basedir = path.abspath(path.dirname(__file__)) 
    load_dotenv(path.join(basedir, ".env")) 
    GITHUB_API_TOKEN = environ.get("GITHUB_API_TOKEN") 
    headers = {'Authorization': 'token   {}'.format(GITHUB_API_TOKEN) }

    response = requests.get('https://api.github.com/repos/edamontology/edamontology', headers=headers)
    home_page_api = response.json()
    #print(home_page_api)

    response = requests.get('https://api.github.com/repos/edamontology/edamontology/contributors', headers=headers)
    contributors_api = response.json()
    nb_contributors = len(contributors_api)
    #print(nb_contributors)
    #print(contributors_api)
    list_contributors=[]
    for c in contributors_api:
        list_contributors.append(c['login'])
    #print(list_contributors)
    #print(contributors_api[0].keys())

    for c in contributors_api:
            
        response = requests.get(c['url'], headers=headers)
        c_api = response.json()
        #print(c_api['location'])
    
    issue_contributors=[]

    for i in range(1,10): ##NOT OPTIMAL!
        response = requests.get('https://api.github.com/repos/edamontology/edamontology/issues?state=all&per_page=100&page={}'.format(i), headers=headers)
        issue_api = response.json()
        #print(len(issue_api))
        for i in issue_api:
            #print(i['number'],i['state'])
            if i['user']['login'] not in issue_contributors:
                issue_contributors.append(i['user']['login'])
    nb_issue_contributors=len(issue_contributors)
    #print(issue_contributors,len(issue_contributors))


    response = requests.get('https://api.github.com/repos/LucieLamothe/edamontology/actions/artifacts', headers=headers)
    artifacts = response.json()
    print(artifacts)

    return(nb_contributors,list_contributors,issue_contributors,nb_issue_contributors)

g,g_last_stable,idx_label,idx_uri=load_edam()

main_topic_children_table=main_topic_children(g)

edam_dev_numbers=get_edam_numbers(g)
edam_stable_numbers=get_edam_numbers(g_last_stable)

nb_contributors,list_contributors,issue_contributors,nb_issue_contributors=compute_repo_metadata()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/expert_curation')
def expert_curation():
    return render_template('index.html')


@app.route('/edam_stats')
def edam_stats():

    return render_template('stats.html', 
        topics = edam_dev_numbers['nb_topics'], 
        operations = edam_dev_numbers['nb_operations'], 
        data = edam_dev_numbers['nb_data'], 
        format = edam_dev_numbers['nb_formats'], 
        total=edam_dev_numbers['nb_formats']+edam_dev_numbers['nb_operations']+edam_dev_numbers['nb_topics']+edam_dev_numbers['nb_data'],
        new_topics = edam_dev_numbers['nb_topics'] - edam_stable_numbers['nb_topics'], 
        new_operations = edam_dev_numbers['nb_operations'] - edam_stable_numbers['nb_operations'], 
        new_data = edam_dev_numbers['nb_data'] - edam_stable_numbers['nb_data'], 
        new_formats = edam_dev_numbers['nb_formats'] - edam_stable_numbers['nb_formats'], 
        new_total=edam_dev_numbers['nb_formats'] - edam_stable_numbers['nb_formats']+edam_dev_numbers['nb_data'] - edam_stable_numbers['nb_data']+edam_dev_numbers['nb_operations'] - edam_stable_numbers['nb_operations']+edam_dev_numbers['nb_topics'] - edam_stable_numbers['nb_topics'],
        nb_contributors=nb_contributors,
        list_contributors=list_contributors,
        issue_contributors=issue_contributors,
        nb_issue_contributors=nb_issue_contributors,
        main_topic_children_table=main_topic_children_table
        )
    
@app.route('/edam_validation')
def edam_validation():
    return render_template('edam_validation.html')

@app.route('/edam_last_report')
def edam_last_report():
    number=0
    # edam ci report
    with open("test_data/output_edam-custom.tsv") as file:
        output_edam_custom = csv.DictReader(file, delimiter="\t")
        edam_custom_output_list = []
        for row in output_edam_custom:
            row["Number"]=number
            number+=1
            edam_custom_output_list.append(row)
        # robot report
    with open("test_data/report_profile.tsv") as file:
        robot_output = csv.DictReader(file, delimiter="\t")
        robot_output_list = []
        for row in robot_output:
            row["Label"]=idx_uri[row["Subject"]]
            row["Number"]=number
            number+=1
            robot_output_list.append(row)    

    return render_template('edam_last_report.html', output_edam_custom_list=edam_custom_output_list, robot_output_list=robot_output_list)

@app.route('/quick_curation')
def quick_curation():

    tests_quick_curation = ["check_wikipedia_link","identifier_property_missing","relation_too_broad","format_property_missing","deprecated_replacement_obsolete","mandatory_property_missing","deprecated_replacement","duplicate_in_concept","duplicate_all","duplicate_scoped_synonym","duplicate_definition","duplicate_label_synonym","duplicate_exact_synonym"]
    with open("test_data/output_edam-custom.tsv") as file:
        output_edam_custom = csv.DictReader(file, delimiter="\t")
        error_list = []
        for row in output_edam_custom:
            if row['Test Name'] in tests_quick_curation:
                error_list.append(row)
    with open("test_data/report_profile.tsv") as file:
        robot_output = csv.DictReader(file, delimiter="\t")
        for row in robot_output:
            row["Label"]=idx_uri[row["Subject"]]
            row["Debug Message"]=row['Rule Name']+" on value \""+row['Value']+"\""
            if row['Rule Name'] in tests_quick_curation:
                error_list.append(row) 
    if len(error_list) > 5:
        error_list = random.sample(error_list, 5)

    return render_template('quick_curation.html',
                           count_errors=len(error_list),
                           error_list = error_list)


if __name__ == "__main__":
    # context = ('myserver-dev.crt', 'myserver-dev.key')
    # app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=context)
    # context = ('myserver-dev.crt', 'myserver-dev.key')
    app.run(host='0.0.0.0', port=5000, debug=True)