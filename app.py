from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, Response, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import base64
#from yourapp import User

# from helpers import login_required

db = SQLAlchemy()
# Function that initializes the db and creates the tables
def db_init(app):
    db.init_app(app)
    # Creates the logs tables if the db doesnt already exist
    with app.app_context():
        db.create_all()

class Img17(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    img = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)

if __name__ == '__main__':
    app.run(debug=True, port=8001)

# Configure application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///img.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 2 * 1000 * 1000
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
db_init(app)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db1 = SQL("sqlite:///website.db")
#upload_folder = os.path.join('static', 'uploads')
#app.config['UPLOAD'] = upload_folder

@app.errorhandler(413)
def too_large(error):
    #return "File is too large", 413
    flash("File is Too Large. Please make it smaller than 2MB")
    return render_template("upload.html")
    #return redirect('/upload')
    return render_template("upload.html", price=request.form.get("price"), title= request.form.get("book_title"), subject= request.form.get("book_subject"), description=request.form.get("book_description"), syllabus=request.form.get("book_syllabus"))

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/', methods=['GET','POST'])
def information():
    return render_template("infotesting.html")

@app.route('/contactus', methods=['GET','POST'])
def contact():
    return render_template("contactus.html")

@app.route('/searchnotes', methods=['GET','POST'])
def searchnotes():
    if request.method == "GET":
        # base64_images = [base64.b64encode(images).decode("utf-8") for image.image in images]
        # read image data from db back to form a rendable in html
        images = db.session.query(Img17).all()
        image_list = []
        list2 = {}
        count_db = db1.execute("SELECT COUNT(id) as count FROM database4")
        count = count_db[0]["count"]
        temp =[]
        #count_db1 = db1.execute("SELECT COUNT(images) as count FROM database3 WHERE load_type = 'UPLOAD'")
        #count1 = count_db[0]["count"]
        #images_db = db1.execute("SELECT images FROM database3")
        #print('')
        #print(images_db[1]["images"])
        #print('')
        for img in images:
            #print(images_db[img]["images"])
            image = base64.b64encode(img.img).decode('ascii')
            image_list.append(image)
        print('')
        print(len(image_list))
        print('')
        image_db = db1.execute("SELECT id, user_id, price, book_title, book_subject, book_description, book_syllabus FROM database4")
        for user in range(count):
            list2["id"] = image_db[user]["id"]
            list2["price"] = image_db[user]["price"]
            list2["user_id"] = image_db[user]["user_id"]
            list2["book_title"] = image_db[user]["book_title"]
            list2["book_subject"] = image_db[user]["book_subject"]
            list2["book_description"] = image_db[user]["book_description"]
            list2["book_syllabus"] = image_db[user]["book_syllabus"]
            #list2["email"] = image_db[user]["email"]
            #list2["phone"] = image_db[user]["phone"]
            #list2["socials"] = image_db[user]["socials"]
            list2["image"] = image_list[user]
            temp.append(list2.copy())      
        return render_template('index.html', list=temp)
    else:
        get_id = request.form.get("id")
        database_get = db1.execute("SELECT username, email, socials, price, book_title, book_subject, book_description, book_syllabus FROM users JOIN database4 ON database4.user_id = users.id WHERE database4.id = ?", get_id)

        print("DATABASE: ", database_get)
        #list1 = database_get[0]["list"]
        images = db.session.query(Img17).filter_by(id = get_id)
        #print('')
        #print("Images: ", images)
        for img in images:
            image = base64.b64encode(img.img).decode('ascii')
            database_get[0]["image"] = image
        #return redirect(url_for('info', list=database_get))
        #print('')
        #print("DATABASE: ", database_get)
        #print("list: ", list1)
        #print('')
        #user_get = 1
        return render_template('info.html', list=database_get)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method =="GET":
        return render_template("upload.html")
    else:
        pic = request.files['pic']
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not pic or not filename or not mimetype:
            #return 'No pic uploaded!', 400
            flash("Please Upload a Picture")
            return render_template("upload.html", price=request.form.get("price"), title= request.form.get("book_title"), subject= request.form.get("book_subject"), description=request.form.get("book_description"), syllabus=request.form.get("book_syllabus"))
        if not allowed_file(filename):
            flash("Please Upload a PNG, JPG, or a JPEG as your photo")
            return render_template("upload.html", price=request.form.get("price"), title= request.form.get("book_title"), subject= request.form.get("book_subject"), description=request.form.get("book_description"), syllabus=request.form.get("book_syllabus"))
            #return render_template("info.html", get_id = edit) #have to create an error message
        #if not filename or not mimetype:
            #flash("Bad Read. Please Try again")
            #return 'Bad upload!', 400
            #return render_template("upload.html")
        
        session_user_id = session["user_id"] #database3 and below had load_type, which was a manual input by me. It was either 'UPLOAD' or 'DELETE', but i removed it to try and possibly save space
        db1.execute("INSERT INTO database4 (user_id, price,  book_title, book_subject, book_description, book_syllabus) VALUES(?, ?, ?, ?, ?, ?)", session["user_id"], request.form.get("price"), request.form.get("book_title"), request.form.get("book_subject"), request.form.get("book_description"), request.form.get("book_syllabus"))
        db_id_list = db1.execute("SELECT id FROM database4 WHERE user_id = ? ORDER BY id DESC LIMIT 1", session_user_id)
        db_id = db_id_list[0]["id"]
        img = Img17(img=pic.read(), name=filename, id=db_id, mimetype=mimetype, user_id=session_user_id)
        db.session.add(img)
        db.session.commit()        

        #db1.execute("INSERT INTO database3 (user_id, price, book_title, book_subject, book_description, book_syllabus, email, phone, socials, load_type) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", session["user_id"], request.form.get("price"), request.form.get("book_title"), request.form.get("book_subject"), request.form.get("book_description"), request.form.get("book_syllabus"), request.form.get("email"), request.form.get("phone"), request.form.get("socials"), 'UPLOAD')
        return redirect("/searchnotes")

