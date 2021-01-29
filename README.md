# A Multi-Dialog Conversational Approach for Service Mashup in IoT Environments

### Branches
- `master` branch is the implementation of CoMMA and was used for the user study.
- `single-utterance` branch is the baseline agent that was compared with CoMMA.
- `video-figure` branch contains the realtime visualization tool (which is named `realtime-vis.ipynb`) and the dialogflow agent file.

### Testing Environment
- Python 3.5 with Flask==1.1.2
- Valid SSL certificate is required with filename of `server.crt` and `server.key`.
- Import the agent in your dialogflow console, and configure the webhook settings.
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
