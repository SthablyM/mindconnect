from datetime import timezone
from pprint import pp
from flask import Flask, flash, redirect, render_template, request, session, url_for
from sqlalchemy import make_url
from db import Post, PostComment, PostLike, User, db

app = Flask(__name__)

# Set up database configuration using SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost:3306/mindconnect"
app.secret_key = 'hgaefdhfaevevyatedv'  # Secret key for session management

# Initialize database with the Flask app
db.init_app(app)

with app.app_context():
    # Create all tables in the database
    db.create_all()

# Route for the home page, renders home.html
@app.route('/', methods=["GET"])
def home():
    return render_template("home.html")

# Route for sign-in functionality, handles both GET and POST requests
@app.route('/signin', methods=["POST", "GET"])
def signin():
    if request.method == "GET":
        return render_template("login.html", message="")  # Render login page if GET request
    else:
        # Get email and password from form
        email = request.form["email"]
        password = request.form["password"]

        # Check if user exists in the database
        existing_user = User.query.filter_by(email=email, password=password).first()

        # If user is found, redirect to feeds page
        if existing_user:
            session["logged_user_id"] = existing_user.id
            return redirect('/feeds')
        else:
            # If login fails, show an error message
            return render_template("login.html", message="Invalid login details")

# Route for sign-up functionality, handles both GET and POST requests
@app.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")  # Render signup form
    else:
        # Retrieve data from the form
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        phone_number = request.form["phone_number"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Basic form validation: check for empty fields and password match
        if first_name == "" or email == "" or password == "" or confirm_password == "":
            return render_template('signup.html')
        if password != confirm_password:
            return render_template('signup.html')
        else:
            # Create a new user and add to the database
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                email=email,
                password=password
            )
            db.session.add(new_user)
            db.session.commit()

            # If user is successfully created, redirect to sign-in page
            if new_user.id > 0:
                return redirect("/signin")
            else:
                return render_template('signup.html')

# Route to handle forgotten password functionality
@app.route('/forgot-password', methods=["POST", "GET"])
def forgotPassword():
    if request.method == "GET":
        return render_template("forgotpassword.html")  # Render forgot password form
    else:
        email = request.form["email"]

        if email == "":
            return render_template('forgotpassword.html')
        else:
            # Check if the email exists in the database
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                session["email"] = email
                return redirect("/reset-password")
            else:
                # Show error message for invalid email
                return render_template("forgotpassword.html", message="Invalid email address")

# Route to reset password
@app.route('/reset-password', methods=["POST", "GET"])
def restPassword():
    if request.method == "GET":
        return render_template("resetpassword.html")  # Render reset password form
    else:
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password == "" or confirm_password == "":
            return render_template('resetpassword.html')
        if password != confirm_password:
            return render_template('resetpassword.html')
        else:
            # Retrieve email from session and update the user's password
            email = session["email"]
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                existing_user.password = password
                db.session.add(existing_user)
                db.session.commit()
            return render_template("login.html")  # Redirect to login page after resetting password

# Route to create a new post
@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        post = request.form.get('CreatPost')
        image_uri = request.form.get('image')

        # If post content is empty, show an error message
        if not post:
            flash('Post content is required', 'error')
            return redirect('create_post')

        # Create a new post and add it to the database
        new_post = Post(
            user_id=session.get("logged_user_id"),
            post=post,
            image_uri=image_uri
        )
        db.session.add(new_post)
        db.session.commit()

        return redirect('/feeds')  # Redirect to feeds page after creating a post

    return render_template('create_post.html')  # Render create post form

# Route to display all posts in feeds
@app.route('/feeds', methods=["POST", "GET"])
def feeds():
    image_url = "https://images.pexels.com/photos/60597/dahlia-red-blossom-bloom-60597.jpeg?auto=compress&cs=tinysrgb&w=250"

    if request.method == "GET":
        posts = Post.query.all()  # Retrieve all posts from the database
        return render_template("feeds.html", posts=posts)  # Render posts on the feeds page

# Route to like a post
@app.route('/like', methods=["POST"])
def like_post():
    post_id = request.form['post_id']

    # Create a new like for the post and add to the database
    new_like = PostLike(
        user_id=session["logged_user_id"],
        post_id=post_id,
    )
    db.session.add(new_like)
    db.session.commit()

    return redirect(url_for('feeds'))  # Redirect to feeds page after liking a post

# Route to add a comment to a post
@app.route('/add_comment', methods=['POST'])
def add_comment():
    comment = request.form['comment']
    post_id = request.form['post_id']

    # Create a new comment and add it to the database
    new_comment = PostComment(
        user_id=session["logged_user_id"],
        post_id=post_id,
        comment=comment,
    )
    db.session.add(new_comment)
    db.session.commit()

    if new_comment.id > 0:
        return redirect("/feeds")  # Redirect to feeds page after adding a comment


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
 
  
  