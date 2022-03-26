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
  
COD | DESCRIÇÃO | PRIORIDADE | DATA DE IMPLEMENTAÇÃO | STATUS |
:--:|:---------:|:----------:|:---------------------:|:-----:|
RF 01 | O  sistema  só  deve  ser  acessado  por  pessoas  devidamente  cadastradas,  de  acordo  com  a natureza das operações a serem executadas pelo mesmo. | Alta | 14-03-21 | ✔️ |
RF 02 | O Administrador do sistema, um único usuário,deve possuir acesso total às funcionalidades do sistema. | Baixa | 15-04-21 | 👎 |
RF 03 | Um Executor  de  Serviço(o  sistema  pode  ter  um  ou  vários  executores),  deve  ser  capaz  de atender  a  uma  solicitação  podendo:  a)  atender a  um  serviço  demandado (ao  final  o  chamado  é fechadoe o serviço executado é descrito), b) rejeitar um serviço(o chamado é fechado mas uma justificativa para a rejeição deve ser apresentada).
RF 04 | Um Usuário Comum (o sistema pode ter um ou muitos usuários) deve ser capaz de abrir uma solicitaçãode  serviço,  visualizar  o  estado  de  todas  as  suas  solicitações,  da  mais  recente  à  mais antiga,e atribuir uma nota (de 0 a 10) à execução de umade suas solicitaçõesque foi fechadapelo executor.
RF 05 | Uma  solicitação  de  serviço,  ao  ser  criada, deve  ser atribuída  automaticamente  a  um  dos executores de serviço cadastrados no sistema.
RF 06 | A  atribuição  da  solicitação  deve  seguir  um  esquema  de  distribuição cíclico/  sequencial  de acordo com o número atual de executores (ex. Se há 3 executores cadastrados (A,B,C) e são criadas7 solicitações, sequencialmente (da1ª à7ª ), então os operadores A,B,C receberão as atribuições das solicitaçõesA =[1ª , 4ª , 7ª ] , B= [2ª , 5ª ] , C= [3ª , 6ª ].
RF 07 | Ao  ser  criada, uma  solicitação/chamadodeve  ser  atreladaao  seu  criador  e  atribuídaa  um executor.
RF 08 | Uma solicitação deve possuir: 1- data/hora de criação(obrigatório).  2- data/hora de fechamento(obrigatório). 3- tipo: Problema de Hardware, Problema de Software ou Esclarecimento/Informação.  4- uma descrição de abertura(obrigatório). 5- uma imagem/arquivo (opcional).  6- uma resposta ou justificativa para o fechamento(obrigatório). 7- uma avaliação atribuída pelo usuário que a originou, após o fechamento (opcional).
RF 09 | O sistema deve prover relatórios que mostrem: 1- Aquantidadepercentualde solicitações abertas e fechadas em um determinado intervalo de  tempo (uma espécie de “instantâneo” considerando um dia, uma semana ou um mês específico). 2- A evolução diáriada quantidade de solicitações abertas e fechadas, considerando intervalos de tempo especificados (1 semana, 15 dias, etc., utilizando datas de início e término para especificar tal intervalo). 3- A avaliação média de cada executor de solicitação.d)A  avaliação  média  global  do  sistema,  tendo  como  base  a  nota  atribuída  a  todos  os chamados.

 
  
  
   ### Requisitos Não Funcionais
  
COD | DESCRIÇÃO | PRIORIDADE | STATUS |
:--:|:---------:|:----------:|:------:|
RNF 01 | O Requisito Funcional RF 09 pode ser implementado utilizando gráficos | Alta | ✔️ |
RNF 02 | Desenvolver o back end com alinguagem Python 3+ e o microframework Flask. | Baixa | 👎 |
RNF 03 | Utilizar o sistema gerenciador de banco de dados MariaDB/MySQL.
RNF 04 | Utilizar HTML 5 para arquitetura da informação da aplicação.
RNF 05 | Utilizar  CSS  3para  especificação  do  layout  e  demais  características  de  renderização  da interface com o usuário.
RNF 06 | Utilizar o GitHub para controle de versão dos artefatos de projeto.
RNF 07 | Interface com navegação intuitiva (e.g. acesso à informação com poucos “cliques”).
RNF 08 | Sistema responsivo.
RNF 09 | Utilizar JavaScript no front end (obs: pode fazer uso de frameworks).

</div>

***
