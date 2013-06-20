#!/usr/bin/env python


from flask import render_template, g, request, jsonify
import util.sparql as s
from bs4 import BeautifulSoup
import requests

from app import app

@app.route('/')
def index():
    
    trials = s.get_trials()
    criteria = s.get_criteria()
    concepts = s.get_concepts()
    
    return render_template('base.html', trials = trials, criteria = criteria, concepts = concepts)


@app.route('/graph', methods= ['GET'])
def graph():
    graph_type = request.args.get('type','')
    
    if graph_type == 'trials':
        trial_uri = request.args.get('uri','')
        trial_id = request.args.get('id','')
        
        if trial_uri == '' :
            return 'Nada'
        else :
            graph = s.build_trial_to_criterion_graph(trial_uri, trial_id)
        
        return jsonify(graph = graph)
    
    elif graph_type == 'criteria' :
        criterion_uri = request.args.get('uri','')
        
        if criterion_uri == '':
            return 'Rien'
        else :
            graph = s.build_pi_graph(criterion_uri)
            
        return jsonify(graph=graph)
    
    elif graph_type == 'concepts' :
        concept_uri = request.args.get('uri','')
        
        if concept_uri == '':
            return 'Niente'
        else :
            matrix, concepts = s.build_concept_matrix(concept_uri)
            
        return jsonify(matrix=matrix, concepts=concepts)
        
    
    return "Nothing! Oops"

@app.route('/editor')
def editor():
    patterns = s.get_patterns()
    
    return render_template('editor.html', patterns = patterns)
    
    
@app.route('/patternvalues')
def patternvalues():
    concepts = s.get_concepts()
    values = s.get_values()
    
    options = []
    options.extend(concepts)
    options.extend(values)
    
    values = []
    for o in options:
        v = {'id' : o['uri'], 'text': o['label']}
        values.append(v)
           
    
    return jsonify(values = values)

@app.route('/patterninstances', methods= ['GET'])
def patterninstances():
    pattern_uri = request.args.get('uri','')
    pattern_instances =  s.get_pattern_instances(pattern_uri)
    
    return jsonify(instances = pattern_instances)


@app.route('/trialtable', methods= ['GET'])
def trialtable():
    trial_id = request.args.get('trial','')
    
    url = "http://clinicaltrials.gov/ct2/show/record/{}".format(trial_id)
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content)

    content = soup.find(id='main-content')
    
    return unicode(content)
