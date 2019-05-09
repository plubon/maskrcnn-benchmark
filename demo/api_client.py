import http.client
import json

class ApiClient():

    username = 'auto-annotator-3000'
    pwd  = 'beets-bears-battlestar-galactica'

    def __init__(self, url='http://3.120.235.67/api'):
        self.base_url = url
        self.token = None
        self.connection = None

    def connect(self):
        self.connection = http.client.HTTPConnection(self.base_url)
    
    def login(self):
        self.connect()
        body_dict = {'username':self.username, 'password':self.password}
        self.connection.request('POST', '/users/login', json.dumps(body_dict))
        response = self.connection.getresponse().decode()
        self.token = json.loads(response)['token']

    def get_latest(self):
        self.connect()
        self.connection.request('GET', '/publications/get-latest', headers={'Authorization':'Token '+self.token})
        response = self.connection.getresponse().decode()
        return json.loads(response)['id']

    def get_pages(self, id):
        self.connect()
        self.connection.request('GET', '/publications/pages?publication-id='+str(id),
            headers={'Authorization':'Token '+self.token})
        response = self.connection.getresponse().decode()
        data = json.loads(response)
        results = []
        for page in data['results']:
            results.append((page['id'], page['image']))
        return results

    def add_annotation(self, id, annotation):
        self.connect()
        body = {'page':id, data:annotation}
        self.connection.request('POST', '/publications/annotations',
            json.dumps(body),
            headers={'Authorization':'Token '+self.token, 'Content-Type':'application/json'}
        )

    
