import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

profile_name = 'DiogoRamos'

bucket_name = 'desafio-sprint5-diogo'
csv_file_name = 'estado-de-residencia-do-declarante.csv'

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

def enviar_arquivo():
    try:
        s3.upload_file(csv_file_name, bucket_name, csv_file_name)
        print(f'Arquivo {csv_file_name} enviado com sucesso para o bucket {bucket_name}!')
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
enviar_arquivo()
