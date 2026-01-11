# sistema-gerenciamento-tarefas-agil

Sistema de gerenciamento de tarefas ágil desenvolvido em Python com Flask.

## Configuração do Kanban com GitHub Projects

Para usar o quadro Kanban integrado com GitHub Projects (recomendado):

1. Crie um repositório no GitHub e adicione um projeto clássico (Projects > Classic).
2. Gere um token de acesso pessoal no GitHub (Settings > Developer settings > Personal access tokens) com permissões para repo e project.
3. Defina variáveis de ambiente:
   - `GITHUB_TOKEN`: Seu token GitHub.
   - `GITHUB_REPO`: Nome do repositório (ex.: `username/repo`).
4. Adicione issues ao projeto e mova entre colunas (To Do, In Progress, Done).

O Kanban da app buscará automaticamente as issues do projeto GitHub. Se não configurado, usa dados locais.

## Instalação

1. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

2. Execute o aplicativo:
   ```
   python app.py
   ```

3. Acesse http://127.0.0.1:5000 e registre um usuário para começar.

## Estrutura do Projeto

- `app.py`: Aplicação principal com rotas e autenticação
- `models.py`: Modelos de dados com hash de senhas
- `forms.py`: Formulários WTForms para entrada de dados
- `templates/`: Templates HTML para interface
- `static/`: Arquivos estáticos (CSS)