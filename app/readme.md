# *Mental Elf* web app

Welcome to the Mental Elf Flask app!

____

### Getting started

- Install the latest Python packages: `pip install -r requirements.txt`
  - This requires pip version 9.0.3, so type `pip -V` to check your pip version. If you have a never version of pip, run `pip install pip==9.0.3` inside your project's activated virtualenv to downgrade pip.
- Install ASK CLI: `npm install -g ask-cli` or `sudo npm install -g ask-cli`
- Initialize ASK CLI: `ask init`
- Go into your Alexa Skills Kit console and create a Mental Elf Dev skill (henceforth, dev-elf). This skill will only be used when *you* work on the project *locally*.
- Place `config.py` and `dev.sh` inside your project's `app` directory. *Never* commit these files.
  - In `config.py`, fill in `SKILL_ID` with your dev-elf's skill ID.
  - No need to change anything in `dev.sh` (yet).
- Watch [this video](https://www.youtube.com/watch?v=cXL8FDUag-s&feature=youtu.be) and learn how to set up **ngrok** with the Alexa Skills Kit. Don't worry about the other stuff in the video.

### Running the web app locally

Inside the `app` directory:

1. Run `source dev.sh` to imbue your environment with the necessary variables.
   - Do this in any terminal window in which you'd like to interact with the web app.
2. <u>If it is your first time serving the web app locally</u>, run `flask upload_model`
3. In a separate terminal window, run `./ngrok http 5000` and use the given HTTPS url as dev-elf's endpoint in the Alexa Skills Kit console.
4. Run `flask run` to start the web server locally. *Voila!* Now you can test out Mental Elf in the Alexa Skills Kit console.

____

### Commands

- Upload the interaction model: `flask upload_model`
  - Upload the interaction model by filename: `flask upload_model --filename MODEL_FN`
  - Update the model before uploading it: `flask upload_model —update`
    - NOT IMPLEMENTED YET
- Create the database tables: `flask initdb`
  - ***Warning***: This will initialize the remote database that everyone shares! <u>Don't do this willy-nilly</u>.
  - NOT IMPLEMENTED YET
- Drop/delete the database tables: `flask dropdb`
  - ***Warning***: This will delete the remote database that everyone shares! <u>Don't do this willy-nilly</u>.
  - NOT IMPLEMENTED YET
____

### Documentation + resources

#### Alexa + AWS

- [Alexa Skills Kit](https://developer.amazon.com/docs/ask-overviews/build-skills-with-the-alexa-skills-kit.html)
- [ASK CLI Command Reference](https://developer.amazon.com/docs/smapi/ask-cli-command-reference.html) (see `update-model`)

#### Flask

- [Flask](http://flask.pocoo.org/) (a Python micro-framework)
  - [Flask CLI](http://flask.pocoo.org/docs/0.12/cli/)
- [Flask-Ask](http://flask-ask.readthedocs.io/en/latest/index.html) (Alexa integration)
  - [Sample Flask-Ask apps](https://github.com/johnwheeler/flask-ask/tree/master/samples)
    - ***NB***: The structure of the files in *speech_assets* is outdated.
- [Flask-Dynamo](https://flask-dynamo.readthedocs.io/en/latest/index.html) (DynamoDB integration)
- [Jinja2 templating language ](http://jinja.pocoo.org/docs/2.10/) (for `templates.yml`)

#### EC2 alternatives

- [Zappa](https://www.zappa.io/) (server-less Lambda-based Python web services)
- [Heroku](https://www.heroku.com/) (cloud platform for web services)

#### Tutorials

- [Deploy Flask-Ask app on AWS Lambda with Zappa](https://developer.amazon.com/blogs/post/8e8ad73a-99e9-4c0f-a7b3-60f92287b0bf/New-Alexa-Tutorial-Deploy-Flask-Ask-Skills-to-AWS-Lambda-with-Zappa)
- [Deploy Flask app on AWS EC2](https://www.codementor.io/dushyantbgs/deploying-a-flask-application-to-aws-gnva38cf0)

#### Hao's repos

- [Lab 1](https://github.com/hao-fang/ee596_spr2018_lab1)
- [Lab 2](https://github.com/hao-fang/ee596_spr2018_lab2)
