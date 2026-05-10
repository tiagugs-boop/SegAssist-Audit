import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# 1. Carregar o dataset que o auditor processou
df = pd.read_csv('data/dataset_final_audit.csv')

# 2. Seleção de Variáveis (Features)
# Importante: Não incluímos datas diretamente, mas sim os valores derivados (delta, meses, valor)
features = ['valor_premio', 'meses_ativo', 'delta_minutos', 'flag_utilizacao']

# Como o Delta pode ser NaN para o Grupo Gama (sem crédito), preenchemos com um valor alto
# para indicar que não há proximidade temporal com nenhum crédito.
df['delta_minutos'] = df['delta_minutos'].fillna(999999)

X = df[features]
y = df['target_auditoria']

# 3. Divisão em Treino e Teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

from sklearn.model_selection import cross_val_score

# ... (mantenha o código anterior até a criação do modelo) ...

# 4. Criação do Modelo
modelo = RandomForestClassifier(n_estimators=100, random_state=42)

# --- VALIDAÇÃO CRUZADA (5-Fold Cross Validation) ---
# O modelo será treinado e testado 5 vezes em partes diferentes dos dados
scores = cross_val_score(modelo, X, y, cv=5)

print("\n--- RESULTADOS DA VALIDAÇÃO CRUZADA ---")
print(f"Scores de cada rodada: {scores}")
print(f"Média de Precisão: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")
print("-" * 40)

# 4.5. Treino Final 
modelo.fit(X_train, y_train)

# 5. Avaliação do Modelo
y_pred = modelo.predict(X_test)

print("--- RELATÓRIO DE CLASSIFICAÇÃO DA AUDITORIA ---")
print(classification_report(y_test, y_pred))

# 6. Importância das Variáveis (O que mais "denuncia" a venda casada?)
importancias = pd.DataFrame({'feature': features, 'importancia': modelo.feature_importances_})
print("\n--- IMPORTÂNCIA DAS VARIÁVEIS NA DETECÇÃO ---")
print(importancias.sort_values(by='importancia', ascending=False))

# 7. Conclusão de Governança
print("\nNota de Auditoria:")
print("Se a precisão para o grupo 'Alfa' for alta, o modelo confirma que a simultaneidade")
print("da venda (delta_minutos) está intrinsecamente ligada à baixa utilização (flag_utilizacao).")