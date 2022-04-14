<h1 align="center">  API - 404 BIS - Projeto de Gestão de Serviços </h1>
<h3 align="center"> Sistema de gestão de serviços de técnologia da Informação </h3>

<p align="center">
    <a href="#sobre">Sobre</a> | 
    <a href="#backlog">Backlogs</a> | 
    <a href="#pastas">Configuração das pastas</a> | 
    <a href="#tec">Tecnologias</a> | 
    <a href="#prototipo">Protótipo</a> | 
    <a href="#rodar">Como Rodar</a> |
    <a href="#equipe">Equipe</a>  

</p>

<span id="sobre">

## :pencil: Sobre o projeto
  
 O projeto tem como objetivo criar um site que auxilie no controle de serviços para a área de tecnlogia da FATEC Profº Jessen Vidal
 possibilitando a abertura/fechamento de chamados e assim agilizando a identificação de problemas dentro do setor. 
  
 <span id="backlog">
  
 ## :dart: Backlogs
   
 <div align="center">
   
 ### Backlog do projeto
   
 #### Requisitos Funcionais  
   
COD | DESCRIÇÃO | PROGRAMAÇÃO |
:--:|:---------:|:-----------:|
RF 01 | Sistema de cadastro e login| SPRINT 2 |
RF 02 | Abertura e fechamento de chamados| SPRINT 1 |
RF 03 | Rejeitar ou aceitar chamados| SPRINT 1 | 
RF 04 | Sistema de avaliação do chamado| SPRINT 2 |
RF 05 | Geração de filtrar por tipo de problema| SPRINT 2 | 
RF 06 | Geração de estatíticas do executor| SPRINT 3 | 

   
#### Requisitos Não Funcionais  
   
COD | DESCRIÇÃO |
:--:|:---------:|
RNF 01 | Banco de dados em MySQL ou MariaDB|
RNF 02 | Frontend em HTML 5, CSS 3 e Javascript|
RNF 03 | Frontend pode utilizar de frameworks|
RNF 04 | Utilizar o gitHub para pra controle de versionamento|
RNF 05 | Interface simples e inuitiva|  
RNF 06 | Sistema deve ser responsivo.|
RNF 07 | Backend em Python 3+ e o microframework Flask|

### Backlog do projeto 

#### Sprint 1
   
COD | DESCRIÇÃO |
:--:|:---------:|
01 | Levantamento de requisitos |
02 | Criação do wireframe|
03 | Desenvolvimento das telas do usuário|
04 | Desenvolvimento das telas do executor|
05 | Criação e integração do banco de dados|  
  
   
#### Sprint 2
   
COD | DESCRIÇÃO |
:--:|:---------:|
01 | Criação das telas de login |
02 | Integração do login aos respetivos usuários|
03 | Criação do sistema de filtros|
05 | Criação do sistema de avaliação| 

#### Sprint 2
   
COD | DESCRIÇÃO |
:--:|:---------:|
01 | Criação da interface de estatisticas do administrador |
02 | Desenvolvimento das telas do administrador|
 
</div>

 <span id="pastas">
   
 ## :file_folder: Configuração das pastas
  
* src: Pasta com os códigos
* doc: Pasta com Documentação relacionada ao Projeto
 
<span id="tec">  

 ## :gear: Técnologias Utilizadas
  
- [Figma](http://www.figma.com): Prototipagem
- [HTML](https://developer.mozilla.org/pt-BR/docs/Web/HTML): Estrutura das páginas do site
- [CSS](https://developer.mozilla.org/pt-BR/docs/Web/CSS): Estilização do site
- [JavaScript](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript): Interações do site
- [Python](https://www.python.org/): Back-end
- [Flask](https://flask.palletsprojects.com/en/2.0.x/): Servidor
- [Visual Studio Code](https://code.visualstudio.com/): Codificação
- [Discord](https://discord.com/): Comunicação
- [GitHub](https://github.com/): Versionamento e documentação


<span id="prototipo"> 
  
## :desktop_computer: Prótotipo
  
<div align="center">
  
  ### Protótipo do Projeto
  #### Tela Login e de Cadastro
![Login](https://user-images.githubusercontent.com/79495727/163172972-9e18f440-1dc3-4a7c-adbc-cba09ff76c5e.png)
![Cadastrar](https://user-images.githubusercontent.com/79495727/163173006-b046683a-5503-417a-b1e0-cfc6e06d7147.png)
  #### Tela de Nova Requisção
![User](https://user-images.githubusercontent.com/79495727/163174079-a4cb83e1-6499-40ea-b649-496966689473.png)
  #### Tela de Requisições sem requisições
![User](https://user-images.githubusercontent.com/79495727/163173165-c038cc75-b515-4b3b-8f8d-3853caa7a5d0.png)
  #### Tela de Requisições com requisições
![User](https://user-images.githubusercontent.com/79495727/163173812-297c409a-0e76-4edf-9e8e-43fca5a1c72a.png)
  #### Tela de Requisições com requisições abertas detalhadas
![User](https://user-images.githubusercontent.com/79495727/163173591-27f47370-4970-4783-9e33-cd33ed57fe77.png)
 #### Tela de Requisições com requisições fechadas detalhadas
![User](https://user-images.githubusercontent.com/79495727/163173708-c82c6e82-ccc2-4071-9f1d-b939d74783c6.png)
 #### Modal de Avaliação  
![User](https://user-images.githubusercontent.com/79495727/163173976-f21eac2a-2a7b-46af-a264-67dad63b1a59.png)
 #### Modal Perfil
![User](https://user-images.githubusercontent.com/79495727/163174170-00d1ddc4-afbc-4e6a-a885-fef374136bd1.png)


</div>

<span id="rodar"> 
  
  ## :mag_right: Como rodar

### Crie um ambiente virtual para rodar o aplicativo
~~~ 
py -3 -m venv venv
~~~
### Instale as dependencias usando o arquivo Requirements.txt
~~~
pip install -r requirements.txt
~~~
### Set o FLASK_ENV e o FLASK_APP
~~~
set FLASK_ENV=development
set FLASK_APP=src/app.py
~~~
### Abra o Workbench e crie o banco de dados de forma local

<div align="center">
  
  ### Jogar imagens aqui

</div>

### Rode o servidor local
~~~
flask run
~~~

## Caso a execução de Scripts esteja desativada - Passo a Passo para ativar

### Abra o PowerShell no modo Administrador e digite o seguinte código
~~~
Set-ExecutionPolicy Unrestricted
~~~
### Digite 'A'

<div align="center">

   ![image](https://user-images.githubusercontent.com/79495727/160821599-f4b87a00-5f66-408b-a201-de8bdea3c394.png)

 </div>

