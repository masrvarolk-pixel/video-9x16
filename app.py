from flask import Flask, render_template, request, send_file
import subprocess
import uuid
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video = request.files["video"]

        input_file = f"input_{uuid.uuid4()}.mp4"
        output_file = f"output_{uuid.uuid4()}.mp4"

        video.save(input_file)

        subprocess.run([
            "ffmpeg",
            "-y",
            "-i", input_file,
            "-vf", "crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=1080:1920",
            "-preset", "veryfast",
            output_file
        ], check=True)

        os.remove(input_file)
        return send_file(output_file, as_attachment=True)

    return render_template("index.html")
