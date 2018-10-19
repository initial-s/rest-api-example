from flask import Flask
from datetime import datetime
import requests, json
app = Flask(__name__)

@app.route('/citl_design') #https://yourdomain.com/
def homepage():
    return '''<!DOCTYPE html>
<html>
<head>
<title>initial_S-Test-api</title>
</head>
<body>
<h1>Initial_S Test API</h1>
<h2>Add me</h2>
<div class="line-it-button" data-lang="en" data-type="friend" data-lineid="devilblack86" style="display: none;"></div>
 <script src="https://d.line-scdn.net/r/web/social-plugin/js/thirdparty/loader.min.js" async="async" defer="defer"></script>
</body>
</html>'''
#======================[ ARSYBAI ]==========================================
@app.route('/hello?<string:name>') #https://yourdomain.com/hello?arsybai
def hello(name):
    return 'Hello.. how are you {}'.format(str(name))
    
@app.route('/json?') #https://yourdomain.com/json?
def out():
    contoh = ['citl','design','kreasi tanpa batas']
    data = {
        'status':'OK',
        'result':contoh
    }
    return(json.dumps(data, indent=4, sort_keys=False))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

