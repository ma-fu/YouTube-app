from flask import render_template,request,redirect,url_for
from youtube_app.youtube import YouTube
from youtube_app import app
import csv, tempfile

def write_csv(title_url):
	temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv',mode='w+t',newline='')
	with open(temp_file.name,'w',newline='') as file:
		writer= csv.writer(file)
		writer.writerow(['Title','videoId'])
		writer.writerows(title_url)
	return temp_file.name

@app.route('/',methods=['GET','POST'])
def home():
	if request.method=='POST':
		channel_name = request.form['channel']
		youtube = YouTube()
		tips = youtube.get_tips(q=channel_name)
		res = youtube.search_video(tips)
		return render_template('channel_list.html',res=res['items'])
	else:
		return render_template('home.html')

@app.route('/url_list',methods=['GET','POST'])
def url_list():
	if request.method=='POST':
		channelId = request.form['channelId']
		youtube = YouTube()
		tips = youtube.get_tips(channel=channelId)
		res = youtube.search_video(tips)
		data = []
		data.extend(res['items'])
		tkn = res.get('nextPageToken')
		while tkn:
			tips = youtube.get_tips(channel=channelId,tkn=tkn)
			res = youtube.search_video(tips)
			data.extend(res['items'])
			tkn = res.get('nextPageToken')
		title_url = []
		for d in data:
			title = d['snippet']['title']
			videoId = d['id']['videoId']
			title_url.append([title,videoId])
		temp_file = write_csv(title_url)

		return render_template('url_list.html',temp_file=temp_file)
	else:
		return redirect('/')

@app.route('/download/<file_name>')
def download(file_name):
	return send_file(file_name, as_attachment=True)
