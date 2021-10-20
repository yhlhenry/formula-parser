from flask import Flask, render_template

app = Flask(__name__)

@app.route("/") ##www.domain.com
def index():


    return render_template("index.html")

@app.route("/parse", methods=['GET', 'POST'])
def select_records():
    if request.method == 'POST':
        # 偷看一下 request.form 
        print(request.form)
        python_records = web_select_specific(request.form)
        return render_template("show_records.html", html_records=python_records)
    else:
        return render_template("select_records.html")

if __name__ == "__main__":

    app.run(debug=False)