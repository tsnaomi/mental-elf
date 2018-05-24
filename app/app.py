# standard
import subprocess as sp

# third-party
import click

from flask import Flask, render_template
from flask_ask import Ask, question, session, statement  # request
# from rasa_nlu.model import Interpreter  # Metadata
# from rasa_core.agent import Agent
# from rasa_core.interpreter import RasaNLUInterpreter

# local
from core import DialogueManager
from speech_assets import update_model

# app configuration -----------------------------------------------------------
app = Flask(__name__)
app.config.from_pyfile('config.py')
ask = Ask(app, '/')  # Alexa integration
dm = DialogueManager(render_template)


# RASA NLU model --------------------------------------------------------------

# model_directory_name = "../trainElfNLU/projects/default/myModel2/"
# # metadata = Metadata.load(model_directory_name)
# # interpreter = Interpreter.load(metadata,RASAConfig("config_spacy.json"))
# interpreter = Interpreter.load(model_directory_name)


# view helpers ----------------------------------------------------------------

CARD_TITLE = 'Mental Elf'


def elf_response(session, bentent, sargs):
    '''Determine the elf's response using DialogueManager.

    The dialogue manager is given the current session, intent (`bentent`), and
    slot arguments (`sargs`).
    '''
    text = dm.get_utterance(session, bentent, sargs)

    try:
        text, reprompt = text

        return question(text).simple_card(CARD_TITLE, text).reprompt(reprompt)

    except ValueError:
        return question(text).simple_card(CARD_TITLE, text)


# intents ---------------------------------------------------------------------

@ask.launch
def launch():
    text = render_template('hello')

    return question(text).simple_card(CARD_TITLE, text)


@ask.intent('GiveOverview', mapping={'condition': 'CONDITION'})
def give_overview(condition):
    ''' '''
    return elf_response(session, 'give_overview', {'condition': condition})


@ask.intent('GiveSymptoms', mapping={'condition': 'CONDITION'})
def give_symptoms(condition):
    ''' '''
    return elf_response(session, 'give_symptoms', {'condition': condition})


@ask.intent('GiveTreatment', mapping={'condition': 'CONDITION'})
def give_treatment(condition):
    ''' '''
    return elf_response(session, 'give_treatment', {'condition': condition})

@ask.intent('GiveForum', mapping={'condition': 'CONDITION'})
def give_forum(condition):

    return elf_response(session, 'give_forum', {'condition': condition})

@ask.intent('SlotFilling', mapping={'condition': 'CONDITION'})
def slot_filling(condition):

    return elf_response(session, 'slot_filling', {'condition': condition})

@ask.intent('AMAZON.HelpIntent')
def help():
    ''' '''
    return elf_response(session, 'help', {})


@ask.intent('AMAZON.StopIntent')
def stop():
    text = render_template('bye')

    return statement(text).simple_card(CARD_TITLE, text)


@ask.intent('AMAZON.CancelIntent')
def cancel():
    text = render_template('bye')

    return statement(text).simple_card(CARD_TITLE, text)

@ask.intent('AffirmativePassive')
def affirmativepassive():
    return elf_response(session, 'affirmativepassive',{})

@ask.intent('Negative')
def negative():
    return elf_response(session,'negative',{})


# @ask.intent('RawText', mapping={'text': 'Text'})
# def do_NLU(text):
#     data = request.intent.slots.Text.value
#     dic = interpreter.parse(data)
#     intent = dic['intent']['name']
#     # raw = dic['text'] #difficult - see if this matches samples, if not check
#     # which gives the highest score in entities, add to interaction model json,
#     # upload before next round, retrain nlu can add a reinforcement style
#     # strategy by asking user if returned answer was correct
#     if dic['entities']:
#         condition = str(dic['entities'][0]['value'])
#         # slottype = str(dic['entities'][0]['entity'])

#         # get disorder list for DB table, check if it exists and then proceed
#         # else return sorry, not in table, ask for another
#         print(session.attributes)
#         if intent == 'GiveOverview':
#             return give_overview(condition)
#         elif intent == 'GiveSymptoms':
#             return give_overview(condition)
#         elif intent == 'GiveTreatment':
#             return give_treatment(condition)
#         elif intent == 'GivePrevalence':
#             return give_prevalence(condition)
#     else:
#         print("unrecognized entity and slot type")
#         return statement('All your base are belong to us')


# custom CLI commands ---------------------------------------------------------

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
        update_model(filename)

    cmd = 'ask api update-model -s %s -f %s -l en-US --debug' % \
        (app.config.get('SKILL_ID'), filename)
    click.echo('Uploading %s...' % filename)

    sp.Popen(cmd.split(), stdout=sp.PIPE).communicate()


# -----------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=app.config.get('TESTING'))
