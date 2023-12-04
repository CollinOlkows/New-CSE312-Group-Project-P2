import json

def get_creds():
    with open('conf.json') as fp:
        return json.loads(fp.read())

