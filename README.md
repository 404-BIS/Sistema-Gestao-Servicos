<h1 align="center">  API - 404 BIS </h1>
<h3 align="center"> Projeto de Gestão de Serviços da Tecnologia da Informação </h3>

<p align="center">
    <a href="#sobre">Sobre</a> | 
    <a href="#backlog">Backlogs</a> | 
    <a href="#prototipo">Protótipo</a> | 
    <a href="#rodar">Como Rodar</a> |
    <a href="#pastas">Configuração das pastas</a> | 
    <a href="#equipe">Equipe</a>
    <a href="#video">Vídeo Técnico</a>
</p>

<span id="sobre">

## :pencil: Sobre o projeto
 O projeto tem como objetivo criar um site que auxilia o controle de serviços para a área de tecnlogia da FATEC Profº Jessen Vidal,
 possibilitando a abertura e fechamento de chamados, assim agilizando a identificação de problemas dentro do setor.
    
  
> :gear: **Tecnologias Utilizadas:** [Figma](http://www.figma.com), [HTML](https://developer.mozilla.org/pt-BR/docs/Web/HTML), [CSS](https://developer.mozilla.org/pt-BR/docs/Web/CSS), [JavaScript](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript), [Python](https://www.python.org/), [Flask](https://flask.palletsprojects.com/en/2.0.x/), [Visual Studio Code](https://code.visualstudio.com/), [Discord](https://discord.com/), [GitHub](https://github.com/)
   
 <span id="backlog">  
   
 ## :dart: Backlogs  
     
 <div align="center">   
  
   
 ### Backlog do produto
 #### Requisitos Funcionais  
| CÓDIGO | DESCRIÇÃO |
|:------:|:---------:|
| RF 01 | Sistema de cadastro e login |
| RF 02 | Abertura e fechamento de chamados |
| RF 03 | Aceite ou rejeite de chamados |
| RF 04 | Sistema de avaliação do chamado |
| RF 05 | Filtragem de chamados por tipo de problema |
| RF 06 | Filtragem de chamados por data |
| RF 07 | Geração de estatíticas |
 
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

</div>     
<span id="backlog">  
   
 ## :dart: User Storys 
     
 <div align="center">   
     
  ![US1](https://user-images.githubusercontent.com/79495727/168456150-58187d3b-67f1-4992-849f-e5f93f2a7f09.png)
     
  ![US2](https://user-images.githubusercontent.com/79495727/168456367-a48f3d18-5880-4562-8d45-4faebe71e831.png)
     
  ![US3](https://user-images.githubusercontent.com/79495727/168456444-9ca9d303-9c3f-4a78-9da9-f75778f2f96a.png)


     
#### Metricas Sprint 1      
 Utilizamos os gráficos de burndown como forma de medir o desempenho e o progeresso durante a sprint:
  
 ![Burndown Chart](https://user-images.githubusercontent.com/92696799/163481889-2437818c-bdb1-4c7a-b16f-e78ee6afe424.png)
 
  
</div>     
<span id="prototipo"> 
  
## :desktop_computer: Prótotipo
  
#### Prótotipo da tela do usuário
    
![API](https://user-images.githubusercontent.com/92696799/163493216-654e13f5-c4b9-43df-a295-8dd7b179e3dc.gif)
    
#### Prótotipo da tela do executor
![API-Exec](https://user-images.githubusercontent.com/92696799/163494007-21cde00e-1f0f-4c82-a52f-51ee6eef6012.gif)

<span id="rodar"> 
    
## :mag_right: Como rodar

Antes de rodar o proejeto, faça o download do MySQL Workbench, que será utilizado para a criação do Banco de Dados, siga este vídeo para poder baixar e configurar: [link do vídeo](https://drive.google.com/drive/folders/1dYaIAg5sDPl6jNXHNghidlp36edTh-SW?usp=sharing)   
    
Tecnologias necessárias: Python 3.10 e Workbench
    
- crie uma pasta para clonar o repositório 
~~~
mkdir cloneprojeto  
~~~
    
- entre na pasta criada  
~~~
cd cloneprojeto
~~~
 
- clone o reposiório dentro da pasta 
~~~   
git clone https://github.com/404-BIS/Sistema-Gestao-Servicos.git
~~~
    
- entre na pasta do projeto 
~~~   
cd Sistema-Gestao-Servicos\src
~~~
    
- instale o ambiente que ele será processado 
~~~   
py -m venv venv
~~~
    
- ative o ambiente 
~~~   
venv\Scripts\activate
~~~
    
- baixe as bibliotecas nescessarias 
~~~   
pip install -r requirements.txt
~~~
    
- inicie o site 
~~~   
flask run
~~~

- caso nao aceite, utilize 
~~~   
python3 app.py
~~~
    
- acesse o site utilizando 
~~~   
http://127.0.0.1:5000
~~~

- para entrar na inteface de usuário, utilize o link    
~~~   
http://127.0.0.1:5000/usuario/menu
~~~
    
- para entrar na inteface de executor, utilize o link    
~~~   
http://127.0.0.1:5000/executor/menu
~~~
    
    
    
<span id="pastas">
   
## :file_folder: Configuração das pastas
* 📂 `src`: Pasta com os códigos
* 📂 `doc`: Pasta com Documentação relacionada ao Projeto
     
<span id="equipe"> 
    
## :busts_in_silhouette: Equipe

|    Função     | Nome                                  |                                                                                                                                                      LinkedIn & GitHub                                                                                                                                                      |
| :-----------: | :------------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| Product Owner | Guilherme Duarte Cenzi Dias           |  [![Linkedin Badge](https://img.shields.io/badge/Linkedin-blue?style=flat-square&logo=Linkedin&logoColor=white)](https://www.linkedin.com/in/guilherme-duarte-cenzi-dias-9737621b6) [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/guilhermedcdias)              |
| Scrum Master  | Wallace Felipe De França Souza       |  [![Linkedin Badge](https://img.shields.io/badge/Linkedin-blue?style=flat-square&logo=Linkedin&logoColor=white)](https://www.linkedin.com/in/wallacefelipe21/) [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/wallacefelipe21)              |
|   Dev Team    | Amanda Vieira de Oliveira             |  [![Linkedin Badge](https://img.shields.io/badge/Linkedin-blue?style=flat-square&logo=Linkedin&logoColor=white)](https://www.linkedin.com/in/amanda-vo/) [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/amandavo)                           |
|   Dev Team    | Lucas Vinicius da Silva Soares        |  [![Linkedin Badge](https://img.shields.io/badge/Linkedin-blue?style=flat-square&logo=Linkedin&logoColor=white)](https://www.linkedin.com/in/lucasviniciussoares/) [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/LucasVinicius32)          |
|   Dev Team    | Valderi Douglas Camargo Queiros Ferreira |  [![Linkedin Badge](https://img.shields.io/badge/Linkedin-blue?style=flat-square&logo=Linkedin&logoColor=white)](https://www.linkedin.com/in/valderidouglas/) [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/ValderiDouglas)             |
 
    
 <span id="video"> 
    
## :movie_camera: Vídeo Técnico 
     
link:[link do vídeo](https://drive.google.com/drive/folders/1dYaIAg5sDPl6jNXHNghidlp36edTh-SW?usp=sharing)   
