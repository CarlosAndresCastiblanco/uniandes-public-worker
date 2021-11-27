from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import sqlalchemy
from sqlalchemy.orm import relationship
import datetime

db = SQLAlchemy()
ma = Marshmallow()


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    conversiones = relationship("Conversion")


class Usuario_Schema(ma.Schema):
    class Meta:
        fields = ("id", "username", "email")


usuario_schema = Usuario_Schema()


class Conversion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    origen = db.Column(db.String(50))
    destino = db.Column(db.String(50))
    estado = db.Column(db.String(50))
    fecha = db.Column(db.String(50))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))


class Conversion_Schema(ma.Schema):
    class Meta:
        fields = ("id", "nombre", "origen", "destino", "estado", "fecha")


conversion_schema = Conversion_Schema()
conversiones_schema = Conversion_Schema(many=True)