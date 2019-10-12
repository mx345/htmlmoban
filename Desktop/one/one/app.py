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
        # user_info = session.get("user_info")
        # print(user_info)
        # if user_info:
        return render_template("./home/home.html")
    else:
        so = request.form.get("index_none_header_sysc1")
        print(so)
        cur = db.cursor()
        cur.execute("select * from products where pname=%s limit 0,5",(so,))
        res = cur.fetchall()
        print(res)
        if not res:
            return "没有查询到任何结果"
        cur.close()
        return render_template("./home/search.html", res=res)

        # elif request.method == "POST":
        #     return  render_template("./home/sort.html")


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

#
# @app.route("/check_user")
# def check_user():
#     user_info = session.get("user_info")
#     uid = user_info.get("uid")
#     try:
#         cur = db.cursor()
#         cur.execute("select * from sp_address where uid=%s" % uid)
#         res = cur.fetchall()
#         print(res)
#         cur.close()
#         return render_template("./home/check_user.html", res=res)  # 收货地址
#

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
        user_info = session.get("user_info")
        print(user_info)
        if user_info:
            return render_template("./person/collection.html",uname=user_info.get("uname"))


# @app.route("/user_center")
# def user_center():
#     return render_template("./home/index.html")  # 个人中心



@app.route("/shopcart")
def shopcart():
    user_info = session.get("user_info")
    # print(user_info)
    if user_info:
        cur = db.cursor()
        cur.execute("select * from shop_trolley limit 0,1")
        res = cur.fetchall()

        cur.close()

        if not res:
            return render_template("./home/shopcart.html", uname=user_info.get("uname"))

        return render_template("./home/shopcart.html", uname=user_info.get("uname"), res=res)

        # else:


# @app.route("/delsp")
# def delsp():
#     add = session.get("spca")

#     dname = add.get("pname")[2]
#     print(dname)
#     cur = db.cursor()
#     cur.execute("delete from shop_trolley where tname='%s'" % dname)  # 删除个人地址
#     cur.close()
#     db.commit()
#     return redirect("./home/shopcart.html")




# @app.route("/delshopcart")
# def delshopcart():



@app.route("/information",methods=["POST","GET"])
def information():
    if request.method == "GET":
        user_info = session.get("user_info")
        if user_info:
            return render_template("./person/information.html",uname=user_info.get("uname"))  # 个人资料
    elif request.method == "POST":

         dname = request.form.get("user-name1")
         real_name = request.form.get("user-name2")
         sex = request.form.get("radio10")
         birth_year = request.form.get("year")
         birth_month = request.form.get("month")
         birtn_day = request.form.get("day")
         birth = birth_year + "/"+ birth_month +"/" + birtn_day
         phone = request.form.get("phone")
         email = request.form.get("email")
         try:
             cur = db.cursor()
             cur.execute("INSERT INTO user_information VALUES (DEFAULT ,%s,%s,%s,%s,%s,%s)",(dname,real_name,sex,birth,phone,email))
             cur.close()
             db.commit()
         except:
             abort(Response("插入失败！"))

         return redirect(url_for("user_center"))



@app.route("/safety")
def safety():
    user_info = session.get("user_info")
    print(user_info)
    if user_info:
        return render_template("./person/safety.html",uname=user_info.get("uname"))  # 安全设置


@app.route("/address", methods=["GET", "POST"])
def address():
    if request.method == "GET":
        user_info = session.get("user_info")
        uid = user_info.get("uid")
        try:
            cur = db.cursor()
            cur.execute("select * from sp_address where uid=%s" % uid)
            res = cur.fetchall()
            print(res)
            cur.close()
        except:
            abort(Response("保存失败"))

        return render_template("./person/address.html", res=res)  # 收货地址
    else:
        user_info = session.get("user_info")
        if not user_info:
            abort(Response("未登录！"))
        uid = user_info.get("uid")
        dname = request.form.get("dname")
        phone = request.form.get("dphone")
        shi = request.form.get("shi")
        qu = request.form.get("qu")
        sheng = request.form.get("sheng")
        address = sheng + shi + qu
        daddress = request.form.get("daddress")

        print(uid, dname, phone, daddress, address)
        try:
            cur = db.cursor()
            cur.execute("INSERT INTO sp_address VALUES (default,%s,%s,%s,%s,%s)",
                        (uid, dname, phone, address, daddress))
            cur.close()
            db.commit()
        except:
            abort(Response("保存失败"))
        return "保存成功"


