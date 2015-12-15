import ConfigParser

cp = ConfigParser.ConfigParser()
cp.read('config.ini')

token = cp.get('config', 'token')
url = cp.get('config', 'url')
path = cp.get('config', 'path')
