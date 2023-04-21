from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    version = ['1', '2']
    context = {
        'versions': version,
        'modloaders': ['Forge', 'não sei']
    }

    return render_template("homepage.html", context=context)


if __name__ == '__main__':
    app.run(debug=True)
