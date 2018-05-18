import argparse
import json

def createjson(samples,synonyms,outFile):
	dic = {}
	dic['rasa_nlu_data'] = {'common_examples':[],'entity_synonyms':[]}
	dx = [x.split('-') for x in samples]
	for x in dx:
		temp = {}
		temp['text'] = x[0]
		temp['intent'] = x[2]
		temp['entities'] = []
		entities = x[1].split(';')
		for entity in entities:
			ent = {}
			tempentity=entity.split(':')
			ent['start']=temp['text'].index(tempentity[0])
			ent['end']=temp['text'].index(tempentity[0]) + len(tempentity[0])
			ent['value']=tempentity[0]
			ent['entity']=tempentity[1]
			temp['entities'].append(ent)
		dic['rasa_nlu_data']['common_examples'].append(temp)
	
	dx = [x.split('-') for x in synonyms]
	for x in dx:
		temp = {}
		temp['value'] = x[0]
		syms = x[1].split(';')
		temp['synonyms']=syms
		dic['rasa_nlu_data']['entity_synonyms'].append(temp)
			
	js = json.dumps(dic,indent=3)
	f = open(outFile,"w")
	f.write(js)
	f.close()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--samplesFile', type= str, default = 'samples.txt')
	parser.add_argument('--synonymsFile', type= str, default = 'synonyms.txt')
	parser.add_argument('--outFile', type= str, default = 'NLU.json')
	args = parser.parse_args()
	f = open(args.samplesFile)
	samples = f.read().strip().split('\n')
	f = open(args.synonymsFile)
	synonyms = f.read().strip().split('\n')
	createjson(samples,synonyms,args.outFile)

