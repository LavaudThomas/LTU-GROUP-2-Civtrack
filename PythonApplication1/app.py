from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello Civic Track"

if __name__ == "__main__":
    print("Flask starting...")
    app.run(debug=True, use_reloader=False)