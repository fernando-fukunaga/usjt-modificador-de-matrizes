from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import SelectField, SubmitField, FileField, IntegerField, BooleanField
from wtforms.validators import InputRequired


class MainForm(FlaskForm):
    image = FileField(validators=[FileAllowed([".jpg", ".jpeg"])])
    effect = SelectField(label="effect", choices=[("no_effect", "Sem efeito"),
                                                  ("black_white", "Preto e Branco"),
                                                  ("red", "Vermelho"),
                                                  ("green", "Verde"),
                                                  ("blue", "Azul"),
                                                  ("inverted", "RGB Invertido")])
    rotation = SelectField(label="rotation", choices=[("no_rotation", "Não rotacionar"),
                                                      ("90_degrees", "90 graus"),
                                                      ("180_degrees", "180 graus"),
                                                      ("270_degrees", "270 graus")])
    translation = SelectField(label="translation", choices=[("up", "Para cima"),
                                                            ("down", "Para baixo"),
                                                            ("left", "Para esquerda"),
                                                            ("right", "Para direita")])
    translation_pixels = IntegerField(label="translationpixels", validators=[InputRequired()])
    scale = SelectField(label="scale", choices=[("100_percent", "100% (não alterar)"),
                                                ("25_percent", "25%"),
                                                ("50_percent", "50%"),
                                                ("75_percent", "75%"),
                                                ("150_percent", "150%"),
                                                ("200_percent", "200%")])
    edge_highlighting = BooleanField(label="edge_highlighting")
    mirroring = BooleanField(label="mirroring")
    homography = BooleanField(label="homography")
    submit = SubmitField("Modificar")
