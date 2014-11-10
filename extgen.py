__author__ = 'Adnan Siddiqi'
#http://extensionizr.com/!#{"modules":["hidden-mode","with-bg","with-persistent-bg","no-options","no-override"],"boolean_perms":[],"match_ptrns":[]}
import os
import json


def get_json(jsondata):
    json_object = None
    try:
        json_object = json.loads(jsondata)
    except ValueError, e:
        return None
    return json_object


def generate_manifest_file(json_dict):
    content = ''
    content = '{\n'
    content += '"manifest_version": 2,\n'
    content += '"name" : "'+json_dict['name']+'",\n'
    content += '"description" : "'+json_dict['description']+'",\n'
    content += '"version" : "1.0",\n'
    content += '"content_scripts" : [{\n'
    content += '\t"matches" : ["'+json_dict['contentscript_matches']+'"],\n'
    content += '\t"js" : ["'+json_dict['contentscript_file']+'"],\n'
    content += '\t"run_at": "document_end"\n'
    content += '}],\n'
    if 'backgroundscript_file' in json_dict:
        content += '"background":{\n'
        content += '\t"scripts": ["'+json_dict['backgroundscript_file']+'"]\n'
        content += '},\n'
    content += '"browser_action": {\n'
    content += '\t"default_title": "'+json_dict['name']+'",\n'
    content += '\t"default_icon": "icon16.png"\n'
    content += '\t}\n'
    content += '}'

    return content


def read_app_json():
    jsoncontent = ''
    file = ''
    try:
        file = open('app.json','r')
    except Exception, ex:
        print(str(ex))
        return

    for line in file:
        jsoncontent += line.replace('\n','')

    m = get_json(jsoncontent)
    if m:
        if not 'name' in m:
            print('missing "name" key in app.json')
            return
        if not 'description' in m:
            print('missing "description" key in app.json')
            return
        print(generate_manifest_file(m))
    else:
        print('not a valid json file')

#check if app.json exist
if os.path.exists('app.json'):
    read_app_json()
else:
    print("it does not")



