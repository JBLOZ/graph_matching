import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np




baseline_rs = pd.read_csv("./baseline_results.csv")
enhanced_rs = pd.read_csv("./enhanced_results.csv")

knn3_rs = pd.read_csv("./enhanced_knn3_results.csv")
knn5_rs = pd.read_csv("./enhanced_knn5_results.csv")
knn7_rs = pd.read_csv("./enhanced_knn7_results.csv")

duck_weight_sensitivity_rs = pd.read_csv("./duck_weight_sensitivity_results.csv")


# Extraer el valor de Mean_Accuracy para 'duck' en baseline
baseline_duck = baseline_rs[baseline_rs['Category'] == 'duck']['Mean_Accuracy'].iloc[0]


# Inicializar las listas de etiquetas y valores
x_labels = []
y_values = []



# Añadir resultados de KNN para duck


# Añadir los resultados de enhanced según la sensibilidad de pesos
for idx, row in duck_weight_sensitivity_rs.iterrows():
    if row["Weight_Combination"] == '(1, 0, 0)':
        x_labels.append('Baseline (1, 0, 0)')
        y_values.append(row['Mean_Accuracy'])
        continue
    x_labels.append(f"Enhanced {row['Weight_Combination']}")
    y_values.append(row['Mean_Accuracy'])

# Crear el gráfico de barras con una paleta de colores
plt.figure(figsize=(12, 6))
colors = sns.color_palette("viridis", len(x_labels))
bars = plt.bar(x_labels, y_values, color=colors)

plt.ylabel('Mean Accuracy')
plt.title('Comparación de Mean Accuracy para Patos')
plt.xticks(rotation=25)

# Ajustar el límite del eje Y para que quede más espacio sobre la barra más alta
y_min = min(y_values) - 0.01
y_max = max(y_values) + 0.03  # Sube el valor superior para más espacio
plt.ylim(y_min, y_max)

plt.grid(axis='y', alpha=0.7)
plt.tight_layout()

# Agregar etiquetas de valor sobre cada barra
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.005, f'{yval:.3f}', 
             ha='center', va='bottom')

plt.savefig('mean_accuracy_comparison_duck.svg')

plt.close()


# Extraer la desviación estándar para 'duck' en baseline
baseline_duck_std = baseline_rs[baseline_rs['Category'] == 'duck']['Std_Deviation'].iloc[0]


# Inicializar las listas de etiquetas (x_labels) y valores (y_values)
x_labels = []
y_values = []




# Añadir los resultados de sensitivity de pesos (std dev) para el método enhanced
for idx, row in duck_weight_sensitivity_rs.iterrows():
    if row["Weight_Combination"] == '(1, 0, 0)':
        x_labels.append('Baseline (1, 0, 0)')
        y_values.append(row['Std_Deviation'])
        continue
    x_labels.append(f"Enhanced {row['Weight_Combination']}")
    y_values.append(row['Std_Deviation'])

# Crear el gráfico de barras con una paleta de colores
plt.figure(figsize=(12, 6))
colors = sns.color_palette("viridis", len(x_labels))
bars = plt.bar(x_labels, y_values, color=colors)

plt.ylabel('Std Deviation')
plt.title('Comparación de Std Deviation para Patos')
plt.xticks(rotation=25)

# Ajustar el límite del eje Y para que quede más espacio
y_min = min(y_values) - 0.01
# La desviación estándar no puede ser negativa, así que forzamos a 0 si min(y_values) < 0
if y_min < 0:
    y_min = 0
y_max = max(y_values) + 0.01
plt.ylim(y_min, y_max)

plt.grid(axis='y', alpha=0.7)
plt.tight_layout()

# Agregar etiquetas de valor sobre cada barra
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.001, f'{yval:.3f}', 
             ha='center', va='bottom')


plt.savefig('mean_std_comparison_duck.svg')
plt.close()

# Agrupar dataframes y sus etiquetas
dfs = [baseline_rs, enhanced_rs, knn3_rs, knn5_rs, knn7_rs]
labels = ["Baseline", "Enhanced", "KNN3", "KNN5", "KNN7"]

# Usar seaborn para definir paletas: Pastel para barras
colors = sns.color_palette("deep6", 5)

# Suponiendo que las categorías están en el mismo orden en cada CSV
categories = baseline_rs["Category"].tolist()

# Configuración de las posiciones y ancho de las barras
x = np.arange(len(categories))  # posiciones para las 5 categorías
width = 0.15                   # ancho de cada sub-barra

def adjust_ylim(values, factor=1.5):
    """Calcula límites y ajusta para ampliar la diferencia entre el más bajo y el más alto.
       factor > 1 amplifica la diferencia."""
    min_val = min(values)
    max_val = max(values)
    diff = max_val - min_val
    new_range = diff * factor
    pad = (new_range - diff) / 2
    return min_val - pad, max_val + pad

# --- Plot para Mean Accuracy ---
all_accuracies = [val for df in dfs for val in df["Mean_Accuracy"].tolist()]
ylim_lower, ylim_upper = adjust_ylim(all_accuracies, factor=1.5)

fig, ax = plt.subplots(figsize=(10, 6))
for i, (df, label) in enumerate(zip(dfs, labels)):
    accuracies = df["Mean_Accuracy"].tolist()
    offset = (i - 2) * width  # centra las barras: índices -2, -1, 0, 1, 2
    ax.bar(x + offset, accuracies, width, label=label, color=colors[i])

ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.set_xlabel("Categoría")
ax.set_ylabel("Mean Accuracy")
ax.set_title("Comparación de accuracy media por Categoría ")
ax.set_ylim(ylim_lower, ylim_upper)
ax.legend()
plt.tight_layout()
plt.savefig("mean_accuracy_comparison.svg")
plt.close()

fig, ax = plt.subplots(figsize=(10, 6))
for i, (df, label) in enumerate(zip(dfs, labels)):
    std_devs = df["Std_Deviation"].tolist()
    offset = (i - 2) * width
    ax.bar(x + offset, std_devs, width, label=label, color=colors[i])

ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.set_xlabel("Categoría")
ax.set_ylabel("Std Deviation")
ax.set_title("Comparación de dseviacion por categoría ")
ax.legend()
plt.tight_layout()
plt.savefig("mean_std_comparison.svg")
plt.close()