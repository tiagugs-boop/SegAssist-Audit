import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configuração de reprodutibilidade
np.random.seed(42)
n_clientes = 2000
data_hoje = datetime(2026, 1, 1)

# --- PASSO 1: CRIAR O UNIVERSO DE CLIENTES E SEUS CONTRATOS DE CRÉDITO ---
# Simulamos que nem todo cliente SegAssist tem crédito (Grupo Gama), 
# mas a esmagadora maioria tem (Alfa e Beta).

clientes_ids = np.arange(10000, 10000 + n_clientes)
tipos_credito = ['Consignado', 'CDC', 'Antecipação Saque Aniversário', 'Crédito Pessoal']

# Datas de concessão de crédito ao longo do ano de 2025
datas_credito = [datetime(2025, 1, 1) + timedelta(days=np.random.randint(0, 365), 
                                                 hours=np.random.randint(9, 17)) 
                 for _ in range(n_clientes)]

credito_data = {
    'id_cliente': clientes_ids,
    'data_liberacao_credito': datas_credito,
    'tipo_credito': np.random.choice(tipos_credito, n_clientes)
}

df_credito_bruto = pd.DataFrame(credito_data)

# Simulando que o Grupo Gama (5%) não tem crédito no sistema
indices_gama = np.random.choice(df_credito_bruto.index, size=int(n_clientes * 0.05), replace=False)
df_credito = df_credito_bruto.drop(indices_gama).reset_index(drop=True)

# --- PASSO 2: CRIAR O DATASET DE VENDAS SEGASSIST ---
# Aqui aplicamos a lógica Alfa (80%), Beta (15%) e Gama (5%)

vendas_segassist = []

for i, id_cl in enumerate(clientes_ids):
    # Definir em qual grupo o cliente cai (para fins de geração do dado)
    sorteio = np.random.random()
    
    if sorteio < 0.80:
        classe_temp = 'Alfa'
    elif sorteio < 0.95:
        classe_temp = 'Beta'
    else:
        classe_temp = 'Gama'
        
    # Lógica de Data de Venda
    if classe_temp == 'Alfa':
        # Venda casada: Mesmo dia do crédito (se houver crédito)
        # Buscamos a data do crédito desse cliente
        dt_ref = next((d for idx, d in enumerate(datas_credito) if clientes_ids[idx] == id_cl), data_hoje)
        dt_venda = dt_ref + timedelta(minutes=np.random.randint(1, 60))
        valor_premio = 200.00 # Valor fixo disfarçado de tarifa
        
    elif classe_temp == 'Beta':
        dt_ref = next((d for idx, d in enumerate(datas_credito) if clientes_ids[idx] == id_cl), data_hoje)
        dt_venda = dt_ref + timedelta(days=np.random.randint(1, 30))
        valor_premio = np.random.choice([150.0, 250.0])
        
    else: # Gama
        dt_venda = datetime(2025, 1, 1) + timedelta(days=np.random.randint(0, 365))
        valor_premio = np.random.choice([150.0, 300.0, 450.0])

    # Cálculo do Tempo de Exposição (Meses de contrato até hoje)
    delta_exposicao = data_hoje - dt_venda
    meses_ativo = max(1, delta_exposicao.days // 30)
    
    # --- PASSO 3: REFINAMENTO DA FLAG_UTILIZACAO (PROBABILIDADE PONDERADA) ---
    if classe_temp == 'Gama':
        # 20% ao ano -> 1.6% ao mês
        prob = (0.20 / 12) * meses_ativo
    elif classe_temp == 'Beta':
        # 8% ao ano -> 0.6% ao mês
        prob = (0.08 / 12) * meses_ativo
    else: # Alfa
        # Flat 2% independente do tempo (cliente não sabe que tem)
        prob = 0.02
        
    flag_uso = np.random.choice([1, 0], p=[min(prob, 1.0), 1 - min(prob, 1.0)])
    
    vendas_segassist.append([id_cl, dt_venda, valor_premio, meses_ativo, flag_uso])

df_vendas = pd.DataFrame(vendas_segassist, columns=['id_cliente', 'data_venda', 'valor_premio', 'meses_ativo', 'flag_utilizacao'])

# --- PASSO 4: EXPORTAÇÃO ---
# Salvando como o "mundo real": dois arquivos que o auditor precisa cruzar
df_vendas.to_csv('data/vendas_segassist.csv', index=False)
df_credito.to_csv('data/concessao_credito.csv', index=False)

print("Datasets 'vendas_segassist.csv' e 'concessao_credito.csv' criados com sucesso.")
print(f"Total SegAssist: {len(df_vendas)}")
print(f"Total Crédito: {len(df_credito)}")