@app.route('/<int:id>')
def get_info(id):
    img = Img17.query.filter_by(id=id).first()
    if not img:
        return 'Img Not Found!', 404
    return Response(img.img, mimetype=img.mimetype)

    get_id = request.form.get("id")
    database_get = db1.execute("SELECT username, email, phone, socials, price, book_title, book_subject, book_description, book_syllabus FROM users JOIN database4 ON database4.user_id = users.id WHERE database4.id = ?", get_id)

    print("DATABASE: ", database_get)
    #list1 = database_get[0]["list"]
    images = db.session.query(Img17).filter_by(id = get_id)
    #print('')
    #print("Images: ", images)
    for img in images:
        image = base64.b64encode(img.img).decode('ascii')
        database_get[0]["image"] = image
    #return redirect(url_for('info', list=database_get))
    #print('')
    #print("DATABASE: ", database_get)
    #print("list: ", list1)
    #print('')
    #user_get = 1
    return render_template('info.html', list=database_get)
    get_id = request.form.get("id")
    database_get = db1.execute("SELECT username, email, phone, socials, price, book_title, book_subject, book_description, book_syllabus FROM users JOIN database4 ON database4.user_id = users.id WHERE database4.id = ?", get_id)

    print("DATABASE: ", database_get)
    #list1 = database_get[0]["list"]
    images = db.session.query(Img17).filter_by(id = get_id)
    #print('')
    #print("Images: ", images)
    for img in images:
        image = base64.b64encode(img.img).decode('ascii')
        database_get[0]["image"] = image
    #return redirect(url_for('info', list=database_get))
    #print('')
    #print("DATABASE: ", database_get)
    #print("list: ", list1)
    #print('')
    #user_get = 1
    return render_template('info.html', list=database_get)
#@app.route('/gallery', methods=['GET','POST'])
#def get_images():

