from flask import render_template,request,redirect,url_for
from youtube_app.youtube import YouTube
from youtube_app import app

@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        channel_name = request.form['channel']
        youtube = YouTube()
        res = youtube.search_video(q=channel_name)
        return render_template('channel_list.html',res=res['items'])
    else:
        return render_template('home.html')

@app.route('/url_list',methods=['GET','POST'])
def url_list():
    if request.method=='POST':
        channelId = request.form['channelId']
        youtube = YouTube()
        res = youtube.search_video(channel=channelId)
        data = []
        data.extend(res['items'])
        while res['nextPageToken']:
            tkn = res.get('nextPageToken')
            res = youtube.search_video(channel=channelId,tkn=tkn)
            data.extend(res['items'])
        return render_template('url_list.html',data=data)
    else:
        return redirect('/')

