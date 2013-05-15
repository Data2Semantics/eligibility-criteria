PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX etv: <http://eligibility.data2semantics.org/vocab/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>


SELECT DISTINCT ?trial ?criterion ?concept WHERE {
  <{{ trial_uri }}> etv:hasCriterion ?c .
  { ?c etv:hasConcept ?concept . }
  UNION
  {
    ?c etv:hasContent ?content1 .
    ?content1 etv:hasConcept ?concept .
  }
  {
    ?criterion etv:hasConcept ?concept .
    ?criterion etv:isUsedInTrial ?trial .
  }
  UNION
  {
    ?criterion etv:hasContent ?content2 .
    ?content2 etv:hasConcept ?concept .
    ?criterion etv:isUsedInTrial ?trial .
  }
  ?concept etv:hasSemanticType ?st .
  FILTER (?criterion != <http://eligibility.data2semantics.org/resource/-+See+._C>)
  
  FILTER (?st != <http://eligibility.data2semantics.org/resource/qnco>)
  FILTER (?st != <http://eligibility.data2semantics.org/resource/resa>)
  FILTER (?st != <http://eligibility.data2semantics.org/resource/ftcn>)

  
}