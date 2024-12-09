import sys
from pyspark.sql import SparkSession
from awsglue.utils import getResolvedOptions
from datetime import datetime

args = getResolvedOptions(sys.argv, ['JOB_NAME', 'input_path', 'output_path'])

spark = SparkSession.builder \
    .appName(args['JOB_NAME']) \
    .getOrCreate()

input_path = args['input_path']
date_str = datetime.now().strftime("%Y/%m/%d")
output_path = f"{args['output_path']}/{date_str}/json/"

df = spark.read.json(input_path)

record_count = df.count()
print(f"Quantidade de registros lidos: {record_count}")

if record_count == 0:
    raise ValueError("adult", "Nenhum registro encontrado no caminho de entrada especificado.")

print("Colunas disponíveis no DataFrame original:", df.columns)

columns_to_exclude = ["adult", "backdrop_path", "overview", "poster_path", "video", "vote_average", "vote_count"]
selected_columns = [col for col in df.columns if col not in columns_to_exclude]

if not selected_columns:
    raise ValueError("Nenhuma coluna foi selecionada para ser escrita no formato PARQUET.")

df_selected = df.select(*selected_columns)

selected_record_count = df_selected.count()
print(f"Quantidade de registros após seleção de colunas: {selected_record_count}")

if selected_record_count > 0:
    df_selected.write.mode("overwrite").parquet(output_path)
    print(f"Dados de filmes salvos com sucesso no caminho: {output_path}")
else:
    print("Nenhum registro válido disponível para ser escrito no formato PARQUET.")

spark.stop()
