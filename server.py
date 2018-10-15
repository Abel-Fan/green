from flask import Flask,render_template,request,redirect,url_for,session,jsonify
from blinker import Namespace
import pymysql,hashlib,math


my_signals=Namespace()#创建命名空间，作用是可创建并存储多个信号发射对象
model_saved=my_signals.signal('model_saved')  #创建一个信号发射对象，参数是名字

# 链接数据库
db = pymysql.connect(host="localhost",user="root",password="",db="green1")

# 创建游标
cur = db.cursor()



# 实例化应用
app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
# 路由

#  前台
@app.route("/")
def index():
    sql = "select * from category order by id desc limit 8"
    cur.execute(sql)
    res = cur.fetchall()
    return render_template("/green-master/index.html",data=res)

@app.route("/products")
def hello():
    return render_template("/green-master/products.html")

@app.route("/news-center")
def newcenter():
    return render_template("/green-master/news-center.html")


@app.route("/join")
def join():
    return render_template("/green-master/join.html")

@app.route("/call")
def call():
    return render_template("/green-master/call.html")

@app.route("/news-list")
def newslist():
    return render_template("/green-master/news-list.html")

@app.route("/news1")
def news1():
    return render_template("/green-master/news1.html")

@app.route("/fruit<cid>_<id>")
def fruit(cid,id):
    sql = "select * from category where cid=%s"%cid
    cur.execute(sql)
    res = cur.fetchall()

    return render_template("/green-master/fruit.html",data=res,id=id)



# 后台逻辑
@app.route("/admin")
def admin():
    if 'username' in session:

        return render_template("/blue-master/index.html",id=session['id'])
    else:
        return redirect(url_for("login"))

@app.route("/login")
def login():
    return render_template("/blue-master/login.html")

@app.route("/loginout")
def loginout():
    del session['username']
    del session['id']
    return redirect(url_for("login"))


@app.route("/checklogin",methods=['post'])
def checklogin():
    username = request.form['username']
    password = request.form['password']

    s = hashlib.md5()
    s.update(password.encode())
    password = s.hexdigest()
    # 组织sql语句

    sql = "select password,level from users where username='%s'"%username

    # 执行sql语句
    cur.execute(sql)
    # 获取查询结果
    password0 = ""
    res = cur.fetchone()
    if res != None:
        password0 = res[0]

    if password0 == password:
        # 登录成功
        session['username'] = username
        session['id'] = res[1]

        return redirect(url_for("admin"))
    else:
        # 登录失败
        return redirect(url_for("tips",state="no",href="login",time=3))


@app.route("/tips/<state>/<href>/<time>")
def tips(state,href,time):
    return render_template("/blue-master/tips.html",state=state,href=href,time=time)


@app.route("/openadduser")
def openadduser():

    if 'username' in session:
        if session["id"] ==1:
            return render_template("/blue-master/adduser.html")
        else:
            return redirect(url_for("tips",state="no",href="admin",time=3))
    else:
        return redirect(url_for("login"))



@app.route("/adduser",methods=['post'])
def adduser():
    if 'username' in session:
        username = request.form['username']
        newpass = request.form['newpass']
        renewpass = request.form['renewpass']

        if username!="" and newpass!="" and renewpass != "":
            if newpass==renewpass:
                s = hashlib.md5()
                s.update(newpass.encode())
                password = s.hexdigest()

                sql = "insert into users (username,password,level) values ('%s','%s',%s)"%(username,password,2)
                cur.execute(sql)
                db.commit()

                return redirect(url_for("tips",state="yes",href="openadduser",time=3))
            else:
                return redirect(url_for("tips", state="loginerror1", href="openadduser", time=3))
        else:
            return redirect(url_for("tips", state="loginerror2", href="openadduser", time=3))




    else:
        return redirect(url_for("login"))


@app.route("/listuser<page>")
def listuser(page):
    page = int(page)
    if 'username' in session:
        sql = "select count(*) from users"
        cur.execute(sql)
        length = cur.fetchone()[0]
        sql = "select id,username,level from users limit %s,2"%((page-1)*2)
        cur.execute(sql)
        res = cur.fetchall()
        pages = range(1,math.ceil(length/2)+1)
        return render_template("/blue-master/listuser.html",data=res,pages=pages,now=page)
    else:
        return redirect(url_for("login"))



@app.route("/openedituser<id>_<username>")
def openedituser(id,username):
    if 'username' in session and session['id']==1:
        return render_template("/blue-master/edituser.html",id=id,username=username)



