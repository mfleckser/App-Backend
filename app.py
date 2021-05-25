from flask import Flask, request, json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return f"id: {self.id}, un: {self.username}, pw: {self.password}"

@app.route("/api/new-account", methods=["POST"])
def new_account():
    request_data = json.loads(request.data)
    uname = request_data["username"]
    pword = request_data["password"]

    new_user = User(username=uname, password=pword)

    if(len(User.query.filter_by(username=uname).all()) > 0): # username taken
        return {"400": "Username already taken"}

    db.session.add(new_user)
    db.session.commit()

    print("Added")

    return {"201": "Added new user"}

@app.route("/")
def index():
    return "Hello world"

if __name__ == "__main__":
    app.run()