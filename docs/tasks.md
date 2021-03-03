#### ***Task***: Fazer um sistema de autenticação usando Django e React

##### Model View Controller pattern (padrão de projeto)
- A camada **Model** é o coração da aplicação, onde se localizam as regras de negócio, as entidades, a camada de acesso a dados, validação
- A camada **View** é responsável por renderizar a resposta à requisição (JavaScript, CSS, HTML, Template Engine)
- No meio das duas camadas anteriores, temos o **Controller**, coordenando o fluxo da aplicação

![Diagram From Wikipedia, the free encyclopedia](https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/MVC-Process.svg/200px-MVC-Process.svg.png)

- **Analogia Aplicação MVC x Prédio comercial**
    - o recepcionista do prédio é o framework MVC/front-controller. Ele recebe as requisições, pode consultar algum arquivo de metadados (xml, json) que possua por exemplo o mapeamento das rotas (qual url aponta para qual método). Ele encaminha para o "setor responsável" a requisição feita pelo usuário.
    - a pessoa que recebe a requisição das mãos do recepcionista, leva ao setor responsável e traz a resposta é o controller. O controller sabe quais informações são necessárias para gerar a view, requisita ao model tais informações e transmite a resposta para quem solicitou.
- O **browser** gera uma requisição a partir de uma URL e envia a --> um **web server** (e.g. Apache), que usando essa URL, direciona ao alvo da requisição, --> uma **aplicação**, na sua camada **controller**.
- Se não houver necessidade de se acessar dados (por exemplo, um GET para renderizar a página inicial du uma simples aplicação que não exija validação de nenhuma regra), o **controller** encaminha a requisição ao **view**, que renderiza a resposta enviada ao browser.
- Caso haja a necessidade de se acessar dados para gerar a resposta, o **controller** direciona a requisição ao **model**, que acessa o banco de dados e devolve as informações ao **controller**. Essa operação se repetirá até que o **controller** tenha obtido as informações necessárias para atender a requisição e encaminhá-las para o **view**, que finalmente renderizará a resposta ao browser.

##### Qual o papel do Django e do React no MVC
- O React atua sobre a camada **view** da aplicação, recebendo as informações do **controller** para renderizar as respostas ao usuário
- O Django, por sua vez, se ocupará das camadas
    - **controller**: mapeamento de rotas, entrypoint e endpoints, julgando se há necessidade de acessar dados, podendo direcionar a requisição tanto para o model (quando há essa necessidade) quanto para a view (quando não há).
    - **model**: regras de neǵocio, validações, camada de acesso ao banco de dados. É instanciado pelo controller e responde a essa mesma camada para o fluxo da aplicação.

##### Qual os passos para a aplicação prática?
- *iniciar uma aplicação do Django*
    - create repository on github (branch `main`)
    - `git clone projectFolder` (when you clone you don't need to add a remote like `git remote add origin <url>`)
    - `django-admin startproject projectName projectFolder`
    - ??? should I add `settings.py` to .gitignore ???
    - `git push -u origin main`
    - ??? save `SECRET_KEY` and database password as environment variables -> is this effective? what else can be done? ???
- *utilizar o sistema de usuários builtin*
    - ***dont use django.contrib.auth for now, only django.models***
        - auth support for Django is in the module `django.contrib.auth`
        - `django-admin startproject` by default creates `settings.py` with two items in `INSTALLED_APPS`:
            1 `django.contrib.auth`: : core of the authentication framework, and its default models.
            2 `django.contrib.contenttypes`: Django content type system, which allows permissions to be associated with models you create.
        - `django-admin startproject` also by default lists these two items in `MIDDLEWARE`:
            1 `SessionMiddleware` manages sessions across requests.
            2 `AuthenticationMiddleware` associates users with requests using sessions.

- *endpoint para criar novos usuários*
- *receber um request com usuário, senha e email*
- *responder um status de created*
    - `django-admin startapp accounts`
    - Each Django model is a Python class that subclasses `django.db.models.Model`
    - Set user model on accounts models.py
    - The most important part of a model – and the only required part of a model – is the list of database fields it defines
    - Also, register the model in the app’s admin.py
    - Once you have defined your models, you need to tell Django you’re going to use those models. Do this by editing your settings file and changing the INSTALLED_APPS setting to add the name of the module that contains your models.py
    - In a database management system, a transaction is a single unit of logic or work, sometimes made up of multiple operations. Any logical calculation done in a consistent mode in a database is known as a transaction. One example is a transfer from one bank account to another: the complete transaction requires subtracting the amount to be transferred from one account and adding that same amount to the other.
    - A database transaction, by definition, must be atomic (it must either be complete in its entirety or have no effect whatsoever), consistent (it must conform to existing constraints in the database), isolated (it must not affect other transactions) and durable (it must get written to persistent storage).[1] Database practitioners often refer to these properties of database transactions using the acronym ACID.
    - Migrations are Django’s way of propagating changes you make to your models (adding a field, deleting a model, etc.) into your database schema. They’re designed to be mostly automatic, but you’ll need to know when to make migrations, when to run them, and the common problems you might run into.
    - On databases that support DDL transactions (SQLite and PostgreSQL), all migration operations will run inside a single transaction by default. In contrast, if a database doesn’t support DDL transactions (e.g. MySQL, Oracle) then all operations will run without a transaction.
    - You can prevent a migration from running in a transaction by setting the atomic attribute to False.
    - With these settings in place, running the command `manage.py migrate` creates the necessary database tables for auth related models and permissions for any models defined in your installed apps
    - add url pattern to admin urls targeting accounts urls
    - add a urls.py to accounts app and target route 'signup/' to signup view
    - `import .view`, and then `path('signup/', <callable from .view>)`
    - add view for responding to `request` -> `from django.http import JsonResponse`
    - create a function on the view that takes the `request.body.decode()` and load it to json (`json.loads()`)
    - it will read a string a cast it to a json object so you can use the info to create a User object
    - The keyword arguments are the names of the fields you’ve defined on your model. Note that instantiating a model in no way touches your database; for that, you need to `save()`
    - Passwords are never saved in the database on plain text format. It needs to be hashed before - that is, a cryptography is applied to it: `bcrypt.hashpw(password.encode(), bcrypt.gensalt()`
    - The HTTP `201 Created` success status response code indicates that the request has succeeded and has led to the creation of a resource.

- *endpoint de logar*
    - *receber um usuário e senha*
        - criar modelo de session (com user_id como foreign key e on_delete cascade)
        - enviar um request com body em json com usuário e senha de User já registrado no sistema
        - validar se informações batem com as que estão no banco de dados
        - bcrypt para fazer hash da password inserido como override da função save no modelo de user
        - retornar um token de sessao como cookie e um body em json 
            - token criado por secrets.token_hex()

    - *retorna um token e um status de ok*
- front-end
    - setup do React
    - tela de criar novo usuário
        - formulário -> user senha e email
        - enviar form para o endpoint
    - tela de login
        - form com user e senha
        - enviar o form para o endpoint
        - dependendo da resposta mandar para outra tela de logado
    - tela de logado que só pode ser acessada se tiver token válido
