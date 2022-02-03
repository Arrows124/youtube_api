#!/usr/bin/python
from flask import Flask,render_template,request,redirect
import sqlite3
import httplib2
import os
import sys

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow


# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the Google API Console at
# https://console.developers.google.com/.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secrets.json"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.

MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the API Console
https://console.developers.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
  message=MISSING_CLIENT_SECRETS_MESSAGE,
  scope=YOUTUBE_READ_WRITE_SCOPE)

storage = Storage("%s-oauth2.json" % sys.argv[0])
credentials = storage.get()

if credentials is None or credentials.invalid:
  flags = argparser.parse_args()
  credentials = run_flow(flow, storage, flags)

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
  http=credentials.authorize(httplib2.Http()))

# This code creates a new, private playlist in the authorized user's channel.
videos_list_responses = youtube.videos().list(
        myRating="like",
        part="snippet,status",
        maxResults=50
    ).execute()

dbname = 'goodvideos.db'
#youtubeAPIにより最新45個高評価の動画を取得し、データベースに登録
for count in range(45):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO videos(title ,thumbnail, video_id) values(?,?,?)',(videos_list_responses['items'][count]['snippet']['title'],videos_list_responses['items'][count]['snippet']['thumbnails']['default']['url'],videos_list_responses['items'][count]['id']))
    conn.commit()

    cur.close()
    conn.close()


app = Flask(__name__)
@app.route("/",methods=["GET", "POST"])
def search():
    if request.method == "POST":
        keyword = request.form.get("keyword")
        if not keyword:
            return redirect("/")
         
        keyword='%'+keyword+'%'
        #データベースに接続し、検索ワードを含む動画を取得
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
        cur.execute("SELECT title, thumbnail, video_id FROM videos WHERE title LIKE ? GROUP BY title",(keyword,))
        result_videos=cur.fetchall()
        return render_template("index.html",result_videos=result_videos)
    else:
        return render_template("search.html")#login.html


@app.route("/index")
def index():
    return render_template("index.html",result_videos=result_videos)


if __name__ == "__main__":
    app.run(debug=True)
