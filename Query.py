# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from SPARQLWrapper import SPARQLWrapper, JSON
from csv import writer
from urllib import unquote_plus
import argparse







def build_graph(name, source, target, query, intermediate = None):
    print "Building graph for {}.".format(name)
    

    
    sparql.setQuery(query)
    results = sparql.query().convert()
    
    edges = writer(open('{}_edges.csv'.format(name),'w'))
    edges.writerow(['Source','Target'])
    
    nodes = writer(open('{}_nodes.csv'.format(name),'w'))
    nodes.writerow(['Id','Label','Type'])

    
    for result in results["results"]["bindings"]:
        if not intermediate :
            source_binding = unquote_plus(result[source]["value"].encode('utf-8').replace('http://eligibility.data2semantics.org/resource/',''))
            target_binding = unquote_plus(result[target]["value"].encode('utf-8').replace('http://eligibility.data2semantics.org/resource/',''))
            
            edges.writerow([source_binding,target_binding])

            
            
            nodes.writerow([source_binding,source_binding,source])
            nodes.writerow([target_binding,target_binding,target])
            

        else :
            source_binding = unquote_plus(result[source]["value"].encode('utf-8').replace('http://eligibility.data2semantics.org/resource/',''))
            intermediate_binding = unquote_plus(result[intermediate]["value"].encode('utf-8').replace('http://eligibility.data2semantics.org/resource/',''))
            target_binding = unquote_plus(result[target]["value"].encode('utf-8').replace('http://eligibility.data2semantics.org/resource/',''))
            
            edges.writerow([source_binding,intermediate_binding])
            edges.writerow([intermediate_binding,target_binding])
            

            
            nodes.writerow([source_binding,source_binding,source])
            nodes.writerow([target_binding,target_binding,target])
            nodes.writerow([intermediate_binding,intermediate_binding,intermediate])
            

            
    
    print "Done"

    return

def build_eligibility_relation_graph(name,query):
    print "Building graph for {}.".format(name)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    
    results = sparql.query().convert()
    
    edges = writer(open('{}_edges.csv'.format(name),'w'))
    edges.writerow(['Source','Target'])
        
    nodes = writer(open('{}_nodes.csv'.format(name),'w'))
    nodes.writerow(['Id','Label','Type'])

    
    for result in results["results"]["bindings"]:
        t1 = unquote_plus(result["t1"]["value"].encode('utf-8').replace('http://eligibility.data2semantics.org/resource/',''))
        t2 = unquote_plus(result["t2"]["value"].encode('utf-8').replace('http://eligibility.data2semantics.org/resource/',''))
        c1 = unquote_plus(result["c1"]["value"].encode('utf-8').replace('http://eligibility.data2semantics.org/resource/',''))
        c2 = unquote_plus(result["c2"]["value"].encode('utf-8').replace('http://eligibility.data2semantics.org/resource/',''))
        concept = unquote_plus(result["concept"]["value"].encode('utf-8').replace('http://eligibility.data2semantics.org/resource/',''))
        
        edges.writerow([c1,concept])
        edges.writerow([c2,concept])
        edges.writerow([t1, c1])
        edges.writerow([t2, c2])
        edges.writerow([c1,c2,''])
        
        nodes.writerow([concept,concept,'concept'])
        nodes.writerow([c1,c1,'criterion'])
        nodes.writerow([c2,c2,'criterion'])
        nodes.writerow([t1,t1,'trial'])
        nodes.writerow([t2,t2,'trial'])

    print "Done"
    return





trial_to_criterion_q = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX etv: <http://eligibility.data2semantics.org/vocab/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>


SELECT DISTINCT ?trial ?criterion WHERE {
  ?trial etv:hasCriterion ?criterion .
  
  FILTER (?criterion != <http://eligibility.data2semantics.org/resource/-+See+._C>)
}"""

    
    
criterion_to_concept_q = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX etv: <http://eligibility.data2semantics.org/vocab/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>


SELECT DISTINCT ?criterion ?concept WHERE {
  { ?criterion etv:hasConcept ?concept . }
  UNION
  { ?criterion etv:hasContent ?content .
    ?content etv:hasConcept ?concept .}
  FILTER (?criterion != <http://eligibility.data2semantics.org/resource/-+See+._C>)
}"""


trials_q = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX etv: <http://eligibility.data2semantics.org/vocab/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>


SELECT DISTINCT ?trial WHERE {
  ?trial etv:hasCriterion ?criterion .
}"""


specific_trial_to_criterion_q = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX etv: <http://eligibility.data2semantics.org/vocab/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>


SELECT DISTINCT ?trial ?criterion ?concept WHERE {{
  <{}> etv:hasCriterion ?c .
  {{ ?c etv:hasConcept ?concept . }}
  UNION
  {{
    ?c etv:hasContent ?content1 .
    ?content1 etv:hasConcept ?concept .
  }}
  {{
    ?criterion etv:hasConcept ?concept .
    ?criterion etv:isUsedInTrial ?trial .
  }}
  UNION
  {{
    ?criterion etv:hasContent ?content2 .
    ?content2 etv:hasConcept ?concept .
    ?criterion etv:isUsedInTrial ?trial .
  }}
  FILTER (?criterion != <http://eligibility.data2semantics.org/resource/-+See+._C>)
}}"""


criteria_q = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX etv: <http://eligibility.data2semantics.org/vocab/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>


SELECT DISTINCT ?t1 ?t2 ?c1 ?c2 ?concept WHERE {{
  <{}> etv:hasCriterion ?c .
  {{ ?c etv:hasConcept ?concept . }}
  UNION
  {{
    ?c etv:hasContent ?content1 .
    ?content1 etv:hasConcept ?concept .
  }}
  ?content2 etv:hasConcept ?concept .
  ?content2 etv:isMoreStrict ?content3 .
  ?c1 etv:hasContent ?content2 .
  ?c2 etv:hasContent ?content3 .
  ?c1 etv:isUsedInTrial ?t1 .
  ?c2 etv:isUsedInTrial ?t2 .
}}"""






if __name__ == "__main__" :
    parser = argparse.ArgumentParser(description="Query for Clinical Trials & Generate Graphs")
    parser.add_argument('sparql_endpoint', type=str, nargs="?", help="URL of the SPARQL endpoint", default="http://localhost:8080/openrdf-sesame/repositories/ct")
    args = parser.parse_args()
    
    ENDPOINT = args.sparql_endpoint
    sparql = SPARQLWrapper(ENDPOINT)
    sparql.setReturnFormat(JSON)
    
    build_graph("trial_to_criterion","trial","criterion",trial_to_criterion_q)
    build_graph("criterion_to_concept","criterion","concept",criterion_to_concept_q)
    
    sparql.setQuery(trials_q)
    results = sparql.query().convert()
    
    
    for result in results["results"]["bindings"]:
        trial_uri = result['trial']['value']
        trial_file = trial_uri.replace("http://eligibility.data2semantics.org/resource/","")
        
        name = "{}_trial_to_criterion".format(trial_file)
        
        build_graph(name,"trial","concept",specific_trial_to_criterion_q.format(trial_uri),intermediate = "criterion")
        
        name = "{}_criteria_relations".format(trial_file)
        
        build_eligibility_relation_graph(name,criteria_q.format(trial_uri))




