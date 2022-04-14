create database if not exists sistema_solicitacao;

use sistema_solicitacao;

create table requisicao_exec (
	id_requisicao int primary key auto_increment,
    titulo varchar (40) not null,
	descricao varchar (150) not null,
    tipo varchar (40) not null,
    condicao varchar (15),
    comentario varchar(200)
);
create table requisicao (
	id_requisicao int primary key auto_increment,
    titulo varchar (40) not null,
	descricao varchar (150) not null,
    tipo varchar (40) not null,
    condicao varchar (15),
    comentario varchar(200)
);
