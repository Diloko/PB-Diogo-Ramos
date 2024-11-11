import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

profile_name = 'DiogoRamos'

bucket_name = 'data-lake-diogo'
csv_file_name1 = 'movies.csv'
csv_file_name2 = 'series.csv'

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

        s3.upload_file(csv_file_name1, bucket_name, caminho_arquivo1)
        print(f'Arquivo {csv_file_name1} enviado com sucesso para o bucket {bucket_name}, caminho {caminho_arquivo1}!')

        s3.upload_file(csv_file_name2, bucket_name, caminho_arquivo2)
        print(f'Arquivo {csv_file_name2} enviado com sucesso para o bucket {bucket_name}, caminho {caminho_arquivo2}!')
    except NoCredentialsError:
        print("Credenciais não encontradas. Verifique se o perfil foi configurado corretamente.")
    except PartialCredentialsError:
        print("Configuração de credenciais incompleta. Por favor, verifique suas credenciais.")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'AccessDenied':
            print("Acesso negado. Verifique suas permissões e a política do bucket.")
        else:
            print(f"Erro ao enviar o arquivo: {e}")

criar_bucket()
enviar_arquivos()
