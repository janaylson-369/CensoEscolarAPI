from sqlite3 import OperationalError

from psycopg2 import DatabaseError
from helpers.logger import logger
from helpers.database import get_connexao
from models.instituicaoensino import InstituicaoEnsino

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

class InstituicaoEnsinoRepository():
    
    def getInstituicao(self, id):
        conn = get_connexao()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, no_entidade, co_entidade, no_uf, sg_uf, co_uf, 
                no_municipio, co_municipio, nu_ano_censo, qt_mat_bas, 
                qt_mat_inf, qt_mat_fund, qt_mat_med, qt_mat_prof, 
                qt_mat_eja, qt_mat_esp, ativo, created
                FROM tb_instituicao_ensino WHERE id = %s AND ativo = True""", (id,))
            row = cursor.fetchone()

            if row is None:
                return None

            instituicao = row_to_instituicao(row)
        except DatabaseError:
            conn.rollback()
            raise

        return instituicao
        
    def getAllInstituicoes(self, limit, offset):
        connection = get_connexao()
        try:
            logger.info("recuperando a conexão com o Banco de dados")
            cursor = connection.cursor()
            cursor.execute("""
                SELECT id, no_entidade, co_entidade, no_uf, sg_uf, co_uf, 
                    no_municipio, co_municipio, nu_ano_censo, qt_mat_bas, 
                    qt_mat_inf, qt_mat_fund, qt_mat_med, qt_mat_prof, 
                    qt_mat_eja, qt_mat_esp, ativo, created
                FROM tb_instituicao_ensino
                WHERE ativo = True
                ORDER BY id
                LIMIT %s OFFSET %s
            """, (limit, offset))
            rows = cursor.fetchall()

            instituicoes = [row_to_instituicao(row) for row in rows]
        except DatabaseError:
            logger.error("Erro no processamento dos dados no Banco de Dados")
            connection.rollback()
            raise

        return instituicoes

    def countInstituicoes(self):
        connection = get_connexao()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT COUNT(*)
                FROM tb_instituicao_ensino
                WHERE ativo = True
            """)
            return cursor.fetchone()[0]
        except DatabaseError:
            connection.rollback()
            raise
    

    def insertInstituicao(self, dados):
        connexao = get_connexao()
        try:
            with connexao:
                cursor = connexao.cursor()
                cursor.execute(""" INSERT INTO tb_instituicao_ensino (
                        no_entidade, co_entidade, no_uf, sg_uf, co_uf, 
                        no_municipio, co_municipio, nu_ano_censo, qt_mat_bas, 
                        qt_mat_inf, qt_mat_fund, qt_mat_med, qt_mat_prof, 
                        qt_mat_eja, qt_mat_esp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                    RETURNING id, created
                    """, (dados["no_entidade"], dados["co_entidade"], dados["no_uf"],
                          dados["sg_uf"], dados["co_uf"], dados["no_municipio"],
                          dados["co_municipio"], dados["nu_ano_censo"], dados["qt_mat_bas"],
                          dados["qt_mat_inf"], dados["qt_mat_fund"], dados["qt_mat_med"],
                          dados["qt_mat_prof"], dados["qt_mat_eja"], dados["qt_mat_esp"])
                )
                resultset = cursor.fetchone()
                id_novo = resultset[0]
                created_novo = resultset[1]

            instituicao = InstituicaoEnsino(**dados, id=id_novo, created=created_novo)
        except DatabaseError:
            connexao.rollback()
            raise

        return instituicao
        
    def updateInstituicao(self, instituicao):
        connexao = get_connexao()
        try:
            with connexao:
                cursor = connexao.cursor()
                cursor.execute(""" UPDATE tb_instituicao_ensino SET no_entidade = %s, co_entidade = %s, qt_mat_bas = %s
                    WHERE id = %s AND ativo = True""",
                    (instituicao.no_entidade, instituicao.co_entidade, instituicao.qt_mat_bas, instituicao.id))
            return instituicao
        except DatabaseError:
            connexao.rollback()
            raise

    def deleteInstituicao(self, id):
        connexao = get_connexao()
        try:
            with connexao:
                cursor = connexao.cursor()
                cursor.execute("UPDATE tb_instituicao_ensino SET ativo = False WHERE id = %s AND ativo = True", (id,))
                apagado = cursor.rowcount
            return apagado
        except DatabaseError:
            connexao.rollback()
            raise