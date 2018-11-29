from flask import render_template, request, redirect, flash
from champ.Workout import returnWorkout
from champ import app, data
from champ.forms import ContactForm
from champ.models import Feedback
from champ.mail import sendFeedback
from champ.personal import adminEmail, adminPassword


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    response.headers['Cache-Control'] = 'public, max-age=0'

    return response


# Homepage
@app.route("/")
def index():
    form = ContactForm()

    return render_template("index.html", form=form)


# About page
@app.route("/config")
def designWorkout():
    form = ContactForm()

    # Decide which page to be shown
    exp = request.args.get("exp")

    # Check validity of use
    if exp is None:
        flash("Please Use The 'Get Started' Navbar Option To Begin.", "info")
        return redirect("/")

    # Beginners are shown a different set of options to experienced people,
    # getting to the page in other ways result in a splash being shown.
    if exp == "beginner":

        return render_template("config_b.html", form=form)

    elif exp == "experienced":

        flash("Experienced Configuration Coming Soon!", "info")
        return render_template("config_b.html", form=form)

    else:

        flash("Please Use The 'Get Started' Navbar Option To Begin.", "info")
        return render_template("config_b.html", form=form)


@app.route("/getWorkout", methods=["GET", "POST"])
def getWorkout():
    form = ContactForm()

    # Has to be post to use form data - if not, bounce to home
    if request.method != "POST":

        # Give feedback & redirect if wrong method
        flash("Please Use The 'Get Started' Navbar Option To Begin.", "info")
        return redirect("/")

    # Get goal from form to determine the second workout param
    goal = request.form.get("goal")

    # For cardio workouts, the required input is different
    if goal == "cardio":

        groupOrCardio = request.form.get("cardio")

        # Jumbotron title generation
        spec1 = goal.capitalize()

        if groupOrCardio == "hiit":

            spec2 = "HIIT"

        elif groupOrCardio == "regular":

            spec2 = "regular"

        else:

            spec2 = "HIIT & regular"

    else:

        groupOrCardio = request.form.get("group")

        # Jumbotron title generation
        spec2 = groupOrCardio

        if goal == "low":

            spec1 = "Strength"

        elif goal == "mix":

            spec1 = "Muscle Growth"

        else:

            spec1 = "Muscle Conditioning"

    # Get gear requirements
    gear = request.form.get("gear")

    # Get Workout class object
    workout = returnWorkout(data, goal, groupOrCardio, gear)

    # Get both warmup and routines
    workout.generateWarmup()
    workout.generateRoutine()

    # Format and extract workout/routine DataFrames
    dfs = workout.formatFullRoutine()

    # Classes for table to have
    tbl_classes = ["table", "routine-custom", "table-hover", "table-sm",
                   "thead-dark"]

    # Coerce to html
    df_html = [df.to_html(index=False, classes=tbl_classes, justify="center")
               for df in dfs]

    return render_template("workout.html", tables=df_html, spec1=spec1,
                           spec2=spec2, form=form)


@app.route("/contact", methods=["GET", "POST"])
def contact():

    # Initialise form
    form = ContactForm()

    # If request is GET, show form
    if request.method == "GET":

        return render_template("contact.html", form=form)

    # Else, post form to db, email to webmaster OR show errors

    # If form is valid:
    if form.validate_on_submit():

        # Extract form data
        userComment = Feedback(name=form.name.data,
                               sentiment=form.sentiment.data,
                               email=form.email.data,
                               positive=form.positive.data,
                               negative=form.negative.data,
                               message=form.contactMessage.data)

        # Add to db
        userComment.save()

        # Email the feedback to admin
        sendFeedback(userComment, adminEmail, adminPassword)

        # Return thanks page
        return render_template("thanks.html")

    # for every error, make flash message
    for i in form.errors.values():
        flash(i[0], "danger")

    return redirect("/contact")
