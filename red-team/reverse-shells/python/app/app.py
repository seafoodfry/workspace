import logging
import subprocess
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/inject", methods=["POST"])
def code_injection():
    """
    https://werkzeug.palletsprojects.com/en/2.1.x/datastructures/#werkzeug.datastructures.ImmutableMultiDict
    """
    app.logger.info(request.form)
    fname = request.form["firstname"]
    lname = request.form["lastname"]
    # The not-commented out version is not vulnerable to command injections.
    result = subprocess.run([f"./some-cli {fname} {lname}"], stdout=subprocess.PIPE, shell=True)
    #result = subprocess.run(["./some-cli", f"{fname} {lname}"], stdout=subprocess.PIPE)
    if result.returncode != 0:
        return "error", 500
    app.logger.info(result.stdout.decode("utf-8"))
    return render_template("home.html", output=result.stdout)


if __name__=="__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
