### required libraries - spacy, rasa nlu
____
### Training NLU model
1. configure config.json (config_spacy.json here) - this configures the training pipeline to be used
2. trainElfNLU_2.json - similar to interaction model in alexa skills, this is the data to train the NLU model
____
### training
train command - python -m rasa_nlu.train --config config_spacy.json  --data trainElfNLU_2.json --path projects/ --fixed_model_name myModel2
____
### testing
1. run server in terminal 1 - python -m rasa_nlu.server --path projects
2. In another terminal - curl -XPOST localhost:5000/parse -d '{"q":"hello there", "project": "default", "model": "myModel2"}'
____
### usage in python code 
refer app.py
___
### resources
-[Rasa NLU](https://nlu.rasa.com/http.html)
