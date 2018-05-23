from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import logging

from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.interpreter import RegexInterpreter
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.channels.channel import InputChannel, OutputChannel

if __name__ == '__main__':
	logging.basicConfig(level='INFO')
	
	training_data_file = './stories.md'
	model_path = './manmodel_online'
	interpreter= RasaNLUInterpreter('./NLUmodel/myModel2')
	agent = Agent('domain.yml', policies = [MemoizationPolicy(), KerasPolicy()],interpreter=interpreter)
	chan = ConsoleInputChannel()	
	agent.train_online(
			training_data_file,
			input_channel=chan,
			augmentation_factor = 50,
			max_history = 2,
			epochs = 500,
			batch_size = 10,
			validation_split = 0.2)
			
	agent.persist(model_path)
