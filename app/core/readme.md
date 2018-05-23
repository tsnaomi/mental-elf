# *Mental Elf* core modules

- DynamoDB integration
- Dialogue Management

____

### Dialogue Managment

Dear Team BS,

Getting started:

1. From the master branch, run `git pull -f origin master`.
2. Run `git checkout -b dialogue-manager`. Feel free to replace `dialogue-manager` with whatever you guys want to name the branch!
3. From inside the `app` directory, run `source dev.sh`, then `flask upload_model`. This will push the most recent version of the interaction model to your dev elf. 

Other notes:

- At the moment, the intents in `app.py` request response utterances from the DialogueManager via `dm.get_utterance(session, bentent, sargs)`. 
  - `get_utterance()` should always return a string (or two strings, if including a reprompt).
- In order to maintain the app's current behavior on the master branch, I mocked up the same functionality in `bs.py`. Feel free to change all of this inside the new branch!
- User `dm.render_template()` to manage response strings. This has the same functionality as the `render_template` described in the [Flask-ASK](http://flask-ask.readthedocs.io/en/latest/responses.html#jinja-templates) docs. `templates.yaml` is located in the `app` directory.

Love, N