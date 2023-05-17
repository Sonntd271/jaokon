from flask import Flask, render_template, redirect, url_for, request
import json

DEFAULT_STATUS = {
    'status': 0, 
    'face': "", 
    'note': "",
    'prev_note': "",
    'note_index': 0,
    'song': "",
    'playback' : False
}

DEFAULT_DIRECT = {
    'next_page': "", 
    'next_image': "", 
    'next_audio': "",
    'note_index': -1,
    'current_image': "",
    'current_audio': "",
}

ERROR_STATUS = {
    'status': -1,
    'face': "", 
    'note': "",
    'prev_note': "",
    'note_index': 0,
    'song': "",
    'playback' : False
}

SONG_DURATION ={
    "twinkle": 15,
    "mary": 18,
    "macdonald": 20,
    "ode": 22,
    "die4you": ["mi","mi","mi","re","sol","fa","mi","re","do","re","mi","sol","mi"],
    "hbd": 24
}

app = Flask(__name__)

def read_page_direction():
    try:
        f = open("./static/pageDirect.json")
        page_direct = json.load(f)
    except FileNotFoundError:
        with open("./static/pageDirect.json", "w") as outfile:
            json.dump(DEFAULT_DIRECT, outfile)
        f = open("./static/pageDirect.json")
        page_direct = json.load(f)
    finally:
        return page_direct

def update_status_to_direct():
    page_direct = read_page_direction()
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
        print("step 1")
        page_direct["current_image"] = page_direct["next_image"]
        page_direct["current_audio"] = page_direct["next_audio"]
        if current_status["status"] == 1:
            if len(current_status["face"]) > 0:
                print("face")
                page_direct["next_page"] = "face"
                page_direct["next_image"] = current_status["face"]
            else:
                print("interaction")
                page_direct["next_page"] = "interaction"
                page_direct["next_image"] = ""
            page_direct["next_audio"] = ""
        elif current_status["status"] == 2:
            if current_status["playback"]:
                    print("song")
                    page_direct["next_page"] = "song"
                    page_direct["next_image"] = ""
                    page_direct["next_audio"] = current_status["song"]
            elif len(current_status["note"]) > 0:
                if page_direct["note_index"] != current_status["note_index"]:
                    print("sound")
                    page_direct["next_page"] = "note_audio"
                    page_direct["next_image"] = current_status["note"][0]
                    page_direct["next_audio"] = current_status["prev_note"]
                else:
                    print("no sound")
                    page_direct["next_page"] = "note"
                    page_direct["next_image"] = current_status["note"][0]
                    page_direct["next_audio"] = current_status["prev_note"]
            else:
                print("music page")
                page_direct["next_page"] = "music"
                page_direct["next_image"] = ""
                page_direct["next_audio"] = ""
        elif current_status["status"] == 0:
            print("no status")
            page_direct["next_page"] = ""
            page_direct["next_image"] = ""
            page_direct["next_audio"] = ""
        elif current_status["status"] == 3:
            print("close")
            page_direct["next_page"] = "close"
            page_direct["next_image"] = ""
            page_direct["next_audio"] = ""
        else:
            print("error")
            page_direct["next_page"] = "error"
            page_direct["next_image"] = ""
            page_direct["next_audio"] = ""
        page_direct["note_index"] = current_status["note_index"]
        with open("./static/pageDirect.json", "w") as outfile:
            json.dump(page_direct, outfile)

def get_page_direction():
    update_status_to_direct()
    return read_page_direction()
            
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", pageDirect=get_page_direction())

@app.route("/error", methods=["GET"])    
def error():
    return render_template("error.html", pageDirect=get_page_direction())

@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", pageDirect=get_page_direction()), 404

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

@app.route("/note_audio", methods=["GET"])
def note_audio():
    return render_template("note_audio.html", pageDirect=get_page_direction())

@app.route("/song", methods=["GET"])
def song():
    f = open("./static/currentStatus.json")
    current_status = json.load(f)
    song_name = current_status["song"]
    return render_template("song.html", pageDirect=get_page_direction(), songDuration = SONG_DURATION[song_name])