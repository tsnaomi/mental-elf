from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

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
