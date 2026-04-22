from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional, URL, ValidationError


class ActionForm(FlaskForm):
    pass


class CourseForm(FlaskForm):
    title = StringField(
        "Course Title",
        validators=[DataRequired(), Length(min=3, max=150)],
    )
    description = TextAreaField(
        "Description",
        validators=[DataRequired(), Length(min=20)],
    )
    image = StringField(
        "Image URL",
        validators=[Optional(), URL()],
    )
    submit = SubmitField("Save Course")


class LessonForm(FlaskForm):
    title = StringField(
        "Lesson Title",
        validators=[DataRequired(), Length(min=3, max=150)],
    )
    content = TextAreaField(
        "Lesson Content",
        validators=[DataRequired(), Length(min=20)],
    )
    video_url = StringField(
        "Video Embed URL",
        validators=[Optional(), URL()],
    )
    submit = SubmitField("Save Lesson")


class QuizForm(FlaskForm):
    title = StringField(
        "Quiz Title",
        validators=[DataRequired(), Length(min=3, max=150)],
    )
    submit = SubmitField("Save Quiz")


class QuestionForm(FlaskForm):
    question_text = TextAreaField(
        "Question",
        validators=[DataRequired(), Length(min=8)],
    )
    options_text = TextAreaField(
        "Options",
        validators=[DataRequired()],
        description="Write one option per line.",
    )
    correct_answer = StringField(
        "Correct Answer",
        validators=[DataRequired(), Length(min=1, max=255)],
    )
    submit = SubmitField("Save Question")

    def parsed_options(self):
        return [line.strip() for line in self.options_text.data.splitlines() if line.strip()]

    def validate_options_text(self, field):
        options = self.parsed_options()
        if len(options) < 2:
            raise ValidationError("Add at least two answer options.")

    def validate_correct_answer(self, field):
        options = self.parsed_options()
        if field.data.strip() not in options:
            raise ValidationError("The correct answer must exactly match one listed option.")

