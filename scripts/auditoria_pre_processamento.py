import pandas as pd
import os

# 1. Carregar os dados
vendas = pd.read_csv('data/vendas_segassist.csv')
credito = pd.read_csv('data/concessao_credito.csv')

# 2. Cruzar as bases
df_final = pd.merge(vendas, credito, on='id_cliente', how='left')

# Converter datas
df_final['data_venda'] = pd.to_datetime(df_final['data_venda'])
df_final['data_liberacao_credito'] = pd.to_datetime(df_final['data_liberacao_credito'])

# 3. Calcular Delta
df_final['delta_minutos'] = (df_final['data_venda'] - df_final['data_liberacao_credito']).dt.total_seconds() / 60

# 4. Rotulagem (Garantindo o nome exato da coluna)
def classificar_auditoria(row):
    if pd.isna(row['data_liberacao_credito']):
        return 'Gama'
    elif row['delta_minutos'] <= 1440: # Mesmo dia
        return 'Alfa'
    else:
        return 'Beta'

# Criando a coluna que a IA vai buscar
df_final['target_auditoria'] = df_final.apply(classificar_auditoria, axis=1)

# 5. Salvar sobrescrevendo o arquivo anterior
caminho_saida = 'data/dataset_final_audit.csv'
df_final.to_csv(caminho_saida, index=False)

print(f"Sucesso! Arquivo {caminho_saida} criado.")
print(f"Colunas disponíveis: {df_final.columns.tolist()}")