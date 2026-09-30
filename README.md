# Herbaria

Aplicação web para organização de plantas, categorias, cuidados, fotografias e usuários, desenvolvida para o trabalho de **Programação de Sistemas Web II**. Permite cadastrar plantas, registrar cuidados, manter um histórico fotográfico e gerenciar contas de acesso.

## Integrantes

- Diogo Vittório Cardoso Oliveira
- Enzo Braga Martins

## Tecnologias

| Tecnologia | Uso |
| --- | --- |
| Python 3.14.7 | Versão utilizada no ambiente local |
| Django 6.0.7 | Framework web, autenticação, formulários e ORM |
| Pillow 12.3.0 | Validação e processamento de imagens |
| SQLite | Banco de dados local |
| HTML, CSS e JavaScript | Interface |
| Bootstrap e tema Alazea | Estilos e componentes visuais |

As versões acima correspondem ao ambiente local consultado. O SQLite acompanha o Python; os recursos utilizados do Bootstrap e do tema estão no repositório.

## Funcionalidades e cinco CRUDs

| Módulo | Informações principais | Operações |
| --- | --- | --- |
| Plantas | Nome popular, nome científico, descrição, data de plantio e categoria | Cadastrar, listar, detalhar, editar e excluir |
| Categorias | Nome e descrição | Cadastrar, listar, detalhar, editar e excluir |
| Cuidados | Planta, tipos de cuidado, data e observações | Cadastrar, listar, detalhar, editar e excluir |
| Fotografias | Planta, imagem e data da fotografia | Cadastrar, listar, detalhar, editar e excluir |
| Pessoas / Usuários | Conta de acesso, identificação, contato e endereço | Cadastro público; listagem, detalhes, edição e exclusão na área do proprietário |

O sistema também oferece login, logout, pesquisa de registros, paginação e controle de acesso por grupos e permissões do Django. A criação de usuários é reaproveitada pela área administrativa, sem um segundo fluxo de cadastro.

## Arquitetura

O projeto segue a organização de aplicações do Django: models representam os dados, forms validam as entradas, views recebem as requisições e templates compõem a interface.

As views da aplicação são **Function-Based Views (FBVs)**, escritas como funções Python (`def`). Classes de models, forms e configurações do Django não são Class-Based Views. O painel nativo Django Admin é uma funcionalidade do framework, separada das telas desenvolvidas para os CRUDs.

`Pessoa` herda do `User` nativo do Django. Por isso, nome de usuário (`username`), e-mail e senha pertencem à estrutura de autenticação herdada. Nascimento, telefone, CPF e endereço são dados complementares de `Pessoa`.

## Como executar localmente

Tenha Git e Python instalados. Os comandos abaixo criam o ambiente virtual **na raiz do repositório**, com o nome `venv`. Use apenas o bloco correspondente ao seu sistema operacional.

### 1. Clonar o repositório

```console
git clone https://github.com/Diogovittori/Trabalho-Psw.git
cd Trabalho-Psw
```

### 2. Criar o ambiente virtual e instalar as dependências

O arquivo `requirements.txt`, na raiz do repositório, fixa as versões das dependências diretas. Instale-as no ambiente virtual:

**Windows — PowerShell:**

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

**Linux — Bash:**

```bash
python3 -m venv venv
./venv/bin/python -m pip install -r requirements.txt
```

Os comandos usam diretamente o Python do ambiente virtual, sem precisar ativá-lo. Caso o Linux informe que `venv` não está disponível, instale o pacote correspondente à sua versão de Python pelo gerenciador de pacotes da distribuição.

### 3. Preparar o banco e os grupos

**Windows — PowerShell:**

```powershell
cd Herbaria
..\venv\Scripts\python.exe manage.py migrate
..\venv\Scripts\python.exe manage.py criar_grupos
```

**Linux — Bash:**

