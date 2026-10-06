import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Pokemon_full.csv")                #Ler o CSV

fig, axes = plt.subplots(2, 2, figsize=(14, 10))    #Criar um plot com 4 subplots


# ============================================================
# 1 - Distribuição do Attack
# ============================================================

axes[0, 0].hist(                #.hist cria um histograma
    df["attack"],               #lê a coluna que quero trabalhar
    bins=30,                    #número de barras que eu quero
    color="#0f939cff",        #cor das barras, está em hexadecimal, mas dá pra ser apenas "blue"
    edgecolor="black"           #cor do contorno das barras
)

axes[0, 0].set_title("Distribuição do Attack")
axes[0, 0].set_xlabel("Attack")
axes[0, 0].set_ylabel("Frequência")

# ============================================================
# 2 - Distribuição do HP e Defense
# ============================================================

axes[0, 1].hist(
    df["hp"],
    bins=30,
    color="#f60202ff",
    edgecolor="black",
    alpha=0.5,               # transparência
    label="HP"
)

axes[0, 1].hist(
    df["defense"],
    bins=30,
    color="#000ecc",
    edgecolor="black",
    alpha=0.5,
    label="Defense"
)

axes[0, 1].set_title("Distribuição de HP e Defense")
axes[0, 1].set_xlabel("Valor do atributo")
axes[0, 1].set_ylabel("Frequência")

axes[0, 1].legend()

# ============================================================
# 3 - Número de Pokémon por tipo primário
# ============================================================

numero_por_tipo = df["type"].value_counts()

axes[1, 0].bar(                 # .bar cria um gráfico de barras
    numero_por_tipo.index,
    numero_por_tipo.values,
    color="#176a00ff",
    edgecolor="black"
)

axes[1, 0].set_title("Número de Pokémon por Tipo Primário")
axes[1, 0].set_xlabel("Tipo")
axes[1, 0].set_ylabel("Número de Pokémon")

axes[1, 0].tick_params(
    axis="x",
    rotation=45
)


# ============================================================
# 4 - Attack x Defense
# ============================================================

axes[1, 1].scatter(         #.scatter cria um gráfico de dispersão.
    df["attack"],           #eixo x
    df["defense"],          #eixo y
    color="#aa00a5ff",
    alpha=0.5              
)

axes[1, 1].set_title("Attack × Defense")
axes[1, 1].set_xlabel("Attack")
axes[1, 1].set_ylabel("Defense")

plt.tight_layout()      #Isso aqui serve para ajustar o espaçmento entre os gráficos.

plt.show()              #Mostrar a imagem