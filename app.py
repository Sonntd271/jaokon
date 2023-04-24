from flask import Flask, render_template, request
import json

DEFAULT_STATUS = {
    'status': 0, 
    'face': "", 
    'note': ""
}

DEFAULT_DIRECT = {
    "mode": "",
    "page": ""
}

ERROR_STATUS = {
    "status": -1,
    "face": "", 
    "note": ""
}

app = Flask(__name__)

def get_page_direction():
    page_direct = {}
    try:
        f = open("./static/currentStatus.json")
        current_status = json.load(f)
    except FileNotFoundError:
        with open("./static/currentStatus.json", "w") as outfile:
            json.dump(DEFAULT_STATUS, outfile)
        f = open("./static/currentStatus.json")
        current_status = json.load(f)
    except:
        with open("./static/currentStatus.json", "w") as outfile:
            json.dump(ERROR_STATUS, outfile)
        f = open("./static/currentStatus.json")
        current_status = json.load(f) 
    finally:
        if current_status["status"] == 1:
            page_direct["mode"] = "interaction"
            if len(current_status["face"]) > 0:
                page_direct["page"] = "/"+current_status["face"]
            else:
                page_direct["page"] = ""
        elif current_status["status"] == 2:
            page_direct["mode"] = "music"
            if len(current_status["note"]) > 0:
                page_direct["page"] = "/"+current_status["note"]
            else:
                page_direct["page"] = ""
        elif current_status["status"] == 0:
            page_direct["mode"] = ""
            page_direct["page"] = ""
        elif current_status["status"] == 3:
            page_direct["mode"] = "close"
            page_direct["page"] = ""
        else:
            page_direct["mode"] = "error"
            page_direct["page"] = ""
        with open("./static/pageDirect.json", "w") as outfile:
            json.dump(page_direct, outfile)
        f = open("./static/pageDirect.json")
        result = json.load(f)
        return result
            
# Index
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", pageDirect=get_page_direction())

@app.route("/error", methods=["GET"])    
def error():
    return render_template("error.html", pageDirect=get_page_direction())

@app.route("/close", methods=["GET"])    
def close():
    with open("./static/pageDirect.json", "w") as outfile:
        json.dump(DEFAULT_DIRECT, outfile)
    with open("./static/currentStatus.json", "w") as outfile:
        json.dump(DEFAULT_STATUS, outfile)
    return render_template("close.html")

#Emotions
@app.route("/interaction", methods=["GET"])
def interaction():
    return render_template("interaction.html", pageDirect=get_page_direction())

@app.route("/interaction/happy", methods=["GET"])    
def happy():
    return render_template("interaction/happy.html", pageDirect=get_page_direction())

@app.route("/interaction/sad", methods=["GET"])    
def sad():
    return render_template("interaction/sad.html", pageDirect=get_page_direction())

@app.route("/interaction/angry", methods=["GET"])    
def angey():
    return render_template("interaction/angry.html", pageDirect=get_page_direction())

@app.route("/interaction/disgusted", methods=["GET"])    
def disgusted():
    return render_template("interaction/disgusted.html", pageDirect=get_page_direction())

@app.route("/interaction/fearful", methods=["GET"])    
def fearful():
    return render_template("interaction/fearful.html", pageDirect=get_page_direction())

@app.route("/interaction/neutral", methods=["GET"])    
def neutral():
    return render_template("interaction/neutral.html", pageDirect=get_page_direction())

#Musiccal notes
@app.route("/music", methods=["GET"])
def music():
    return render_template("music.html", pageDirect=get_page_direction())

@app.route("/music/do", methods=["GET"])
def do():
    return render_template("music/do.html", pageDirect=get_page_direction())

#Images