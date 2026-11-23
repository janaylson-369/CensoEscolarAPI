import math
from http import HTTPStatus
from models.paginacao import PAGE_DEFAULT, PER_PAGE_DEFAULT
from repositories.instituicaoEnsinoRepository import InstituicaoEnsinoRepository

class instEnsinoService():
    def __init__(self):
        self.instituicaoEnsinoRepository = InstituicaoEnsinoRepository()
    
    def get_all(self, page=PAGE_DEFAULT, per_page=PER_PAGE_DEFAULT):
        offset = (page - 1) * per_page
        itens = self.instituicaoEnsinoRepository.getAllInstituicoes(per_page, offset)
        total = self.instituicaoEnsinoRepository.countInstituicoes()
        return {
            "data": itens,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "total_pages": math.ceil(total / per_page) if total else 0
            }
        }

    def get_by_id(self,id):
        return self.instituicaoEnsinoRepository.getInstituicao(id)

    def create_instituicao(self, dados):
        return self.instituicaoEnsinoRepository.insertInstituicao(dados)
    
    
    def update_instituicao(self, id, dados_validados):
        instituicao = self.instituicaoEnsinoRepository.getInstituicao(id)
        if instituicao is None:
            return {"erro": "não encontrei nada bixo"}, HTTPStatus.NOT_FOUND
        
        instituicao.no_entidade = dados_validados.get("no_entidade", instituicao.no_entidade)
        instituicao.co_entidade = dados_validados.get("co_entidade", instituicao.co_entidade)
        instituicao.qt_mat_bas = dados_validados.get("qt_mat_bas", instituicao.qt_mat_bas)
        
        return self.instituicaoEnsinoRepository.updateInstituicao(instituicao)

    def delete_instituicao(self, id):
        return self.instituicaoEnsinoRepository.deleteInstituicao(id)