from flask import request
from models.usuarios import Usuarios
from helpers.file.json import read,write
from pathlib import Path
from helpers.application import app
from http import HTTPStatus
from controllers.instituicaoDeEnsinoControll import instituicao_ensino_bp
from controllers.indexController import index_bp

BASE_DIR = Path(__file__).resolve().parent
arquivoUsuarios = BASE_DIR / "usuarios.json"

app.register_blueprint(instituicao_ensino_bp)
app.register_blueprint(index_bp)




def listarUsuarios():
    dataset = read(arquivoUsuarios)
    usuarioss = [Usuarios(
        row["id"], row["nome"], row["idade"], row["cpf"]) for row in dataset]
    return usuarioss

def salvaUsuarios(usuarios):
    write(arquivoUsuarios, [usr.toDict() for usr in usuarios])
    


@app.route("/health")
def health():
    return {"health": "ok"}, HTTPStatus.OK



# USUARIOS
@app.post("/usuarios")
def postUsuarios():
    dados = request.get_json()

    usuarios = listarUsuarios()
    
    novo_usuario = Usuarios(
        id=dados.get("id"),
        nome=dados.get("nome"),
        idade=dados.get("idade"),
        cpf=dados.get("cpf")
    )
    
    usuarios.append(novo_usuario)
    salvaUsuarios(usuarios)
    
    return novo_usuario.toDict()


@app.put("/usuarios/<int:id>")
def putUsuarios(id):
    dados = request.get_json()
    
    usuarios = listarUsuarios()
    a = next((usr for usr in usuarios if int(usr.id) == id), None)
    
    if not a:
        return { "erro":"não encontrei bixo."}, 404
     
    a.nome = dados.get("nome", a.nome)
    a.idade = dados.get("idade", a.idade)
    a.cpf = dados.get("cpf", a.cpf)
    
    salvaUsuarios(usuarios)
    return {"messagem": "atualizado man"}, 200


@app.delete("/usuarios/<int:id>")
def deleteUsuarios(id):
    usuarios = listarUsuarios()
    resto_dalista = [u for u in usuarios if int(u.id) != id]
    
    salvaUsuarios(resto_dalista)
    return {"mensagem": "usuario apagado olha no arquivo"}, 200

@app.get("/usuarios/<int:id>")
def getByIdUsuarios(id):
    usuarios = listarUsuarios()
    a = [u.toDict() for u in usuarios if int(u.id) == id]
    if not a:
        return { "erro":"não encontrei bixo."}, 404
    return a[0] , 200

def main(arg=[]):
    app.run(debug=True)


if __name__ == '__main__':
    main()