@app.route("/edituser",methods=['post'])
def edituser():
    if 'username' in session and session['id'] == 1:
        id = request.form['id']
        username = request.form['username']
        mpass = request.form['mpass'] #原始密码
        newpass = request.form['newpass'] #新密码

        s = hashlib.md5()
        s.update(mpass.encode())
        mpass = s.hexdigest()

        sql = "select password from users where id=%s"%id
        cur.execute(sql)
        res = cur.fetchone()[0]

        if res == mpass:
            h = hashlib.md5()
            h.update(newpass.encode())
            newpass = h.hexdigest()
            sql = "update users set password='%s' where id=%s"%(newpass,id)

            cur.execute(sql)
            db.commit()
            return redirect(url_for("tips", state="yes", href="listuser1", time=3))

        else:
            return redirect(url_for("tips",state="no",href="openedituser%s_%s"%(id,username),time=3))


@app.route("/deluser<name>")
def deluser(name):
    if name != "admin":
        try:
            sql = "delete from users where name=%s"%name
            cur.execute(sql)
            db.commit()
            return redirect(url_for("tips", state="yes", href="listuser1", time=3))
        except:
            db.rollback() # 回滚
            return redirect(url_for("tips", state="no", href="listuser1", time=3))

    else:
        return redirect(url_for("tips", state="no", href="listuser1", time=3))

@app.route("/send")
def send():
    model_saved.send(app, data='A')


@model_saved.connect_via(app)
def signal_recv(app,data):
    print(data)
    pass


# 添加产品分类
@app.route("/openpcategory")
def openaddproducts():
    sql = "select * from pcategory"
    cur.execute(sql)
    res = cur.fetchall()

    return render_template("/blue-master/addpcategory.html",data = res)

@app.route("/addpcategory",methods=['post'])
def addpcategory():
    name = request.form['name']
    sql = "insert into pcategory (name) values ('%s')"%name
    cur.execute(sql)
    db.commit()

    sql = "select id from pcategory where name='%s'"%name
    cur.execute(sql)
    id = cur.fetchone()[0]

    rep = {'info':"ok",'id':id}

    return jsonify(rep)


@app.route("/selectpcategory",methods=["post"])
def selectpcategory():
    name = request.form['name']
    sql = "select count(*) from pcategory where name='%s'"%name
    cur.execute(sql)
    length = cur.fetchone()[0]

    if length>0:
        return "no"
    else:
        return "yes"


@app.route("/openeditpcategory<id>_<name>")
def openeditpcategory(id,name):
    return render_template("/blue-master/editpcategory.html",id=id,name=name)

@app.route("/editpcategory",methods=['post'])
def editpcategory():
    id = request.form['id']
    name = request.form['name']
    sql = "update pcategory set name='%s' where id=%s"%(name,id)

    cur.execute(sql)
    db.commit()

    return redirect(url_for("tips",state="yes",href='openpcategory',time=3))

@app.route("/delpcategory",methods=['post'])
def delpcategory():
    id = request.form['id']

    sql = "delete from pcategory where id=%s"%id

    cur.execute(sql)
    db.commit()
    return "ok"


# 产品管理
@app.route("/openlistcategory<page>")
def openlistcategory(page):
    sql = "select category.*,pcategory.name from category left join pcategory on category.cid=pcategory.id order by category.id desc"
    cur.execute(sql)
    res = cur.fetchall()

    return render_template("blue-master/listcategory.html",data=res)

@app.route("/openaddcategory")
def openaddcategory():
    sql = "select * from pcategory"
    cur.execute(sql)
    res = cur.fetchall()
    print(res)
    return render_template("blue-master/addcategory.html",data=res)

@app.route("/addcategory",methods=["post"])
def addcategory():
    imgurl = request.form['imgurl1']
    name = request.form['name']
    star = request.form['star']
    cid = request.form['cid']
    con = request.form['con']

    sql = "insert into category (imgurl,name,star,cid,con,author) values ('%s','%s',%s,%s,'%s','%s')"%(imgurl,name,star,cid,con,session['username'])

    cur.execute(sql)
    db.commit()



    return redirect(url_for("tips",state="yes",href="openaddcategory",time=3))

@app.route("/uploadPimg",methods=['post'])
def uploadPimg():
    f = request.files['imgurl']
    imgurl =  "static/upload/img/"+f.filename
    f.save(imgurl)
    rep = {'info':"ok","imgurl":"/"+imgurl}
    return jsonify(rep)




if __name__ == "__main__":
    app.run(debug=True)