@app.route('/items', methods=['GET','POST'])
def my_items():
    if request.method == "POST":
        if session["user_id"] != 1:
            delete_id = request.form.get("delete_id")
            edit = request.form.get("edit_id")
            print("id of delete: ", delete_id)
            print("id of edit: ", edit)
            user_id = session["user_id"]
            if delete_id is not None:
                db1.execute("DELETE FROM database4 WHERE user_id = ? AND id = ?", user_id, delete_id)
                delete_item = db.session.query(Img17).filter_by(id = delete_id).first()
                db.session.delete(delete_item)
                db.session.commit()
                return redirect("/items")
            elif edit is not None:
                print('hey')
                return redirect(url_for('edit', id=edit))
                return render_template("info.html", get_id = edit)
        else:
            delete_id = request.form.get("delete_id")
            edit = request.form.get("edit_id")
            print("id of delete: ", delete_id)
            print("id of edit: ", edit)
            user_id = session["user_id"]
            if delete_id is not None:
                db1.execute("DELETE FROM database4 WHERE id = ?", delete_id)
                delete_item = db.session.query(Img17).filter_by(id = delete_id).first()
                db.session.delete(delete_item)
                db.session.commit()
                return redirect("/items")
            elif edit is not None:
                print('hey')
                return redirect(url_for('edit', id=edit))
                return render_template("info.html", get_id = edit)
        
    else:
        if session["user_id"] != 1:
            delete_id = request.form.get("id")
            #print("DELETE ID: ", delete_id)
            images = db.session.query(Img17).filter_by(user_id = session["user_id"])
            print("User_ID: ", session["user_id"])
            image_list = []
            list2 = {}
            count_db = {}
            count_db = db1.execute("SELECT COUNT(id) as count FROM database4 WHERE user_id = ?", session["user_id"])
            count = count_db[0]["count"]
            #print('')
            #print("count", count)
            temp =[]
            for img in images:
                image = base64.b64encode(img.img).decode('ascii')
                image_list.append(image)
            print('')
            print("Image List Length: ", len(image_list))
            print("")
            if len(image_list) > 0:
                image_db = db1.execute("SELECT id, user_id, price, book_title, book_subject, book_description, book_syllabus FROM database4 WHERE user_id = ?", session["user_id"])
                for user in range(count):
                    list2["id"] = image_db[user]["id"]
                    list2["user_id"] = image_db[user]["user_id"]
                    list2["book_title"] = image_db[user]["book_title"]
                    list2["book_subject"] = image_db[user]["book_subject"]
                    list2["book_description"] = image_db[user]["book_description"]
                    list2["book_syllabus"] = image_db[user]["book_syllabus"]
                    #list2["email"] = image_db[user]["email"]
                    #list2["phone"] = image_db[user]["phone"]
                    #list2["socials"] = image_db[user]["socials"]
                    list2["image"] = image_list[user]
                    temp.append(list2.copy())
        else:
            delete_id = request.form.get("id")
            #print("DELETE ID: ", delete_id)
            images = db.session.query(Img17)
            print("User_ID: ", session["user_id"])
            image_list = []
            list2 = {}
            count_db = {}
            count_db = db1.execute("SELECT COUNT(id) as count FROM database4")
            count = count_db[0]["count"]
            #print('')
            #print("count", count)
            temp =[]
            for img in images:
                image = base64.b64encode(img.img).decode('ascii')
                image_list.append(image)
            print('')
            print("Image List Length: ", len(image_list))
            print("")
            if len(image_list) > 0:
                image_db = db1.execute("SELECT id, user_id, price, book_title, book_subject, book_description, book_syllabus FROM database4")
                for user in range(count):
                    list2["id"] = image_db[user]["id"]
                    list2["user_id"] = image_db[user]["user_id"]
                    list2["book_title"] = image_db[user]["book_title"]
                    list2["book_subject"] = image_db[user]["book_subject"]
                    list2["book_description"] = image_db[user]["book_description"]
                    list2["book_syllabus"] = image_db[user]["book_syllabus"]
                    #list2["email"] = image_db[user]["email"]
                    #list2["phone"] = image_db[user]["phone"]
                    #list2["socials"] = image_db[user]["socials"]
                    list2["image"] = image_list[user]
                    temp.append(list2.copy())
        return render_template('items.html', list=temp, image_list=image_list)


@app.route('/edit_post', methods=['GET','POST'])
def edit_post():
    if request.method == "POST":
        print('')
        print("WORK: ", request.form.get("editid"))
        print('')
        db1.execute("UPDATE database4 SET price = ?, book_title = ?, book_subject = ?, book_description = ?, book_syllabus = ? WHERE user_id = ? AND id = ?", request.form.get("price"), request.form.get("book_title"), request.form.get("book_subject"), request.form.get("book_description"), request.form.get("book_syllabus"), session["user_id"], request.form.get("editid"))
        #print('hello from ')
        return redirect('/')

