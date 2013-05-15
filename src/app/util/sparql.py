#!/usr/bin/env python

from SPARQLWrapper import SPARQLWrapper, JSON
from flask import render_template
import re
from urllib import unquote_plus
import networkx as nx
from networkx.readwrite import json_graph
import json

from app import app

endpoint = app.config['SPARQL_ENDPOINT']

sparql = SPARQLWrapper(endpoint)
sparql.setReturnFormat(JSON)


concept_type_color_dict = {'popg': '#9edae5', 'inpo': '#ffbb78', 'elii': '#dbdb8d', 'idcn': '#9edae5', 'neop': '#2ca02c', 'vita': '#9467bd', 'inpr': '#c5b0d5', 'phsu': '#c5b0d5', 'blor': '#98df8a', 'hops': '#c7c7c7', 'menp': '#f7b6d2', 'phsf': '#d62728', 'ftcn': '#e377c2', 'anim': '#ff9896', 'food': '#bcbd22', 'grpa': '#ffbb78', 'geoa': '#2ca02c', 'hcpp': '#98df8a', 'lbtr': '#c7c7c7', 'ocdi': '#17becf', 'tisu': '#17becf', 'orch': '#7f7f7f', 'tmco': '#dbdb8d', 'clas': '#bcbd22', 'lipd': '#c49c94', 'dsyn': '#f7b6d2', 'horm': '#aec7e8', 'bact': '#2ca02c', 'grup': '#e377c2', 'bacs': '#ffbb78', 'enty': '#c5b0d5', 'resa': '#98df8a', 'medd': '#9467bd', 'cell': '#bcbd22', 'fndg': '#ff7f0e', 'sbst': '#ff9896', 'prog': '#ff9896', 'celf': '#aec7e8', 'chvf': '#1f77b4', 'diap': '#aec7e8', 'celc': '#8c564b', 'hcro': '#ff7f0e', 'inbe': '#9467bd', 'clna': '#ffbb78', 'acab': '#d62728', 'bodm': '#9467bd', 'patf': '#e377c2', 'carb': '#c7c7c7', 'bpoc': '#d62728', 'dora': '#8c564b', 'moft': '#7f7f7f', 'plnt': '#7f7f7f', 'ortf': '#f7b6d2', 'bmod': '#9edae5', 'sosy': '#dbdb8d', 'enzy': '#d62728', 'qnco': '#1f77b4', 'imft': '#7f7f7f', 'antb': '#1f77b4', 'bdsy': '#c5b0d5', 'nnon': '#9467bd', 'socb': '#c49c94', 'ocac': '#8c564b', 'bdsu': '#8c564b', 'rcpt': '#ff9896', 'nsba': '#c5b0d5', 'mnob': '#e377c2', 'orga': '#1f77b4', 'orgf': '#c7c7c7', 'lbpr': '#d62728', 'orgt': '#aec7e8', 'gngm': '#f7b6d2', 'virs': '#17becf', 'fngs': '#98df8a', 'aapp': '#17becf', 'opco': '#c49c94', 'irda': '#98df8a', 'famg': '#2ca02c', 'acty': '#ff7f0e', 'inch': '#bcbd22', 'cnce': '#9edae5', 'topp': '#ffbb78', 'spco': '#2ca02c', 'lang': '#dbdb8d', 'podg': '#aec7e8', 'mobd': '#ff9896', 'qlco': '#c49c94', 'npop': '#ff7f0e', 'hlca': '#1f77b4', 'phpr': '#ff7f0e', 'strd': '#8c564b'}


def uri_to_label(uri):
    return unquote_plus(uri.encode('utf-8').replace('http://eligibility.data2semantics.org/resource/','')).replace('_',' ').lstrip('-').lstrip(' ').title()


def get_trials():
    q = render_template('trials.q')
    
    sparql.setQuery(q)

    results = sparql.query().convert()
    
    trials = []
    
    for result in results["results"]["bindings"]:
        trial_uri = result['trial']['value']
        
        m = re.search('.*(?P<id>NCT\d+).*',trial_uri)
        
        if m :
            trial_id = m.group('id')
        else :
            trial_id = trial_uri
            
        trials.append({'uri': trial_uri, 'id': trial_id})
        
    return trials
        
    
def get_criteria():
    q = render_template('criteria.q')
    
    sparql.setQuery(q)
    
    
    results = sparql.query().convert()
    
    criteria = []
    
    for result in results["results"]["bindings"]:
        criterion_uri = result['criterion']['value']
        criterion_text = result['text']['value']

            
        criteria.append({'uri': criterion_uri, 'text': criterion_text})
        
        
    return criteria

    
    
def get_concepts():
    q = render_template('concepts.q')
    
    sparql.setQuery(q)
    
    
    results = sparql.query().convert()
    
    concepts = []
    
    for result in results["results"]["bindings"]:
        concept_uri = result['concept']['value']
        concept_label = uri_to_label(concept_uri)
            
        concepts.append({'uri': concept_uri, 'label': concept_label})
        
        
    return concepts






