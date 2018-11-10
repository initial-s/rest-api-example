from flask import Flask
from datetime import datetime
import requests, json, re
from re import match
from bs4 import BeautifulSoup
app = Flask(__name__)

@app.route('/') #https://yourdomain.com/
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

@app.route('/downloadsmule=https://www.smule.com/p/<string:key>')
def smule(key):
    url = requests.get('https://www.smule.com/p/{}'.format(key))
    soup = BeautifulSoup(url.content, 'html5lib')
    image = soup.find(attrs={"name": "twitter:image:src"})['content']
    meta = soup.find(attrs={"name": "twitter:player:stream"})['content']
    meta2 = soup.find(attrs={"name": "twitter:description"})['content'].replace('amp;','')
    result = {
        "status": "succes",
        "creator": "initial_s",
        "result":[
            {
                "image": image,
                "url": meta,
                "description": meta2
            }
        ]
    }
    return(json.dumps(result, indent=4, sort_keys=False))

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
                "Creator": "Initial_S",
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
@app.route('/igstory=<string:username>')
def igtory(username):
    r = requests.get("https://saveig.com/?link={}".format(username))
    soup = BeautifulSoup(r.content,"lxml")
    result=[]
    try:
        data = soup.findAll('div',{'class':'line'})
        result = []
        for hasil in data:
            video = hasil.find('video')['src']
            result.append({'video':video})
    except:
        data = soup.findAll('div',{'class':'line'})
        for hasil in data:
            image=hasil.find('img')['src']
            result.append({'image':image})
    return(json.dumps(result, indent=4, sort_keys=False))
@app.route('/postig=<string:usn>')
def instapost(usn):
    datas = []
    #result = {'status':'ok'}, data=datas
    link = 'https://instagram.com/{}'.format(usn)
    r = requests.get(link)
    soup = BeautifulSoup(r.content,"lxml")
    for getInfoInstagram in soup.findAll("script", {"type":"text/javascript"})[3]:
        getJsonInstagram = re.search(r'window._sharedData\s*=\s*(\{.+\})\s*;', getInfoInstagram).group(1)
        data = json.loads(getJsonInstagram)
        for insta in data["entry_data"]["ProfilePage"]:
            md = insta["graphql"]["user"]
            md = md["edge_owner_to_timeline_media"]
            for post in md["edges"]:
                url = post["node"]["display_url"]
                video = post["node"]["is_video"]
                datas.append({'url':url,'vid':video})
    return(json.dumps(datas, indent=4, sort_keys=False))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

