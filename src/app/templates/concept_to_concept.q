PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX etv: <http://eligibility.data2semantics.org/vocab/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>


SELECT DISTINCT ?c1 ?c1t ?c2 ?c2t ?trial WHERE {

  { ?c etv:hasConcept <{{ concept_uri }}> . }
  UNION
  {
    ?c etv:hasContent ?content1 .
    ?content1 etv:hasConcept <{{ concept_uri }}> .
  }

  ?trial etv:hasCriterion ?c . 
  
  {
    ?criterion etv:hasConcept ?c1 .
    ?criterion etv:hasConcept ?c2 . 
    ?criterion etv:isUsedInTrial ?trial .
  }
  UNION
  {
    ?criterion etv:hasConcept ?c1 .
    ?criterion etv:hasContent ?content2 .
    ?content2 etv:hasConcept ?c2 .
    ?criterion etv:isUsedInTrial ?trial .
  }
  UNION
  {
    ?criterion etv:hasContent ?content2 .
    ?content2 etv:hasConcept ?c1 .
    ?criterion etv:hasContent ?content3 .
    ?content2 etv:hasConcept ?c2 .
    ?criterion etv:isUsedInTrial ?trial .
  }
  ?c1 etv:hasSemanticType ?c1t .
  ?c2 etv:hasSemanticType ?c2t .

  FILTER (?c1 != ?c2 )
  FILTER (?criterion != <http://eligibility.data2semantics.org/resource/-+See+._C>)
}