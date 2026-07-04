from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Usuario, Comentario
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
usuario_tag = Tag(name="Usuario", description="Adição, visualização e remoção de usuários à base")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário à um usuário cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/usuario', tags=[usuario_tag],
          responses={"200": UsuarioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_usuario(form: UsuarioSchema):
    """Adiciona um novo Usuário à base de dados

    Retorna uma representação dos usuários e comentários associados.
    """
    usuario = Usuario(
        nome=form.nome,
        sexo=form.sexo,
        idade=form.idade)
    logger.debug(f"Adicionando usuario de nome: '{usuario.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando usuario
        session.add(usuario)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado usuário de nome: '{usuario.nome}'")
        return apresenta_usuario(usuario), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Usuário de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar usuário '{usuario.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo usuário :/"
        logger.warning(f"Erro ao adicionar usuário '{usuario.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/usuarios', tags=[usuario_tag],
         responses={"200": ListagemUsuariosSchema, "404": ErrorSchema})
def get_usuarios():
    """Faz a busca por todos os usuários cadastrados

    Retorna uma representação da listagem de Usuários.
    """
    logger.debug(f"Coletando usuários ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    usuarios = session.query(Usuario).all()

    if not usuarios:
        # se não há produtos cadastrados
        return {"usuários": []}, 200
    else:
        logger.debug(f"%d usuários encontrados" % len(usuarios))
        # retorna a representação de produto
        print(usuarios)
        return apresenta_usuarios(usuarios), 200


@app.get('/usuario', tags=[usuario_tag],
         responses={"200": UsuarioViewSchema, "404": ErrorSchema})
def get_usuario(query: UsuarioBuscaSchema):
    """Faz a busca por um Usuário a partir do nome do usuário informado

    Retorna uma representação dos usuários e comentários associados.
    """
    usuario_nome = query.nome
    logger.debug(f"Coletando dados sobre usuario #{usuario_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    usuario = session.query(Usuario).filter(Usuario.nome == usuario_nome).first()

    if not usuario:
        # se o usuario não foi encontrado
        error_msg = "usuario não encontrado na base :/"
        logger.warning(f"Erro ao buscar Usuário '{usuario_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"usuário econtrado: '{usuario.nome}'")
        # retorna a representação de usuario
        return apresenta_usuario(usuario), 200


@app.delete('/usuario', tags=[usuario_tag],
            responses={"200": UsuarioDelSchema, "404": ErrorSchema})
def del_usuario(query: UsuarioBuscaSchema):
    """Deleta um Usuário a partir do nome de usuário informado

    Retorna uma mensagem de confirmação da remoção.
    """
    usuario_nome = unquote(unquote(query.nome))
    print(usuario_nome)
    logger.debug(f"Deletando dados sobre usuario #{usuario_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Usuario).filter(Usuario.nome == usuario_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado Usuario #{usuario_nome}")
        return {"mesage": "Usuário removido", "id": usuario_nome}
    else:
        # se o usuario não foi encontrado
        error_msg = "Usuário não encontrado na base :/"
        logger.warning(f"Erro ao deletar usuário #'{usuario_nome}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.post('/cometario', tags=[comentario_tag],
          responses={"200": UsuarioViewSchema, "404": ErrorSchema})
def add_comentario(form: ComentarioSchema):
    """Adiciona de um novo comentário à um usuário cadastrado na base identificado pelo id

    Retorna uma representação dos usuarios e comentários associados.
    """
    usuario_id  = form.usuario_id
    logger.debug(f"Adicionando comentários ao usuário #{usuario_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo produto
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        # se usuario não encontrado
        error_msg = "Usuario não encontrado na base :/"
        logger.warning(f"Erro ao adicionar comentário ao usuário '{usuario_id}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando o comentário
    texto = form.texto
    comentario = Comentario(texto)

    # adicionando o comentário ao usuário
    usuario.adiciona_comentario(comentario)
    session.commit()

    logger.debug(f"Adicionado comentário ao usuário #{usuario_id}")

    # retorna a representação de produto
    return apresenta_usuario(usuario), 200

