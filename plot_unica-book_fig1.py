# -*- coding: utf-8 -*-

__author__      = "Leidinice Silva"
__email__       = "leidinicesilva@gmail.com"
__date__        = "Dec 04, 2024"
__description__ = "Script to plot textbook figures"

import matplotlib.pyplot as plt

# Dados fictícios de classificação de Köppen para regiões do Brasil
regions = [
    "Amazônia (Af)", 
    "Nordeste (BSh)", 
    "Centro-Oeste (Aw)", 
    "Sul (Cfa)", 
    "Sudeste (Cwb)"
]
precipitation = [2200, 700, 1400, 1600, 1500]  # mm anuais
temperature = [27, 28, 26, 17, 20]  # °C médios anuais

# Criando gráfico
fig, ax1 = plt.subplots(figsize=(10, 6))

color = 'tab:blue'
ax1.set_xlabel('Região do Brasil')
ax1.set_ylabel('Precipitação anual (mm)', color=color)
ax1.bar(regions, precipitation, color=color, alpha=0.6, label='Precipitação')
ax1.tick_params(axis='y', labelcolor=color)
plt.xticks()

# Segundo eixo para temperatura
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Temperatura média anual (°C)', color=color)
ax2.plot(regions, temperature, color=color, marker='o', label='Temperatura')
ax2.tick_params(axis='y', labelcolor=color)

plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('classificação_climática_Köppen.png', dpi=300)
plt.show()

