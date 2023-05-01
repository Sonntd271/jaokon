from flask import Flask, render_template, redirect, url_for, request
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
            if len(current_status["face"]) > 0:
                page_direct["page"] = "face"
            else:
                page_direct["page"] = "interaction"
        elif current_status["status"] == 2:
            if len(current_status["note"]) > 0:
                page_direct["page"] = "note"
            else:
                page_direct["page"] = "music"
        elif current_status["status"] == 0:
            page_direct["page"] = ""
        elif current_status["status"] == 3:
            page_direct["page"] = "close"
        else:
            page_direct["page"] = "error"
        page_direct["face"] = current_status["face"]
        page_direct["note"] = current_status["note"]
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

@app.route("/interaction", methods=["GET"])
def interaction():
    return render_template("interaction.html", pageDirect=get_page_direction())

@app.route("/face", methods=["GET"])    
def face():
    return render_template("face.html", pageDirect=get_page_direction())

@app.route("/music", methods=["GET"])
def music():
    return render_template("music.html", pageDirect=get_page_direction())

@app.route("/note", methods=["GET"])
def note():
    return render_template("note.html", pageDirect=get_page_direction())
