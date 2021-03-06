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


