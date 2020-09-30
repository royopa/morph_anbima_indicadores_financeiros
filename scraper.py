#!/usr/bin/env python
# coding: utf-8
import os
import shutil
from datetime import datetime

import pandas as pd
import scraperwiki

import utils

os.environ['SCRAPERWIKI_DATABASE_NAME'] = 'sqlite:///data.sqlite'

utils.prepare_download_folder('bases')

url = 'https://www.anbima.com.br/informacoes/indicadores/'
df = pd.read_html(url, thousands='.', decimal=',')[2]


data_referencia = df.head(1).iloc[0][0]
data_referencia = data_referencia.split('Data e Hora da Última Atualização: ')
data_referencia = data_referencia[1].split(' - ')[0]
data_referencia = datetime.strptime(data_referencia, '%d/%m/%Y')
data_referencia

df['data_captura'] = data_referencia
df['data_captura'] = pd.to_datetime(
    df['data_captura'], errors='coerce').dt.date

df.dropna(inplace=True)

# remove o primeiro registro do dataframe
df = df.loc[1:]
df['descricao'] = df[1].copy(deep=False)
df[1] = pd.to_datetime(df[1], format="%d/%m/%Y", errors='coerce').dt.date
df[1].fillna(df['data_captura'], inplace=True)


def formata_indicador(valor, descricao):
    if valor.startswith('Estimativa SELIC'):
        return 'selic_estimativa_anbima'
    if valor.startswith('Taxa SELIC do BC2'):
        return 'selic'
    if valor.startswith('DI-CETIP3'):
        return 'cdi'
    if valor.startswith('IGP-M (') and descricao.startswith('Número Índice'):
        return 'igpm_numero_indice'
    if valor.startswith('IGP-M (') and descricao.startswith('Var % no mês'):
        return 'igpm_variacao_percentual_mes'
    if valor.startswith('IGP-M1') and descricao.startswith('Projeção'):
        return 'igpm_projecao_anbima'
    if valor.startswith('IPCA (') and descricao.startswith('Número Índice'):
        return 'ipca_numero_indice'
    if valor.startswith('IPCA (') and descricao.startswith('Var % no mês'):
        return 'ipca_variacao_percentual_mes'
    if valor.startswith('IPCA1') and descricao.startswith('Projeção'):
        return 'ipca_projecao_anbima'
    if valor.startswith('Dolar Comercial Compra'):
        return 'dolar_comercial_compra'
    if valor.startswith('Dolar Comercial Venda'):
        return 'dolar_comercial_venda'
    if valor.startswith('Euro Compra'):
        return 'euro_compra'
    if valor.startswith('Euro Venda'):
        return 'euro_venda'
    if valor.startswith('TR2'):
        return 'tr'
    if valor.startswith('TBF2'):
        return 'tbf'
    if valor.startswith('FDS4'):
        return 'fds'


df[0] = df.apply(lambda x: formata_indicador(x[0], x['descricao']), axis=1)

# renomeia e formata as colunas
df.rename(columns={0: 'indice', 1: 'data_referencia',
                   2: 'valor'}, inplace=True)

keys = [
    'data_referencia',
    'data_captura',
    'indice',
    'descricao',
    'valor'
]

df = df[keys]

# salva o arquivo de saída
file_path = os.path.join(
    'bases', f"{data_referencia.strftime('%Y%m%d')}_registros.csv")
print('Salvando resultado capturado no arquivo', file_path)
df.to_csv(file_path, index=False)

print('Iniciando importação para base de dados')

for index, row in enumerate(df.to_dict('records')):
    print('Importando', index+1, 'de', len(df), row['indice'])
    try:
        scraperwiki.sqlite.save(
            unique_keys=keys, data=row)
    except Exception as e:
        print("Error occurred:", e)

print('Importação realizada com sucesso')

# rename file
print('Renomeando arquivo sqlite')
if os.path.exists('scraperwiki.sqlite'):
    shutil.copy('scraperwiki.sqlite', 'data.sqlite')
