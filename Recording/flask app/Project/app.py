from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', method=['GET'])
def hello_word():
    return render_template('C:\\Users\\HP\\Desktop\\Project\\Recording\\flask app\\Project\\template\\index.html')


if __name__ == '__main__':
    app.run(port=3000, debug=True)