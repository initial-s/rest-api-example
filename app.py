from flask import Flask
from datetime import datetime
import requests, json, re
from re import match
from bs4 import BeautifulSoup
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
 
@app.route('/test', methods=['POST'])
def post():
    headers = {
        'Content-Type': 'application/json'
    }
    message = none
   # url = 'https://game.linefriends.com/jbp-lcs-ranking/lcs/sendMessage'
    data = {'status':'ok', 'message': message}
    return (json.dumps(data, indent=4, sort_keys=False))
@app.route('/username=<string:un>')
def instaprofile(un):
    uReq = requests
    bSoup = BeautifulSoup
    website = uReq.get("https://www.instagram.com/{}/".format(str(un)))
    data = bSoup(website.content, "lxml")
    for getInfoInstagram in data.findAll("script", {"type":"text/javascript"})[3]:
        getJsonInstagram = re.search(r'window._sharedData\s*=\s*(\{.+\})\s*;', getInfoInstagram).group(1)
        data = json.loads(getJsonInstagram)
        for instagramProfile in data["entry_data"]["ProfilePage"]:
    	    username = instagramProfile["graphql"]["user"]["username"]
    	    name = instagramProfile["graphql"]["user"]["full_name"]
    	    picture = instagramProfile["graphql"]["user"]["profile_pic_url_hd"]
    	    biography = instagramProfile["graphql"]["user"]["biography"]
    	    followers = instagramProfile["graphql"]["user"]["edge_followed_by"]["count"]
    	    following = instagramProfile["graphql"]["user"]["edge_follow"]["count"]
    	    private = instagramProfile["graphql"]["user"]["is_private"]
    	    media = instagramProfile["graphql"]["user"]["edge_owner_to_timeline_media"]["count"]
    	    result = {
    			"result": {
    				"username": username,
    				"fullname": name,
    				"bio": biography,
    				"followers": followers,
    				"following": following,
    				"media": media,
    				"private": private,
    				"profile_img": picture
    			}
    		}
    	    return(json.dumps(result, indent=4, sort_keys=False))
@app.route('/template' ,methods=['POST'])
def out():
    test = [{"type": "template","altText": "testing","template": {"type": "image_carousel","columns": [{"imageUrl": "https://image.ibb.co/b9JR5p/20180811_194145.png","action": {"type": "uri","uri": "http://line.me/ti/p/~devilblack86","area": {"x": 520,"y": 0,"width": 520,"height": 1040}}}]}}]
    data = {
        'status':'OK',
        'message':test
    }
    return(json.dumps(data, indent=4, sort_keys=False))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

