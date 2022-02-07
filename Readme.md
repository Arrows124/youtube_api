# Youtube高評価検索ツール(メインはapp.pyです)

Video Demo: https://youtu.be/wMm0Ux_k8FQ

# Description
It is a web application that allows you to search highly rated youtube videos based on search keywords using the framework Flsak. I often watch youtube, but when I want to look back on the videos that I highly rated in the past, there are too many highly rated videos and it is difficult to find them. Therefore, I want to make a web application that can search highly rated youtube videos.

1 Use the Youtube API to get information about highly rated videos (python)

2 Insert information about the highly rated video into the SQL table (SQL, python)

3 Set up a search form on the home screen of the Web application and use the SELECT statement to acquire videos related to the keyword (SQL, python, HTML).

# Directory and files

application/

┣ client_secrets.json (APIを利用するためのjson形式のファイル)

┣ goodvideos.db (高評価動画のデータベース)

┣ run.py　(プログラム実行用のファイル)

┣ run.py-oauth2.json (API OAuth2を利用するためのjson形式のファイル)

┣ app/

　　　　└ ┣ app.py (webアプリのメインの部分。それぞれのルートに対する処理はここでコードされている)

┣ create_db.py (SQLでデータベースを作るためのpythonのファイル)

┣ create_table.py (SQLでtableを作るためのpythonのファイル)

┣ templates/

└ ┣ index.html　(検索結果を表示するhtml)

┣ layout.html (レイアウト用のhtml)

┣ search.html (検索フォームがコードされたhtml)

# The details of the main app.py

The first few lines import modules used for flask, sqlite3, youtube API, etc. After that, code as described in How to use youtube api. Store what was executed by youtube.videos (). list (myRating = "like", part = "snippet, status", maxResults = 50) .execute () in videos_list_responses. This execution result gets all the information of the highly rated video through the API. Next, name the database created with create_db.py dbname, get the title, thumbnail and video ID of the highly rated video you got earlier, and insert it into the SQL table created with create_table.py.

After that, it is coded to create a flask object and perform different processing depending on the route.

If the root is ("/"), when you receive the GET method, get the title, thumbnail, and video ID of the video related to that keyword from the database table based on the keyword obtained from the search form, and index.html Display the results using.

When the POST method is received, the search form described in search.html will be displayed.

If the route is ("/ index"), index.html will be displayed. I wanted to get the highly rated videos of each user using google login, but I gave up because it was difficult for me.
