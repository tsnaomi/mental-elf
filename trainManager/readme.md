### required libraries
rasa core, tensorflow, keras
### training manager model
1. need trained NLU model from trainElfNLU or you can train an NLU model here itself, similar procedure as described in trainElfNLU
2. domain.yml - this is kind of a toned down version of interaction model. check the yml files to know how it is structured
3. sories.md - this tell the model how human-bot interactions happen
4. run train_init.py - this does an offline training of the model based on stories.md
5. Or you can run train_online.py - this runs an interactive training environment, run the command and you will understand
### testing the model
1. run the server in one terminal - python -m rasa_core.server -d manmodel/ -u NLUmodel/default_model/ -o out.log --port 5001
2. post a request to the server in another terminal - curl -XPOST localhost:5001/conversations/default/parse -d '{"query":"hello there"}'
3. to run the model in a python code, check app.py
### resources
[Rasa core](https://core.rasa.com/http.html) 
