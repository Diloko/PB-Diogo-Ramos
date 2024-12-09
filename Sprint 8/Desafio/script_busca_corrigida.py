import boto3
import json
import requests
from datetime import datetime

# Configurações do TMDB
tmdb_api_key = '8bde01dd9413e23e4f16b774e6057f98'
tmdb_movie_endpoint = 'https://api.themoviedb.org/3/discover/movie'
tmdb_movie_detail_endpoint = 'https://api.themoviedb.org/3/movie/'

# Configurações do S3
profile_name = 'DiogoRamos'  # Substitua com o nome do seu perfil configurado
bucket_name = 'data-lake-diogo'

# Criar uma sessão usando o perfil configurado
session = boto3.Session(profile_name=profile_name)
# Criar um cliente S3 usando a sessão
s3_client = session.client('s3')

def fetch_tmdb_data(endpoint, params):
    all_results = []
    for page in range(1, 6):  # Buscar até 5 páginas
        params['page'] = page
        response = requests.get(endpoint, params=params)
        data = response.json()
        if 'results' in data:
            all_results.extend(data['results'])
        else:
            break
    return all_results

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

# Parâmetros para buscar animações da década passada
animation_params = {
    'api_key': tmdb_api_key,
    'language': 'pt-BR',
    'sort_by': 'popularity.desc',
    'primary_release_date.gte': '2010-01-01',
    'primary_release_date.lte': '2019-12-31',
    'with_genres': '16'  # Filtro para Animação (16)
}

# Parâmetros para buscar comédias da década passada
comedy_params = {
    'api_key': tmdb_api_key,
    'language': 'pt-BR',
    'sort_by': 'popularity.desc',
    'primary_release_date.gte': '2010-01-01',
    'primary_release_date.lte': '2019-12-31',
    'with_genres': '35',  # Filtro para Comédia (35)
    'without_genres': '16'  # Exclui Animação (16)
}

# Buscar animações populares da década passada
animations_data = fetch_tmdb_data(tmdb_movie_endpoint, animation_params)

# Adicionar detalhes de orçamento e receita às animações
for movie in animations_data:
    movie_details = fetch_movie_details(movie['id'])
    movie['budget'] = movie_details.get('budget')
    movie['revenue'] = movie_details.get('revenue')

# Buscar comédias populares da década passada que não sejam animações
comedies_data = fetch_tmdb_data(tmdb_movie_endpoint, comedy_params)

# Adicionar detalhes de orçamento e receita às comédias
for movie in comedies_data:
    movie_details = fetch_movie_details(movie['id'])
    movie['budget'] = movie_details.get('budget')
    movie['revenue'] = movie_details.get('revenue')

# Verificar se as listas de filmes estão sendo preenchidas corretamente
print(f"Total de animações encontradas: {len(animations_data)}")
print(f"Total de comédias não animadas encontradas: {len(comedies_data)}")

# Caminho do arquivo no S3 (incluir data atual)
date_str = datetime.now().strftime("%Y/%m/%d")
movies_animacoes_file_path = f'Raw/TMDB/JSON/{date_str}/filmes_animacoes_decada_passada.json'
movies_comedias_file_path = f'Raw/TMDB/JSON/{date_str}/filmes_comedias_decada_passada.json'

# Verificar se os dados estão corretos antes de enviar ao S3
print(f"Primeiro filme de animação: {json.dumps(animations_data[0], indent=4)}") if animations_data else print("Nenhuma animação encontrada.")
print(f"Primeira comédia não animada: {json.dumps(comedies_data[0], indent=4)}") if comedies_data else print("Nenhuma comédia não animada encontrada.")

# Salvar dados no S3
save_to_s3(animations_data, movies_animacoes_file_path)
save_to_s3(comedies_data, movies_comedias_file_path)

print("Dados de filmes salvos com sucesso no S3!")
