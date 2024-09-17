from datetime import timezone
from pprint import pp
from flask import Flask, redirect, render_template, request, session, url_for
from db import Post, PostComment, PostLike, User, db

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
            session["logged_user_id"] = existing_user.id
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
   
@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    post = {"user_id": 1, "content": "new_post"}
    if request.method == 'POST':
        content = request.form['CreatPost']
        new_post = Post(
            user_id=session["logged_user_id"],
            content=content,
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('feeds'))
    return render_template('create_post.html', post=post)



@app.route('/success', methods = ['POST'])   
def success():   
    if request.method == 'POST':   
        f = request.files['file'] 
        f.save(f.filename)
        return render_template('create_post.html', name = f.filename)

        
         
@app.route('/feeds', methods=["POST", "GET"])
def feeds():
    image_url= "https://images.pexels.com/photos/60597/dahlia-red-blossom-bloom-60597.jpeg?auto=compress&cs=tinysrgb&w=250"    
    if (request.method == "GET"):
        posts = Post.query.all()
        for post in posts:
            likes = PostLike.query.filter_by(post_id = post.id)
        return render_template("feeds.html", posts=posts)
    

@app.route('/like', methods=["POST"])
def like_post():
    post_id = request.form['post_id']
    new_like = PostLike(
        user_id = session["logged_user_id"],
        post_id = post_id,
    )
    db.session.add(new_like)
    db.session.commit()
    return redirect(url_for('feeds'))


@app.route('/add_comment', methods=['POST'])
def add_comment():
    comment = request.form['comment']
    post_id = request.form['post_id']
    new_comment = PostComment(
        user_id = session["logged_user_id"],
        post_id = post_id,
        comment = comment,
    )
    db.session.add(new_comment)
    db.session.commit()
    if (new_comment.id > 0):
        return redirect("/feeds")    
    

app.run(debug=True)
from flask import Flask, request, render_template 
  
app = Flask(__name__) 
  
  
@app.route('/', methods=['GET', 'POST']) 
def index(): 
    if request.method == 'POST': 
        # Retrieve the text from the textarea 
        text = request.form.get('textarea') 
  
        # Print the text in terminal for verification 
        print(text) 
  
    return render_template('home.html') 
  
  
  