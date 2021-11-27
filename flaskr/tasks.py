from datetime import datetime
from celery import Celery
from celery.utils.log import get_task_logger
from pydub import AudioSegment
import os
from pathlib import Path
from celery.schedules import crontab
from datetime import timedelta
from pydub.utils import which
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.sqltypes import DateTime
import smtplib
from flaskr.storage.storage import *
from flask import Flask
from flask_restful import Api
from flaskr.vistas.vistas import RecursoDescargar
from flaskr.models.modelos import db

settings_module = os.getenv('APP_SETTINGS_MODULE')
flask_app = Flask(__name__)
flask_app.config.from_object(settings_module)
app_context = flask_app.app_context()
app_context.push()
db.init_app(flask_app)
api = Api(flask_app)

api.add_resource(RecursoDescargar, '/service')

"""
Config Enviroment
"""
#uri_database = os.getenv('SQLALCHEMY_DATABASE_URI')
"""
Launch DataBase

engine = create_engine(uri_database, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

Config Entities DataBase
"""
"""

class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(50), unique=True)
    password = Column(String(50))
    conversiones = relationship("Conversion")


class Conversion(Base):
    __tablename__ = 'conversion'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50))
    origen = Column(String(50))
    destino = Column(String(50))
    estado = Column(String(50))
    fecha = Column(String(50))
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
"""

AudioSegment.converter = which("ffmpeg")

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

appC = make_celery(flask_app)
logger = get_task_logger(__name__)
PATH = str(Path().absolute(), )

appC.conf.beat_schedule = {
    'add-every-180-seconds': {
        'task': 'tasks.add',
        'schedule': 180,
    },
}
appC.conf.timezone = 'UTC'


@appC.task(name="tasks.add")
def test():
    receive_and_delete_messages_queue()

    result = session.query(Conversion).filter(Conversion.estado.in_(['uploaded'])).all()
    print('size query............. ', len(result))


"""
    for row in result:
        print('row.................... ',row)
        try:
            if find_object('uniandes-bucket-s3', 'us-east-1',
                           "origin-{}-{}.{}".format(row.usuario_id, row.id, row.origen)):
                downloading_files(
                    'originales/{}'.format("origin-{}-{}.{}".format(row.usuario_id, row.id, row.origen)),
                    'uniandes-bucket-s3',
                    "origin-{}-{}.{}".format(row.usuario_id, row.id, row.origen),
                    'us-east-1'
                )
                archivo = AudioSegment.from_file(
                    "originales/origin-{}-{}.{}".format(row.usuario_id, row.id, row.origen),
                    str(row.origen))
                archivo.export(
                    "originales/destino-{}-{}.{}".format(row.usuario_id, row.id, row.destino),
                    format=row.destino)
                print('convertido satisfactoriamente',
                      "destino-{}-{}.{}".format(row.usuario_id, row.id, row.destino))
                upload_file("originales/destino-{}-{}.{}".format(row.usuario_id, row.id, row.destino),
                            'uniandes-bucket-s3',
                            "destino-{}-{}.{}".format(row.usuario_id, row.id, row.destino),
                            'us-east-1')
                remove_file("originales/destino-{}-{}.{}".format(row.usuario_id, row.id, row.destino))
                row.estado = "processed"
                session.commit()
            else:
                print("Archivo no encontrado en S3")
        except Exception as err:
            print('error convirtiendo')
            print(err)
            print(err.args)
"""
