from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, rand
from pyspark.sql.types import StringType
import random

# Criar a Spark Session
spark = SparkSession \
    .builder \
    .master("local[*]") \
    .appName("Exercicio Intro") \
    .getOrCreate()

# Ler o arquivo 'nomes_aleatorios.txt' e carregá-lo em um dataframe
df_nomes = spark.read.csv("nomes_aleatorios.txt", header=False, inferSchema=True)

# Renomear a coluna para 'Nomes'
df_nomes = df_nomes.withColumnRenamed("_c0", "Nomes")

# Imprimir o esquema do dataframe
df_nomes.printSchema()

# Mostrar as primeiras 10 linhas do dataframe
df_nomes.show(10)

# Etapa 3: Adicionar coluna 'Escolaridade' com valores aleatórios
escolaridades = ["Fundamental", "Medio", "Superior"]

df_nomes = df_nomes.withColumn(
    "Escolaridade",
    when(rand() < 0.33, escolaridades[0])
    .when((rand() >= 0.33) & (rand() < 0.66), escolaridades[1])
    .otherwise(escolaridades[2])
)

# Etapa 4: Adicionar coluna 'Pais' com valores aleatórios
paises = ["Argentina", "Bolívia", "Brasil", "Chile", "Colômbia", "Equador", 
          "Guiana", "Paraguai", "Peru", "Suriname", "Uruguai", "Venezuela"]

df_nomes = df_nomes.withColumn(
    "Pais",
    when(rand() < 1/12, paises[0])
    .when((rand() >= 1/12) & (rand() < 2/12), paises[1])
    .when((rand() >= 2/12) & (rand() < 3/12), paises[2])
    .when((rand() >= 3/12) & (rand() < 4/12), paises[3])
    .when((rand() >= 4/12) & (rand() < 5/12), paises[4])
    .when((rand() >= 5/12) & (rand() < 6/12), paises[5])
    .when((rand() >= 6/12) & (rand() < 7/12), paises[6])
    .when((rand() >= 7/12) & (rand() < 8/12), paises[7])
    .when((rand() >= 8/12) & (rand() < 9/12), paises[8])
    .when((rand() >= 9/12) & (rand() < 10/12), paises[9])
    .when((rand() >= 10/12) & (rand() < 11/12), paises[10])
    .otherwise(paises[11])
)

# Etapa 5: Adicionar coluna 'AnoNascimento' com valores aleatórios entre 1945 e 2010
df_nomes = df_nomes.withColumn(
    "AnoNascimento", 
    (rand() * (2010 - 1945 + 1) + 1945).cast("int")
)

# Etapa 6: Selecionar pessoas que nasceram neste século
df_select = df_nomes.filter(col("AnoNascimento") >= 2000)

# Mostrar 10 nomes do dataframe resultante
df_select.show(10)

# Etapa 7: Repetir a seleção usando SparkSQL
df_nomes.createOrReplaceTempView("pessoas")

df_select_sql = spark.sql("SELECT * FROM pessoas WHERE AnoNascimento >= 2000")

# Mostrar 10 nomes do dataframe resultante do SparkSQL
df_select_sql.show(10)

# Usando o método filter do DataFrame
millennials_count = df_nomes.filter((col("AnoNascimento") >= 1980) & (col("AnoNascimento") <= 1994)).count()
print(f"Número de pessoas da geração Millennials: {millennials_count}")

# Usando Spark SQL
df_nomes.createOrReplaceTempView("pessoas")
millennials_count_sql = spark.sql("SELECT COUNT(*) AS Millennials_Count FROM pessoas WHERE AnoNascimento BETWEEN 1980 AND 1994")
millennials_count_sql.show()

# Definir as gerações
geracoes = [
    ("Baby Boomers", 1944, 1964),
    ("Geração X", 1965, 1979),
    ("Millennials", 1980, 1994),
    ("Geração Z", 1995, 2015)
]

# Criar uma consulta para cada geração e combinar os resultados
queries = []
for geracao, start_year, end_year in geracoes:
    query = f"""
    SELECT 
        Pais, 
        '{geracao}' AS Geracao, 
        COUNT(*) AS Quantidade 
    FROM pessoas 
    WHERE AnoNascimento BETWEEN {start_year} AND {end_year} 
    GROUP BY Pais
    """
    queries.append(query)

# Combinar as consultas em uma só
final_query = " UNION ALL ".join(queries)
df_result = spark.sql(final_query)

# Mostrar todas as linhas em ordem crescente de Pais, Geracao e Quantidade
df_result.orderBy("Pais", "Geracao", "Quantidade").show()
