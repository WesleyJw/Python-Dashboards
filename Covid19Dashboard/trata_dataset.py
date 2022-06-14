import pandas as pd

# Lendo todas as bases de Dados
dados20_1 = pd.read_csv(
    "/home/wesley/Downloads/DatasetsTutorials/DashboardsDatas/Dataset/HIST_PAINEL_COVIDBR_2020_Parte1_13jun2022.csv", sep=";")
dados20_2 = pd.read_csv(
    "/home/wesley/Downloads/DatasetsTutorials/DashboardsDatas/Dataset/HIST_PAINEL_COVIDBR_2020_Parte2_13jun2022.csv", sep=";")
dados21_1 = pd.read_csv(
    "/home/wesley/Downloads/DatasetsTutorials/DashboardsDatas/Dataset/HIST_PAINEL_COVIDBR_2021_Parte1_13jun2022.csv", sep=";")
dados21_2 = pd.read_csv(
    "/home/wesley/Downloads/DatasetsTutorials/DashboardsDatas/Dataset/HIST_PAINEL_COVIDBR_2021_Parte2_13jun2022.csv", sep=";")
dados22_1 = pd.read_csv(
    "dataset/HIST_PAINEL_COVIDBR_2022_Parte1_13jun2022.csv", sep=";")

# Merge em todas as bases

dados = pd.concat([dados20_1, dados20_2, dados21_1, dados21_2, dados22_1])


# Separa dados por estado
estados = dados[(~dados["estado"].isna()) & (dados["codmun"].isna())]
estados.to_csv("dataset/dados_estaduais_covid_19.csv", index=False)

# Separa para o Brasil

brasil = dados[dados["regiao"] == "Brasil"]
brasil.to_csv("dataset/dados_brasil_covid_19.csv", index=False)
