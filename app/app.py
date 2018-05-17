# standard
import subprocess as sp

# third-party
import click

from flask import Flask, render_template
from flask_ask import Ask, question, request, session, statement
from flask_dynamo import Dynamo
from rasa_nlu.model import Metadata, Interpreter
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
#from rasa_nlu import RasaNLUConfig as RASAConfig

# local
from core import NLG
from core import db
#from speech_assets import update_model

# app configuration -----------------------------------------------------------
app = Flask(__name__)
app.config.from_pyfile('config.py')


ask = Ask(app, '/')  # Alexa integration
#db = None  # TODO: Dynamo(app)  # DynamoDB integration

#nlg = NLG(db)  # language generation module

# database --------------------------------------------------------------------

#app.config['DYNAMO_TABLES'] = [
    # INSERT SCHEMA HERE:
    # this outlines the db's structure, but does not initialize it
    # (we can optionally move this to a different file)
#]

# test NLU Model
## change to your dir paths
model_directory_name = "/home/dhanush/Workspace/spring2018/ee596/Project_repo/trainElfNLU/projects/default/myModel2/"
#metadata = Metadata.load(model_directory_name)
#interpreter = Interpreter.load(metadata,RASAConfig("config_spacy.json"))
interpreter = Interpreter.load(model_directory_name)
agent = Agent.load('/home/dhanush/Workspace/spring2018/ee596/Project_repo/trainManager/manmodel/', interpreter = interpreter)

# intents ---------------------------------------------------------------------

CARD_TITLE = 'Mental Elf'

@ask.launch
def launch():
    text = render_template('hello')
    print("hello")
    print(format)
    print(request)
    print(session.attributes)
    return question(text).simple_card(CARD_TITLE, text)

@ask.intent('GiveOverview', mapping={'condition': 'CONDITION'})
def give_overview(condition):
    try:
        # get the provided condition from the database
        condition = db.get_condition(condition)

        # here is an example of how to store information across requests
        # for a given session; when the session ends, this information will
        # go away
        session.attributes['current condition'] = condition.name

        # if the current session has yet to involve any condition overviews,
        # begin the overview with "Let's talk {{ condition }}" and, post-
        # overview, ask the user if they would like to learn more about
        # symptoms or treatments; otherwise, we can assume the user is familiar
        # with what Mental Elf can do, so we can eliminate this chit chat
        if session.attributes.get('overview given'):
            text = condition.overview

        else:
            text = render_template(
                'first_overview',
                condition=condition.name,
                overview=condition.overview,
                )

            # here is an example of how to store information across requests
            # for a given session; when the session ends, this information will
            # go away
            session.attributes['overview given'] = True

    # if there was no matching condition in the database, say so
    except ValueError:
        text = render_template('no_condition')
    print(session.attributes) 
    print(session)
#    text = render_template('overview', condition=condition)
#    print(request)
    return question(text).simple_card(CARD_TITLE, text)

@ask.intent('GiveSymptoms', mapping={'condition': 'CONDITION'})
def give_symptoms(condition):
    text = render_template('symptoms', condition=condition)
    return question(text).simple_card(CARD_TITLE, text)

@ask.intent('GiveTreatment', mapping={'condition': 'CONDITION'})
def give_treatment(condition):
    text = render_template('treatment', condition=condition)
    return question(text).simple_card(CARD_TITLE, text)

@ask.intent('GivePrevalence', mapping={'condition': 'CONDITION'})
def give_prevalence(condition):
    text = render_template('prevalence', condition=condition)
    return question(text).simple_card(CARD_TITLE, text)

@ask.intent('RawText', mapping={'text':'Text'})
def do_NLU(text):
	data = request.intent.slots.Text.value
	dic = interpreter.parse(data)
	#print(dic)
	intent = dic['intent']['name']
	raw = dic['text'] #difficult - see if this matches samples, if not check which gives the highest score in entities, add to interaction model json, upload before next round, retrain nlu can add a reinforcement style strategy by asking user if returned answer was correct
	if dic['entities']:
		condition = str(dic['entities'][0]['value'])
		slottype =  str(dic['entities'][0]['entity'])
		msg = agent.handle_message(raw)
		print(msg)	
		# get disorder list for DB table, check if it exists and then proceed
		# else return sorry, not in table, ask for another
		print(session.attributes)
		if intent == 'GiveOverview':
			return give_overview(condition)
		elif intent == 'GiveSymptoms':
			return give_overview(condition)
		elif intent == 'GiveTreatment':
			return give_treatment(condition)
		elif intent == 'GivePrevalence':
			return give_prevalence(condition)
	else:
		print("unrecognized entity and slot type")
		return statement('All your base are belong to us')	


@ask.intent('AMAZON.HelpIntent')
def help():
    text = render_template('help')

    return question(text).simple_card(CARD_TITLE, text).reprompt(text)


@ask.intent('AMAZON.StopIntent')
def stop():
    text = render_template('bye')

    return statement(text).simple_card(CARD_TITLE, text)


@ask.intent('AMAZON.CancelIntent')
def cancel():
    text = render_template('bye')

    return statement(text).simple_card(CARD_TITLE, text)


# custom CLI commands ---------------------------------------------------------

@app.cli.command()
def initdb():
    '''Create the tables on DynamoDB.'''
    db.create_all()
    click.echo('Database initialized.\n\t--Mental Elf')


@app.cli.command()
def dropdb():
    '''Delete the tables on DynamoDB.'''
    db.destroy_all()
    click.echo('Database bye bye.\n\t--Mental Elf')


@app.cli.command()
@click.option('--filename', default='./speech_assets/InteractionModel.json')
@click.option('--update', is_flag=True)
def upload_model(filename, update):
    '''Upload the interaction model (after optionally updating it).

    Usages:
        `flask upload_model`
        `flask upload_model --update`
        `flask upload_model --filename MODEL_FN`
    '''
    if update:
        click.echo('Updating model...')
        #update_model(filename)
        # TODO: update interaction model

    cmd = 'ask api update-model -s %s -f %s -l en-US --debug' % \
        (app.config.get('SKILL_ID'), filename)
    click.echo('Uploading %s...' % filename)
    sp.Popen(cmd.split(), stdout=sp.PIPE).communicate()


# -----------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=app.config.get('TESTING'))
