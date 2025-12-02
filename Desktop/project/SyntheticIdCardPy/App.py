from flask import Flask, render_template, flash, request, session
import warnings
import os
import mysql.connector

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/AdminLogin")
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route("/NewUser")
def NewUser():
    return render_template('NewUser.html')


@app.route("/UserLogin")
def UserLogin():
    return render_template('UserLogin.html')


@app.route("/ServerLogin")
def ServerLogin():
    return render_template('ServerLogin.html')


@app.route("/serverlogin", methods=['GET', 'POST'])
def serverlogin():
    if request.method == 'POST':
        if request.form['uname'] == 'server' and request.form['password'] == 'server':
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3syidcarddb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb")
            data = cur.fetchall()
            return render_template('ServerHome.html', data=data)

        else:
            flash('Username or Password is Incorrect !')
            return render_template('ServerLogin.html')


@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        uname = request.form['uname']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        username = request.form['uname']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3syidcarddb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "'  ")
        data = cursor.fetchone()
        if data is None:

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3syidcarddb')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO regtb VALUES ('','" + uname + "','" + mobile + "','" + email + "','" + address + "','" + username + "','" + password + "')")
            conn.commit()
            conn.close()
            flash('Record Saved!')
            return render_template('UserLogin.html')

        else:
            flash('Already Register Username !')
            return render_template('NewUser.html')


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':

        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3syidcarddb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and Password='" + password + "' ")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('UserLogin.html')

        else:
            conn = mysql.connector.connect(user='root', password='', host='localhost',
                                           database='3syidcarddb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where username='" + session['uname'] + "'")
            data = cur.fetchall()
            return render_template('UserHome.html', data=data)


@app.route("/UserHome")
def UserHome():
    cname = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3syidcarddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where USerName='" + cname + "'")
    data = cur.fetchall()
    return render_template('UserHome.html', data=data)


@app.route("/IdcardInfo")
def IdcardInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3syidcarddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM idcardtb ")
    data = cur.fetchall()
    return render_template('IdcardInfo.html', data=data)


@app.route("/AIdCardInfo")
def AIdCardInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3syidcarddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM idcardtb ")
    data = cur.fetchall()
    return render_template('AIdCardInfo.html', data=data)


@app.route("/Remove")
def Remove():
    id = request.args.get('id')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3syidcarddb')
    cursor = conn.cursor()
    cursor.execute("delete from  idcardtb  where id='" + id + "' ")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3syidcarddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM idcardtb ")
    data = cur.fetchall()

    return render_template('IdcardInfo.html', data=data)


@app.route("/View")
def View():
    id = request.args.get('id')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3syidcarddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM idcardtb  where Id='" + id + "'")
    data = cur.fetchall()

    return render_template('Uidcard.html', data=data)


@app.route("/View1")
def View1():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3syidcarddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM idcardtb  where Id='" + id + "'")
    data = cur.fetchall()
    return render_template('AUidcard.html', data=data)


@app.route("/NewCard")
def NewCard():
    return render_template('NewCard.html')


import hmac
import hashlib
import binascii


def create_sha256_signature(key, message):
    byte_key = binascii.unhexlify(key)
    message = message.encode()
    return hmac.new(byte_key, message, hashlib.sha256).hexdigest().upper()


@app.route("/newidcard", methods=['GET', 'POST'])
def newidcard():
    if request.method == 'POST':
        from stegano import lsb
        uname = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        Aadhaar = request.form['Aadhaar']
        VoterId = request.form['VoterId']
        blood = request.form['blood']
        import random
        file = request.files['file']
        fnew = random.randint(1111, 9999)
        savename = str(fnew) + ".png"
        file.save("static/upload/" + savename)

        num1 = VoterId + blood + Aadhaar
        hash2 = create_sha256_signature("E49756B4C8FAB4E48222A3E7F3B97CC3", str(num1))

        secret = lsb.hide("./static/upload/" + savename, hash2)
        secret.save("./static/Encode/" + savename)

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3syidcarddb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from idcardtb where Aadhaar='" + Aadhaar + "'  ")
        data = cursor.fetchone()
        if data is None:

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3syidcarddb')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO idcardtb VALUES ('','" + uname + "','" + mobile + "','" + email + "','" + address + "','" +
                Aadhaar + "','" + VoterId + "','" + blood + "','" + savename + "','" + hash2 + "')")
            conn.commit()
            conn.close()
            flash('Record Saved!')
            return render_template('NewCard.html')

        else:
            flash('Already Register Username !')
            return render_template('NewCard.html')


@app.route("/VerifierLogin")
def VerifierLogin():
    return render_template('VerifierLogin.html')


@app.route("/vlogin", methods=['GET', 'POST'])
def vlogin():
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3syidcarddb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM idcardtb")
            data = cur.fetchall()
            return render_template('VHome.html', data=data)

        else:
            flash('Username or Password is Incorrect !')
            return render_template('VerifierLogin.html')


@app.route("/VHome")
def VHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3syidcarddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM idcardtb ")
    data = cur.fetchall()
    return render_template('VHome.html', data=data)


@app.route("/Verify")
def Verify():
    id = request.args.get('id')

    from stegano import lsb
    clear_message =''
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3syidcarddb')
    cursor = conn.cursor()
    cursor.execute("SELECT * from idcardtb where id='" + id + "'  ")
    data = cursor.fetchone()
    if data:
        newfilepath2=data[8]
        hash1 = data[9]

        newfilepath2 = "./static/Encode/"+newfilepath2

        try:
            clear_message = lsb.reveal(newfilepath2)
            print(clear_message)

        except:
            clear_message=''



        if hash1 == clear_message:
            flash("IDCard Original")
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3syidcarddb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM idcardtb ")
            data = cur.fetchall()
            return render_template('VHome.html', data=data)
        else:
            flash("IDCard Fake")
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3syidcarddb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM idcardtb ")
            data = cur.fetchall()
            return render_template('VHome.html', data=data)





if __name__ == '__main__':
    # app.run(host='0.0.0.0',debug = True, port = 5000)
    app.run(debug=True, use_reloader=True)
