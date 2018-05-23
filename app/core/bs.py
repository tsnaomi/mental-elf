# local
import db  # DATABASE


class DialogueManager:

    def __init__(self, render_template):
        self.render_template = render_template

    def get_utterance(self, session, bentent, sargs):  # sargs = dict
        # e.g.,
        # bentent = 'give_overview'
        # sargs = {'condition': 'depression'}
        self.history = session.attributes

        return getattr(self, bentent)(**sargs)

    def give_overview(self, condition):
        '''Create a response utterance for the `give_overview` intent.'''
        try:
            # get the provided condition from the database
            condition = db.get_condition(condition)

            # if the current history has yet to involve any condition
            # overviews, begin the overview with "Let's talk {{ condition }}"
            # and, afterwards, ask the user if they would like to learn
            # more about symptoms or treatments; otherwise, we can assume the
            # user is familiar with what Mental Elf can do, so we can eliminate
            # this chit chat
            if self.history.get('overview given'):
                return condition.overview  # RETURNS UTTERANCE

            else:
                # here is an example of how to store information across a
                # user's requests for a given session; when the session ends,
                # this information will go away
                self.history['overview given'] = True  # RETURNS UTTERANCE

                return self.render_template(
                    'first_overview',
                    condition=condition.name,
                    overview=condition.overview,
                    )

        # if there was no matching condition in the database, say so
        except ValueError:
            return self.render_template('no_condition')  # RETURNS UTTERANCE

    def give_symptoms(self, condition):
        '''Create a response utterance for the `give_symptoms` intent.'''
        return self.render_template('symptoms', condition=condition)

    def give_treatment(self, condition):
        '''Create a response utterance for the `give_treament` intent.'''
        return self.render_template('treatment', condition=condition)

    def help(self):
        '''Create a response utterance for the `help` intent.'''
        return self.render_template('help')
