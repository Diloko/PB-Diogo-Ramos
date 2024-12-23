import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame

# Parâmetros do job
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'CSV_PATH', 'JSON_PATH'])

# Configurações do Spark e Glue
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Carregar dados do Parquet da pasta CSV
filmes_df = spark.read.parquet(args['CSV_PATH'])

# Carregar dados do Parquet da pasta JSON
receitas_df = spark.read.parquet(args['JSON_PATH'])

# Realizar o join com base no título original e original_title
joined_df = filmes_df.join(receitas_df, filmes_df.tituloOriginal == receitas_df.original_title)

# Selecionar colunas relevantes
result_df = joined_df.select("tituloOriginal", "anoLancamento", "genero", "original_title", "revenue", "budget", "popularity")

# Converter de volta para DynamicFrame
result_dynamic_df = DynamicFrame.fromDF(result_df, glueContext, "result_dynamic_df")

# Salvar dados na camada Refined
glueContext.write_dynamic_frame.from_options(
    frame=result_dynamic_df,
    connection_type="s3",
    connection_options={"path": "s3://data-lake-diogo/Refined/"},
    format="parquet"
)

# Commit do job
job.commit()
