from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class ActionForm(FlaskForm):
    submit = SubmitField("Submit")


class CommentForm(FlaskForm):
    content = TextAreaField(
        "Comment",
        validators=[DataRequired(), Length(min=3, max=500)],
    )
    submit = SubmitField("Post Comment")

