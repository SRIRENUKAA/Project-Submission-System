import urllib.parse
import os

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

username = "srirenu2004"
password = "oDvtE1cUkcS4FgtW"
cluster = "cluster2"

escaped_username = urllib.parse.quote_plus(username)
escaped_password = urllib.parse.quote_plus(password)

MONGO_URI = f"mongodb+srv://srirenu2004:oDvtE1cUkcS4FgtW@cluster2.8yt1ddx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster2"
