import csv
from flask import Flask, redirect, url_for, request, render_template
import random
import nbformat

from rdflib import ConjunctiveGraph, Namespace

import requests

app = Flask(__name__)

ns = {"dc": "http://dcterms/",
      "edam": "http://edamontology.org/",
      "owl": "http://www.w3.org/2002/07/owl#"
      }

g = ConjunctiveGraph()
g.load('https://raw.githubusercontent.com/edamontology/edamontology/master/EDAM_dev.owl', format='xml')
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/expert_curation')
def expert_curation():
    return render_template('index.html')

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


@app.route('/edam_stats')
def edam_stats():

    data = {
        'ontology1url': 'https://edamontology.org/EDAM.owl',
        'ontology2url': 'https://raw.githubusercontent.com/edamontology/edamontology/main/EDAM_dev.owl',
        'modifiedClasses': 'on',
        'newClasses': 'on',
        'deletedClasses': 'on',
    }

    response = requests.post('http://www.ebi.ac.uk/efo/bubastis/BubastisDiffResults', data=data)
    print(response.url)

    res = get_edam_numbers(g)
    res_last = get_edam_numbers(g_last_stable)

    return render_template('stats.html', 
        topics = res['nb_topics'], 
        operations = res['nb_operations'], 
        data = res['nb_data'], 
        format = res['nb_formats'], 
        new_topics = res['nb_topics'] - res_last['nb_topics'], 
        new_operations = res['nb_operations'] - res_last['nb_operations'], 
        new_data = res['nb_data'] - res_last['nb_data'], 
        new_formats = res['nb_formats'] - res_last['nb_formats'], 
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
    # with open("test_data/output_edam-custom.tsv") as file:
    #     output_edam_custom = csv.DictReader(file, delimiter="\t")
    error_list = []
    #     for row in output_edam_custom:
    #         if row['Test Name'] in tests_quick_curation:
    #             error_list.append(row)
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