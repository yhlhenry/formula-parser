from flask import Flask, render_template

app = Flask(__name__)

@app.route("/") ##www.domain.com
def index():


    return render_template("index.html")


if __name__ == "__main__":

    app.run(debug=False)