```bash
cd Herbaria
../venv/bin/python manage.py migrate
../venv/bin/python manage.py criar_grupos
```

As migrações criam o banco local e os tipos iniciais de cuidado. Também configuram o grupo `proprietario` com as permissões de pessoas e aplicam os ajustes de compatibilidade dos registros antigos.

O comando `criar_grupos` configura `Herbaria - Leitores`, `Observadores` e `Herbaria - Editores` para os módulos de plantas, categorias, cuidados e fotografias. Ele não cria o grupo de funcionários. Ao executá-lo novamente, as permissões desses três grupos são redefinidas conforme o comando.

**Permaneça em `Herbaria` para os comandos seguintes.** No Linux, respeite as letras maiúsculas e minúsculas dos caminhos.

### 4. Criar uma conta administrativa

**Windows — PowerShell:**

```powershell
..\venv\Scripts\python.exe manage.py createsuperuser
```

**Linux — Bash:**

```bash
../venv/bin/python manage.py createsuperuser
```

Informe nome de usuário, e-mail e senha. Não há credenciais padrão documentadas para o projeto: crie sua própria conta.

O superusuário pode acessar o Django Admin e administrar os quatro módulos de plantas. Para acessar a seção **Usuários**, também deve pertencer ao grupo de proprietário, conforme a configuração abaixo.

### 5. Iniciar o servidor

**Windows — PowerShell:**

```powershell
..\venv\Scripts\python.exe manage.py runserver
```

**Linux — Bash:**

```bash
../venv/bin/python manage.py runserver
```

Abra http://127.0.0.1:8000/. Para encerrar, pressione `Ctrl+C` no terminal.

### 6. Configurar o proprietário

1. Acesse http://127.0.0.1:8000/admin/ com o superusuário.
2. Abra a conta desejada no cadastro de usuários do Admin.
3. Adicione-a ao grupo **`proprietario`**, criado pelas migrações, e salve.
4. Entre na aplicação com essa conta. O menu **Usuários** dá acesso à área de gerenciamento.

O código também reconhece o grupo legado **`Proprietário`**. Para esse grupo, confira as permissões de pessoas no Admin. Não basta marcar uma conta como membro da equipe (`is_staff`), nem conceder permissões diretamente sem colocá-la no grupo exigido.

Se essa área não aparecer, confira os grupos e as permissões na seção seguinte.

## Grupos e permissões

| Grupo | Papel |
| --- | --- |
| `Observadores` | Grupo atribuído pelo cadastro público; o comando `criar_grupos` concede permissões de consulta dos quatro módulos de plantas |
| `Herbaria - Leitores` | Permissões de consulta dos quatro módulos de plantas |
| `Herbaria - Editores` | Permissões de cadastro, consulta, edição e exclusão dos quatro módulos de plantas |
| `proprietario` / `Proprietário` | Acesso à seção Usuários, condicionado à permissão da ação |
| `Funcionário` | Identifica as contas que podem receber vínculos de plantas na edição de seus dados |

Para configurar um funcionário, crie ou selecione o grupo `Funcionário` no Django Admin e adicione a conta a ele. Para permitir que também edite plantas, categorias, cuidados e fotografias, adicione `Herbaria - Editores` ou atribua as permissões correspondentes. O nome do grupo de funcionário, sozinho, não concede essas permissões.

A compatibilidade do código também aceita `Funcionario`, `funcionario`, `Funcionários` e `funcionarios` para a vinculação de plantas. Prefira usar `Funcionário` de forma consistente.

As consultas aos quatro módulos exigem autenticação; as operações de escrita verificam as permissões nativas. A área de Usuários exige conta ativa, grupo de proprietário e permissão da ação:

| Ação em Usuários | Permissão |
| --- | --- |
| Listar e visualizar detalhes | `pessoas.view_pessoa` |
| Editar | `pessoas.change_pessoa` |
| Excluir | `pessoas.delete_pessoa` |
| Mostrar o atalho de cadastro na listagem | `pessoas.add_pessoa` |

