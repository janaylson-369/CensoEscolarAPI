from flask import Blueprint, jsonify, request
from helpers.logger import logger
from models.instituicaoensino import InstituicaoEnsino, InstituicaoEnsinoSchema
from http import HTTPStatus
from marshmallow import ValidationError
from services.instEnsinoService import instEnsinoService

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
def getAllInstituicoes():
    logger.info("listando as insituições")
    Service = instEnsinoService()
    instituicoes = Service.get_all()
    logger.info("finalizando a listagem das insituições")
    return jsonify(instituicoes_schema.dump(instituicoes)), HTTPStatus.OK


@instituicao_ensino_bp.get("/<int:id>")
def getByIdInstituicoes(id):
    logger.info(f"listando a insituição de ensino com ID: {id}")
    Service = instEnsinoService()
    instituicao = Service.get_by_id(id)
    if instituicao is None:
        return {"erro": "não encontrei nada bixo"}, HTTPStatus.NOT_FOUND
    
    logger.info(f"finalizando a Listagem da insituição de ensino com ID: {id}")

    return jsonify(instituicao_schema.dump(instituicao)), HTTPStatus.OK


@instituicao_ensino_bp.post("/")
def postInstituicoes():
    logger.info("iniciando a criação da nova insituição")
    body = request.get_json()
    try:
        dados = instituicao_schema.load(body, partial=False)
    except ValidationError as e:
        return jsonify({"error": e.messages}), HTTPStatus.BAD_REQUEST
    
    Service = instEnsinoService()    
    instituicao = Service.create_instituicao(dados)
    return jsonify(instituicao_schema.dump(instituicao)), HTTPStatus.CREATED


@instituicao_ensino_bp.put("/<int:id>")
def putInstituicoes(id):
    dados = request.get_json()
    if not dados:
        return {"erro": "Nenhum dado informado"}, HTTPStatus.BAD_REQUEST

    try:
        dados_validados = instituicao_schema.load(dados, partial=True)
    except ValidationError as e:
        return jsonify({"error": e.messages}), HTTPStatus.BAD_REQUEST
    
    logger.info(f"iniciando atualização fo item ID: {id}")
    try:
        Service = instEnsinoService()
        instituicao = Service.update_instituicao(id, dados_validados)

        logger.info(f"finalizando atualização da instituição com ID: {id}")
        return jsonify(instituicao_schema.dump(instituicao)), HTTPStatus.OK
    except ValidationError as e:
        return jsonify({"error": e.messages}), HTTPStatus.INTERNAL_SERVER_ERROR
    
    
@instituicao_ensino_bp.delete("/<int:id>")
def deleteInstituicoes(id):
    logger.info(f"iniciando o delete, apagando com ID: {id}")
    Service = instEnsinoService()
    apagado = Service.delete_instituicao(id)

    return jsonify({"mensagem": f"coluna ativo: {apagado} o registro com ID: {id} foi apagado"}), HTTPStatus.OK
