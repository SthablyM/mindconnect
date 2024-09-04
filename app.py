from datetime import timezone
from flask import Flask, redirect, render_template, request, session, url_for
from db import Post, User, db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost:3306/mindconnect"
app.secret_key = 'hgaefdhfaevevyatedv'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=["GET"])
def home():
    return render_template("home.html")

@app.route('/signin', methods=["POST", "GET"])
def signin():
    if (request.method == "GET"):
        return render_template("login.html", message = "")   
    else:
        email = request.form["email"]
        password = request.form["password"]
        existing_user = User.query.filter_by(email=email, password = password).first()
        if (existing_user is not None):
            # session["logged_in"] = "success"
            return redirect('/feeds')
        else: 
            return render_template("login.html", message = "Invalid login details") 
        
@app.route('/signup', methods=["POST", "GET"])
def signup():
    if (request.method == "GET"):
        return render_template("signup.html")
    else:
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        phone_number = request.form["phone_number"]        
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        
        if (first_name == "" or email == "" or password == "" or confirm_password == ""):
            return render_template('signup.html')
        if (password != confirm_password):
            return render_template('signup.html')
        else: 
            new_user = User(
                first_name = first_name,
                last_name = last_name,
                phone_number = phone_number,
                email = email,
                password = password
            )
            db.session.add(new_user)
            db.session.commit()
            if (new_user.id > 0):
                return redirect("/signin")
            else: 
                return render_template('signup.html')
    
@app.route('/forgot-password', methods=["POST", "GET"])
def forgotPassword():
    if (request.method == "GET"):
        return render_template("forgotpassword.html")  
    else:
        email = request.form["email"]
        if (email == ""):
            return render_template('forgotpassword.html')
        else: 
            existing_user = User.query.filter_by(email=email).first()
            if (existing_user is not None):
                session["email"] = email
                return redirect("/reset-password")
            else:
                return render_template("forgotpassword.html", message = "Invalid email address")      
    
@app.route('/reset-password', methods=["POST", "GET"])
def restPassword():
    if (request.method == "GET"):
        return render_template("resetpassword.html")  
    else:
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if (password == "" or confirm_password == ""):
            return render_template('resetpassword.html')
        if (password != confirm_password):
            return render_template('resetpassword.html')
        else: 
            email = session["email"]
            existing_user = User.query.filter_by(email=email).first()
            if (existing_user is not None):
                existing_user.password = password
                db.session.add(existing_user)
                db.session.commit()
            return render_template("login.html")     


@app.route('/feeds', methods=["POST", "GET"])
def feeds():
    image_url= "https://images.pexels.com/photos/60597/dahlia-red-blossom-bloom-60597.jpeg?auto=compress&cs=tinysrgb&w=600"
    return render_template("feeds.html", image_url=image_url)
    if (request.method == "GET"):
        return render_template("feeds.html") 
likes_count = 0
comments = []
@app.route('/like', methods=["POST", "GET"])
def like_post():
    global likes_count
    likes_count += 1
    return redirect(url_for('feeds'))
@app.route('/add_comment', methods=['POST'])
def add_comment():
    global comments
    comment = request.form['comment']
    comments.append(comment)
    return redirect(url_for('feeds'))


app.run(debug=True)