import json

with open("settings.json", "r") as filehandle:
    settings = json.loads(filehandle.read())
