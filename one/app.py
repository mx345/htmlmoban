from flask import  Flask,render_template,request,jsonify,session,redirect,abort,Response
import  os,re
import pymysql 
app = Flask(__name__)
app.secret_key = os.urandom(24)

db =pymysql.connect("47.103.50.75","mx123","123456","my_shop")
@app.route("/",methods=["POST","GET"])
def main_handle():
    if request.method == "GET":
        return render_template("./home/home.html")

@app.route("/login",methods=["POST","GET"])
def login_handle():
    if request.method == "GET":
        return render_template("./home/login.html")
    elif request.method == "POST":
        pwd = request.form.get("password")
        phone = request.form.get("phone")
        print(phone)
        print(pwd)

        return render_template("./home/index.html")

@app.route("/reg", methods=["GET", "POST"])
def reg():
    if request.method == "GET":
        return render_template("./home/reg.html")
    elif request.method == "POST":
        uname = request.form.get("uname")
        pwd = request.form.get("password")
        pwd2 = request.form.get("password2")
       
        if not re.match("^([a-zA-Z0-9_@.]){4,20}$", uname):

            return "注册失败，用户名格式错误！"
        if not re.match("^[0-9]{1}([a-zA-Z0-9]|[._]){6,15}$", pwd):
            return "密码格式错误"
        if pwd != pwd2:
            return "密码输入不一致"
        # if not re.match("^[1][3,4,5,7,8][0-9]{9}$", phone):
        #     return "手机格式不对"

        # if not user_reg_login.user_reg(uname, pwd, phone, email):
        #     # 注册失败
        #     return "注册失败，用户名已经存在，请换一个用户名试一下！"
        # else:
        #     # 注册成功
        try:
            cur = db.cursor()
            cur.execute("INSERT INTO sp_user VALUES (default, %s, md5(%s), sysdate(), sysdate(), '1', '1')", (uname, uname + pwd))
            cur.close()
            db.commit()
        except:
            abort(Response("用户注册失败！"))

        
        # 注册成功就跳转到登录页面
        
        return render_template("./home/login.html")


@app.route("/user_center", methods=["GET", "POST"])
def user_center():
    if request.method == "GET":
        return render_template("./home/index.html")


@app.route("/collection", methods=["GET", "POST"])
def collection():
    if request.method == "GET":
        return render_template("./home/collection.html")



if __name__ == "__main__":
    app.run(port=80, debug=True)

