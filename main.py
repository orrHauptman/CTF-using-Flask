from flask import Flask , request , render_template , redirect , url_for , session
import base64
from datetime import datetime
import socket
clues: dict = {
    "/ Clue" : base64.b64encode("Well done! But top programers don't need clues!!!!".encode()).decode(),
    "title clue" : base64.b64encode("I love robots (;".encode()).decode()
}


app = Flask(__name__)
app.secret_key = "pakscmopdva0dgyv9182762akxzxc1"

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

#stage 3
def send_UDP_packet(message : str):
    client = socket.socket(socket.AF_INET ,socket.SOCK_DGRAM)
    client.connect(("127.0.0.1" ,9912 ))
    client.send(message.encode())

#stage 4 
@app.route("/711")
def fake_stage4():
    return "You need to be in the night_shift directory"

@app.route("/night_shift/711" , methods = ["POST" , "GET"])
def stage4():

    if request.method == "POST":
        user_password = request.form["password"]
        if user_password == "91245":
            session["pass"] = True
        else:
            session["pass"] = False

        return redirect(url_for("check_password" ))
    
    return render_template("password.html")


@app.route("/night_shift/pass")
def check_password():
    if "pass" in session and session["pass"]:
        return render_template("in_development.html")
    return redirect(url_for("stage4"))

if __name__ == "__main__":
    app.run(debug=True)

