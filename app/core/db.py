import Boto_Flask_Lib as db

from boto3.dynamodb.conditions import Attr


# the "Conditions" table on DynamoDB
Conditions = db.Open_DynamoDB('Conditions')


class Condition:

    def __init__(self, **kwargs):
        self.name = kwargs['Condition']
        self.id = kwargs['Id']
        self.overview = kwargs['Overview']
        self.symptoms = kwargs['Symptoms']
        self.treatments = kwargs['Treatments']
        # self.causes = kwargs['Causes']
        # self.diagnosis = kwargs['Diagnosis']


def get_condition(condition_name):
    '''Get a condition by its name.'''
    try:
        # unforunately, DynamoDB scans are case-sensitive...
        condition_name = condition_name[0].upper() + condition_name[1:].lower()

        # scan for matching conditions
        response = Conditions.scan(
            FilterExpression=Attr('Condition').begins_with(condition_name))

        return Condition(**response['Items'].pop())

    except (TypeError, IndexError):
        msg = 'Could not recognize the following condition: ' + condition_name

        raise ValueError(msg)
