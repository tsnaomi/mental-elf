from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function

import logging

from rasa_core.agent import Agent
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.interpreter import RasaNLUInterpreter

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet

class ActionGiveOverview(Action):
    def name(self):
        return 'action_GiveOverview'
	
	def run(self, dispatcher, tracker, domain):
		loc = tracker.get_slot('ListOfConditions')
		dispatcher.utter_message("OverviewReq")
		return [] #[SlotSet("ListOfConditions", loc)]		
		
class ActionGiveSymptoms(Action):
    def name(self):
        return 'action_GiveSymptoms'

	def run(self, dispatcher, tracker, domain):
		loc = tracker.get_slot('ListOfConditions')
		dispatcher.utter_message("SymptomsReq")
		return [] #[SlotSet("ListOfConditions", loc)]

class ActionGiveTreatment(Action):
    def name(self):
        return 'action_GiveTreatment'

	def run(self, dispatcher, tracker, domain):
		loc = tracker.get_slot('ListOfConditions')
		dispatcher.utter_message("TreatmentsReq")		
		return [] #[SlotSet("ListOfConditions", loc)]

class ActionGivePrevalence(Action):
    def name(self):
        return 'action_GivePrevalence'

	def run(self, dispatcher, tracker, domain):
		loc = tracker.get_slot('ListOfConditions')
		dispatcher.utter_message("PrevalenceReq")
		return [] #[SlotSet("ListOfConditions", loc)]

if __name__ == '__main__':
	logging.basicConfig(level='INFO')
	
	training_data_file = './stories.md'
	model_path = './manmodel'
	interpreter= RasaNLUInterpreter('./NLUmodel/myModel2')
	#interpreter= './NLUmodel/default_model'
	agent = Agent('domain.yml', policies = [MemoizationPolicy(), KerasPolicy()],interpreter=interpreter)
	
	agent.train(
			training_data_file,
			augmentation_factor = 50,
			max_history = 2,
			epochs = 500,
			batch_size = 10,
			validation_split = 0.2)
			
	agent.persist(model_path)
