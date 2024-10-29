import boto3
import pandas as pd
from io import StringIO
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

profile_name = 'DiogoRamos'
bucket_name = 'desafio-sprint5-diogo'
csv_file_name = 'estado-de-residencia-do-declarante.csv'

session = boto3.Session(profile_name=profile_name, region_name='us-east-1')
s3 = session.client('s3')

def ler_csv_do_s3():
    try:
        csv_obj = s3.get_object(Bucket=bucket_name, Key=csv_file_name)
        body = csv_obj['Body'].read().decode('utf-8')

        df = pd.read_csv(StringIO(body), delimiter=';')
        return df
    except NoCredentialsError:
        print("Credenciais não encontradas. Verifique se o perfil foi configurado corretamente.")
    except PartialCredentialsError:
        print("Configuração de credenciais incompleta. Por favor, verifique suas credenciais.")
    except ClientError as e:
        print(f"Erro ao ler o arquivo do S3: {e}")
        return None

def converter_tipos(df, colunas):
    for coluna in colunas:
        df[coluna] = pd.to_numeric(df[coluna], errors='coerce').fillna(0)
    return df

def salvar_e_enviar_csv(df, nome_arquivo):
    if df is not None and not df.empty:
        try:
            df.to_csv(nome_arquivo, index=False)
            s3.upload_file(nome_arquivo, bucket_name, nome_arquivo)
            print(f'Arquivo {nome_arquivo} enviado com sucesso para o bucket {bucket_name}!')
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
    else:
        print("Dataframe está vazio, não há nada para salvar e enviar.")

df = ler_csv_do_s3()

colunas_para_converter = [
    'Quantidade de Declarantes', 
    'Rendimentos Tributáveis', 
    'Ano-Calendário', 
    'Imposto Devido Total', 
    'Imposto Pago'
]

df = converter_tipos(df, colunas_para_converter)

print("Dados iniciais:")
print(df.head())

def manipulacao1(df):
    df1_filtered = df[(df['Ano-Calendário'] > 2019) & (df['Rendimentos Tributáveis'] < 2824)]
    return df1_filtered

def manipulacao2(df):
    df2_agg = df.groupby('Ano-Calendário').agg({
        'Doações Efetuadas': 'sum', 
        'Rendimentos Tributáveis': 'mean',
        'Imposto Devido Total': 'sum',
        'Imposto Pago': 'sum'
    })
    return df2_agg

def manipulacao3(df):
    df3 = df.copy()
    df3['Receita Imposto'] = df3.apply(
        lambda row: 'Déficit' if row['Imposto Devido Total'] > row['Imposto Pago'] else (
            'Superávit' if row['Imposto Devido Total'] < row['Imposto Pago'] else 'Igual'
        ), axis=1
    )
    return df3

def manipulacao4(df):
    df4 = df.copy()
    df4['Estado'] = df4['Estado'].str.upper()
    return df4

def manipulacao5(df):
    df5 = df.copy()
    df5['Quantidade de Declarantes'] = df5['Quantidade de Declarantes'].astype(float)
    return df5

df1 = manipulacao1(df)
salvar_e_enviar_csv(df1, 'manipulacao1.csv')

df2 = manipulacao2(df)
salvar_e_enviar_csv(df2, 'manipulacao2.csv')

df3 = manipulacao3(df)
salvar_e_enviar_csv(df3, 'manipulacao3.csv')

df4 = manipulacao4(df)
salvar_e_enviar_csv(df4, 'manipulacao4.csv')

df5 = manipulacao5(df)
salvar_e_enviar_csv(df5, 'manipulacao5.csv')