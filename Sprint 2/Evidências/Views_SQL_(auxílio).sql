--
SELECT * FROM tb_locacao;


--
Create view dim_locacao_veiculos as
Select
	idLocacao as idLocacao,
	idCliente as idCLiente,
	idCarro as idCarro,
	idCombustivel as idCombustivel,
	dataLocacao as dataLocacao,
	horaLocacao as horaLocacao,
	qtdDiaria as qtdDiaria,
	vlrDiaria as vlrDiaria,
	dataEntrega as dataEntrega,
	horaEntrega as horaEntrega,
	idVendedor as idVendedor
From tb_locacao

SELECT * from dim_locacao_veiculos dlv 

CREATE view dim_carro as
Select
	idCarro as IdCarro,
	kmCarro as kmCarro,
	classiCarro as chassiCarro,
	marcaCarro as marcaCarro,
	modeloCarro as modeloCarro,
	anoCarro as anoCarro,
	idCombustivel as idCombustivel
from tb_locacao 

SELECT * from dim_carro div

CREATE view dim_Clientes as
select
	idCliente as idCliente,
	nomeCliente as nomeCliente,
	cidadeCliente as cidadeCliente,
	estadoCliente as cidadeCliente,
	paisCliente as paisCLiente
from tb_locacao

SELECT distinct * from dim_clientes

CREATE view dim_vendedor as
select
	idVendedor as idVendedor,
	nomeVendedor as idVendedor,
	sexoVendedor as idVendedor,
	estadoVendedor as estadoVendedor
from tb_locacao

SELECT distinct * from dim_vendedor

CREATE view dim_combustivel as 
select
	idCombustivel as idCombustivel,
	tipoCombustivel as tipoCombustivel
from tb_locacao

SELECT distinct * from dim_combustivel
	