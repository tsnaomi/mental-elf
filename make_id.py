import json
import sys

data = json.loads("".join(sys.argv[1:]))
print(data['Items'][0]['number']['N'])
