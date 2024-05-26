from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import SelectField, SubmitField, FileField, IntegerField, BooleanField
from wtforms.validators import InputRequired


class MainForm(FlaskForm):
    image = FileField(validators=[FileAllowed([".jpg", ".jpeg"])])
    effect = SelectField(label="effect", choices=[("blackwhite", "Preto e Branco"),
                                                  ("red", "Vermelho"),
                                                  ("green", "Verde"),
                                                  ("blue", "Azul"),
                                                  ("inverted", "RGB Invertido")])
    rotation = SelectField(label="rotation", choices=[("90degrees", "90 graus"),
                                                      ("180degrees", "180 graus"),
                                                      ("270degrees", "270 graus")])
    translation = SelectField(label="translation", choices=[("up", "Para cima"),
                                                            ("down", "Para baixo"),
                                                            ("left", "Para esquerda"),
                                                            ("right", "Para direita")])
    translation_pixels = IntegerField(label="translationpixels", validators=[InputRequired()])
    scale = SelectField(label="scale", choices=[("25percent", "25%"),
                                                ("50percent", "50%"),
                                                ("75percent", "75%"),
                                                ("150percent", "150%"),
                                                ("200percent", "200%")])
    edge_highlighting = BooleanField(label="edge_highlighting")
    mirroring = BooleanField(label="mirroring")
    homography = BooleanField(label="homography")
    submit = SubmitField("Modificar")
