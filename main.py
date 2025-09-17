from flask import Flask , request , render_template
import base64
from datetime import datetime
import socket
clues: dict = {
    "/ Clue" : base64.b64encode("Well done! But top programers don't need clues!!!!".encode()).decode(),
    "title clue" : base64.b64encode("I love robots (;".encode()).decode()
}


app = Flask(__name__)

def get_path():
    url = request.url

    if "<" in url or ">" in url : 
        return " < and > are not allowed to be part of the path "
    
    return url

#base functionality 
@app.route("/<path:path>")
def echo_path(path):
    return get_path()

#home
@app.route("/")
def index_html():
    return render_template("index.html" , fake_clue = clues["/ Clue"] , real_clue = clues["title clue"]) 


#stage 1 
@app.route("/robots.txt")
def stage1():
    return render_template("robots.txt" )

#stage 2

@app.route("/night_shift")
def stage2():
    now = datetime.now()

    if now.hour == 5:
        
        send_UDP_packet("Go to /number .number is the last number printed on the screen")

        return render_template("night_shift.html")
    
    return "The night shift starts at 5:00 and ends in 6:00 "


def send_UDP_packet(message : str):
    client = socket.socket(socket.AF_INET ,socket.SOCK_DGRAM)
    client.connect(("127.0.0.1" ,9912 ))
    client.send(message.encode())



if __name__ == "__main__":
    app.run()

