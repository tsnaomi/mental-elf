# local
import db  # DATABASE
from random import choice as choose

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

        # get the provided condition from the database
        condition = db.get_condition(condition)
	if condition == None:
	    self.history['slotfilling']='overview'
	    return self.render_template(choose['no_condition_1','no_condition_2'],trigger='an overview of')	
        self.history['lastcondition']=condition.name
	self.history['lasttrigger']='overview'
    	if self.history['grounded']:
            # if the current history has yet to involve any condition
            # overviews, begin the overview with "Let's talk {{ condition }}"
            # and, afterwards, ask the user if they would like to learn
            # more about symptoms or treatments; otherwise, we can assume the
            # user is familiar with what Mental Elf can do, so we can eliminate
            # this chit chat
	    self.history['last-sem-hub']=True
	    if self.history.get('elaborate'):
	        self.history['elaborate']=False
		return condition.overview.split('.',1)[1]  # RETURNS UTTERANCE
	    else:
	        return condition.overview.split('.',1)[0]
	else: # haven't grounded yet
   	    self.history['to grounding']=True
	    return self.render_template(choose(['grounding_1', 'grounding_2']),condition=condition.name,trigger='an overview of')

        # if there was no matching condition in the database, say so
        #except ValueError:
	#    self.history['slotfilling']='overview'
        #    return self.render_template(choose(['no_condition_1', 'no_condition_2']),trigger='an overview of')  # RETURNS UTTERANCE

    def give_symptoms(self, condition):
        '''Create a response utterance for the `give_overview` intent.'''
        try:
            # get the provided condition from the database
            condition = db.get_condition(condition)    
	    self.history['lastcondition']=condition.name
	    self.history['lasttrigger']='symptoms'
    	    if self.history['grounded']:
		self.history['last-sem-hub']=True
		if self.history.get('elaborate'):
  		    self.history['elaborate']=False
		    return condition.symptoms.split('.',1)[1]  # RETURNS UTTERANCE
		else:
		    return condition.symptoms.split('.',1)[0]

  	    else: # haven't grounded yet
		self.history['to grounding']=True
		return self.render_template(choose(['grounding_1', 'grounding_2']),condition=condition.name,trigger='the symptoms of')

        # if there was no matching condition in the database, say so
        except ValueError:
	    self.history['slotfilling']='symptoms'
            return self.render_template(choose(['no_condition_1', 'no_condition_2']),trigger='the symptoms of')  # RETURNS UTTERANCE

    def give_treatment(self, condition):
        '''Create a response utterance for the `give_overview` intent.'''
        try:
            # get the provided condition from the database
            condition = db.get_condition(condition)
	    self.history['lastcondition']=condition.name
	    self.history['lasttrigger']='treatment'
    	    if self.history['grounded']:
		self.history['last-sem-hub']=True
		if self.history.get('elaborate'):
		    self.history['elaborate']=False
		    return condition.treatment.split('.',1)[1]  # RETURNS UTTERANCE
		else:
		    return condition.treatment.split('.',1)[0]

	    else: # haven't grounded yet
		self.history['to grounding']=True
		return self.render_template(choose(['grounding_1', 'grounding_2']),condition=condition.name,trigger='the treatment for')

        # if there was no matching condition in the database, say so
        except ValueError:
	    self.history['slotfilling']='treatment'
            return self.render_template(choose(['no_condition_1', 'no_condition_2']),trigger='the treatment options for')  # RETURNS UTTERANCE

    def give_forum(self,condition):
        '''Create a response utterance for the `give_overview` intent.'''
        try:
            # get the provided condition from the database
            condition = db.get_condition(condition)    
	    self.history['lastcondition']=condition.name
	    self.history['lasttrigger']='forum'
    	    if self.history['grounded']:
		self.history['last-sem-hub']=True
		if self.history.get('elaborate'):
		    self.history['elaborate']=False
		    return condition.forum.split('.',1)[1]  # RETURNS UTTERANCE
		else:
		    return condition.forum.split('.',1)[0]

	    else: # haven't grounded yet
		self.history['to grounding']=True
		return self.render_template(choose(['grounding_1','grounding_2']),condition=condition.name,trigger='an experience of someone living with')

        # if there was no matching condition in the database, say so
        except ValueError:
	    self.history['slotfilling']='forum'
            return self.render_template(choose(['no_condition_1', 'no_condition_2']),trigger='a personal story about')  # RETURNS UTTERANCE

    def affirmativepassive(self):
	if self.history.get('last-sem-hub'):
	    self.history['last-sem-hub']=False
	    self.history['last-affirm']=True
	    return self.render_template(choose(['sounds-familiar', 'affirm-and-elaborate']))
	elif self.history.get('last-affirm'):
	    self.history['last-affirm']=False
	    self.history['last-elaborate']=True
	    historysearch = self.search_history()
	    if self.history.get('lasttrigger')=='overview':
	    	self.history['elaborate']=True
	        elaborate = self.give_overview(self.history['lastcondition'])
	    	return elaborate + historysearch
	    elif self.history.get('to-grounding'):
	        self.history['to-grounding']=False
	        self.history['grounded']=True

		if self.history.get('lasttrigger')=='overview':
		    self.history['lasttrigger']=''
	  	    return self.give_overview(self.history['lastcondition'])
		elif self.history.get('lasttrigger')=='symptoms':
		    self.history['lasttrigger']=''
		    return self.give_symptoms(self.history['lastcondition'])
		elif self.history.get('lasttrigger')=='treatment':
		    self.history['lasttrigger']=''
		    return self.give_treatment(self.history['lastcondition'])
		elif self.history.get('lasttrigger')=='forum':
		    self.history['lasttrigger']=''
		    return self.give_forum(self.history['lastcondition'])
		else:
		    self.history['lastcondition']=''
		    self.history['lasttrigger']=''
		    return self.help()
 	    else:
		self.history['lastcondition']=''
		self.history['lasttrigger']=''
		return self.help()
	else:
	    self.history['lasttrigger']=''
	    self.history['lastcondition']=''
	    return self.help()

    def negative(self):
	if self.history.get('last-elaborate'):
	    self.history['last-elaborate']=False
	    return self.search_history()
	elif self.history.get('to-grounding'):
	    self.history['to-grounding']=False
	    self.history['lastcondition']=''
	    self.history['lasttrigger']=''
	    return self.help()
	else:
	    self.history['lasttrigger']=''
	    self.history['lastcondition']=''
	    return self.help()

    def slot_filling(self,condition):
	''' is used to fill in the slot when a condition was not found'''
	# need something to keep track if they've just been here
	try:
	    condition=db.get_condition(condition)
	except ValueError:
	    self.history['slotfilling']='' # i don't know if i actually want this
	    return self.render_template('bad_slot')
	if self.history.get('slotfilling')=='overview':
	    self.history['slotfilling']=''
	    return self.give_overview(condition.name)
	elif self.history.get('slotfilling')=='symptoms':
	    self.history['slotfilling']=''
	    return self.give_symptoms(condition.name)
	elif self.history.get('slotfilling')=='treatment':
	    self.history['slotfilling']=''
	    return self.give_treatment(condition.name)
	elif self.history.get('slotfilling')=='forum':
	    self.history['slotfilling']=''
	    return self.give_forum(condition.name)
	else: # the default is to give an overview
	    self.history['slotfilling']=''
	    return self.give_overview(condition.name)
    def search_history(self):
	'''is used to see if the user should be asked to continue talking about the same condition'''
	if self.history.get('overview') and self.history.get('treatment') and self.history.get('symptoms') and self.history.get('forum'):
	    self.history['overview']=False
	    self.history['treatement']=False
	    self.history['symptoms']=False
	    self.history['forum']=False
	    self.history['lastcondition']=''
	    return self.render_template(choose(['generic_1', 'generic_2', 'generic_3']))
	elif not self.history.get('overview'):
	    return self.render_template(choose(['would-you-like', 'how-about']),condition=self.history['lastcondition'],trigger='an overview of')
	elif not self.history.get('symptoms'):
	    return self.render_template(choose(['would-you-like', 'how-about']),condition=self.history['lastcondition'],trigger='about the symptoms of')
	elif not self.history.get('treatment'):
	    return self.render_template(choose(['would-you-like', 'how-about']),condition=self.history['lastcondition'],trigger='about the treatments for')
	else:
	    return self.render_template(choose(['would-you-like', 'how-about']),condition=self.history['lastcondition'],trigger='an experience from a person diagnosed with')

    def help(self):
        '''Create a response utterance for the `help` intent.'''
        return self.render_template('help')
