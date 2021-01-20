from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from helpers import apology, isint, login_required
import datetime
import time
from tempfile import mkdtemp
from sql import SQL
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure DB using SQL lib (from CS50)
db = SQL('sqlite:///databases/ticketing.db')


@app.route("/")
@login_required
def index():
    """Welcome page"""
    user = session['user_id']
    # user = "temp_user"
    role = get_role(user)
    # role = "user"
    if role == "admin":
        # Look for every open ticket
        rows = db.execute("SELECT * FROM 'tickets' WHERE status = :status ORDER BY date ASC", status='open')

    else:
        # Look for every open ticket by that user
        rows = db.execute("SELECT * FROM 'tickets' WHERE username = :username AND status = :status ORDER BY date ASC",
                          username=user, status='open')

    # Format date
    for row in rows:
        row['date'] = datetime.datetime.fromtimestamp(row['date'])
        row['proj_name'] = db.execute("SELECT * from projects WHERE id = :proj_id", proj_id=row['project'])[0]['name']

    return render_template("home.html", text=user, items=rows)


@app.route('/sayhi', methods=["GET", "POST"])
def say_hi():
    if request.method == "POST":
        # apology if name is blank
        print(request.form.get("name"))
        if not request.form.get("name"):
            return apology("Must provide a name", 403)

        name = request.form.get("name")
        return render_template("hello.html", name=name)

    else:
        return render_template("sayhi.html")


@app.route("/lookup/<ticketnr>", methods=["GET", "POST"])
@app.route("/lookup", methods=["GET", "POST"])
# @login_required
def lookup(ticketnr=None):
    """Lookup a ticket and its modifications"""

    if request.method == "POST":

        # apology if description blank
        if not request.form.get("ticket"):
            return apology("must provide a ticket number", 403)

        # check if number is an integer
        if not isint(request.form.get("ticket")):
            return apology("ticket number must be an integer", 403)
        elif int(request.form.get("ticket")) <= 0:
            return apology("ticket number must be a positive integer", 403)
        else:
            ticket_nr = int(request.form.get("ticket"))

        # depending on user : basic user can only see his tickets
        rows1 = db.execute("SELECT * FROM tickets WHERE id = ?", ticket_nr)
        if not rows1:
            return apology("ticket doesnt exist", 403)

        # looks for modifications
        rows2 = db.execute("SELECT * FROM jobs WHERE ticket = ?", ticket_nr)
        for row in rows1:
            row['date'] = datetime.datetime.fromtimestamp(row['date'])

        # Create a list of items to print and pass them as an argument to the template
        for row in rows2:
            row['date'] = datetime.datetime.fromtimestamp(row['date'])

        return render_template("lookedup.html", ticket=rows1[0], jobs=rows2)

    else:
        return render_template("lookup.html", ticket=ticketnr)


@app.route("/drop", methods=["GET", "POST"])
def drop():
    """Creates a new ticket"""
    if request.method == "POST":

        # apology if description blank
        if not request.form.get("description"):
            return apology("must provide a description", 403)

        # apology if project blank
        if not request.form.get("project"):
            return apology("must provide a project name", 403)

        # if drop menu is "new project" then project name is the one from the popup input box, unless already exists
        # if... :
        #    proj_name =
        # else :
        proj_name = request.form.get("project")

        # make sure project exists in database
        projects = db.execute("SELECT * FROM projects WHERE name = :name", name=proj_name)
        if not projects:
            return apology("project not found", 403)

        # add ticket to database
        db.execute("INSERT INTO tickets (project, date, username, status) VALUES (?, ?, ?, ?)",
                   projects[0]['id'], round(time.time()), session['user_id'], 'open')

        # select latest ticket
        rows = db.execute("SELECT * FROM tickets ORDER  BY id DESC LIMIT 1")

        # add intervention to the list
        db.execute("INSERT INTO jobs (ticket, date, username, description, status) VALUES (?, ?, ?, ?, ?)",
                   rows[0]['id'], round(time.time()), session['user_id'], request.form.get("description"), "open")

        return render_template("dropped.html", ticket=rows[0]['id'], project=request.form.get("project"))

    else:
        projects = db.execute("SELECT * FROM projects")
        return render_template("drop.html", projects=projects)


