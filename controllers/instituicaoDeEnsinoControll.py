from flask import Blueprint, jsonify, request
from psycopg2 import DatabaseError
from helpers.logger import logger
from models.instituicaoensino import InstituicaoEnsino, InstituicaoEnsinoSchema
from http import HTTPStatus
from marshmallow import ValidationError
from services.instEnsinoService import instEnsinoService
from models.paginacao import PaginacaoSchema

paginacao_schema = PaginacaoSchema()
instituicao_schema = InstituicaoEnsinoSchema()
instituicoes_schema = InstituicaoEnsinoSchema(many=True)

def row_to_instituicao(row):
    return InstituicaoEnsino(
        id=row[0],
        no_entidade=row[1],
        co_entidade=row[2],
        no_uf=row[3],
        sg_uf=row[4],
        co_uf=row[5],
        no_municipio=row[6],
        co_municipio=row[7],
        nu_ano_censo=row[8],
        qt_mat_bas=row[9],
        qt_mat_inf=row[10],
        qt_mat_fund=row[11],
        qt_mat_med=row[12],
        qt_mat_prof=row[13],
        qt_mat_eja=row[14],
        qt_mat_esp=row[15],
        ativo=row[16],
        created=row[17]
    )

instituicao_ensino_bp = Blueprint( 'instituicaoensino', __name__, url_prefix='/instituicoesensino')

@instituicao_ensino_bp.get("/")
def get_all_instituicoes():
    try:
        logger.info("listando as insituições")
        paginacao = paginacao_schema.load(request.args)

        service = instEnsinoService()
        page = paginacao["page"]
        per_page = paginacao["per_page"]
        logger.info(
            f"Listando as Instituições de Ensino - página {page} com {per_page} registros")

    
        instituicoes = service.get_all(page, per_page)
        instituicoes["data"] = instituicoes_schema.dump(instituicoes["data"])

        logger.info("finalizando a listagem das insituições")
        return jsonify(instituicoes), HTTPStatus.OK

    except ValidationError as err:
        return {"erro": "Parâmetros de paginação inválidos", "campos": err.messages}, HTTPStatus.BAD_REQUEST
    except DatabaseError:
        logger.error(f"Erro no banco de dados: {err}")
        return {
            "mensagem": "Problema ao estabelecer a conexão"
        }, HTTPStatus.INTERNAL_SERVER_ERROR


@instituicao_ensino_bp.get("/<int:id>")
def get_instituicao_by_id(id):
    try:
        logger.info(f"listando a insituição de ensino com ID: {id}")
        Service = instEnsinoService()
        instituicao = Service.get_by_id(id)
        if instituicao is None:
            return {
                "mensagem": "Instituição de ensino não encontrada"
            }, HTTPStatus.NOT_FOUND

        logger.info(f"finalizando a Listagem da insituição de ensino com ID: {id}")
        return jsonify(instituicao_schema.dump(instituicao)), HTTPStatus.OK
    except DatabaseError:
        return {
            "mensagem": "Problema ao estabelecer a conexão"
        }, HTTPStatus.INTERNAL_SERVER_ERROR



@instituicao_ensino_bp.post("/")
def post_instituicao():
    try:
        logger.info("iniciando a criação da nova insituição")
        dados = instituicao_schema.load(request.get_json())

        Service = instEnsinoService()
        instituicao = Service.create_instituicao(dados)

        return jsonify(instituicao_schema.dump(instituicao)), HTTPStatus.CREATED

    except ValidationError as err:
        return {"erro": "Dados inválidos", "campos": err.messages}, HTTPStatus.BAD_REQUEST

    except DatabaseError:
        return {
            "mensagem": "Problema ao estabelecer a conexão"
        }, HTTPStatus.INTERNAL_SERVER_ERROR

@instituicao_ensino_bp.put("/<int:id>")
def put_instituicao(id):
    try:
        dados = request.get_json()
        if not dados:
            return {"erro": "Nenhum dado informado"}, HTTPStatus.BAD_REQUEST

        dados_validados = instituicao_schema.load(dados, partial=True)

        logger.info(f"iniciando atualização fo item ID: {id}")
        Service = instEnsinoService()
        instituicao = Service.update_instituicao(id, dados_validados)

        if instituicao is None:
            return {
                "mensagem": "Instituição de ensino não encontrada"
            }, HTTPStatus.NOT_FOUND

        logger.info(f"finalizando atualização da instituição com ID: {id}")
        return jsonify(instituicao_schema.dump(instituicao)), HTTPStatus.OK

    except ValidationError as err:
        return {"erro": "Dados inválidos", "campos": err.messages}, HTTPStatus.BAD_REQUEST

    except DatabaseError:
        return {
            "mensagem": "Problema ao estabelecer a conexão"
        }, HTTPStatus.INTERNAL_SERVER_ERROR
    

@instituicao_ensino_bp.delete("/<int:id>")
def deleteInstituicoes(id):
    try:
        logger.info(f"iniciando o delete, apagando com ID: {id}")
        Service = instEnsinoService()
        apagado = Service.delete_instituicao(id)

        if not apagado:
            return {
                "mensagem": "Instituição de ensino não encontrada"
            }, HTTPStatus.NOT_FOUND

        return "", HTTPStatus.NO_CONTENT

    except DatabaseError:
        return {
            "mensagem": "Problema ao estabelecer a conexão"
        }, HTTPStatus.INTERNAL_SERVER_ERROR
