from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from  model import Base


class Comentario(Base):
    __tablename__ = 'comentario'

    id = Column(Integer, primary_key=True)
    texto = Column(String(4000))
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o comentário e um usuario.
    # Aqui está sendo definido a coluna 'usuario' que vai guardar
    # a referencia ao usuario, a chave estrangeira que relaciona
    # um usuario ao comentário.
    usuario = Column(Integer, ForeignKey("usuario.pk_usuario"), nullable=False)

    def __init__(self, texto:str, data_insercao:Union[DateTime, None] = None):
        """
        Cria um Comentário

        Arguments:
            texto: o texto de um comentário.
            data_insercao: data de quando o comentário foi feito ou inserido
                           à base
        """
        self.texto = texto
        if data_insercao:
            self.data_insercao = data_insercao
