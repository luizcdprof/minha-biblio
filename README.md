# Minha-Biblio
Um WebApp em Django para gerenciamento de biblioteca pessoal. Esse repositório tem fim educacional.

# Configuração do projeto
* criado um repositório no Github com os arquivos README e .gitignore do Python. Utilizando a licença GPL.
* realizado o clone do repositório
    * git clone endereco-do-repositorio.git
* acessando a pasta do repositório
    * cd nome-da-pasta
* criado o ambiente virtual
    * python -m venv .venv
* criado o arquivo "requirements.txt" com o Django e o Pillow.
* ativado o ambiente virtual
    * .venv/Scripts/activate (Windows)
    * source .venv/bin/activate (Linux / Firebase Studio)
* instalado o conteúdo do requirements
    * pip install -r requirements.txt
* criado o projeto Django no local atual
    * django-admin startproject djangoapp .
* alteradas as configurações de localização, pasta raiz de templates e static files no settings.py
* realizado o commit após a configuração básica do projeto (first commit)

# criando o template base
* criada a pasta "templates" na raiz do projeto
    * criado o arquivo "base.html"
    * criado o arquivo "home.html"

# Criando os arquivos static
* criada a pasta "static" na raiz do projeto
    * criado o arquivo "style.css"
    * criado o arquivo "script.js"
    * criado o arquivo "minha-biblio.png" para ser o Logotipo
* coletados os arquivos estáticos
    * python manage.py collectstatic

# Criando o app usuario
* criado o app
    * python manage.py startapp usuario
* adicionado o app ao settings.py
* adicionado o arquivo urls.py ao app usuario
* configuradas as rotas do projeto django (incluindo o home e o urls.py do usuario)
* criados os templates do usuario
* criadas as views do usuario
* criados os forms do usuario
* criados os models do usuario
* criadas e realizadas as migrações do models
    * python manage.py makemigrations
    * python manage.py migrate
* criado o superuser
    * python manage.py createsuperuser

# Incluindo adaptações para testes do backend
* Alterações comentadas nas views login e exibir

# Incluindo projeto do Bruno API Client
* adicionada a pasta bruno_client ao projeto