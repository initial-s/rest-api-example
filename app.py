from flask import Flask, request, abort, redirect, jsonify
from datetime import datetime
import requests, json, re, pafy, sys, os, base64
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

@app.route('yt-search=<ytsearch>', methods=['GET'])
def ytsearch():
    hasil = []
    hasilnya = {"creator":"Initial_S","result": hasil}
    url = requests.get("https://www.youtube.com/results?search_query={}".format(ytsearch))
    soup = BeautifulSoup(url.content, 'html5lib')
    data = soup.findAll('h3' ,{'class':"yt-lockup-title"})
    for hasil in data:
        title = "{}".format(str(hasil.find('a')['title']))
        link = "https://m.youtube.com{}".format(str(hasil.find('a')['href']))
        id = "id: {}".format(str(hasil.find('a')['href'].replace('/watch?v=','')))
        hasil.append({"title": title,"link": link,"id": id})
   return jsonify(hasilnya)
@app.route('/bmkg', methods=['GET'])
def bmkg():
    r = requests.get('https://inatews.bmkg.go.id/light/?')
    citl = BeautifulSoup(r.content,'html5lib')
    info = citl.find('div',{'class':'col-md-12'}).find('h4').text
    saran = citl.findAll('div',{'class':'col-sm-6'})[1].find('h5').text
    result = {
        "info": info,
        "saran": saran
    }
    return jsonify(result)
@app.route('/zodiak=<zodiak>', methods=['GET'])
def zodiak(zodiak):
    
    r = requests.get('https://kuis.online/ramalan-zodiak?bintang={}'.format(zodiak))
    citl = BeautifulSoup(r.content,'html5lib')
    sri = citl.findAll('div',{'class':'col-md-12'})
    hasil = "Ramalan Zodiak {} Hari Ini\n".format(zodiak)
    for citl in sri:
        hasil += citl.find('small').text
        thumbnail = "https://kuis.online/images/zodiak/{}.gif".format(zodiak)
        result = {
            "creator": "Initial_S",
            "result":  hasil,
            "thumbnail": thumbnail
        }
        return jsonify(result)
@app.route('/joox-search=<query>', methods=['GET'])
def jooxlist(query):
    hasil = []
    url = requests.get("http://api-jooxtt.sanook.com/web-fcgi-bin/web_search?country=id&lang=id&search_input={}&sin=1&ein=30".format(str(query)))
    data = url.text
    data = json.loads(data)
    result = {"status": "succes","Creator":"Initial_S","result": hasil}
    for music in data['itemlist']:
        judul = base64.b64decode(music['info1']).decode('utf-8')
        songid = music['songid']
        hasil.append({"judul": judul,"songid": songid})
    return jsonify(result)
@app.route('/songid=<sid>', methods=['GET'])
def joox(sid):
    url = requests.get("http://api-jooxtt.sanook.com/web-fcgi-bin/web_get_songinfo?country=id&lang=id&songid={}".format(sid))
    data = url.text
    data = json.loads(data)
    artis = data['msinger']
    song = data['msong']
    single = data['malbum']
    mp3 = data['mp3Url']
    img = data['imgSrc']
    result = {
        "Joox-Api-By": "Initial_S",
        "result": [
            {
                "artis": artis,
                "judul": song,
                "single":single,
                "mp3Url": mp3,
                "imgUrl": img
            }
        ]
    }
    return jsonify(result)
@app.route('/downloadsmule=https://www.smule.com/p/<key>', methods=['GET'])
def smule(key):
    url = requests.get("https://www.smule.com/p/{}".format(key))
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
    return jsonify(result)
@app.route('/ytdownload=<link>', methods=['GET'])
def ytdownload(link):
    url = requests.get("http://saveoffline.com/process/?url={}&type=json".format(link))
    hasil = url.text
    data = json.loads(hasil)
    return jsonify(data)
@app.route('/infoig=<un>', methods=['GET'])
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
    	    return jsonify(result)

@app.route('/igstory=<username>', methods=['GET'])
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
    return jsonify(result)

@app.route('/postig=<usn>', methods=['GET'])
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
    return jsonify(datas)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)
