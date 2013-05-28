PREFIX  res:  <http://dbpedia.org/resource/>
PREFIX  rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX etv: <http://eligibility.data2semantics.org/vocab/>
    
SELECT ?instance WHERE {
  ?instance rdf:type <{{ pattern_uri }}> .
}