<h2>Proposta Desafio</h2>

<p>O desafio propõe que seja criado um bucket a partir de um script python rodando em um container .</p>

<br>
<br>

<h2>Metodologia</h2>

<p>A metodologia utilizada foi inicialmente criar o script python e posteriormente montar o docker<br>
Estes foram criados em seguida testados, como poderemos ver nas imagens.</p>

<br>

<h2>Execução</h2>

<h3>Criação do script python</h3>

O script python foi montado como pode ser consultado no código e na imagem a seguir:<br>
![script python](../Evidências/código_criação_bucket.png)

A criação da imagem do docker rodou normalmente, mas tive problemas na hora de executar o container por conta da autenticação via AWS CLI,<br>
mas foi resolvido utilizando o código que está no print na hora de rodar a imagem<br>
![docker e container](../Evidências/criação_conteiner_e_execução_para_criar_bucket.png)

Como podemos verificar foram além da criação ter sido executada corretamente, foram enviados os arquivos no formato solicitado<br>
![caminho objetos](../Evidências/caminho_objetos_bucket_desafio.png)

O bucket gerado é arn:aws:s3:::data-lake-diogo, não compreendi totalmente a parte de subir o laboratório s3 do feedback<br>
OBS.: Os arquivos movies.csv e series.csv foram retirados da pasta app detro do desafio pois são muito grandes para serem enviados para o github

<h2>Análise à ser executada</h2>

Para a análise final do desafio, pretendo ter as respostas para as seguintes perguntas:<br>

-O que foi mais rentável entre séries e filmes mais populares da última década?;<br>
-Baseado nos custos é preferível investir em séries ou filmes com o foco principal sendo lucro?<br>
-Existe relação entre as obras mais populares e os prêmios que a indústria distribui?<br>


<h2>Considerações Finais</h2>

Gostaria que as API's fossem apresentadas juntamente com os arquivos csv's, pois apesar de ter escolhido um tema que envolve a parte financeira,<br>
a mesma não se encontra no csv, de forma que não poderia pensar nela antes de serem apresentadas as api's na sprint 7. Felizmente o monitor me ajudou mostrando<br>
que esses dados, apesar de não serem garantidos para todos os filmes e séries, se fazem presentes nas api's.