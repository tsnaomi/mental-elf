# local
import db  # DATABASE
from random import choice as choose

from get_sentiment import get_sentiment

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
            return self.render_template(choose(['no_condition_1','no_condition_2']),trigger='an overview of'), self.render_template('no-condition-r',trigger='an overview of')
        self.history['lastcondition']=condition.name
        self.history['lasttrigger']='overview'
        if 'grounded' in self.history.keys() and self.history['grounded']:

            # if the current history has yet to involve any condition
            # overviews, begin the overview with "Let's talk {{ condition }}"
            # and, afterwards, ask the user if they would like to learn
            # more about symptoms or treatments; otherwise, we can assume the
            # user is familiar with what Mental Elf can do, so we can eliminate
            # this chit chat

            if 'elaborate' in self.history.keys() and self.history.get('elaborate'):
                self.history['elaborate']=False
                return condition.overview.split('.',1)[1]  # RETURNS UTTERANCE
            else:
                self.history['last-sem-hub']=True
                # next_choice = 'opinion'
                next_choice = choose(['opinion', 'elaborate_1', 'elaborate_2']) #'opinion',
                if next_choice == 'elaborate_1' or next_choice == 'elaborate_2':
                    self.history['can-elaborate']= len(condition.overview.split('.',1))>1
                    if not self.history.get('can-elaborate') or not len(condition.overview.split('.',1)[1]) > 1:
                        next_choice = 'opinion'
                        next_reprompt = self.render_template('opinion-r')
                        next_move = self.render_template(next_choice)
                        self.history['overview']=True
                        return condition.overview.split('.',1)[0]+ '. ' + next_move, next_reprompt
                    print('i shouldnt be here if opinion')
                    self.history['last-sem-hub']=False
                    self.history['last-affirm']=True
                    # self.history['last-elaborate']=True
                    next_reprompt = self.render_template('elaborate-r')
                else:
                    next_reprompt = self.render_template('opinion-r')
                next_move = self.render_template(next_choice)
                self.history['overview']=True
                return condition.overview.split('.',1)[0]+ '. ' + next_move, next_reprompt
        else:  # haven't grounded yet
            self.history['to-grounding']=True
            return self.render_template(choose(['grounding_1', 'grounding_2']),condition=condition.name,trigger='an overview of'), self.render_template('grounding-r',condition=condition.name,trigger='an overview of')
        # if there was no matching condition in the database, say so
        # except ValueError:
        #    self.history['slotfilling']='overview'
        #    return self.render_template(choose(['no_condition_1', 'no_condition_2']),trigger='an overview of')  # RETURNS UTTERANCE

    def give_symptoms(self, condition):
        '''Create a response utterance for the `give_overview` intent.'''
        try:
            # get the provided condition from the database
            condition = db.get_condition(condition)
            if condition==None:
                raise ValueError('needs slot filling')
            self.history['lastcondition']=condition.name
            self.history['lasttrigger']='symptoms'
            if 'grounded' in self.history.keys() and self.history['grounded']:
                if 'elaborate' in self.history.keys() and self.history.get('elaborate'):
                    self.history['elaborate']=False
                    return condition.symptoms.split('.',1)[1]  # RETURNS UTTERANCE
                else:
                    self.history['last-sem-hub']=True
                    next_choice = choose(['opinion','elaborate_1','elaborate_2'])
                    if next_choice == 'elaborate_1' or next_choice == 'elaborate_2':
                        self.history['can-elaborate']= len(condition.symptoms.split('.',1))>1
                        if not self.history.get('can-elaborate') or not len(condition.symptoms.split('.',1)[1]) > 1:
                            next_choice = 'opinion'
                            next_reprompt = self.render_template('opinion-r')
                            next_move = self.render_template(next_choice)
                            self.history['symptoms']=True
                            return condition.symptoms.split('.',1)[0]+ '. ' + next_move, next_reprompt

                        self.history['last-sem-hub']=False
                        self.history['last-affirm']=True
                        # self.history['last-elaborate']=True
                        next_reprompt = self.render_template('elaborate-r')
                    else:
                        next_reprompt = self.render_template('opinion-r')
                    next_move = self.render_template(next_choice)
                    self.history['symptoms']=True
                    return condition.symptoms.split('.',1)[0]+'. '+next_move, next_reprompt

            else:  # haven't grounded yet
                self.history['to-grounding']=True
                return self.render_template(choose(['grounding_1', 'grounding_2']),condition=condition.name,trigger='the symptoms of'), self.render_template('grounding-r',condition=condition.name,trigger='the symptoms of')

        # if there was no matching condition in the database, say so
        except ValueError:
            self.history['slotfilling']='symptoms'
            return self.render_template(choose(['no_condition_1', 'no_condition_2']),trigger='the symptoms of'), self.render_template('no-condition-r',trigger='the symptoms of')  # RETURNS UTTERANCE

    def give_treatment(self, condition):
        '''Create a response utterance for the `give_overview` intent.'''
        try:
            # get the provided condition from the database
            condition = db.get_condition(condition)
            if condition == None:
                raise ValueError('needs slot filling')
            self.history['lastcondition']=condition.name
            self.history['lasttrigger']='treatment'
            if 'grounded' in self.history.keys() and self.history['grounded']:

                if 'elaborate' in self.history.keys() and self.history.get('elaborate'):
                    self.history['elaborate']=False
                    return condition.treatments.split('.',1)[1]  # RETURNS UTTERANCE
                else:
                    self.history['last-sem-hub']=True
                    next_choice = choose(['elaborate_1','elaborate_2']) #'opinion',
                    if next_choice == 'elaborate_1' or next_choice == 'elaborate_2':
                        self.history['can-elaborate']= len(condition.treatments.split('.',1))>1
                        if not self.history.get('can-elaborate') or not len(condition.treatments.split('.',1)[1]) > 1:
                            next_choice = 'opinion'
                            next_reprompt = self.render_template('opinion-r')
                            next_move = self.render_template(next_choice)
                            self.history['treatment']=True
                            return condition.treatments.split('.',1)[0]+ '. ' + next_move, next_reprompt
                        self.history['last-sem-hub']=False
                        self.history['last-affirm']=True
                        # self.history['last-elaborate']=True
                        next_reprompt = self.render_template('elaborate-r')
                    else:
                        next_reprompt = self.render_template('opinion-r')
                    next_move = self.render_template(next_choice)
                    self.history['treatment']=True
                    return condition.treatments.split('.',1)[0]+'. '+next_move, next_reprompt

            else:  # haven't grounded yet
                self.history['to-grounding']=True
                return self.render_template(choose(['grounding_1', 'grounding_2']),condition=condition.name,trigger='the treatment for'),self.render_template('grounding-r',condition=condition.name,trigger='the treatment for')

        # if there was no matching condition in the database, say so
        except ValueError:
            self.history['slotfilling']='treatment'
            return self.render_template(choose(['no_condition_1', 'no_condition_2']),trigger='the treatment options for') , self.render_template('no-condition-r',trigger='the treatment options for') # RETURNS UTTERANCE

    def give_forum(self,condition):
        '''Create a response utterance for the `give_overview` intent.'''
        try:
            # get the provided condition from the database
            condition = db.get_condition_for_anecdote(condition)
            if condition == None:
                raise ValueError('needs slot filling')
            self.history['lastcondition']=condition.name
            self.history['lasttrigger']='forum'
            if 'grounded' in self.history.keys() and self.history['grounded']:

                if 'elaborate' in self.history.keys() and self.history.get('elaborate'):
                    self.history['elaborate']=False
		    try:
                        return condition.forum.split('.',3)[3]  # RETURNS UTTERANCE
    		    except IndexError:
			return condition.forum.split('.',3)[2] 
	        else:
                    self.history['last-sem-hub']=True
                    next_choice = choose(['elaborate_1','elaborate_2'])
                    if next_choice == 'elaborate_1' or next_choice == 'elaborate_2':
                        self.history['can-elaborate']= len(condition.forum.split('.',1))>1
                        if not self.history.get('can-elaborate') or not len(condition.forum.split('.',1)[1]) > 1:
                            next_choice = 'opinion'
                            next_reprompt = self.render_template('opinion-r')
                            next_move = self.render_template(next_choice)
                            self.history['forum']=True
                            return '.'.join(condition.forum.split('.',3)[:3])+ '. ' + next_move, next_reprompt
                        self.history['last-sem-hub']=False
                        self.history['last-affirm']=True
                        # self.history['last-elaborate']=True
                        next_reprompt = self.render_template('elaborate-r')
                    else:
                        next_reprompt = self.render_template('opinion-r')
                    next_move = self.render_template(next_choice)
                    self.history['forum']=True
                    return 'Here is a story from someone living with this condition. '+ '.'.join(condition.forum.split('.',3)[:3])+'. '+next_move, next_reprompt

            else:  # haven't grounded yet
                self.history['to-grounding']=True
                return self.render_template(choose(['grounding_1','grounding_2']),condition=condition.name,trigger='an experience of someone living with'), self.render_template('grounding-r',condition=condition.name,trigger='an experience of someone living with')

        # if there was no matching condition in the database, say so
        except ValueError:
            self.history['slotfilling']='forum'
            return self.render_template(choose(['no_condition_1', 'no_condition_2']),trigger='a personal story about') ,self.render_template('no-condition-r',trigger='a personal story about') # RETURNS UTTERANCE

    def affirmativepassive(self,raw=None):
        print(self.history.get('to-grounding'))
        print(self.history.get('lasttrigger'))
        print(self.history.get('last-sem-hub'))
        print(self.history.get('last-affirm'))
        print(self.history.get('grounded'))
        if 'last-sem-hub' in self.history.keys() and self.history.get('last-sem-hub'):
            self.history['last-sem-hub']=False
            if 'can_elaborate' in self.history.keys() and self.history.get('can_elaborate'):
                self.history['last-affirm']=True
		elaborate = self.render_template(choose(['elaborate_1','elaborate_2']))
		if raw == None:
                    return self.render_template(choose(['sounds-familiar', 'affirm-and-elaborate']))+' '+elaborate,self.render_template('affirm-r')
		senti = get_sentiment(str(raw))
		if senti == 'negative':
		    return self.render_template(choose(['negative_1','negative_2','negative_3']))+' '+elaborate,self.render_template('affirm-r')
		elif senti == 'positive':
		    return self.render_template(choose(['positive_1','positive_2','positive_3']))+' '+elaborate,self.render_template('affirm-r')
		else:
		    return self.render_template(choose(['sounds-familiar','affirm-and-elaborate']))+' '+elaborate,self.render_template('affirm-r')
            else:
                self.history['last-affirm'] =False
                self.history['last-elaborate'] = True
		print('raw')
		print(raw)
		if raw == None:
		    return self.render_template(choose(['sounds-familiar','affirm-and-elaborate'])) +' ' +self.search_history()

		senti = get_sentiment(str(raw))
		if senti == 'negative':
		    return self.render_template(choose(['negative_1','negative_2','negative_3']))+' '+ self.search_history()
		elif senti == 'positive':
		    return self.render_template(choose(['positive_1','positive_2','positive_3']))+' ' + self.search_history()
		else:
               	    return self.render_template(choose(['sounds-familiar','affirm-and-elaborate']))+' '+ self.search_history() #self.render_template('just-affirm')
		
        elif 'last-affirm' in self.history.keys() and self.history.get('last-affirm'):
            print('i should be here')
            print(self.history.get('lasttrigger'))
            self.history['last-affirm']=False
            self.history['last-elaborate']=True
            historysearch = self.search_history()
            if 'lasttrigger' in self.history.keys() and self.history.get('lasttrigger')=='overview':
                self.history['elaborate']=True
                elaborate = self.give_overview(self.history['lastcondition'])
                return elaborate + ' ' + historysearch, self.render_template('wyl-r', trigger='an overview of',condition=self.history['lastcondition'])
            # TODO add the other triggers here
            elif 'lasttrigger' in self.history.keys() and self.history.get('lasttrigger')=='symptoms':
                self.history['elaborate']=True
                elaborate = self.give_symptoms(self.history['lastcondition'])
                return elaborate + ' ' + historysearch, self.render_template('wyl-r', trigger='the symptoms of',condition=self.history['lastcondition'])
            elif 'lasttrigger' in self.history.keys() and self.history.get('lasttrigger')=='treatment':
                self.history['elaborate']=True
                elaborate = self.give_treatment(self.history['lastcondition'])[0]
                return elaborate + ' ' + historysearch, self.render_template('wyl-r', trigger='the treatment for',condition=self.history['lastcondition'])
            else:
                self.history['elaborate']=True
                elaborate = self.give_forum(self.history['lastcondition'])
                return elaborate + ' ' + historysearch, self.render_template('wyl-r', trigger='an experience of',condition=self.history['lastcondition'])

        elif 'to-grounding' in self.history.keys() and self.history.get('to-grounding'):
            self.history['to-grounding']=False
            self.history['grounded']=True
            if 'lasttrigger' in self.history.keys() and self.history.get('lasttrigger')=='overview':
                self.history['lasttrigger']=''
                return self.give_overview(self.history['lastcondition'])
            elif 'lasttrigger' in self.history.keys() and self.history.get('lasttrigger')=='symptoms':
                self.history['lasttrigger']=''
                return self.give_symptoms(self.history['lastcondition'])
            elif 'lasttrigger' in self.history.keys() and self.history.get('lasttrigger')=='treatment':
                self.history['lasttrigger']=''
                return self.give_treatment(self.history['lastcondition'])
            elif 'lasttrigger' in self.history.keys() and self.history.get('lasttrigger')=='forum':
                self.history['lasttrigger']=''
                return self.give_forum(self.history['lastcondition'])
            else:
                self.history['lastcondition']=''
                self.history['lasttrigger']=''
                return self.help()
            # else:
                # self.history['lastcondition']=''
                # self.history['lasttrigger']=''
                # return self.help()
        elif 'last-elaborate' in self.history.keys() and self.history.get('last-elaborate'):
            # send to sem hub from history search
            print("yes got here too")
            self.history['last-elaborate']=False
            self.history['grounded']=True
            if self.history.get('hist_match')=='overview':
                return self.give_overview(self.history['lastcondition'])
            elif self.history.get('hist_match')=='symptoms':
                return self.give_symptoms(self.history['lastcondition'])
            elif self.history.get('hist_match')=='treatment':
                return self.give_treatment(self.history['lastcondition'])
            else:
                return self.give_forum(self.history['lastcondition'])
        else:
            self.history['lasttrigger']=''
            self.history['lastcondition']=''
            return self.help()

    def clear_board(self):
        self.history['last-elaborate']=False
        self.history['lastcondition']=''
        self.history['lasttrigger']=''
        self.history['overview']=False
        self.history['treatment']=False
        self.history['symptoms']=False
        self.history['forum']=False
        self.history['last-affirm']=False
        self.history['to-grounding']=False
        self.history['last-affirm']=False
        self.history['grounded']=False
        self.history['hist_match']=''
        self.history['slotfilling']=''
        self.history['can-elaborate']=True

    def negative(self):
        if 'last-elaborate' in self.history.keys() and self.history.get('last-elaborate'):
            # when you've just asked the history question, and they say no, then let them go to the open question
            self.clear_board()
            return self.render_template(choose(['generic_1','generic_2','generic_3'])),self.render_template('generic-r')
        elif 'to-grounding' in self.history.keys() and self.history.get('to-grounding'):
            # grounded was wrong
            self.clear_board()
            return self.render_template(choose(['generic_1','generic_2','generic_3'])),self.render_template('generic-r')
        elif 'last-affirm' in self.history.keys() and self.history.get('last-affirm'):
            # don't want to elaborate
            print("yes, i got here")
            self.history['last-affirm'] = False
            self.history['last-elaborate']=True # a trick
            return self.search_history(),self.render_template('wyl-r',trigger=self.history['hist_match'],condition=self.history['lastcondition'])
        else:
            #self.history['lasttrigger']='' TODO maybe we should clear the board here, too?
            #self.history['lastcondition']=''
            return self.help()

    def slot_filling(self,condition):
        ''' is used to fill in the slot when a condition was not found'''
        # need something to keep track if they've just been here
        try:
            condition=db.get_condition(condition)
            if condition == None:
                raise ValueError('slot filling unsuccessful')
        except ValueError:
            return self.render_template('bad_slot'),self.render_template('bad-slot-r')
        if 'slotfilling' in self.history.keys() and self.history.get('slotfilling')=='overview':
            self.history['slotfilling']=''
            return self.give_overview(condition.name)
        elif 'slotfilling' in self.history.keys() and self.history.get('slotfilling')=='symptoms':
            self.history['slotfilling']=''
            return self.give_symptoms(condition.name)
        elif 'slotfilling' in self.history.keys() and self.history.get('slotfilling')=='treatment':
            self.history['slotfilling']=''
            return self.give_treatment(condition.name)
        elif 'slotfilling' in self.history.keys() and self.history.get('slotfilling')=='forum':
            self.history['slotfilling']=''
            return self.give_forum(condition.name)
        else: # the default is to give an overview
            self.history['slotfilling']=''
            return self.give_overview(condition.name)

    def search_history(self):
        '''is used to see if the user should be asked to continue talking about the same condition'''
        self.history['last-elaborate'] = True
        self.history['can-elaborate'] = True
        if 'overview' and 'treatment' and 'symptoms' and 'forum' in self.history.keys() and self.history.get('overview') and self.history.get('treatment') and self.history.get('symptoms') and self.history.get('forum'):
            self.history['overview'] = False
            self.history['treatement'] = False
            self.history['symptoms'] = False
            self.history['forum'] = False
            self.history['lastcondition'] = ''
            self.history['hist_match']=''
            self.history['grounded']=False
            return self.render_template(choose(['generic_1', 'generic_2', 'generic_3']))
        elif not 'overview' in self.history.keys() or not self.history.get('overview'):
            self.history['hist_match']='overview'
            return self.render_template(choose(['would-you-like', 'how-about']),condition=self.history['lastcondition'],trigger='an overview of')
        elif not 'symptoms' in self.history.keys() or not self.history.get('symptoms'):
            self.history['hist_match']='symptoms'
            return self.render_template(choose(['would-you-like', 'how-about']),condition=self.history['lastcondition'],trigger='about the symptoms of')
        elif not 'treatment' in self.history.keys() or not self.history.get('treatment'):
            self.history['hist_match']='treatment'
            return self.render_template(choose(['would-you-like', 'how-about']),condition=self.history['lastcondition'],trigger='about the treatments for')
        else:
            self.history['hist_match']='forum'
            return self.render_template(choose(['would-you-like', 'how-about']),condition=self.history['lastcondition'],trigger='an experience from a person diagnosed with')

    def help(self):
        '''Create a response utterance for the `help` intent.'''
        return self.render_template('help'),self.render_template('help-r')
