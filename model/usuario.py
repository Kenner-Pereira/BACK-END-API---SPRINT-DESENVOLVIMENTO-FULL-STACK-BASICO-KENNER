from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Comentario


class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column("pk_usuario", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    sexo = Column(String(40))
    idade = Column(Integer)
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o produto e o comentário.
    # Essa relação é implicita, não está salva na tabela 'produto',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    comentarios = relationship("Comentario")

    def __init__(self, nome:str, sexo:str, idade:int,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Usuario

        Arguments:
            nome: nome do usuario.
            sexo: sexo do usuario cadastrado
            idade: idade do usuario
            data_insercao: data de quando o usuario foi cadastrado
        """
        self.nome = nome
        self.sexo = sexo
        self.idade = idade

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_comentario(self, comentario:Comentario):
        """ Adiciona um novo comentário ao Usuario
        """
        self.comentarios.append(comentario)

