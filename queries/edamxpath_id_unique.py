#!/usr/bin/env python
"""EDAM XPath validator module script, striped down to only the unique id test"""

import sys
import argparse
from lxml import etree
from blessings import Terminal

# parsing and declaring namespaces...
EDAM_NS = {'owl' : 'http://www.w3.org/2002/07/owl#',
           'rdf':"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
           'rdfs':"http://www.w3.org/2000/01/rdf-schema#",
           'oboInOwl': "http://www.geneontology.org/formats/oboInOwl#",
           'eo': 'http://edamontology.org/'}

term = Terminal()


def check_unique_id(file_path):
    
    doc = etree.parse(file_path)
    all_ids = {}
    els = doc.xpath("//owl:Class[@rdf:about and starts-with(@rdf:about, 'http://edamontology.org/')]", namespaces=EDAM_NS)
    duplicate_id = []
    for element in els:
        current_id = int(element.xpath('@rdf:about', namespaces=EDAM_NS)[0].split('_')[1])
        if current_id in all_ids:
            duplicate_id.append(element.xpath('@rdf:about', namespaces=EDAM_NS)[0])
            all_ids[current_id].append(element)
        else:
            all_ids[current_id] = [element]
    return (duplicate_id)

