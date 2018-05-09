"""This is a small script for building a langauge model.

The command line is python ./make_lang_model.py {FILEDIR} {OUTPUTDIR},
where {FILEDIR} is a path to the folder where intent and slot
information is stored, and each subfolder represents an intent.

Within a single intent, there should be one file named "samples.txt",
which contains a line separated list of sample utterances for the intent.
There also needs to be one file named "slots.txt", which consists of lines where the first word is the slot name, and the second is it's type.  For ex:  for an intent with two slot types, the file would look like:

CONDITION ListOfConditions
TOPTION ListOfTreatmentOptions

For each slot type used in the intents, you need a file called "{TYPE}.txt"
corresponding to the possible fillers for that slot type.  The syntax should be a d-space separated list, where synonyms for a single filler are s-spaced.  For example, the file "ListOfConditions.txt" might look like:

P. T. S. D
post traumatic stress
post-traumatic stress disorder

anxiety
anxiety disorder
general anxiety
general anxiety disorder

depression
general depression
chronic depression

This should be in the parent folder, not the intent folder.
"""

import os

parent_file_dir = './language_model'
output_dir = '.'

def make_intents ():
    allsub = os.listdir(parent_file_dir)
    intent_texts = []
    slot_types = set()
    for folder in allsub:
        # if folder[-4:] != '.txt':
        if not folder.endswith(('.txt', '.py', '.pyc')):
            text,types = one_intent(folder)
            intent_texts += text
            slot_types = slot_types.union(types)
    last = intent_texts[-1][:-1]
    del intent_texts[-1]
    intent_texts.append(last)
    intent_texts.append('\t\t\t],\n\t\t\t"types": [')
    intent_texts += make_slot_types(slot_types)
    intent_texts.append('\t\t}')
    return (intent_texts)

def one_intent (folder):
    path = parent_file_dir + '/' + folder
    with open(path+'/samples.txt') as f:
        g = f.read()
    all_samples = [a for a in g.split('\n') if len(a)>0]

    try:
        with open(path+'/slots.txt') as f:
            g = f.read()
        all_slots = [a.split(' ') for a in g.split('\n') if len(a)>0]
        slot_type = dict()
        for pair in all_slots:
            slot_type[pair[0]] = pair[1]
        unique_types = set(slot_type.values())
    
    except IOError:
        slot_type = {}
        unique_types = set()

    intent_text = ['\t\t\t\t{\n\t\t\t\t\t"name": "'+folder+'",','\t\t\t\t\t"slots": [']
    for k,v in slot_type.iteritems():
        intent_text.append('\t\t\t\t\t\t{\n\t\t\t\t\t\t\t"name": "'+k+'",\n\t\t\t\t\t\t\t"type": "'+v+'"\n\t\t\t\t\t\t}')
    intent_text.append('\t\t\t\t\t],\n\t\t\t\t\t"samples": [')
    for sample in all_samples:
        intent_text.append('\t\t\t\t\t\t"'+sample+'",')
    last = intent_text[-1][:-1]
    del intent_text[-1]
    intent_text.append(last)
    intent_text.append('\t\t\t\t\t]\n\t\t\t\t},')
    return (intent_text, unique_types)

def make_slot_types (slot_types):
    text = []
    types = list(slot_types)
    for t in types:
        text.append('\t\t\t\t{\n\t\t\t\t\t"name": "'+t+'",\n\t\t\t\t\t"values": [')
        text += make_slot_values(parent_file_dir+'/'+t+'.txt')
    last = text[-1][:-1]
    del text [-1]
    text.append(last)
    text.append('\t\t\t]')
    return(text)

def make_slot_values (path):
    with open(path) as f:
        g = f.read()
    text = []
    values = g.split('\n\n')
    synonyms = [a.split('\n') for a in values]
    for nym in synonyms:
        if len(nym)==1:
            text.append('\t\t\t\t\t\t{\n\t\t\t\t\t\t\t"name": {\n\t\t\t\t\t\t\t\t"value": "'+nym[0]+'"\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t,')
        else:
            text.append('\t\t\t\t\t\t{\n\t\t\t\t\t\t\t"name": {\n\t\t\t\t\t\t\t\t"value": "'+nym[0]+'",\n\t\t\t\t\t\t\t\t"synonyms": [')
            for n in nym[1:]:
                if len(n)>0:
                    text.append('\t\t\t\t\t\t\t\t\t"'+n+'",')
            last = text[-1][:-1]
            del text[-1]
            text.append(last)
            text.append('\t\t\t\t\t\t\t\t]\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t},')
    last = text[-1]
    if last[-1] == ',':
        del text[-1]
        text.append(last[:-1])
    text.append('\t\t\t\t\t]\n\t\t\t\t},')
    return(text)

def main ():
    tp = ['{\n\t"interactionModel": {']
    tp += ['\t\t"languageModel": {\n\t\t\t"invocationName": "mental elf",\n\t\t\t"intents": [']
    tp += make_intents()
    tp += ['\t}\n}']
    with open(output_dir+'/LanguageModel.json','w+') as f:
        f.write('\n'.join(tp))
    print "done!"


main()
