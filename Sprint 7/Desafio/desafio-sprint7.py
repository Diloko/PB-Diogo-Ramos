import boto3
import json
import requests
from datetime import datetime

# Configurações do TMDB
tmdb_api_key = '8bde01dd9413e23e4f16b774e6057f98'
tmdb_movie_endpoint = 'https://api.themoviedb.org/3/discover/movie'
tmdb_movie_detail_endpoint = 'https://api.themoviedb.org/3/movie/'
tmdb_tv_endpoint = 'https://api.themoviedb.org/3/discover/tv'

# Configurações do S3
profile_name = 'DiogoRamos'  # Substitua com o nome do seu perfil configurado
bucket_name = 'data-lake-diogo'

# Criar uma sessão usando o perfil configurado
session = boto3.Session(profile_name=profile_name)
# Criar um cliente S3 usando a sessão
s3_client = session.client('s3')

def fetch_tmdb_data(endpoint, params):
    response = requests.get(endpoint, params=params)
    return response.json()

def fetch_movie_details(movie_id):
    url = f"{tmdb_movie_detail_endpoint}{movie_id}"
    params = {'api_key': tmdb_api_key, 'language': 'pt-BR'}
    response = requests.get(url, params=params)
    return response.json()

def save_to_s3(data, file_name):
    s3_client.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=json.dumps(data),
        ContentType='application/json'
    )

# Parâmetros para buscar os filmes da década passada, filtrados por gênero
movie_params = {
    'api_key': tmdb_api_key,
    'language': 'pt-BR',
    'sort_by': 'popularity.desc',
    'primary_release_date.gte': '2010-01-01',
    'primary_release_date.lte': '2019-12-31',
    'with_genres': '35,16'  # Filtro para Comédia (35) e Animação (16)
}

# Parâmetros para buscar as séries da década passada, filtradas por gênero
tv_params = {
    'api_key': tmdb_api_key,
    'language': 'pt-BR',
    'sort_by': 'popularity.desc',
    'first_air_date.gte': '2010-01-01',
    'first_air_date.lte': '2019-12-31',
    'with_genres': '35,16'  # Filtro para Comédia (35) e Animação (16)
}

# Buscar filmes populares da década passada
movies_data = fetch_tmdb_data(tmdb_movie_endpoint, movie_params)

# Adicionar detalhes de orçamento e receita aos filmes
for movie in movies_data.get('results', []):
    movie_details = fetch_movie_details(movie['id'])
    movie['budget'] = movie_details.get('budget')
    movie['revenue'] = movie_details.get('revenue')

# Buscar séries populares da década passada
tv_data = fetch_tmdb_data(tmdb_tv_endpoint, tv_params)

# Caminho do arquivo no S3 (incluir data atual)
date_str = datetime.now().strftime("%Y/%m/%d")
movies_file_path = f'Raw/TMDB/JSON/{date_str}/filmes_populares_decada_passada.json'
tv_file_path = f'Raw/TMDB/JSON/{date_str}/series_populares_decada_passada.json'

# Salvar dados no S3
save_to_s3(movies_data, movies_file_path)
save_to_s3(tv_data, tv_file_path)

print("Dados de filmes e séries salvos com sucesso no S3!")
