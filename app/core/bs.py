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
	    
	    self.history['lastcondition']=condition.name
	    self.history['lasttrigger']='overview'
    	    if self.history['grounded']:
                # if the current history has yet to involve any condition
                # overviews, begin the overview with "Let's talk {{ condition }}"
                # and, afterwards, ask the user if they would like to learn
                # more about symptoms or treatments; otherwise, we can assume the
                # user is familiar with what Mental Elf can do, so we can eliminate
                # this chit chat
                if self.history.get('overview'):
    		    self.history['last-sem-hub']=True
		    if self.history.get('elaborate'):
			self.history['elaborate']=False
                        return condition.overview.split('.',1)[1]  # RETURNS UTTERANCE
		    else:
			return condition.overview.split('.',1)[0]
                else:
                    # here is an example of how to store information across a
                    # user's requests for a given session; when the session ends,
                    # this information will go away
                    self.history['overview'] = True  # RETURNS UTTERANCE
	    	    self.history['last-sem-hub']=True
                    return self.render_template('first_overview',condition=condition.name,overview=condition.overview)
	    else: # haven't grounded yet
		self.history['to grounding']=True
		return self.render_template('grounding',condition=condition.name,trigger='an overview of')

        # if there was no matching condition in the database, say so
        except ValueError:
            return self.render_template('no_condition')  # RETURNS UTTERANCE

    def give_symptoms(self, condition):
        '''Create a response utterance for the `give_symptoms` intent.'''
        return self.render_template('symptoms', condition=condition)

    def give_treatment(self, condition):
        '''Create a response utterance for the `give_treament` intent.'''
        return self.render_template('treatment', condition=condition)

    def give_forum(self,condition)
	return self.render_template('help')

    def affirmativepassive(self):
	if self.history.get('last-sem-hub'):
	    self.history['last-sem-hub']=False
	    self.history['last-affirm']=True
	    return self.render_template('affirm-and-elaborate')
	elif self.history.get('last-affirm'):
	    self.history['last-affirm']=False
	    self.history['last-elaborate']=True
	    historysearch = self.search_history()	
	    if self.history.get('lasttrigger')=='overview':
		self.history['elaborate']=True
		elaborate = self.give_overview(self.history['lastcondition'])
    	    return elaborate + historysearch
	elif self.history.get('to-grounding')==True:
	    self.history['to-grounding']=False
	    self.history['grounded']=True
	
	    if self.history.get('lasttrigger')=='overview':
		return self.give_overview(self.history['lastcondition'])
	    elif self.history.get('lasttrigger')=='symptoms':
		return self.give_symptoms(self.history['lastcondition'])
	    elif self.history.get('lasttrigger')=='treatment':
		return self.give_treatment(self.history['lastcondition']))
	    elif self.history.get('lasttrigger')=='forum':
		return self.give_forum(self.history['lastcondition'])
	    self.history['lasttrigger']=''
	    else:
		self.history['lastcondition']=''
		self.history['lasttrigger']=''
		return self.render_template('help')
	else:
	    return self.render_template('help')

    def negative(self):
	if self.history.get('last-elaborate'):
	    self.history['last-elaborate']=False
	    return self.search_history()
	elif self.history.get('to-grounding'):
	    self.history['to-grounding']=False
	    self.history['lastcondition']=''
	    self.history['lasttrigger']=''
	    return self.render_template('help')
	else:
	    self.history['lasttrigger']=''
	    self.history['lastcondition']=''
	    return self.render_template('help')

    def search_history(self):
	'''is used to see if the user should be asked to continue talking about the same condition'''
	if self.history.get('overview') and self.history.get('treatment') and self.history.get('symptoms') and self.history.get('forum'):
	    self.history['overview']=False
	    self.history['treatement']=False
	    self.history['symptoms']=False
	    self.history['forum']=False
	    self.history['lastcondition']=''
	    return self.render_template('generic_q')
	elif not self.history.get('overview'):
	    return self.render_template('would-you-like',condition=self.history['lastcondition'],trigger='an overview of')
	elif not self.history.get('symptoms'):
	    return self.render_template('would-you-like',condition=self.history['lastcondition'],trigger='about the symptoms of')
	elif not self.history.get('treatment'):
	    return self.render_template('would-you-like',condition=self.history['lastcondition'],trigger='about the treatments for')
	else:
	    return self.render_template('would-you-like',condition=self.history['lastcondition'],trigger='an experience from a person diagnosed with')
		

    def help(self):
        '''Create a response utterance for the `help` intent.'''
        return self.render_template('help')
