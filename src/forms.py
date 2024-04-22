from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import SelectField, SubmitField, FileField


class MainForm(FlaskForm):
    image = FileField(validators=[FileAllowed([".jpg", ".jpeg"])])
    effect = SelectField(label="effect", choices=[("blackwhite", "Preto e Branco"),
                                                  ("red", "Vermelho"),
                                                  ("green", "Verde"),
                                                  ("blue", "Azul"),
                                                  ("inverted", "RGB Invertido")])
    submit = SubmitField("Modificar")
