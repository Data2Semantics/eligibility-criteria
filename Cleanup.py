# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>
import re
import argparse
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean up a messy OWL file")
    parser.add_argument('filename', type=str, help="Name of the OWL file to be cleaned")
    parser.add_argument('outputfilename', type=str, nargs="?", help="Name of the file to which the cleaned up file should be written.", default="clean.owl")
    args = parser.parse_args()
    
    etfile = open(args.filename,'r')
    
    etstring = ""
    
    for l in etfile.readlines() :
        etstring += l
    
    # <codecell>
    

    
    
    
    namespaces = re.findall('ENTITY (?P<nsprefix>\w+) \"(?P<uri>.+)\" \>',etstring)
    
    for (nsprefix,uri) in namespaces :
        etstring = re.sub("&{};".format(nsprefix),uri,etstring)
        
    
        
    # <codecell>
    
    
    VOCAB_URI = "http://eligibility.data2semantics.org/vocab/"
    
    etstring = re.sub("http://www.semanticweb.org/ontologies/2011/9/LibraryOfEligibilityCriteriaTest.owl#",VOCAB_URI,etstring)
    
    
    # <codecell>
    
    RESOURCE_URI = "http://eligibility.data2semantics.org/resource/"
    etstring = re.sub('file:/.*\.owl#',RESOURCE_URI,etstring)
    
    # <codecell>
    
    etstring = re.sub('\<\!ENTITY.+\>\n','',etstring)
    etstring = re.sub('xmlns:.+?=\".+\"\n','',etstring)
    
    RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    RDFS = "http://www.w3.org/2000/01/rdf-schema#"
    OWL = "http://www.w3.org/2002/07/owl#"
    XSD = "http://www.w3.org/2001/XMLSchema#"
    
    etstring = re.sub('xmlns:.+?=\".+\"\>','xmlns:et=\"{}\" xmlns:etv=\"{}\" xmlns:rdf=\"{}\" xmlns:rdfs=\"{}\" xmlns:owl=\"{}\" xmlns:xsd=\"{}\">'.format(RESOURCE_URI,VOCAB_URI,RDF,RDFS,OWL,XSD),etstring)
    
    etstring = re.sub('LibraryOfEligibilityCriteriaTest:','etv:',etstring)
    
    # <codecell>
    print "Writing to {}".format(args.outputfilename)
    out = open(args.outputfilename,'w')
    
    out.write(etstring)
    out.close()
    print "Done!"
    
    # <codecell>


