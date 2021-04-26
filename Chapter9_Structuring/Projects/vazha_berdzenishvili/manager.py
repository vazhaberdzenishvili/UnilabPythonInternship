from app import app
from flask import render_template
from app import pages


@app.route('/')
def home():
    return render_template("home.html", pages=pages)


if __name__ == "__main__":
    app.run(debug=True, port=8885)
