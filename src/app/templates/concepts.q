PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX etv: <http://eligibility.data2semantics.org/vocab/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>


SELECT DISTINCT ?concept WHERE {
  ?concept rdf:type etv:Concept .
  ?concept etv:hasSemanticType ?st .
  
  FILTER (?st != <http://eligibility.data2semantics.org/resource/qnco>)
  FILTER (?st != <http://eligibility.data2semantics.org/resource/resa>)
  FILTER (?st != <http://eligibility.data2semantics.org/resource/ftcn>)
} ORDER BY ?concept