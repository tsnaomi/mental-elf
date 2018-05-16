# standard
import subprocess as sp

# third-party
import click

from flask import Flask, render_template
from flask_ask import Ask, question, session, statement

# local
from core import db  # NLG
from speech_assets import update_model


# app configuration -----------------------------------------------------------

app = Flask(__name__)
app.config.from_pyfile('config.py')
ask = Ask(app, '/')  # Alexa integration
# nlg = NLG(db)  # language generation module


# intents ---------------------------------------------------------------------

CARD_TITLE = 'Mental Elf'


@ask.launch
def launch():
    text = render_template('hello')

    return question(text).simple_card(CARD_TITLE, text)


# TODO: We should handle cases where CONDITION comes in as empty/None (e.g.,
# try asking Mental Elf about "binge-eating")
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
