import json
import sys

data = "{\"number\": {\"N\": \"%s\"}}" %sys.argv[1]
with open("tmp.json", "w") as f:
  json.dump(json.loads(data), f)
