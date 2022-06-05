import logging
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
# Certain flows and features require a session. In our case, our use of "flash()" requires us to set a secret key, else we get
# RuntimeError: The session is unavailable because no secret key was set.  Set the secret_key on the application to something unique and secret.
app.secret_key = "dontthrowsomerandomlygeneratedkeyasyoudinvalidatesessionsoneachrestart"
app.logger.setLevel(logging.DEBUG)

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/override", methods=["GET"])
def random_page():
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Coming...</h1>
    """

@app.route("/override", methods=["POST"])
def upload_file_vulnerable_to_override():
    """
    Each value in `request.files` is a https://tedboy.github.io/flask/generated/generated/werkzeug.FileStorage.html
    The key is based on the name of the file "input".
    """
    app.logger.info(request.files)
    if "uploaded_file" not in request.files:
        flash("No file part")
        return redirect(url_for("home")) #redirect(request.url)
    
    uploaded = request.files["uploaded_file"]
    if uploaded.filename == "":
        flash("Browser sent an empty file because you didn't select one")
        return redirect(url_for("home")) #redirect(request.url)
    
    app.logger.info(f"content type: {uploaded.content_type}. content length: {uploaded.content_length}")
    uploaded.save(uploaded.filename)
    return redirect(url_for("home"))


if __name__=="__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
