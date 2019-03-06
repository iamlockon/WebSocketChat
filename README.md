# WebsocketChat

A Django Channels Web App. Just for learning Django/Python/Javascript.

# Usage

You need to set up database connection first in chat/settings.py and relevant files.

Then, run channel layer's back store:
```
#docker run -p 6379:6379 -d redis:2.8
```
Finally, cd into the "chat" directory and run the app with following command:
```
#python3 manage.py runserver 0.0.0.0:8000
```
Then, open a browser window, type localhost:8000/chatapp in address bar..
You should see this login page:

![Login Page](/Login.png?raw=true "Optional Title")

In the chat lobby:

![Lobby](/ChatRoomList.png?raw=true "Optional Title")

In the chat room:

![Chat room](/ChatRoom.png?raw=true "Optional Title")
# Disclaimer
The original code of the chat app comes from Django Channels tutorial:
https://channels.readthedocs.io/en/latest/tutorial/index.html
