from flask import  Flask,render_template,request,jsonify,session,redirect
import  os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/",methods=["POST","GET"])
def main_handle():
    if request.method == "GET":
         return render_template("./home/home.html")

@app.route("/login.html",methods=["POST","GET"])
def login_handle():
    if request.method == "GET":
        return render_template("./home/login.html")



if __name__ == "__main__":
    app.run(port=80, debug=True)

