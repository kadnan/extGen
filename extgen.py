__author__ = 'Adnan Siddiqi<kadnanATgmail.com>'
import os
import json


def get_json(jsondata):
    json_object = None
    try:
        json_object = json.loads(jsondata)
    except ValueError, e:
        return None
    return json_object


def generate_manifest_text(json_dict):
    content = ''
    content = '{\n'
    content += '"manifest_version": 2,\n'
    content += '"name" : "'+json_dict['name']+'",\n'
    content += '"description" : "'+json_dict['description']+'",\n'
    content += '"version" : "1.0",\n'
    content += '"content_scripts" : [{\n'
    content += '\t"matches" : ["'+json_dict['contentscript_matches']+'"],\n'
    if 'contentscript_file' in json_dict:
        content += '\t"js" : ["'+json_dict['contentscript_file']+'"],\n'
        content += '\t"run_at": "document_end"\n'
        content += '}],\n'

    if 'backgroundscript_file' in json_dict:
        content += '"background":{\n'
        content += '\t"scripts": ["'+json_dict['backgroundscript_file']+'"]\n'
        content += '},\n'
    content += '"browser_action": {\n'
    content += '\t"default_title": "'+json_dict['name']+'"\n'
    #content += '\t"default_icon": "icon16.png"\n'
    content += '\t}\n'
    content += '}'
    return content


def read_app_json():
    jsoncontent = ''
    file = ''
    try:
        file = open('app.json','r')
        for line in file:
            jsoncontent += line.replace('\n','')
    except Exception, ex:
        print(str(ex))
    return jsoncontent


#check if app.json exist
def process():
    jsontext = read_app_json()
    name = ''
    contentscript_file = ''
    backgroundscript_file  = ''
    if jsontext != '':
        jsondict = get_json(jsontext)
        if jsondict is not None:
            if not 'name' in jsondict:
                print('missing "name" key in app.json')
            elif not 'description' in jsondict:
                print('missing "description" key in app.json')
            else:
                name = jsondict['name']
                name = name.replace(' ','_')
                if 'contentscript_file' in jsondict:
                    contentscript_file = jsondict['contentscript_file']

                if 'backgroundscript_file' in jsondict:
                    backgroundscript_file = jsondict['backgroundscript_file']

                manifest = generate_manifest_text(jsondict)
                if manifest != '':
                    try:
                        if not os.path.exists(name):
                            os.makedirs(name)
                            os.chdir(name)
                            manifest_file = open('manifest.json','w')
                            manifest_file.write(manifest)
                            manifest_file.flush()
                            manifest_file.close()
                            if contentscript_file != '':
                                open(contentscript_file, 'w').close()

                            if contentscript_file != '':
                                open(backgroundscript_file, 'w').close()

                            print('Process finished successfully. You can now visit directory "'+name+'" and check required extension files.')
                        else:
                            print('Directory already exist')
                    except Exception, e:
                        print(str(e))

if __name__ == "__main__":
    process()