# @app.route("/kaddress", methods=["GET", "POST"])
# def kaddress():
#     if request.method == "GET":
#         try:
#             cur = db.cursor()
#             cur.execute("select * from sp_address")
#             res = cur.fetchall()
#             print(res)
#             cur.close()
#         except:
#             abort(Response("保存失败"))

#         return render_template("./person/address.html",res=res)



@app.route("/kaddress", methods=["GET", "POST"])
def kaddress():
    user_info = session.get("user_info")

    uid = user_info.get("uid")
    print(uid, type(uid))

    try:
        cur = db.cursor()
        cur.execute("select * from sp_address where uid=%s" % uid)
        res = cur.fetchall()
        if not res:
            return render_template("./person/address.html")
        print(res)
        cur.close()
        session["address"] = {
            "dname": res[0]

        }
    except:
        abort(Response("保存失败"))
    return render_template("./person/address.html", res=res)  # 查看个人地址


@app.route("/compile1", methods=["GET", "POST"])
def compile1():
    if request.method == "GET":
        return render_template("./home/compile1.html")
    else:
        user_info = session.get("user_info")
        uid = user_info.get("uid")
        dname = request.form.get("dname")
        phone = request.form.get("dphone")
        shi = request.form.get("shi")
        qu = request.form.get("qu")
        sheng = request.form.get("sheng")
        address = sheng + shi + qu
        daddress = request.form.get("daddress")
        print(uid)
        try:
            cur = db.cursor()
            cur.execute("update sp_address set dname=%s,phone=%s,address=%s,daddress=%s where uid =%s",
                        (dname, phone, address, daddress, uid))

            cur.close()
            db.commit()
        except Exception as e:
            print(e)
        return redirect("/address")


@app.route("/delete")
def delete():
    add = session.get("address")

    dname = add.get("dname")[2]
    print(dname)
    cur = db.cursor()
    cur.execute("delete from sp_address where dname='%s'" % dname)  # 删除个人地址
    cur.close()
    db.commit()
    return redirect("/kaddress")


@app.route("/order")
def order():
    user_info = session.get("user_info")
    print(user_info)
    if user_info:
     return render_template("./person/order.html",uname=user_info.get("uname"))    # 订单管理


@app.route("/change")
def change():
    user_info = session.get("user_info")
    print(user_info)
    if user_info:
        return render_template("./person/change.html",uname=user_info.get("uname"))   # 退款售后


@app.route("/coupon")
def coupon():
    user_info = session.get("user_info")
    print(user_info)
    if user_info:
        return render_template("./person/coupon.html",uname=user_info.get("uname"))   # 优惠卷


@app.route("/bonus")
def bonus():
    user_info = session.get("user_info")
    print(user_info)
    if user_info:
        return render_template("./person/bonus.html",uname=user_info.get("uname"))  # 红包


@app.route("/bill")
def bill():
    user_info = session.get("user_info")
    print(user_info)
    if user_info:
        return render_template("./person/bill.html",uname=user_info.get("uname"))  # 账单明细


# @app.route("/collection")
# def collection():
#     return render_template("/person/collection.html")  # 收藏


@app.route("/foot")
def foot():
    user_info = session.get("user_info")
    print(user_info)
    if user_info:
        return render_template("./person/foot.html",uname=user_info.get("uname"))  # 足迹


@app.route("/news")
def news():
    user_info = session.get("user_info")
    print(user_info)
    if user_info:
        return render_template("./person/news.html",uname=user_info.get("uname"))  # 我的消息


@app.route("/comment")
def comment():
    user_info = session.get("user_info")
    print(user_info)
    if user_info:
        return render_template("./person/comment.html",uname=user_info.get("uname"))  # 我的评价

# @app.route("/refund")
# def refund():
#     return render_template("./person/refund.html")


@app.route("/blog")
def blog_handle():
    user_info = session.get("user_info")
    print(user_info)
    if user_info:
        return render_template("./person/blog.html")


