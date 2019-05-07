from datetime import datetime
from app.constants import json_template
import json, os

class SileoGenerator:
    
    def __init__(self, title, short_description, author, long_description, version, headerImage, price, screenshots):
        self.title = title.replace(' ', '')
        self.summary = short_description
        self.headerImage = headerImage
        self.author = author
        self.description = long_description
        self.version = version
        self.screenshots = screenshots.replace('\n', '').replace(' ','').replace('\r', '').split(',')
        self.now = datetime.today().strftime('%m-%d-%Y')
        self.price = price
        
    def generate_template(self):
        try:
            with open('app/templates/sileo_depiction_template.json', 'r+') as json_file:
                data = json.load(json_file)
                rootObj = data['tabs'][0]['views']
                rootObj[0]['title'] = self.title
                data['headerImage'] = self.headerImage
                rootObj[4]['markdown'] = self.description
                sscount = 0
                for screenshot in self.screenshots:
                    rootObj[3]['screenshots'].append({
                        "accessibilityText": "Screenshot"+str(sscount),
                        "url": screenshot
                        })
                    sscount += 1
                rootObj[6]['text'] = self.version
                rootObj[7]['text'] = self.now
                rootObj[8]['text'] = self.price
                rootObj[10]['text']  = self.author
                rootObj[1]['markdown'] = self.summary
                data['tabs'][0]['views'] = rootObj
                json_file.seek(0)
                os.system('echo "{}" > tmp/%s.json' % self.title)
                with open('tmp/{}.json'.format(self.title), 'r+') as new_json:
                    json.dump(data, new_json, indent=4)
                    json_file.truncate()
                    new_json.close()
                with open('app/templates/sileo_depiction_template.json', 'w') as f:
                    f.write(str(json_template))
                    f.close()
                json_file.close()
        except Exception as e:
            print(e)
