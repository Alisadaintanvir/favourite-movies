from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, FloatField
from wtforms.validators import DataRequired, NumberRange, URL


class MovieForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    year = IntegerField('Year')
    description = TextAreaField('Description')
    rating = FloatField('Rating', validators=[NumberRange(min=0, max=10)])
    ranking = IntegerField('Ranking', validators=[NumberRange(min=1)])
    review = TextAreaField('Review')
    img_url = StringField('Image URL', validators=[URL()])
    submit = SubmitField("Add")