@app.route("/pay")
def pay():
    return render_template("./home/pay.html")   # 结算页面
@app.route("/search")
def search():
    return render_template("./home/search.html")    # 搜索页面
@app.route("/sort")
def sort():
    return render_template("./home/sort.html")  # 全部分类
@app.route("/success")
def success():
    return render_template("./home/success.html")   #  付款成功页面
@app.route("/bindphone")
def bindphone():
    return render_template("./person/bindphone.html")  # 绑定手机
@app.route("/blog")
def blog():
    return render_template("./person/blog.html")  # 新闻页面
@app.route("/email")
def email():
    return render_template("./person/email.html")  # 验证邮箱
@app.route("/idcard")
def idcard():
    return render_template("./person/idcard.html")  # 实名认证
@app.route("/iogistics")
def iogistics():
    return render_template("./person/logistics.html")  # 物流
@app.route("/orderinfo")
def orderinfo():
    return render_template("./person/orderinfo.html")  # 订单详情


@app.route("/password", methods=["GET", "POST"])
def updatapasswd():
    if request.method == "GET":

        return render_template("person/password.html")
    else:
        uname = request.form.get("uname")
        upass2 = request.form.get("upass2")
        upass = request.form.get("upass3")
        if upass != upass2:
            return "两次密码输入不一一致"
        # user_info = session.get("user_info")
        # uid = user_info.get("uid")
        # print(uid)
        print(upass2, upass, uname)
        cur = db.cursor()
        cur.execute("update sp_user set upass=md5(%s) where uname =%s", (uname + upass, uname))
        res = cur.rowcount
        cur.close()
        db.commit()

        print("修改成功")
        return redirect("/")
        # 修改密码


@app.route("/question",methods=["GET","POST"])
def question():
    if request.method == "GET":
        return render_template("./person/question.html")
    elif request.method == "POST":
        issue = request.form.get("question1")
        answer = request.form.get("answerl")
        issue1 = request.form.get("question2")
        answer1 = request.form.get("answer2")
        print(issue)
        print(answer)
        print(issue1)
        print(answer1)
        cur = db.cursor()
        cur.execute("INSERT INTO encrypted VALUES (%s,md5(%s),%s,md5(%s))",
                    (issue,answer,issue1,answer1))
        cur.close()
        db.commit()
        return render_template("./person/question.html")


@app.route("/record")
def record():
    return render_template("./person/record.html")  #  钱款去向
@app.route("/refund")
def refund():
    return render_template("/refund.html")  # 退换货
@app.route("/setpay")
def setpay():
    return render_template("./person/setpay.html")  #支付密码
@app.route("/commentlist")
def commemtlist():
    return  render_template("./person/commentlist.html")

@app.route("/billlist")
def billlist():
    return render_template("./person/billlist.html")




@app.route("/check_user",methods=["GET","POST"])
def check_user():
    if request.method == "GET":
        user_info = session.get("user_info")
        print(user_info)
        if user_info:
            cur = db.cursor()
            cur.execute("select * from sp_user ")
            res = cur.fetchall()
            print(res)
            cur.close()
            db.commit()
            # abort(Response("删除成功"))
            return render_template("./home/check_user.html",uname=user_info.get("uname"),res=res)  # 收货地址

# @app.route("/delect_user",methods=["GET","POST"])
# def delect_user():
#     # if request.method == "GET":
#     #     return render_template("./home/delect_user.html")
#     uname = session.get("user_info")
#     uad = uname.get("uname")
#     print(uad)
#     cur = db.cursor()
#     cur.execute("select * from sp_user")
#     res = cur.fetchall()
#     print(res)
#
#     cur.close()
#     for i in res:
#         str = i[1]
#     if not uad:
#         abort(Response("您未登陆"))
#
#     if request.method == "POST":
#         try:
#             cur = db.cursor()
#             cur.execute("delect from sp_user where uname = %s",(uname))
#             cur.close()
#             db.commit()
#         except:
#             abort(Response("删除失败"))
#         return render_template("./home/check_user")
#
# # @app.route("/check_user1",methods=["GRT","POST"])
# # def delect1_user():
# #     if request.method
# #
# #


if __name__ == "__main__":
    app.run(port=80, debug=True)

