from flask import Flask, render_template, request, send_file, after_this_request
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

        try:
            # Comando FFmpeg seguro
            subprocess.run([
                "ffmpeg",
                "-y",
                "-i", input_file,
                # Crop simplificado 9:16 + scale 1080x1920
                "-vf", "crop='min(iw,ih*9/16)':ih:(iw-(min(iw,ih*9/16)))/2:0,scale=1080:1920",
                "-preset", "veryfast",
                output_file
            ], stderr=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as e:
            # Salva log de erro caso dê problema
            error_log = f"ffmpeg_error_{uuid.uuid4()}.log"
            with open(error_log, "wb") as f:
                f.write(e.stderr)
            return f"Erro ao processar o vídeo. Log salvo em {error_log}", 500

        # Cleanup após envio
        @after_this_request
        def cleanup(response):
            try:
                os.remove(input_file)
                os.remove(output_file)
            except Exception:
                pass
            return response

        return send_file(output_file, as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    app.run()
