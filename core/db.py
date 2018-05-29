import random

import Boto_Flask_Lib as db

from boto3.dynamodb.conditions import Attr


# the "Conditions" and "Anecdote" tables on DynamoDB
Conditions = db.Open_DynamoDB('Conditions')
Anecdotes = db.Open_DynamoDB('Anecdotes')

DIRTY_DICT = {
    'a. s. d.': 'autism',
    'a.s.d.': 'autism',
    'asd': 'autism',
    'a s d': 'autism',
    's. a. d.': 'seasonal affective disorder',
    's.a.d.': 'seasonal affective disorder',
    's a d': 'seasonal affective disorder',
    'sad': 'seasonal affective disorder',
    'p. t. s. d.': 'posttraumatic stress disorder',
    'p.t.s.d.': 'posttraumatic stress disorder',
    'ptsd': 'posttraumatic stress disorder',
    'p t s d': 'posttraumatic stress disorder',
    'o. c. d.': 'obsessive compulsive disorder',
    'o.c.d.': 'obsessive compulsive disorder',
    'ocd': 'obsessive compulsive disorder',
    'o c d': 'obsessive compulsive disorder',
    'a. d. h. d.': 'attention deficit hyperactivity disorder',
    'a.d.h.d.': 'attention deficit hyperactivity disorder',
    'adhd': 'attention deficit hyperactivity disorder',
    'a d h d': 'attention deficit hyperactivity disordr',
    }


class Condition:

    def __init__(self, **kwargs):
        self.name = kwargs['Condition']
        self.id = kwargs['Id']
        self.overview = kwargs['Overview']
        self.symptoms = kwargs['Symptoms']
        self.treatments = kwargs['Treatments']
        # self.causes = kwargs['Causes']
        # self.diagnosis = kwargs['Diagnosis']


class Anecdote:

    def __init__(self, **kwargs):
        self.name = kwargs['Condition']
        self.id = kwargs['Anecdote_ID']
        self.conid = kwargs['Condition_ID']
        self.forum = kwargs['Anecdote']


def get_condition(condition_name, retry=True):
    '''Get a condition by its name.'''
    try:
        # unforunately, DynamoDB scans are case-sensitive...
        condition_name = condition_name[0].upper() + condition_name[1:].lower()

        # scan for matching conditions
        response = Conditions.scan(
            FilterExpression=Attr('Condition').begins_with(condition_name))

        return Condition(**response['Items'].pop())

    except (TypeError, IndexError):
        # could not recognize the  condition
        if condition_name and retry:
            long_name = DIRTY_DICT.get(condition_name.lower())

            if long_name:
                return get_condition(long_name, retry=False)


def get_condition_for_anecdote(condition_name):
    try:
        condition_name = condition_name[0].upper() + condition_name[1:].lower()
        response = Anecdotes.scan(FilterExpression=Attr('Condition').begins_with(condition_name))['Items'] # do i need to pop here?
        return (Anecdote(**random.choice(response)))

    except (TypeError, IndexError):
        return None
