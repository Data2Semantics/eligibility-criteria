#!/usr/bin/env python


from flask import render_template, g, request, jsonify
import util.sparql as s
from bs4 import BeautifulSoup
import requests
import os
import os.path
from datetime import datetime

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
    
@app.route('/savetrial', methods=['POST'])
def savetrial():
    print request.json
    
    patterns = request.json['patterns']
    trial = request.json['trial']
    
    trial_rdf = s.build_trial_rdf(trial, patterns)
    
    trial_output_path = app.config['TRIAL_OUTPUT_PATH']
    
    print "Checking if directory exists:", trial_output_path
    if not os.path.exists(trial_output_path):
        print "Creating", trial_output_path
        os.makedirs(trial_output_path)
        print "Created"
        
    now = datetime.now()
    
    trial_file = open('{}/{}_{}.ttl'.format(trial_output_path,trial, now.isoformat('T')),'w')

    trial_file.write(trial_rdf)
    
    trial_file.close()
    
    print "Written RDF to", trial_file.name
    
    return 'Success!'



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



@app.route('/experiment2')
def experi():
    patterns = s.get_patterns()
    
    return render_template('experiment2.html')


@app.route('/saveevaluation', methods=['POST'])
def saveevaluation():
    print "??"
    #print request.json
    
    
    result = request.json['evaluation']
    eval_output_path = app.config['EVALUATION_OUTPUT_PATH']
    
    print "Checking if directory exists:", eval_output_path
    if not os.path.exists(eval_output_path):
        print "Creating", eval_output_path
        os.makedirs(eval_output_path)
        print "Created"
        
    now = datetime.now()
    
    eval_file = open('{}/{}.txt'.format(eval_output_path, now.isoformat('T')),'w')

    s = str(result)
    eval_file.write(s)
    
    eval_file.close()
    
    print "Written txt to", eval_file.name 
    
    return 'Success!'

