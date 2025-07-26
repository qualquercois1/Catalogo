# Catálogo de Filmes e Séries

Este é um projeto desenvolvido em Django que funciona como um catálogo pessoal, permitindo que usuários cadastrados gerenciem e avaliem os filmes e séries que assistiram.

## Funcionalidades Principais

* **Autenticação de Usuários:** Sistema completo de registro, login e logout.
* **Catálogo Pessoal:** Cada usuário possui seu próprio catálogo, e os itens cadastrados são privados.
* **Cadastro de Itens:** Formulários para adicionar novos filmes/séries, incluindo informações como diretor, atores e gêneros.
* **Sistema de Avaliação:** Usuários podem dar uma nota de 1 a 10 para cada item em seu catálogo.
* **Interface Dinâmica:** Adição de novos atores e diretores através de janelas pop-up sem sair da página de cadastro do item.

## Pré-requisitos

Antes de começar, garanta que você tenha o Python (versão 3.8 ou superior) e o `pip` instalados na sua máquina.

* [Python](https://www.python.org/downloads/)
* [Git](https://git-scm.com/downloads/) (Opcional, mas recomendado para controle de versão)

---

## 🚀 Configuração e Execução do Projeto

Siga os passos abaixo para configurar e rodar o ambiente de desenvolvimento localmente.

### 1. Clonar o Repositório (Opcional)

Se você estiver configurando o projeto a partir de um repositório Git, primeiro clone-o:
```bash
git clone https://URL_DO_SEU_REPOSITORIO.git
cd nome-da-pasta-do-projeto
```

### 2. Criar e Ativar o Ambiente Virtual

É uma prática essencial usar um ambiente virtual para isolar as dependências do projeto.

```bash
# Criar o ambiente virtual (pode ser venv, .venv, ou outro nome de sua preferência)
python -m venv venv

# Ativar o ambiente virtual
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate
```
Com o ambiente ativado, você verá `(venv)` no início da linha do seu terminal.

### 3. Instalar as Dependências

O arquivo `requirements.txt` lista todas as bibliotecas Python que o projeto precisa.

```bash
pip install -r requirements.txt
```

### 4. Configurar o Banco de Dados

Este comando irá criar o banco de dados SQLite e aplicar todas as estruturas de tabelas necessárias.

```bash
python manage.py migrate
```

### 5. Criar uma Conta de Administrador

Você precisará de um superusuário para acessar o painel de administração (`/admin/`), gerenciar dados globais (como gêneros) e promover outros usuários.

```bash
python manage.py createsuperuser
```
Siga as instruções para criar um nome de usuário, e-mail e senha.

### 6. Executar o Servidor de Desenvolvimento

Agora, tudo está pronto! Inicie o servidor do Django.

```bash
python manage.py runserver
```

O projeto estará rodando e acessível no seu navegador através do seguinte endereço:
* **Página Principal:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* **Painel de Administração:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Estrutura do Projeto

* **`catalogo/`**: Pasta de configuração principal do projeto Django.
* **`catalog/`**: Aplicação principal do projeto, onde reside toda a lógica de modelos, views, formulários e templates.
* **`db.sqlite3`**: Arquivo do banco de dados de desenvolvimento.
* **`manage.py`**: Utilitário de linha de comando do Django.
* **`requirements.txt`**: Lista de dependências do projeto.
* **`.gitignore`**: Arquivo que especifica arquivos e pastas a serem ignorados pelo Git.