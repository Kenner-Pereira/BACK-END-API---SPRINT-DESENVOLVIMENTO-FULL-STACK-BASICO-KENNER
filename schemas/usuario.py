from pydantic import BaseModel
from typing import Optional, List
from model.usuario import Usuario

from schemas import ComentarioSchema


class UsuarioSchema(BaseModel):
    """ Define como um novo produto a ser inserido deve ser representado
    """
    nome: str = "João Silva"
    sexo: str = "Masculino"
    idade: int = 31


class UsuarioBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do produto.
    """
    nome: str = "Teste"


class ListagemUsuariosSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    usuarios:List[UsuarioSchema]


def apresenta_usuarios(usuarios: List[Usuario]):
    """ Retorna uma representação do usuario seguindo o schema definido em
        UsuarioViewSchema.
    """
    result = []
    for usuario in usuarios:
        result.append({
            "nome": usuario.nome,
            "sexo": usuario.sexo,
            "idade": usuario.idade,
        })

    return {"usuarios": result}


class UsuarioViewSchema(BaseModel):
    """ Define como um produto será retornado: produto + comentários.
    """
    id: int = 1
    nome: str = "João Silva"
    sexo: str = "Masculino"
    idade: int = 31
    total_cometarios: int = 1
    comentarios:List[ComentarioSchema]


class UsuarioDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_usuario(usuario: Usuario):
    """ Retorna uma representação do usuario seguindo o schema definido em
        UsuarioViewSchema.
    """
    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "sexo": usuario.sexo,
        "idade": usuario.idade,
        "total_cometarios": len(usuario.comentarios),
        "comentarios": [{"texto": c.texto} for c in usuario.comentarios]
    }
