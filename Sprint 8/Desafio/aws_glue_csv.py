import sys
from pyspark.sql import SparkSession
from awsglue.utils import getResolvedOptions
from datetime import datetime

# Parâmetros do job
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'input_path', 'output_path'])

# Inicializar SparkSession
spark = SparkSession.builder \
    .appName(args['JOB_NAME']) \
    .getOrCreate()

# Caminhos dos dados
input_path = args['input_path']
date_str = datetime.now().strftime("%Y/%m/%d")
output_path = f"{args['output_path']}/{date_str}/csv/"

# Leitura dos dados CSV com delimitador "|"
df = spark.read.csv(input_path, header=True, sep='|', inferSchema=True)

# Verificar a quantidade de registros no DataFrame
record_count = df.count()
print(f"Quantidade de registros lidos: {record_count}")

if record_count == 0:
    raise ValueError("Nenhum registro encontrado no caminho de entrada especificado.")

# Verificar colunas disponíveis
print("Colunas disponíveis no DataFrame original:", df.columns)

# Selecionar todas as colunas, exceto as especificadas
columns_to_exclude = [
    "tempoMinutos", "notaMedia", "numeroVotos", "generoArtista", "personagem",
    "nomeArtista", "anoNascimento", "anoFalescimento", "profissao", "titulosMaisConhecidos"
]
selected_columns = [col for col in df.columns if col not in columns_to_exclude]

# Verificar se há colunas selecionadas
if not selected_columns:
    raise ValueError("Nenhuma coluna foi selecionada para ser escrita no formato PARQUET.")

# Selecionar as colunas desejadas
df_selected = df.select(*selected_columns)

# Verificar a quantidade de registros no df_selected
selected_record_count = df_selected.count()
print(f"Quantidade de registros após seleção de colunas: {selected_record_count}")

# Gravação dos dados em formato PARQUET
if selected_record_count > 0:
    df_selected.write.mode("overwrite").parquet(output_path)
    print(f"Dados salvos com sucesso no caminho: {output_path}")
else:
    print("Nenhum registro válido disponível para ser escrito no formato PARQUET.")

# Finalizar SparkSession
spark.stop()
