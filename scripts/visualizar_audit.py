import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1. Carregar o dataset final
df = pd.read_csv('data/dataset_final_audit.csv')

# 2. Preparar os dados para visualização
# Para o Grupo Gama (sem crédito), o delta é NaN ou muito alto. 
# Vamos limitar o Delta para 2 dias (2880 min) para o gráfico não ficar esmagado,
# mas mantendo a proporção de quem é "mesmo dia".
df_plot = df.copy()
df_plot['delta_minutos'] = df_plot['delta_minutos'].fillna(3000) 
df_plot['Utilizou_Servico'] = df_plot['flag_utilizacao'].map({1: 'Sim', 0: 'Não'})

# 3. Configuração do Gráfico
plt.figure(figsize=(12, 7))
sns.set_theme(style="whitegrid")

# Criando o gráfico de dispersão (Scatter Plot)
plot = sns.scatterplot(
    data=df_plot, 
    x='delta_minutos', 
    y='valor_premio', 
    hue='target_auditoria', 
    style='Utilizou_Servico',
    s=100, 
    alpha=0.7,
    palette={'Alfa': '#e74c3c', 'Beta': '#f1c40f', 'Gama': '#2ecc71'}
)

# 4. Personalização técnica
plt.title('Evidência de Auditoria: SegAssist vs Crédito PF', fontsize=16, fontweight='bold')
plt.xlabel('Diferença de Tempo entre Contratos (Minutos)', fontsize=12)
plt.ylabel('Valor do SegAssist (R$)', fontsize=12)

# Adicionando uma linha vertical em 60 minutos para destacar a "Zona de Alerta"
plt.axvline(x=60, color='red', linestyle='--', alpha=0.5)
plt.text(70, 400, 'Zona de Venda Casada (< 1h)', color='red', fontweight='bold')

# Ajustando a legenda
plt.legend(title='Grupo / Utilização', bbox_to_anchor=(1.05, 1), loc='upper left')

# 5. Salvar e Mostrar
plt.tight_layout()
plt.savefig('data/evidencia_visual_auditoria.png', dpi=300)
print("Gráfico gerado com sucesso em: data/evidencia_visual_auditoria.png")
plt.show()