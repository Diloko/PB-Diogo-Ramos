import boto3
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

profile_name = 'DiogoRamos'

bucket_name = 'data-lake-diogo'
csv_file_name1 = 'app/movies.csv' 
csv_file_name2 = 'app/series.csv' 

session = boto3.Session(profile_name=profile_name, region_name='us-east-1')

s3 = session.client('s3')

def criar_bucket():
    try:
        s3.create_bucket(Bucket=bucket_name)
        print(f'Bucket {bucket_name} criado com sucesso!')
    except s3.exceptions.BucketAlreadyExists:
        print(f'O bucket {bucket_name} já existe. Continuando com o upload.')
    except s3.exceptions.BucketAlreadyOwnedByYou:
        print(f'Você já possui o bucket {bucket_name}. Continuando com o upload.')
    except NoCredentialsError:
        print("Credenciais não encontradas. Verifique se o perfil foi configurado corretamente.")
    except PartialCredentialsError:
        print("Configuração de credenciais incompleta. Por favor, verifique suas credenciais.")
    except Exception as e:
        print(f"Erro ao criar o bucket: {e}")

def enviar_arquivos():
    try:
        caminho_arquivo1 = 'Raw/Local/CSV/Movies/2024/11/10/movies.csv'
        caminho_arquivo2 = 'Raw/Local/CSV/Series/2024/11/10/series.csv'

        current_directory = os.getcwd()
        print("Diretório de trabalho atual:", current_directory)

        arquivos_no_diretorio = os.listdir(current_directory)
        print("Arquivos no diretório atual:", arquivos_no_diretorio)

        abs_csv_file_name1 = os.path.join(current_directory, csv_file_name1)
        abs_csv_file_name2 = os.path.join(current_directory, csv_file_name2)

        print("Caminho absoluto de movies.csv:", abs_csv_file_name1)
        print("Caminho absoluto de series.csv:", abs_csv_file_name2)

        if os.path.isfile(abs_csv_file_name1) and os.path.isfile(abs_csv_file_name2):
            s3.upload_file(abs_csv_file_name1, bucket_name, caminho_arquivo1)
            print(f'Arquivo {csv_file_name1} enviado com sucesso para o bucket {bucket_name}, caminho {caminho_arquivo1}!')

            s3.upload_file(abs_csv_file_name2, bucket_name, caminho_arquivo2)
            print(f'Arquivo {csv_file_name2} enviado com sucesso para o bucket {bucket_name}, caminho {caminho_arquivo2}!')
        else:
            print(f"Erro: os arquivos '{csv_file_name1}' e/ou '{csv_file_name2}' não foram encontrados no diretório especificado.")
    except NoCredentialsError:
        print("Credenciais não encontradas. Verifique se o perfil foi configurado corretamente.")
    except PartialCredentialsError:
        print("Configuração de credenciais incompleta. Por favor, verifique suas credenciais.")
    except FileNotFoundError as e:
        print(f"Erro: {e}. Verifique se os arquivos '{csv_file_name1}' e '{csv_file_name2}' existem no diretório especificado.")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'AccessDenied':
            print("Acesso negado. Verifique suas permissões e a política do bucket.")
        else:
            print(f"Erro ao enviar o arquivo: {e}")

criar_bucket()
enviar_arquivos()
