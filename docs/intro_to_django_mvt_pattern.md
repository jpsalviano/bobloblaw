#### ***Task***: Fazer um sistema de autenticação usando Django e React


* *_ Suporte de Tamoios _*

    * o Django utiliza a estrutura MVT, e não o MVC https://www.geeksforgeeks.org/difference-between-mvc-and-mvt-design-patterns/
    * em resumo, o que você conhece por View, do Django, na verdade é o controller
    * Model View Template (MVT)
        * It has 3 components and each component has a specific purpose:
            * This *Model* similar to MVC acts as an interface for your data and is basically the logical structure behind the entire web application which is represented by a database such as MySql, PostgreSQL.
            * The *View* executes the business logic and interacts with the Model and renders the template. It accepts HTTP request and then return HTTP responses.
            * The *Template* is the component which makes MVT different from MVC. Templates act as the presentation layer and are basically the HTML code that renders the data. The content in these files can be either static on dynamic.

*O que estudei sobre o MVC (Examples are ASP.NET MVC, Spring MVC etc.):*
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