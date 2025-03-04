## Jordi Blasco Lozano

### Informe de Prácticas: Técnicas de Algoritmos de Búsqueda

## Índice

1. [Introducción](#introducción)
2. [DataLoader](#dataloader)
3. [Visualización de Imágenes y Keypoints - Parte 1](#visualización-de-imágenes-y-keypoints---parte-1)
4. [Visualización de Imágenes y Keypoints - Parte 2](#visualización-de-imágenes-y-keypoints---parte-2)
   1. [Triangulación de Delaunay](#triangulación-de-delaunay)
   2. [Grafos K-NN (K vecinos más cercanos)](#grafos-knn-k-vecinos-más-cercanos)
5. [Generación de Grafos Matcheados - Parte 1](#generación-de-grafos-matcheados---parte-1)
6. [Generación de Grafos Matcheados - Parte 2](#generación-de-grafos-matcheados---parte-2)
7. [Conclusiones sobre los resultados obtenidos](#conclusiones-sobre-los-resultados-obtenidos)
   1. [Experimentos 1 y 2](#experimentos-1-y-2)
   2. [Experimento 3](#experimento-3)
   3. [Experimento 4](#experimento-4)

## Introducción

El objetivo de esta práctica ha sido profundizar en técnicas de algoritmos de búsqueda aplicadas al problema de correspondencia de grafos (graph matching). El trabajo se ha centrado principalmente en la visualización, construcción y matching de grafos basados en puntos clave (keypoints) de imágenes del conjunto de datos Willow-ObjectClass.

Este conjunto de datos contiene imágenes de cinco categorías (car, duck, face, motorbike y winebottle), cada una con sus keypoints específicos. El objetivo principal ha sido implementar y comparar diferentes algoritmos para establecer correspondencias entre keypoints de pares de imágenes, evaluando su precisión y rendimiento.

He estructurado el trabajo en varios módulos, dentro del directorio principal del programa encontramos las subcarpetas `archivos` y `results` y los notebooks de cada bloque requerido. Todo esto se detalla más adelante.

## DataLoader

Para facilitar el trabajo con los datos, decidí crear una clase externa llamada `DataLoader` que se encarga de leer y organizar todas las carpetas de datos, se encuentra dentro de la carpeta `arhivos`. Esta clase itera sobre la carpeta de `WILLOW-ObjectClass` y busca imágenes `.png` junto con sus correspondientes archivos `.mat` de keypoints. Guarda los paths de estas imagenes y keypoints en un diccionario que luego se usa para generar cada dataset de cada categoría, por ultimo estos datasets se guardan en un diccionario en el que la `key` es la categoria en minusculas y el `valor` el dataset con los paths de la categoría correspondiente, la función `load_data` se encarga de devolver este diccionario.

Esta clase evita la duplicación de código y proporciona un acceso facil a todos los datos.

## Visualización de Imágenes y Keypoints - Parte 1

El objetivo de esta primera parte de la práctica fue la visualización básica de las imágenes y sus keypoints. Cargué las imágenes y sus correspondientes keypoints. Redimensioné todas las imágenes a un tamaño uniforme de 256x256 píxeles. Ajusté las coordenadas de los keypoints para mantener su correspondencia con las imágenes redimensionadas. Finalmente visualicé los conjuntos de 8 imágenes aleatorias por categoria en grids de 2x4 con sus respectivos keypoints superpuestos

La función `load_img_and_keypoints_from_row` resultó super útil, ya que abstrae todo el proceso de carga y redimensionamiento, permitiéndome reutilizarla en las siguientes partes de la práctica. Al repetirla tantas veces en las partes de la práctica posteriores, me aprendí de memoria como buscar y redimensionar las imágenes, ajustar los keypoints y devolver todo redimensionado.

## Visualización de Imágenes y Keypoints - Parte 2

En esta segunda parte de la visualización se basaba en la construcción de grafos a partir de los keypoints. Para esto usamos dos métodos diferentes:

### Triangulación de Delaunay

La triangulación de Delaunay es una técnica geométrica que conecta puntos formando triángulos uniformes dentro de un grafo. Decidí implementar este método en su forma más primitiva, sin utilizar libreria Delaunay. Esto lo hice para entender mejor su funcionamiento desde el más bajo nivel. La función usaba 3 bucles anidados para iterar sobre todos los puntos y comprobar si formaban un triángulo válido. Realmente pensaba que iba a ser más dificil de implementar, estos puntos en los que iteraban los bucles hacian operaciones matemáticas sencillas como calcular la distancia entre dos puntos, comprobar si un punto estaba dentro de un triángulo, incluir en una lista los puntos validos, etc.

- pd(for ahmed): Este método creo que se usa mucho en tecnicas de reescalado de objetos 3D, generación de mallas en blender, etc. Supongo que existirán varias tecnicas de triangulación, no se si conoces Nanite, pero creo que es la tecnica de triangulación más avanzada para objetos 3D que existe actualmente. La usaba hace tiempo cuando hacia algún que otro juego en Unreal Engine 5.

### Grafos K-NN (K vecinos más cercanos)

Este otro tipo de técnica de triangulación se basa en la construcción de grafos K-NN, donde cada punto se conecta con sus K vecinos más cercanos. Esta función es bastante más sencilla que la triangulación de Delaunay, simplemente calcula las distancias entre todos los puntos y selecciona los K más cercanos, cuantos mas K más conexiones se generan. Esto se puede ver con los valores K (3, 5 y 7) que tomé para cada categoría de imagen, lo que permitió observar cómo la densidad de conexiones afecta a la estructura del grafo resultante.

La visualización de ambos métodos nos permite compararlos y entender sus diferencias: mientras que Delaunay genera una triangulación uniforme, K-NN tiende a crear más conexiones en áreas donde los puntos están más concentrados.

## Generación de Grafos Matcheados - Parte 1

Esta parte de la practica tenía como objetivo generar las correspondencias entre pares de grafos utilizando los grafos construidos anteriormente. El objetivo es encontrar qué keypoints de una imagen se corresponden con los de otra imagen de la misma categoría.

En esta parte he implementado tres funciones de `carga y plotteo de imagenes`, la función de `triangulacion Delunay`, para visualizar las triangulaciones de las imagenes, la función de `matching` con el uso del algoritmo húngaro que realiza un matching basandose en las distancias euclidianas entre los keypoints y finalmente las funciones que evaluan y generan las precisiones del matching para todas las categorías de imágenes.

Indagaré un poco más en las tres funciones de carga y plotteo de imagenes y kaypoints. `Load_img_and_keypoints_from_row` genera las imagenes y keypoints redimensionados y triangulados, esta nos va a servir solamente para visualizar las imagenes y keypoints de las categorias. Para hacer los matchings finales con el algoritmo húngaro, se usará la función de `load_keypoints_from_row` que solamente tiene en cuenta los keypoints de las imagenes ya que el algoritmo húngaro solo necesita los keypoints para hacer el matching, esto hará nuestro codigo más eficiente que si solo usaramos la función de `load_img_and_keypoints_from_row`. Finalmente, usaremos la función de `visualize_combined` que nos generará la visualización de las imagenes con los grafos

## Generación de Grafos Matcheados - Parte 2

En esta parte veremos las diferencias entre los métodos de triangulación de Delaunay y K-NN en el matching de grafos, también se compararán todos los resultados obtenidos con cada tipo de matching y en si veremos cual es el mejor método para el matching de grafos. También veremos algunos problemas que he tenido y como creo que se podrian solucionar. Cargaremos primero todos los datos de los resultados de los matchings, luego visualizaremos en forma de gráficas y tablas estos resultados y finalmente veremos las conclusiones de los resultados obtenidos.

baseline_rs


|   | Category   | Mean_Accuracy | Std_Deviation | Number_of_Pairs |
| -: | :--------- | ------------: | ------------: | --------------: |
| 0 | car        |        0.7118 |        0.3007 |             780 |
| 1 | duck       |        0.6753 |        0.2878 |            1225 |
| 2 | face       |        0.8452 |        0.1879 |            5886 |
| 3 | motorbike  |        0.8265 |        0.2302 |             780 |
| 4 | winebottle |        0.8826 |        0.1792 |            2145 |

enhanced_rs


|   | Category   | Mean_Accuracy | Std_Deviation | Number_of_Pairs |
| -: | :--------- | ------------: | ------------: | --------------: |
| 0 | car        |         0.653 |        0.3159 |              66 |
| 1 | duck       |        0.7909 |        0.2586 |              66 |
| 2 | face       |        0.8511 |        0.2031 |              66 |
| 3 | motorbike  |        0.9091 |        0.1433 |              66 |
| 4 | winebottle |        0.8939 |        0.1402 |              66 |

knn3_rs


|   | Category   | Mean_Accuracy | Std_Deviation | Number_of_Pairs |
| -: | :--------- | ------------: | ------------: | --------------: |
| 0 | car        |        0.6545 |        0.3271 |              66 |
| 1 | duck       |        0.7727 |        0.2694 |              66 |
| 2 | face       |        0.7871 |        0.2094 |              66 |
| 3 | motorbike  |         0.903 |        0.1435 |              66 |
| 4 | winebottle |        0.9303 |        0.1231 |              66 |

knn5_rs


|   | Category   | Mean_Accuracy | Std_Deviation | Number_of_Pairs |
| -: | :--------- | ------------: | ------------: | --------------: |
| 0 | car        |        0.6773 |        0.3237 |              66 |
| 1 | duck       |        0.7742 |        0.2653 |              66 |
| 2 | face       |        0.8205 |        0.2275 |              66 |
| 3 | motorbike  |        0.9106 |        0.1372 |              66 |
| 4 | winebottle |        0.9455 |        0.0956 |              66 |

knn7_rs


|   | Category   | Mean_Accuracy | Std_Deviation | Number_of_Pairs |
| -: | :--------- | ------------: | ------------: | --------------: |
| 0 | car        |        0.6652 |        0.3296 |              66 |
| 1 | duck       |        0.7591 |        0.2685 |              66 |
| 2 | face       |        0.7871 |        0.2101 |              66 |
| 3 | motorbike  |        0.8985 |        0.1472 |              66 |
| 4 | winebottle |        0.9545 |        0.0838 |              66 |

![media](./results/mean_accuracy_comparison.svg)

![sdt](./results/mean_std_comparison.svg)

duck_weight_sensitivity_rs


|   | Weight_Combination | Mean_Accuracy | Std_Deviation | Number_of_Pairs |
| -: | :----------------- | ------------: | ------------: | --------------: |
| 0 | (0.3, 0.3, 0.4)    |        0.7427 |        0.2801 |            1225 |
| 1 | (0.3, 0.4, 0.3)    |        0.7412 |        0.2831 |            1225 |
| 2 | (0.4, 0.3, 0.3)    |        0.7389 |        0.2842 |            1225 |
| 3 | (0.5, 0.2, 0.3)    |        0.7353 |        0.2859 |            1225 |
| 4 | (0.5, 0.3, 0.2)    |        0.7293 |        0.2851 |            1225 |
| 5 | (0.6, 0.2, 0.2)    |        0.7268 |        0.2858 |            1225 |
| 6 | (1, 0, 0)          |        0.6753 |        0.2878 |            1225 |

![media](./results/mean_accuracy_comparison_duck.svg)

![desviacion](./results/mean_std_comparison_duck.svg)

## Conclusiones sobre los resultados obtenidos

### Experimentos 1 y 2

Bajo las dos primeras gráficas que corresponden a los análisis de los metodos de matching utilizados, podemos observar dos cosas. El rendimiento de los métodos con `Delunay` usando `hitting_time` y `node2vec` es superior en precisión media al metodo `baseline` en casi todas las categorias. Esta diferencia no es muy notoria, pero en el momento que comparamos las tablas de desviación vemos como el metodo `baseline` tiene una desviación estandar mucho mayor que los otros metodos. Esto nos indica que el metodo `baseline` es poco robusto a la hora de encontrar correspondencias entre grafos.

Si pasamos a las gráficas de la categoría `duck` podemos observar como el metodo `baseline` tiene una precisión media muy baja en comparación al enhanced matching. También es posible observar en estas dos gráficas como a medida que le vamos dando más peso al componente `espacial` la precisión media va disminuyendo progresivamente.

### Experimento 3

Bajo las dos primera gráficas de este experimento podemos observar como los metodos que utilizan `KNN` tienen un comportamiento similar entre si, con una precisión media muy similar en todas las categorias menos en `winebottle` donde cada vez que aumentamos el valor de `K` la precisión media aumenta.

Se supone que que KNN(3) debería de ser similar a enhanced con delunay ya que ambos métodos conectan 3 keypoints, pero esto no sucede así, si usamos enhanced con delunay obtenemos una correspondencia más alta ya que el metodo enhanced con KNN vuelve a tener en cuenta la distancia entre puntos para realizar los embeddings y el hitting time y se olvida de la topología del grafo para generar estas matrices. Entonces en los casos donde los puntos estan muy juntos, como en `winebottle` la precisión media aumenta, pero como en las demás categorias esto no sucede, la precisión media disminuye al no tener en cuenta la topología del grafo.

### Experimento 4

Como podemos observar en las dos ultimas gráficas sobre la media y la desviación estándar de las precisiones de las sensibilidades de los pesos utilizados para duck, podemos observar como la precisión media disminuye y la desviación aumenta a medida que le damos más peso al componente `espacial`. Esto nos indica que el componente `espacial` no es muy útil para encontrar correspondencias entre grafos, o al menos en la categoría `duck`.

La triangulación de Delaunay proporciona una estructura de grafo más uniforme y consistente, lo que permite a estos métodos capturar mejor las relaciones topológicas entre los keypoints, independientemente de su proximidad física. Por lo tanto, estos métodos son más robustos frente a variaciones en la distribución espacial de los puntos, lo que se refleja en una mayor precisión y menor desviación estándar en los resultados obtenidos.
