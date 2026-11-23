# CensoEscolarData

🔗 **Link para o script na branch Postgres:** [extrair_dados_csv.py](https://github.com/janaylson-369/CensoEscolarData/blob/c1b12f5fba422ffc8c44f3b771eb5312f196db77/extrair_dados_csv.py)

---

## 📄 Sobre o Projeto

O **CensoEscolarData** é um projeto focado na extração, limpeza e processamento dos dados abertos do Censo Escolar (INEP). O script de extração permite ler bases de dados volumosas em formato CSV e prepará-las para inserção e estruturação em bancos de dados relacionais, com foco em PostgreSQL.

## 🚀 Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Manipulação de Dados:** Pandas / CSV (Embutido no Python)
* **Banco de Dados:** PostgreSQL
* **Conexão com banco:** psycopg2-binary

## 2. CensoEscolarAPI (Aplicação Backend)

### 📄 Sobre o Módulo da API
O **CensoEscolarAPI** é uma aplicação backend desenvolvida em Python que fornece acesso aos dados processados. O projeto tem uma arquitetura organizada em camadas e utiliza uma base de dados local para armazenar e consultar informações, focando-se em entidades como instituições de ensino.

### 🏗️ Estrutura e Arquitetura
O projeto está organizado nos seguintes diretórios e módulos principais, seguindo padrões de responsabilidade única:
* **`controllers/`**: Contém os controladores que lidam com as requisições, incluindo `instituicaoDeEnsinoControll.py` e `indexController.py`.
* **`models/`**: Define as estruturas de dados e entidades de domínio, com arquivos como `instituicaoensino.py`.
* **`repositories/`**: Responsável pela camada de abstração de acesso aos dados, destacando-se o `instituicaoEnsinoRepository.py`.
* **`services/`**: Contém a lógica de negócio e regras do serviço, como o `instEnsinoService.py`.
* **`helpers/`**: Módulos auxiliares transversais para:
  * Configuração da aplicação (`application/`)
  * Gestão da base de dados (`database/`)
  * Variáveis de ambiente (`enviroment/`)
  * Manipulação de arquivos (`file/json.py`)
  * Sistema de logs/registros (`logger/`)

### ⚙️ Configuração e Arquivos Principais
* **Execução**: A aplicação possui arquivos principais para o servidor/arranque, nomeadamente `app.py`.
* **Dependências**: As bibliotecas do ambiente Python estão gerenciadas nos arquivos `requeriments.txt` e `pyproject.toml`. O ecossistema suporta injeção de variáveis via arquivos `.env`.
* **Registros (Logs)**: O monitoramento das atividades e erros da aplicação é centralizado no arquivo `app.log`.