O cadastro público continua disponível sem login; a permissão `add_pessoa` controla o atalho administrativo, não transforma esse cadastro em uma página privada.

## Cadastro e gerenciamento de usuários

### Campos do cadastro público

**Obrigatórios:** nome de usuário, e-mail, nome completo, CPF, data de nascimento, telefone, senha e confirmação de senha.

**Opcionais:** número do endereço, bairro, cidade, estado (UF) e CEP.

- O login utiliza **nome de usuário e senha**, não e-mail.
- O CPF aceita 11 dígitos ou o formato `000.000.000-00`; é validado e salvo sem máscara.
- CPF e nome de usuário passam por verificações de duplicidade.
- A data de nascimento não pode estar no futuro.
- A UF, quando preenchida, deve ser válida e é normalizada para maiúsculas.
- As senhas passam pelas validações configuradas no Django e são armazenadas como hash.
- O cadastro público não permite escolher grupos, privilégios ou plantas vinculadas.

### Área Usuários

A listagem inclui todas as contas de `User`, inclusive funcionários antigos sem perfil complementar de `Pessoa`. Na primeira edição dessas contas, os dados do perfil podem ser preenchidos sem recriar a conta ou substituir senha e grupos.

A edição administrativa permite atualizar identificação, contato e endereço. O campo de plantas vinculadas só aparece quando **a conta editada** pertence ao grupo de funcionários. Essa tela não permite alterar senhas, grupos, permissões ou privilégios administrativos.

A exclusão exige confirmação por POST com proteção CSRF. Remove a conta e o perfil, preservando as plantas. A conta conectada não pode excluir a si própria nessa área.

## Endereços principais

Com o servidor local em execução, use `http://127.0.0.1:8000` antes dos caminhos abaixo:

| Página | Caminho |
| --- | --- |
| Início | `/` |
| Login | `/contas/login/` |
| Cadastro de usuário | `/contas/cadastro/` |
| Plantas | `/plantas/` |
| Categorias | `/categorias/` |
| Cuidados | `/cuidados/` |
| Fotografias | `/fotografias/` |
| Pesquisa | `/pesquisa/` |
| Usuários — área do proprietário | `/pessoas/administracao/` |
| Detalhes de usuário | `/pessoas/administracao/<id>/` |
| Editar usuário | `/pessoas/administracao/<id>/editar/` |
| Excluir usuário | `/pessoas/administracao/<id>/excluir/` |
| Django Admin | `/admin/` |

Substitua `<id>` pelo identificador do registro. A seção **Usuários** faz parte da interface do Herbaria; o **Django Admin** é o painel nativo utilizado também para configurar grupos e permissões.

## Roteiro de uso

1. Prepare o banco e configure as contas e seus grupos.
2. Entre com uma conta que tenha as permissões necessárias.
3. Cadastre uma categoria.
4. Cadastre uma planta e selecione sua categoria, se desejado.
5. Registre um cuidado, escolhendo a planta, um ou mais tipos de cuidado e a data.
6. Cadastre uma fotografia, selecionando a planta, o arquivo de imagem e a data da foto.
7. Use as listagens, os detalhes e a pesquisa para consultar os registros.
8. Com a conta do proprietário, acesse Usuários para consultar e atualizar contas; vincule plantas apenas aos funcionários.

## Estrutura principal

