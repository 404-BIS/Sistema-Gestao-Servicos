## API - 404 BIS - Projeto de Gestão de Serviços
**Tema:** Sistema de gestão de serviços de técnologia da Informação

**Descrição das Pastas:**
* src: Pasta com os códigos
* doc: Pasta com Documentação relacionada ao Projeto


***
## Técnologias Utilizadas

<div align="center">
  

   ![icons8-flask-96](https://user-images.githubusercontent.com/79495727/160216619-4a76adbf-afbe-46ed-ac14-33512209cebf.png)
   ![icons8-html-5-96](https://user-images.githubusercontent.com/79495727/160216737-0dd4e3f6-3aff-4571-b5ec-b288c5eae0c9.png)
   ![icons8-css3-96](https://user-images.githubusercontent.com/79495727/160216946-0861b4e1-a715-4e3a-844d-2d8c9b1af8ad.png)
   ![icons8-javascript-logo-96](https://user-images.githubusercontent.com/79495727/160217125-227bc0fd-ac36-4284-97d2-4c9cdf6eccbd.png)
   ![icons8-logo-mysql-96](https://user-images.githubusercontent.com/79495727/160220199-c55137ac-6541-446e-8d6a-72598c0313d4.png)



  
</div>

***


## Backlog do Produto

<div align="center">
  
  ### Requisitos Funcionais
  
COD | DESCRIÇÃO | PROGRAMAÇÃO | STATUS |
:--:|:---------:|:-----------:|:-----:|
RF 01 | O  sistema  só  deve  ser  acessado  por  pessoas  devidamente  cadastradas,  de  acordo  com  a natureza das operações a serem executadas pelo mesmo. | SPRINT 2| 👎🏻 |
RF 02 | O Administrador do sistema, um único usuário,deve possuir acesso total às funcionalidades do sistema. | SPRINT 2 | 👎 |
RF 03 | Um Executor  de  Serviço(o  sistema  pode  ter  um  ou  vários  executores),  deve  ser  capaz  de atender  a  uma  solicitação  podendo:  a)  atender a  um  serviço  demandado (ao  final  o  chamado  é fechado e o serviço executado é descrito), b) rejeitar um serviço(o chamado é fechado mas uma justificativa para a rejeição deve ser apresentada). | SPRINT 1 | ✔
RF 04 | Um Usuário Comum (o sistema pode ter um ou muitos usuários) deve ser capaz de abrir uma solicitaçãode  serviço,  visualizar  o  estado  de  todas  as  suas  solicitações,  da  mais  recente  à  mais antiga,e atribuir uma nota (de 0 a 10) à execução de uma de suas solicitações que foi fechada pelo executor. | SPRINT 1 E 3 | ✔
RF 05 | Uma  solicitação  de  serviço,  ao  ser  criada, deve  ser atribuída  automaticamente  a  um  dos executores de serviço cadastrados no sistema. | SPRINT 1 | ✔
RF 06 | A  atribuição  da  solicitação  deve  seguir  um  esquema  de  distribuição cíclico/  sequencial  de acordo com o número atual de executores (ex. Se há 3 executores cadastrados (A,B,C) e são criadas 7 solicitações, sequencialmente (da1ª à7ª ), então os operadores A,B,C receberão as atribuições das solicitações A =[1ª , 4ª , 7ª ] , B= [2ª , 5ª ] , C= [3ª , 6ª ]. | SPRINT 2 | ✔ 
RF 07 | Ao  ser  criada, uma  solicitação/chamadodeve  ser  atreladaao  seu  criador  e  atribuídaa  um executor. | SPRINT 1 | ✔
RF 08 | Uma solicitação deve possuir: 1- data/hora de criação(obrigatório).  2- data/hora de fechamento(obrigatório). 3- tipo: Problema de Hardware, Problema de Software ou Esclarecimento/Informação.  4- uma descrição de abertura(obrigatório). 5- uma imagem/arquivo (opcional).  6- uma resposta ou justificativa para o fechamento(obrigatório). 7- uma avaliação atribuída pelo usuário que a originou, após o fechamento (opcional). | SPRINT 1 | ✔
RF 09 | O sistema deve prover relatórios que mostrem: 1- Aquantidadepercentualde solicitações abertas e fechadas em um determinado intervalo de  tempo (uma espécie de “instantâneo” considerando um dia, uma semana ou um mês específico). 2- A evolução diáriada quantidade de solicitações abertas e fechadas, considerando intervalos de tempo especificados (1 semana, 15 dias, etc., utilizando datas de início e término para especificar tal intervalo). 3- A avaliação média de cada executor de solicitação.d)A  avaliação  média  global  do  sistema,  tendo  como  base  a  nota  atribuída  a  todos  os chamados. | SPRINT 3 | 👎🏻

 
  
  
   ### Requisitos Não Funcionais
  
COD | DESCRIÇÃO | STATUS |
:--:|:---------:|:------:|
RNF 01 | O Requisito Funcional RF 09 pode ser implementado utilizando gráficos | ✔️ |
RNF 02 | Desenvolver o back end com alinguagem Python 3+ e o microframework Flask. | ✔ |
RNF 03 | Utilizar o sistema gerenciador de banco de dados MariaDB/MySQL. | ✔ |
RNF 04 | Utilizar HTML 5 para arquitetura da informação da aplicação. | ✔ |
RNF 05 | Utilizar  CSS  3para  especificação  do  layout  e  demais  características  de  renderização  da interface com o usuário. | ✔ |
RNF 06 | Utilizar o GitHub para controle de versão dos artefatos de projeto. | ✔ |
RNF 07 | Interface com navegação intuitiva (e.g. acesso à informação com poucos “cliques”). | ✔ |
RNF 08 | Sistema responsivo. | ✔ |
RNF 09 | Utilizar JavaScript no front end (obs: pode fazer uso de frameworks). | ✔ |

</div>

***


<div align="center">
  
  ### Backlog da Sprint 1

  
COD | DESCRIÇÃO | AREA | STATUS |
:--:|:---------:|:------:|:-----|
SP01 01 | Prototipação do sistema de solicitações. | Front-end e Back-end | ✔ |
SP01 02 | Criação do Front para o sistema de solicitações. | Front-end | ✔ |
SP01 03 | Criação do Banco de dados para o sistema de solicitações. | Back-end | ✔ |
SP01 04 | CRUD para sistema de solicitações. | Back-end | ✔ |
SP01 05 | Implementação da Parte de solicitações. | Front-end e Back-end | ✔ |


</div>

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

<div align="center">
  
  ### Como Rodar

</div>

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