def build_graph(G, name, source, target, query, intermediate = None):
    #print "Building graph for {}.".format(name)
    
    #print query
    
    sparql.setQuery(query)
    results = sparql.query().convert()


    
    
    
    for result in results["results"]["bindings"]:
        if not intermediate :
            source_binding = uri_to_label(result[source]["value"]).replace("'","")
            target_binding = uri_to_label(result[target]["value"]).replace("'","")
            
            
            G.add_node(source_binding, label=source_binding, type=source)
            G.add_node(target_binding, label=target_binding, type=target)
            G.add_edge(source_binding,target_binding)
            
            
            

        else :
            source_binding = uri_to_label(result[source]["value"]).replace("'","")
            intermediate_binding = uri_to_label(result[intermediate]["value"]).replace("'","")
            target_binding = uri_to_label(result[target]["value"]).replace("'","")
            
            G.add_node(source_binding, label=source_binding, type=source)
            G.add_node(intermediate_binding, label=intermediate_binding, type=intermediate)
            G.add_node(target_binding, label=target_binding, type=target)
            
            G.add_edge(source_binding, intermediate_binding)
            G.add_edge(intermediate_binding, target_binding)

    #print "Done"

    return G


def build_trial_to_criterion_graph(trial_uri, trial_id):
    G = nx.Graph()
    
    q = render_template('specific_trial_to_criterion.q', trial_uri = trial_uri)
    
    G = build_graph(G, trial_uri, "trial", "concept", q, intermediate = "criterion")
    
    origin_node_id = "Trial{}".format(trial_id.lower())
    
    G.node[origin_node_id]['type'] = 'origin'
    
    deg = nx.degree(G)
    nx.set_node_attributes(G,'degree',deg)
    
    
    g_json = json_graph.node_link_data(G) # node-link format to serialize
    
    graph_json =  json.dumps(g_json)

    return graph_json


def build_pi_graph(criterion_uri):
    G = nx.DiGraph()
    
    q_up = render_template('pi_to_pi_upwards.q', criterion_uri = criterion_uri)
    q_down = render_template('pi_to_pi_downwards.q', criterion_uri = criterion_uri)
    G = build_graph(G, criterion_uri, "child", "trial", q_up, intermediate = "parent")
    G = build_graph(G, criterion_uri, "parent", "trial", q_down, intermediate = "child")
    
    deg = nx.degree(G)
    
    ndeg = {}
    
    for k,v in deg.items():
        ndeg[k] = v*8
    
    
    nx.set_node_attributes(G,'degree', ndeg)
    
    
    g_json = json_graph.node_link_data(G) # node-link format to serialize
    
    graph_json =  json.dumps(g_json)

    return graph_json


def build_concept_matrix(concept_uri):
    q = render_template('concept_to_concept.q', concept_uri = concept_uri)
    
    sparql.setQuery(q)

    results = sparql.query().convert()
    
    concept_mapping = {}
    
    concept_set = set()
    
    concept_types = {}
    
    for result in results["results"]["bindings"]:
        c1 = uri_to_label(result['c1']['value'])
        c1t = uri_to_label(result['c1t']['value'])
        c2 = uri_to_label(result['c2']['value'])
        c2t = uri_to_label(result['c2t']['value'])
        
        
        # Add the mapping between c1 and c2 in both directions 
        concept_mapping.setdefault(c1,{}).setdefault(c2,0)
        concept_mapping.setdefault(c2,{}).setdefault(c1,0)
        
        concept_mapping[c1][c2] += 1
        concept_mapping[c2][c1] += 1
        
        concept_set.add(c1)
        concept_set.add(c2)
        
        concept_types[c1] = c1t
        concept_types[c2] = c2t
        
    

    
    
    concepts = list(concept_set)
    
    concept_matrix = range(0,len(concepts))
    
    total = 0
    for c1 in concepts:
        concept_row = range(0,len(concepts))
        
        for c2 in concepts:
            if c2 in concept_mapping[c1]:
                concept_row[concepts.index(c2)] = concept_mapping[c1][c2]
                total += concept_mapping[c1][c2]
            else :
                concept_row[concepts.index(c2)] = 0

        concept_matrix[concepts.index(c1)] = concept_row
    
    percent_concept_matrix = range(0, len(concepts))
    
    i = 0
    for row in concept_matrix :
        
        percent_concept_row = range(0, len(concepts))
        
        j = 0 
        for cell in row :
            percent_concept_row[j] = float(cell)/float(total)
            
            j += 1
            
        percent_concept_matrix[i] = percent_concept_row
            
        i += 1
    
    
    concept_dictionary = {}
    
    concept_list = []
    
    for c in concepts :
        c_dict = {'name': c.replace("'",""), 'type': concept_types[c].lower(), 'color': concept_type_color_dict[concept_types[c].lower()] }
        concept_list.append(c_dict) 
    
    
    percent_concept_matrix_json = json.dumps(percent_concept_matrix)
    concept_list_json = json.dumps(concept_list)
    
    
    return percent_concept_matrix_json, concept_list_json
    
    

    

