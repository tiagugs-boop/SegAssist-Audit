# Auditoria de Conformidade: Projeto SegAssist

Este projeto utiliza Machine Learning (Random Forest) para identificar padrões de venda casada no produto SegAssist (Seguro de Assistência), correlacionando o tempo de contratação com a taxa de utilização.

## Estrutura do Projeto
- `scripts/`: Códigos Python para geração, processamento e modelagem.
- `data/`: Local para armazenamento dos datasets (arquivos .csv ignorados no git).

## Como Executar
1. Instale as dependências: `pip install pandas scikit-learn seaborn matplotlib`
2. Execute os scripts na ordem:
   - `python scripts/gerar_datasets.py`
   - `python scripts/auditoria_processamento.py`
   - `python scripts/treinar_modelo_audit.py`