@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == "POST":
        print('hey')
        id_list =[]
        search_form = request.form.get("search")
        print('')
        print("SEARCH REQUEST: ", request.form.get("search"))
        print('')
        search_db = db1.execute("SELECT * FROM database4 WHERE book_title LIKE '%{s}%' OR book_subject LIKE '%{s}%' OR book_description LIKE '%{s}%'" .format(s=request.form.get("search")))
        if search_form:
            print('')
            print("SEARCH: ", search_db)
            for user in range(len(search_db)):
                id_list.append(search_db[user]["id"])
            print("ID LIST: ", id_list)
            image_list = []
            images = Img17.query.filter(Img17.id.in_(id_list))
            #images = db.session.query(Img17).filter(id.in_([7, 10])).first()
            for img in images:
                image = base64.b64encode(img.img).decode('ascii')
                image_list.append(image)
            for user in range(len(search_db)):
                search_db[user]["image"] = image_list[user]
            print(len(image_list))
            print(len(search_db))
            print('')
            #print("DB: ", search_db)
            return render_template("search.html", list=image_list, db = search_db)
        return redirect('/')
    else:
        return redirect('/')
    
@app.route('/edit', methods=['GET','POST'])
def edit_1():
    id = request.form.get("edit_id")
    database_get = db1.execute("SELECT database4.id, price, book_title, book_subject, book_description, book_syllabus FROM users JOIN database4 ON database4.user_id = users.id WHERE database4.id = ?", id)
    images = db.session.query(Img17).filter_by(id=database_get[0]["id"])
    print('')
    print(database_get[0])
    image_list =[]
    for img in images:
        image = base64.b64encode(img.img).decode('ascii')
        image_list.append(image)
    #for img in images:
    database_get[0]["image"] = image_list[0]
    #print('')
    #print(id)
    return render_template("edit_data.html", list=database_get, get_id=id)

@app.route('/accounts', methods=['GET','POST'])
def account():
    if request.method == "GET":
        session_user_id = session["user_id"]
        info = db1.execute("SELECT * FROM users WHERE id = ?", session_user_id)
        count_db = db1.execute("SELECT COUNT(id) as count FROM database4 WHERE user_id = ?", session["user_id"])
        count = count_db[0]["count"]
        if count == 0:
            count = 'none'
        info[0]["uploads"] = count
        return render_template("account.html", info=info)
    
@app.route('/changeinformation', methods=['GET','POST'])
def changeinfo():
    if request.method == "GET":
        session_user_id = session["user_id"]
        info = db1.execute("SELECT username, hash, email, socials FROM users WHERE id = ?", session_user_id)
        return render_template("changeinformation.html", list=info)
    else:
        session_user_id = session["user_id"]
        info = db1.execute("SELECT username, hash, email, socials FROM users WHERE id = ?", session_user_id)
        if not check_password_hash(info[0]["hash"], request.form.get("oldpassword")):
            flash("Old password isn't correct")
            return render_template("changeinformation.html", list=info)
        db1.execute("UPDATE users SET username = ?, email = ?, socials = ?  WHERE id = ?", request.form.get("username"), request.form.get("email"), request.form.get("socials"), session_user_id)
        #print('HEY')
        flash("Information Changed")
        return redirect('/accounts')

@app.route('/changepassword', methods=['GET','POST'])
def change():
    if request.method == "GET":
        return render_template("changepassword.html")
    else:
        session_user_id = session["user_id"]
        info = db1.execute("SELECT hash FROM users WHERE id = ?", session_user_id)
        if not request.form.get("oldpassword"):
            flash("Please enter old password")
            return render_template("changepassword.html")
        elif not request.form.get("password"):
            flash("Please enter password")
            return render_template("changepassword.html")
        elif not request.form.get("confirmation"):
            flash("Please enter confirmation password")
            return render_template("changepassword.html")
        elif not check_password_hash(info[0]["hash"], request.form.get("oldpassword")):
            flash("Old password isn't correct")
            return render_template("changepassword.html")
        elif request.form.get("password") != request.form.get("confirmation"):
            flash("Passwords don't match")
            return render_template("changepassword.html")
        db1.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(request.form.get("password")), session_user_id)
        #print('HEY')
        flash("Password Changed")
        return redirect('/accounts')