@app.route("/edit", methods=["GET", "POST"])
@app.route("/edit/<ticketnr>", methods=["GET", "POST"])
def edit(ticketnr=None):
    """Display a ticket, its history and a form for modification"""

    if request.method == "POST":

        # apology if description blank
        if not request.form.get("ticket"):
            return apology("must provide a ticket number", 403)

        # check if number is an integer
        if not isint(request.form.get("ticket")):
            return apology("ticket number must be an integer", 403)
        elif int(request.form.get("ticket")) <= 0:
            return apology("ticket number must be a positive integer", 403)
        else:
            ticket_nr = int(request.form.get("ticket"))

        # depending on user : basic user can only edit his tickets
        user = session['user_id']
        # user = "temp_user"
        role = get_role(user)
        # role = "user"
        if role == "admin":
            rows1 = db.execute("SELECT * FROM tickets WHERE id = :ticket_nr", ticket_nr=ticket_nr)
            if not rows1:
                return apology("ticket doesnt exist", 403)
        else:
            rows1 = db.execute("SELECT * FROM tickets WHERE id = :ticket_nr AND username = :username",
                               ticket_nr=ticket_nr, username=user)
            if not rows1:
                return apology("ticket doesnt belong to user", 403)

        # looks for modifications
        rows2 = db.execute("SELECT * FROM jobs WHERE ticket = :ticket", ticket=ticket_nr)
        for row in rows1:
            row['date'] = datetime.datetime.fromtimestamp(row['date'])

        # Create a list of items to print and pass them as an argument to the template
        for row in rows2:
            row['date'] = datetime.datetime.fromtimestamp(row['date'])

        # Find out project name
        proj_name = db.execute("SELECT * from projects WHERE id = :proj_id", proj_id=rows1[0]['project'])[0]['name']

        # Create list of project to pass as an argument to the page
        projects = db.execute("SELECT * FROM projects")
        return render_template("editing.html", ticket=rows1[0], jobs=rows2, projects=projects, proj_name=proj_name)

    else:
        return render_template("edit.html", ticket=ticketnr)


@app.route("/editing", methods=["POST"])
def editing():
    """Edits the ticket in the database"""

    # make sure project exists in database
    projects = db.execute("SELECT * FROM projects WHERE name = :name", name=request.form.get("project"))
    if not projects:
        return apology("project not found", 403)

    # TODO : make sure there's a status and a list

    # add job
    db.execute("INSERT INTO jobs (ticket, date, username, description, status) VALUES (?, ?, ?, ?, ?)",
               request.form.get("ticket"), round(time.time()), session['user_id'], request.form.get("comment"),
               request.form.get("status"))
    # Update status of ticket accordingly
    db.execute("UPDATE tickets SET project = ?, status = ? WHERE id = ?", projects[0]['id'], request.form.get("status"),
               request.form.get("ticket"))

    # Request (up to date) data to the base
    rows1 = db.execute("SELECT * FROM tickets WHERE id = :ticket_nr", ticket_nr=request.form.get("ticket"))
    rows2 = db.execute("SELECT * FROM jobs WHERE ticket = :ticket", ticket=request.form.get("ticket"))

    # Format dates
    for row in rows1:
        row['date'] = datetime.datetime.fromtimestamp(row['date'])
    for row in rows2:
        row['date'] = datetime.datetime.fromtimestamp(row['date'])

    # Find out project name
    proj_name = db.execute("SELECT * from projects WHERE id = :proj_id", proj_id=rows1[0]['project'])[0]['name']

    # Create list of project to pass as an argument to the page
    projects = db.execute("SELECT * FROM projects")
    return render_template("editing.html", ticket=rows1[0], jobs=rows2, projects=projects, proj_name=proj_name)


@app.route("/newproject", methods=["GET", "POST"])
def newproject():
    """creates a new project"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure user is admin
        if not get_role(session['user_id']) == 'admin':
            return apology("must be an admin", 403)

        # Ensure username was submitted
        if not request.form.get("projectname"):
            return apology("must provide projectname", 403)

        # Look for projectname in the base and apology if exists
        project_name = request.form.get("projectname")
        rows = db.execute("SELECT * FROM projects WHERE name = :name", name=project_name)

        a = len(rows)
        print(a)
        if a != 0:
            print(rows[0])

        if len(rows) == 0:
            db.execute("INSERT INTO projects (name) VALUES (?)", project_name)
        else:
            return apology("project already exists", 403)

        return render_template("projectcreated.html", projectname=project_name)

    else:
        return render_template("newproject.html")


@app.route("/history")
def history():
    """Show history of tickets opened by user"""

    # Create a list of items to print and pass them as an argument to the template

    # depending on user : basic user can only see his tickets
    user = session['user_id']
    # user = "temp_user"
    role = get_role(user)
    # role = "admin"
    if role == "admin":
        rows = db.execute("SELECT * FROM tickets ORDER BY date DESC")
        if not rows:
            return apology("No tickets to display", 403)
    else:
        rows = db.execute("SELECT * FROM 'tickets' WHERE username = :username ORDER BY date DESC", username=user)
        if not rows:
            return apology("ticket doesnt belong to user", 403)

    for row in rows:
        row['date'] = datetime.datetime.fromtimestamp(row['date'])
        row['proj_name'] = db.execute("SELECT * from projects WHERE id = :proj_id", proj_id=row['project'])[0]['name']

    return render_template("history.html", items=rows)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure email was submitted
        elif not request.form.get("email"):
            return apology("must provide email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username doesn't exists and password is correct
        if len(rows) != 0:
            return apology("username already exists", 403)
        elif request.form.get("password") != request.form.get("confirmation"):
            # TODO : compare strings or hash and compare hashs ?
            return apology("passwords don't match", 403)
        else:
            # Insert new user in users table (hash user's password)
            db.execute("INSERT INTO users (username, hash, email) VALUES (?, ?, ?)",
                       request.form.get("username"), generate_password_hash(request.form.get("confirmation")),
                       request.form.get("email"))

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


def get_role(user):
    # Check if user is admin or user
    role = db.execute("SELECT role FROM 'users' WHERE username = :username", username=user)
    return role[0]['role']


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
