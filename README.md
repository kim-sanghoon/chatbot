# A Multi-Dialog Conversational Approach for Feature-Rich Services Mashup in IoT Environments

### Testing Environment
- Python 3.5 with Flask==1.1.2
- Valid SSL certificate is required with filename of `server.crt` and `server.key`.
- Simply `sudo ./app.py` from your local environment.

### Descriptions
- `app.py` : Webhook responses management.
- `mashup.py` : Class definitions for mashup and each service.
- `identifier2ont.py` : Converting user utterance to corresponding ontology definition.
- `ont2nl.py` : Converting ontology definition to corresponding natural langauge.

### Functionality Tests
- `mashup-test-generate.ipynb` : Test if the mashup is properly generated from the dump interaction file.
- `mashup-test-merge.ipynb` : (Deprecated) Test if two mashup with the same trigger is properly merged.
- `mashup-test-speak.ipynb` : Test if the description for a mashup is properly generated from the dump interaction file.
