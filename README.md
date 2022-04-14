<h1 align="center">  API - 404 BIS </h1>
<h3 align="center"> Projeto de Gestão de Serviços da Tecnologia da Informação </h3>

<p align="center">
    <a href="#sobre">Sobre</a> | 
    <a href="#backlog">Backlogs</a> | 
    <a href="#prototipo">Protótipo</a> | 
    <a href="#rodar">Como Rodar</a> |
     <a href="#pastas">Configuração das pastas</a> | 
    <a href="#equipe">Equipe</a>
</p>

<span id="sobre">

## :pencil: Sobre o projeto
 O projeto tem como objetivo criar um site que auxilia o controle de serviços para a área de tecnlogia da FATEC Profº Jessen Vidal,
 possibilitando a abertura e fechamento de chamados, assim agilizando a identificação de problemas dentro do setor.
    
  
> :gear: **Tecnologias Utilizadas:** [Figma](http://www.figma.com), [HTML](https://developer.mozilla.org/pt-BR/docs/Web/HTML), [CSS](https://developer.mozilla.org/pt-BR/docs/Web/CSS), [JavaScript](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript), [Python](https://www.python.org/), [Flask](https://flask.palletsprojects.com/en/2.0.x/), [Visual Studio Code](https://code.visualstudio.com/), [Discord](https://discord.com/), [GitHub](https://github.com/)
   
 <div align="center">   
 <span id="backlog">
  
 ## :dart: Backlogs
   
 ### Backlog do produto
 #### Requisitos Funcionais  
| CÓDIGO | DESCRIÇÃO | PRVISÃO DE CONCLUSÃO |
|:------:|:---------:|:--------------------:|
| RF 01 | Sistema de cadastro e login | SPRINT 2 |
| RF 02 | Abertura e fechamento de chamados | SPRINT 1 |
| RF 03 | Aceite ou rejeite de chamados | SPRINT 1 |
| RF 04 | Sistema de avaliação do chamado | SPRINT 2 |
| RF 05 | Filtragem de chamados por tipo de problema | SPRINT 2 |
| RF 06 | Filtragem de chamados por data | SPRINT 2 |
| RF 07 | Geração de estatíticas | SPRINT 3 |
 
#### Requisitos Não Funcionais  
| CÓDIGO | DESCRIÇÃO | 
|:------:|:---------:|
| RNF 01 | Banco de dados em MySQL ou MariaDB |
| RNF 02 | Frontend em HTML 5, CSS 3 e Javascript |
| RNF 03 | Utilização de frameworks pelo frontend |
| RNF 04 | Utilização do GitHub para pra controle de versionamento |
| RNF 05 | Interface simples e intuitiva |  
| RNF 06 | Sistema deve ser responsivo |
| RNF 07 | Backend em Python 3+ e microframework Flask |
     
### Backlog das sprints 
#### Sprint 1
| CÓDIGO | DESCRIÇÃO |
|:------:|:---------:|
| --    | Levantamento de requisitos |
| --    | Criação do wireframe |
| RF 02 | Abertura e fechamento de chamados |
| RF 03 | Aceite ou rejeite de chamados |
| --    | Criação e integração do banco de dados |  
     
#### Metricas Sprint 1      
 Utilizamos os gráficos de burndown como forma de medir o desempenho e o progeresso durante a sprint:
  
 ![Burndown Chart](https://user-images.githubusercontent.com/92696799/163481889-2437818c-bdb1-4c7a-b16f-e78ee6afe424.png)
 
 ![Tarefas da sprint](https://user-images.githubusercontent.com/92696799/163482971-bf152d18-be96-4270-8b33-98c68c556097.jpg)

  
     
#### Sprint 2
| CÓDIGO | DESCRIÇÃO |
|:------:|:---------:|
| RF 01 | Sistema de cadastro e login |
| RF 04 | Sistema de avaliação do chamado 
| RF 05 | Filtragem de chamados por tipo de problema |
| RF 06 | Filtragem de chamados por data |

#### Sprint 3
| CÓDIGO | DESCRIÇÃO |
|:------:|:---------:|
| RF 07 | Geração de estatíticas | SPRINT 3 |

</div>     
<span id="pastas">
   
## :file_folder: Configuração das pastas
* 📂 `src`: Pasta com os códigos
* 📂 `doc`: Pasta com Documentação relacionada ao Projeto
 
<span id="prototipo"> 
  
## :desktop_computer: Prótotipo
  
<div align="center">
  
### Protótipo do Projeto
#### Tela Login e de Cadastro
![Login](https://user-images.githubusercontent.com/79495727/163172972-9e18f440-1dc3-4a7c-adbc-cba09ff76c5e.png)
![Cadastrar](https://user-images.githubusercontent.com/79495727/163173006-b046683a-5503-417a-b1e0-cfc6e06d7147.png)

</div>

<span id="rodar"> 
    
## :mag_right: Como rodar

- Crie um ambiente virtual para rodar o aplicativo
~~~ 
py -3 -m venv venv
~~~
- Instale as dependencias usando o arquivo Requirements.txt
~~~
pip install -r requirements.txt
~~~
- Set o FLASK_ENV e o FLASK_APP
~~~
set FLASK_ENV=development
set FLASK_APP=src/app.py
~~~
- Abra o Workbench e crie o banco de dados de forma local

<div align="center">
  
  ### Jogar imagens aqui
</div>

-  Rode o servidor local
~~~
flask run
~~~

- Caso a execução de Scripts esteja desativada... Passo a Passo para ativar:

Abra o PowerShell no modo Administrador e digite o seguinte código
~~~
Set-ExecutionPolicy Unrestricted
~~~
Digite 'A'

<div align="center">

   ![image](https://user-images.githubusercontent.com/79495727/160821599-f4b87a00-5f66-408b-a201-de8bdea3c394.png)

 </div>
    
<span id="equipe"> 
    
## :busts_in_silhouette: Equipe

|    Função     | Nome                                  |                                                                                                                                                      LinkedIn & GitHub                                                                                                                                                      |
| :-----------: | :------------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| Product Owner | Guilherme Duarte Cenzi Dias           |  [![Linkedin Badge](https://img.shields.io/badge/Linkedin-blue?style=flat-square&logo=Linkedin&logoColor=white)](https://www.linkedin.com/in/guilherme-duarte-cenzi-dias-9737621b6) [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/guilhermedcdias)              |
| Scrum Master  | MWallace Felipe De França Souza       |  [![Linkedin Badge](https://img.shields.io/badge/Linkedin-blue?style=flat-square&logo=Linkedin&logoColor=white)](https://www.linkedin.com/in/wallacefelipe21/) [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/wallacefelipe21)              |
|   Dev Team    | Amanda Vieira de Oliveira             |  [![Linkedin Badge](https://img.shields.io/badge/Linkedin-blue?style=flat-square&logo=Linkedin&logoColor=white)](https://www.linkedin.com/in/amanda-vo/) [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/amandavo)                           |
|   Dev Team    | Lucas Vinicius da Silva Soares        |  [![Linkedin Badge](https://img.shields.io/badge/Linkedin-blue?style=flat-square&logo=Linkedin&logoColor=white)](https://www.linkedin.com/in/lucasviniciussoares/) [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/LucasVinicius32)          |
|   Dev Team    | Valderi Douglas Camargo Queiros Ferreira |  [![Linkedin Badge](https://img.shields.io/badge/Linkedin-blue?style=flat-square&logo=Linkedin&logoColor=white)](https://www.linkedin.com/in/valderidouglas/) [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/ValderiDouglas)             |
