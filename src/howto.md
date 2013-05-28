# Howto

### Prerequisites

* `pip install flask`
* `pip install sparqlwrapper`
* `pip install networkx`


### Running

* in `src` run `python run.py` from the command line
* Then go to `http://localhost:5000`

### Troubleshooting

* If nothing shows up in the dropdown boxes, go to <http://semweb.cs.vu.nl:8080/openrdf-workbench/repositories/ct>
* And add `eligibility-criteria.owl` to the repository

#### Plan B

* Install your own OWLIM store locally, add the `eligibility-criteria.owl` to it and set the SPARQL endpoint in `config.py`

