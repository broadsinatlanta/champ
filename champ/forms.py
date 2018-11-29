from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Regexp, Length


class ContactForm(FlaskForm):
    name = StringField("Username", [DataRequired()])
    # Email regex from https://emailregex.com/
    email = StringField("Email", validators=[DataRequired(message="Please enter your email address."), Regexp(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", message="Please enter a valid email.")])
    positive = StringField("One thing you like about Champ", validators=[DataRequired(message="Please mention something you have enjoyed about Champ.")])
    negative = StringField("One thing would improve in Champ", validators=[DataRequired(message="Please mention something you think could be improved in Champ.")])
    contactMessage = TextAreaField("Message", validators=[DataRequired(message="Please enter your message."), Length(min=1, max=500, message="Message must be between 1 and 500 characters long.")])
    sentiment = HiddenField("Experience", id="sentiment")
    positiveSubmit = SubmitField("I think Champ is great :)")
    negativeSubmit = SubmitField("I don't think Champ is great :(")
