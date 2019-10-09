import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, abort, Response, url_for
import  os,re
import pymysql 
app = Flask(__name__)

app.secret_key = b'\xa3P\x05\x1a\xf8\xc6\xff\xa4!\xd2\xb5\n\x96\x05\xed\xc3\xc90=\x07\x8d>\x8e\xeb'
db =pymysql.connect("47.103.50.75","mx_shop","123456","mydb1")

@app.route("/",methods=["POST","GET"])
def main_handle():
    if request.method == "GET":
        # if  session : 
        #     user_info = session.get("user_info")
        #     return render_template("./home/home.html",uname = user_info.get("uname"))
        #uname = user_info.get("uname"
        return render_template("./home/home.html")


# @app.route("/d", methods=["POST", "GET"])
# def mainhandle():
#     if request.method == "GET":
#         user_info = session.get("user_info")
#
#     # if user_info:
#         return render_template("./home/home.html",uname = user_info.get("uname"))
#

@app.route("/reg", methods=["GET", "POST"])
def reg():
    if request.method == "GET":
        return render_template("./home/reg.html")
    elif request.method == "POST":
        uname = request.form.get("uname")
        pwd = request.form.get("password")
        pwd2 = request.form.get("password2")
        print(uname,type(uname))
        print(pwd)
        print(pwd2)
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





@app.route("/login", methods=["GET", "POST"])
def login_handle():
    if request.method == "GET":
        return render_template("./home/login.html")
    elif request.method == "POST":
        uname = request.form.get("uname")
        upass = request.form.get("password")

        if not (uname and uname.strip() and upass and upass.strip()):
            abort(Response("登录失败！"))
        if not re.fullmatch("[a-zA-Z0-9_]{4,20}", uname):
            abort(Response("用户名不合法"))
        if not (len(upass) >= 6 or len(upass) <= 15):
            abort(Response("密码错误"))

        cur = db.cursor()
        cur.execute(
            "select * from sp_user where uname=%s and upass=md5(%s) ", (uname, uname+upass))
        res = cur.fetchone()
        cur.close()
        if res:
            cur_login_time = datetime.datetime.now()
            session["user_info"] = {

                "uid": res[0],
                "uname": res[1],
                "upass": res[2],
                "reg_time": res[3],
                "last_login_time": res[4],
                "priv": res[5],
                "state": res[6],
                "login_time": cur_login_time
            }
        try:
            cur = db.cursor()
            cur.execute(
                "update into sp_user set last_login_time=%s where uid =%s ", (cur_login_time, res[0]))
            res = cur.rowcount
            cur.close()
            db.commit()
        except Exception as e:
            print(e)
        print("登录成功！", session)
        return redirect("/")
    else:
            #登录失败
        return render_template("./home/login.html", login_fail=1)


@app.route("/check_uname")
def check_uname():
    uname = request.args.get("uname")
    if not uname:
        abort(500)

    res = {"err": 1, "desc": "用户名没有被注册！"}
    cur = db.cursor()
    cur.execute("select uid FROM sp_user where uname=%s", (uname,))
    if cur.rowcount == 0:
        #用户没有被注册
        res["err"] = 0
        res["desc"] = "用户名没有被注册！"
        cur.close()
        return jsonify(res)
    else:
        #用户名已经被注册
        print(res)
        return jsonify(res)

@app.route("/user_center", methods=["GET", "POST"])
def user_center():
    if request.method == "GET":
        user_info = session.get("user_info")
        print(user_info)
        if user_info:
            return render_template("./home/index.html", uname=user_info.get("uname"))
        else:
            return redirect(url_for("login_handle"))


@app.route("/logout")
def logout_handle():
    res = {"err": 1, "desc": "未登录"}
    if session.get("user_info"):

        print(session.get("user_info")["uname"])
        session.pop("user_info")

        res["err"] = 0
        res["desc"] = "注销成功！"

    return jsonify(res)


@app.route("/collection", methods=["GET", "POST"])
def collection():
    if request.method == "GET":
        return render_template("./person/collection.html")


# @app.route("/user_center")
# def user_center():
#     return render_template("./home/index.html")  # 个人中心


@app.route("/shopcart")
def shopcart():
    return render_template("./home/shopcart.html")  # 购物车


@app.route("/information")
def information():
    return render_template("./person/information.html")  # 个人资料


@app.route("/safety")
def safety():
    return render_template("./person/safety.html")  # 安全设置


@app.route("/address")
def address():
    return render_template("./person/address.html")  # 收货地址


@app.route("/order")
def order():
    return render_template("./person/order.html")    # 订单管理


@app.route("/change")
def change():
    return render_template("./person/change.html")   # 退款售后


@app.route("/coupon")
def coupon():
    return render_template("./person/coupon.html")   # 优惠卷


@app.route("/bonus")
def bonus():
    return render_template("./person/bonus.html")  # 红包


@app.route("/bill")
def bill():
    return render_template("./person/bill.html")  # 账单明细


# @app.route("/collection")
# def collection():
#     return render_template("/person/collection.html")  # 收藏


@app.route("/foot")
def foot():
    return render_template("./person/foot.html")  # 足迹


@app.route("/news")
def news():
    return render_template("./person/news.html")  # 我的消息


@app.route("/comment")
def comment():
    return render_template("./person/comment.html")  # 我的评价

# @app.route("/refund")
# def refund():
#     return render_template("./person/refund.html")


@app.route("/blog")
def blog_handle():
    return render_template("./person/blog.html")



if __name__ == "__main__":
    app.run(port=80, debug=True)

