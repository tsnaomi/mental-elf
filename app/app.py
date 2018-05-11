# standard
import subprocess as sp

# third-party
import click

from flask import Flask, render_template
from flask_ask import Ask, question, request, session, statement
from flask_dynamo import Dynamo

# local
from core import NLG
from speech_assets import update_model


# app configuration -----------------------------------------------------------

app = Flask(__name__)
app.config.from_pyfile('config.py')

ask = Ask(app, '/')  # Alexa integration
db = None  # TODO: Dynamo(app)  # DynamoDB integration

nlg = NLG(db)  # language generation module

# database --------------------------------------------------------------------

app.config['DYNAMO_TABLES'] = [
    # INSERT SCHEMA HERE:
    # this outlines the db's structure, but does not initialize it
    # (we can optionally move this to a different file)
]


# intents ---------------------------------------------------------------------

CARD_TITLE = 'Mental Elf'


@ask.launch
def launch():
    text = render_template('hello')

    return question(text).simple_card(CARD_TITLE, text)


@ask.intent('GiveOverview', mapping={'condition': 'CONDITION'})
def give_overview(condition):
    text = render_template('overview', condition=condition)

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
        update_model(filename)

    cmd = 'ask api update-model -s %s -f %s -l en-US --debug' % \
        (app.config.get('SKILL_ID'), filename)
    click.echo('Uploading %s...' % filename)

    sp.Popen(cmd.split(), stdout=sp.PIPE).communicate()


# -----------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=app.config.get('TESTING'))
