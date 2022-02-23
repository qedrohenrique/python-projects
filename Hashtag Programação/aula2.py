import pandas as pd
import plotly.express as px
###########

tabela = pd.read_csv(r"C:\Users\Pichau\Documents\Jupyter\telecom_users.csv")

### TRATAMENTO ###

## Para visualizar a tabela (Uso no jupyter)
##display(tabela)
##print(tabela.info())

##Remove Coluna com nome XXX (eixo 1 coluna, eixo 0 linha)
tabela = tabela.drop("Unnamed: 0", axis=1)

## Transforma os dados de uma coluna (string) em (float64), além disso excluí casos diferentes
## Para reconhecimento errado de dados
tabela["TotalGasto"] = pd.to_numeric(tabela["TotalGasto"], errors = "coerce")

##Exclui valores vazios
tabela = tabela.dropna(how="all", axis=1)
tabela = tabela.dropna(how="any", axis=0)

### ANALISE INICIAL ###
#Valores inteiros
print(tabela["Churn"].value_counts())
#Valores em porcentagem
print(tabela["Churn"].value_counts(normalize=True))

### ANALISE PROFUNDA ###
#x = coluna, porém colorindo de acordo com color = coluna
#para mudar cor do gráfico color_discrete_sequence=["blue", "green"]
for coluna in tabela.columns:
    grafico = px.histogram(tabela, x=coluna, color="Churn", color_discrete_sequence=["blue", "green"])
    grafico.show()