@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    if request.method == "GET":
        database_get = db1.execute("SELECT price, book_title, book_subject, book_description, book_syllabus FROM users JOIN database4 ON database4.user_id = users.id WHERE database4.id = ?", id)
        return render_template("edit_data.html" )
    else:
        #db1.execute("UPDATE database4 SET price = ?, book_title = ?, book_subject = ?, book_description = ?, book_syllabus = ?", request.form.get("price"), request.form.get("book_title"), request.form.get("book_subject"), request.form.get("book_description"), request.form.get("book_syllabus"))
        #print('hello from ')
        return render_template('index.html')
        pic = request.files['pic']
        if not pic:
            return 'No pic uploaded!', 400
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
            return 'Bad upload!', 400
        session_user_id = session["user_id"] #database3 and below had load_type, which was a manual input by me. It was either 'UPLOAD' or 'DELETE', but i removed it to try and possibly save space
        db1.execute("INSERT INTO database4 (user_id, price, book_title, book_subject, book_description, book_syllabus) VALUES(?, ?, ?, ?, ?, ?)", session["user_id"], request.form.get("price"), request.form.get("book_title"), request.form.get("book_subject"), request.form.get("book_description"), request.form.get("book_syllabus"))
        db_id_list = db1.execute("SELECT id FROM database4 WHERE user_id = ? ORDER BY id DESC LIMIT 1", session_user_id)
        db_id = db_id_list[0]["id"]
        img = Img17(img=pic.read(), name=filename, id=db_id, mimetype=mimetype, user_id=session_user_id)
            

        db.session.add(img)
        db.session.commit()

@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        rows = db1.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Please enter username")
            return render_template("login.html")
        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Please enter password")
            return render_template("login.html")
        # Query database for username
        # Ensure username exists and password is correct
        elif len(rows) != 1:
            flash("Username not found")
            return render_template("login.html")
        elif not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Password isn't correct")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        return redirect("/searchnotes")
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        register_rows = db1.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # Validating entered information
        if not request.form.get("username"):
            flash("Please enter username")
            return render_template("register.html")
        elif not request.form.get("password"):
            flash("Please enter password")
            return render_template("register.html")
        elif not request.form.get("confirmation"):
            flash("Please enter confirmation password")
            return render_template("register.html")
        elif request.form.get("password") != request.form.get("confirmation"):
            flash("Passwords don't match")
            return render_template("register.html")
        elif len(register_rows) > 0:
            flash("Username isn't available")
            return render_template("register.html")
        #username = request.form.get("username")
        #password = generate_password_hash(request.form.get("password"))
        db1.execute("INSERT INTO users (username, hash, email, socials) VALUES(?, ?, ?, ?)", request.form.get("username"), generate_password_hash(request.form.get("password")), request.form.get("email"), request.form.get("socials"))

        register_rows = db1.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        session["user_id"] = register_rows[0]["id"]
        return redirect("/")

@app.route("/info/<int:id>")
def info(id):
    images = db.session.query(Img17).filter_by(id = id)
    if not images:
        return 'Img Not Found!', 404
    #return Response(img.img, mimetype=img.mimetype)

    #get_id = request.form.get("id")
    database_get = db1.execute("SELECT username, email, socials, price, book_title, book_subject, book_description, book_syllabus FROM users JOIN database4 ON database4.user_id = users.id WHERE database4.id = ?", id)

    print("DATABASE: ", database_get)
    #list1 = database_get[0]["list"]
    images = db.session.query(Img17).filter_by(id = id)
    #print('')
    #print("Images: ", images)
    for img in images:
        image = base64.b64encode(img.img).decode('ascii')
        database_get[0]["image"] = image
    #return redirect(url_for('info', list=database_get))
    #print('')
    #print("DATABASE: ", database_get)
    #print("list: ", list1)
    #print('')
    #user_get = 1
    return render_template('info.html', list=database_get)


    #if request.method == "GET":
    #return "hey"
    #else:
    #return "yo"
    #img = Img17.query.filter_by(id=id).first()

    get_id = request.form.get("id")
    print("ID: ", get_id)
    database_get = db1.execute("SELECT username, email, phone, socials, price, book_title, book_subject, book_description, book_syllabus FROM users JOIN database4 ON database4.user_id = users.id WHERE database4.id = ?", get_id)
    print("DATABASE: ", database_get)
    #list1 = database_get[0]["list"]
    images = db.session.query(Img17).filter_by(id = get_id)
    for img in images:
        image = base64.b64encode(img.img).decode('ascii')
        database_get[0]["image"] = image
    return render_template('info.html', list=database_get)
    return render_template("info.html")

@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    flash("Logged Out")
    return redirect("/")