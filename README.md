# Painel de Senhas com Flask e Docker

Este projeto é uma aplicação Flask para gerenciar senhas em uma clínica, utilizando Flask, Socket.IO e PostgreSQL.

## Pré-requisitos

Antes de começar, certifique-se de ter os seguintes softwares instalados:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Como Rodar o Projeto

Siga os passos abaixo para iniciar o projeto em um ambiente Docker:

### 1. Clonar o Repositório

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO


 ## Atualizações Futuros (Push)
 1 - Adicione os arquivos modificados: git add .
 2 - Faça um novo commit: git commit -m "Descrição das mudanças"
 3 - Envie as mudanças para o GitHub: git push

Construir e Iniciar o Projeto com Docker
   no diretório raiz do projeto, execute o seguinte comando para construir e iniciar os contêineres:
   docker-compose up --build


 ## Configurar Variáveis de Ambiente
 Crie um arquivo .env na raiz do projeto com as seguintes variáveis de ambiente:
 # .env
POSTGRES_DB=painel_senhas_db
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin123
POSTGRES_HOST=db
POSTGRES_PORT=5432

Com base nas informações fornecidas anteriormente sobre o seu projeto Flask e suas rotas configuradas, os links de acesso devem ser similares a estes:

Página principal (Atendente):

URL: http://localhost:5000/
Rota: Essa é a página padrão onde o atendente pode interagir com o sistema.
Painel de Senhas (por clínica):

URL: http://localhost:5000/clinica/<clinic_id>/panel
Exemplo: http://localhost:5000/clinica/1/panel
Rota: Exibe o painel de senhas para a clínica especificada pelo ID.
Área de administração de atendentes:

URL: http://localhost:5000/admin/attendants
Rota: Administra os atendentes para cada clínica.
Área de administração de clínicas:

URL: http://localhost:5000/admin/clinics
Rota: Administra as clínicas no sistema.
Área do Atendente (por clínica):

URL: http://localhost:5000/clinica/<clinic_id>/attendant
Exemplo: http://localhost:5000/clinica/1/attendant
Rota: Exibe a interface do atendente para uma clínica específica.

# Painel de Senhas

Aqui está uma imagem que mostra a interface do painel:

![Interface do Painel](imagensPanel/imagePanel.png)
![Interface do PainelAtedente](imagensPanel/imageAtendante.png)