```text
Trabalho-Psw/
├── README.md
├── requirements.txt            # Dependências para instalação
├── Herbaria (2).png            # Diagrama existente (revisão pendente)
└── Herbaria/
    ├── manage.py
    ├── mysite/                    # Configurações e rotas principais
    ├── Plantas/                   # Plantas, pesquisa e recursos compartilhados
    │   ├── static/                # CSS, JavaScript e recursos do tema
    │   ├── templates/             # Layout base e páginas de plantas
    │   └── templatetags/          # Renderização compartilhada dos formulários
    ├── Categoria/                 # Categorias e comando criar_grupos
    ├── Cuidados/                  # Cuidados e tipos de cuidado
    ├── Fotografia/                # Fotografias das plantas
    └── Pessoas/
        ├── models.py             # Perfil Pessoa, herdado de User
        ├── forms.py              # Cadastro, edição e autenticação
        ├── validacoes.py         # Validações compartilhadas de CPF e usuário
        ├── acesso.py             # Verificações de grupos e permissões
        ├── views.py              # Cadastro público, login e logout
        ├── views_administracao.py # FBVs de gerenciamento de usuários
        ├── urls.py               # Rotas administrativas do módulo
        ├── migrations/           # Histórico de alterações do banco
        ├── templates/            # Templates de cadastro, login e administração
        └── templatetags/          # Visibilidade das ações administrativas
```

## Banco de dados e fotografias

O banco local fica em `Herbaria/db.sqlite3`. As fotografias enviadas ficam em `Herbaria/media/`, conforme `MEDIA_ROOT`. Esses arquivos são dados de execução: clonar o repositório e executar as migrações não reproduz automaticamente os cadastros ou fotografias de outro computador.

Para preservar uma instalação, faça backup do banco e da pasta de mídia. Evite copiar o SQLite enquanto houver gravações em andamento. Ao atualizar o projeto, execute `manage.py migrate` para aplicar as migrações pendentes; não apague o banco como procedimento normal de atualização.

## Verificações e testes

Execute a partir de `Herbaria`.

**Windows — PowerShell:**

```powershell
..\venv\Scripts\python.exe manage.py check
..\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
..\venv\Scripts\python.exe manage.py test --noinput
```

**Linux — Bash:**

```bash
../venv/bin/python manage.py check
../venv/bin/python manage.py makemigrations --check --dry-run
../venv/bin/python manage.py test --noinput
```

`check` verifica a configuração do Django; `makemigrations --check --dry-run` aponta alterações de models sem migração correspondente, sem criar arquivos. Os testes usam um banco separado do banco local de desenvolvimento.

Para testar apenas Pessoas, substitua o último comando por `manage.py test Pessoas --noinput`, mantendo o caminho do Python do ambiente virtual.



## Problemas comuns

| Situação | O que verificar |
| --- | --- |
| `No module named django` ou `PIL` | Instale as dependências usando o mesmo Python do ambiente virtual utilizado para iniciar o servidor |
| `no such table` | Execute `manage.py migrate` na pasta `Herbaria` |
| Menu Usuários não aparece | Confira conta ativa, grupo `proprietario` ou `Proprietário` e permissão `pessoas.view_pessoa` |
| Acesso negado em Usuários | Confira a permissão da ação e a participação no grupo de proprietário, inclusive para superusuários |
| Funcionário não consegue editar plantas | Configure `Herbaria - Editores` ou as permissões correspondentes; o grupo de funcionário não basta |
| Fotografia não carrega | Verifique se o arquivo enviado ainda existe em `Herbaria/media/` |
| CSS antigo após uma atualização | Recarregue a página sem cache, por exemplo com `Ctrl+F5` |
| Porta 8000 ocupada | Execute `manage.py runserver 8001` com o Python do ambiente virtual e acesse a porta 8001 |

## Ambiente de desenvolvimento

As configurações atuais são destinadas ao desenvolvimento local, com SQLite, `DEBUG=True` e chave de desenvolvimento no arquivo de configuração. Não representam uma configuração pronta para publicação. Uma implantação exige configurações próprias de segredo, hosts, arquivos estáticos e mídia, além de um servidor apropriado.

## Créditos da interface

A interface utiliza Bootstrap e recursos do tema **Alazea**, da **Colorlib**, adaptados para o Herbaria. Os créditos do tema estão preservados no código e no rodapé da aplicação.
