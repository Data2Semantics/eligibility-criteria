PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX etv: <http://eligibility.data2semantics.org/vocab/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>


SELECT DISTINCT ?criterion ?text WHERE {
  ?criterion rdf:type etv:Criterion .
  ?criterion etv:hasOriginalText ?text .
} ORDER BY ?criterion