import sqlite3

dbname = 'goodvideos.db'
conn = sqlite3.connect(dbname)
# sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

# personsというtableを作成してみる
# 大文字部はSQL文。小文字でも問題ない。
# データベースへコミット。これで変更が反映される。
conn.commit()
conn.close()
