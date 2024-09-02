#!/bin/bash

#Acessando o diretório ecommerce

cd /mnt/c/users/diogo/documents/desafios-uol/sprint1/ecommerce

#criando as pastas vendas e backup

mkdir -p vendas/backup

#copiando o arquivo csv para as pastas criadas

cp -rf dados_de_vendas.csv dir vendas

cp -rf dados_de_vendas.csv dir vendas/backup

#acessando o diretório vendas e renomeando o arquivo

cd vendas

mv dados_de_vendas.csv dados-$(date +"%Y_%m_%d").csv

#acessando o diretório backup e renomeando o arquivo

cd backup

mv dados_de_vendas.csv backup-dados-$(date +"%Y_%m_%d").csv

touch relatorio.txt

#incluindo data do sistema no relatório

echo 'Data do Sistema:'$(date +"%Y_%m_%d-%H:%M") > relatorio.txt

echo >> relatorio.txt

#Incluindo primeiro registro de vendas no relatório

echo Data Primeiro Registo de Vendas >> relatorio.txt

cat backup-dados-$(date +"%Y_%m_%d").csv | awk -F ',' '{print $5}' | head -n2 | tail -1 >> relatorio.txt

echo >> relatorio.txt

#incluindo data do último registro de vendas no relatório

echo Data Ultimo Registro de Vendas >> relatorio.txt

cat backup-dados-$(date +"%Y_%m_%d").csv | awk -F ',' '{print $5}' | tail -n1 >> relatorio.txt

echo >> relatorio.txt

#incluindo o total de itens diferentes vendidos

echo Quantidade total de itens diferentes vendidos >> relatorio.txt

tail -n +2 backup-dados-$(date +"%Y_%m_%d").csv | wc -l >> relatorio.txt

echo >> relatorio.txt

#incluindo as 10 primeiras linhas do arquivo de vendas

echo 10 primeiras linhas do arquivo backup-dados >> relatorio.txt

head backup-dados-$(date +"%Y_%m_%d").csv >> relatorio.txt

echo >> relatorio.txt

#criando cópia do relatório com a data do mesmo

cp -rf relatorio.txt relatorio-$(date +"%Y_%m_%d").txt

#comprimindo o arquivo de vendas para economizar espaço em disco

zip -r backup-dados-$(date +"%Y_%m_%d").zip backup-dados-$(date +"%Y_%m_%d").csv

#apagando os arquivos .csv originais após gerar o arquivo zip

rm backup-dados-$(date +"%Y_%m_%d").csv

cd ..

rm dados-$(date +"%Y_%m_%d").csv
