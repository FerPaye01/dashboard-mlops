Viabilidad, Modelado Matemático e Impacto del Prompt Caching en la Arquitectura MLOps de Osinergmin
La optimización de costos de infraestructura y la reducción de la latencia en la fase de prellenado constituyen dos de los desafíos más críticos en el despliegue de sistemas de generación aumentada por recuperación (RAG) a escala corporativa [cite: 1, 2]. Para una entidad pública como el Organismo Supervisor de la Inversión en Energía y Minería (Osinergmin) en Perú, que requiere auditar leyes, bases de licitación y términos de referencia (TDR) que superan habitualmente decenas de miles de tokens [cite: 3, 4], el reprocesamiento lineal de estos documentos estáticos representa una ineficiencia operativa insostenible [cite: 3, 5]. El mecanismo de caché de prompts (prompt caching) permite almacenar y reutilizar los tensores de claves y valores (KV cache) calculados durante las capas de atención del transformador [cite: 6, 7], evitando la recomputación de prefijos de texto idénticos entre diferentes llamadas a la interfaz de programación de aplicaciones (API) o motores de inferencia locales [cite: 6, 8]. Este reporte analiza detalladamente la viabilidad técnica, el modelado matemático del costo total de propiedad (TCO), la física temporal de la latencia y las directrices de integración para incorporar esta tecnología en el portal de decisiones MLOps de Osinergmin.
1. Estado del Arte de Prompt Caching por Proveedor de Nube
La madurez tecnológica del almacenamiento en caché de prompts ha llevado a los proveedores de frontera a adoptar esquemas de facturación, condiciones de activación y límites de persistencia temporal marcadamente diferenciados [cite: 7, 9]. Comprender estas dinámicas es esencial para estructurar las reglas de recomendación del simulador MLOps [cite: 10].
Anthropic (Claude 3.5 Sonnet y Claude 3.5 Haiku)
La arquitectura de Anthropic implementa un esquema de almacenamiento en caché explícito y controlado por el desarrollador a través de la API [cite: 11]. Para que el sistema almacene los estados de atención, es obligatorio declarar explícitamente puntos de interrupción o breakpoints utilizando el bloque de control de caché en el payload de la solicitud [cite: 11].
La estructura financiera de Anthropic penaliza la primera transacción mediante un recargo de escritura (write premium) que puede elevar de forma sustancial el costo de la llamada inicial, compensándolo posteriormente con un descuento del 90% en todas las lecturas de caché subsiguientes [cite: 9, 12]. El sistema ofrece dos políticas de tiempo de vida (TTL): una ventana por defecto de 5 minutos, cuyo costo de escritura asciende a un multiplicador de 1.25× respecto a la tarifa estándar de entrada, y una ventana extendida de 1 hora, que eleva el multiplicador de escritura a 2.0× la tarifa base [cite: 12, 13]. Las lecturas de caché, independientemente del TTL seleccionado, se facturan de manera uniforme a un multiplicador de 0.10× de la tarifa de entrada estándar [cite: 12, 13].
La activación del almacenamiento exige cumplir con umbrales de tamaño mínimo de prefijo tokens [cite: 11, 14]. Para Claude 3.5 Sonnet, el límite inferior de activación es de 1,024 tokens [cite: 14], mientras que para las versiones actualizadas Claude Sonnet 4.x se eleva a 2,048 tokens [cite: 11, 14]. En el caso de Claude 3.5 Haiku, el umbral mínimo es de 2,048 tokens [cite: 11, 14], ascendiendo a 4,096 tokens en Claude Haiku 4.5 [cite: 11, 14]. El ciclo de vida de la caché es auto-renovable: cada acierto de caché (cache hit) dentro de la ventana del TTL reinicia automáticamente el temporizador a cero sin incurrir en costos adicionales de escritura [cite: 15, 16].
OpenAI (GPT-4o y GPT-4o-mini)
A diferencia de Anthropic, OpenAI opta por un enfoque de gestión de caché completamente automatizado y transparente para el usuario final [cite: 11, 17, 18]. El motor de inferencia analiza dinámicamente las solicitudes entrantes y aplica el almacenamiento de manera oportuna si se cumplen los requisitos mínimos de coincidencia criptográfica del prefijo [cite: 8, 17, 18].
El sistema de OpenAI no aplica ningún tipo de recargo por escritura de caché, cobrando la primera llamada fría exactamente al precio base de entrada del modelo [cite: 9, 10]. Las lecturas subsecuentes que logran un acierto de caché reciben un descuento uniforme del 50% en los modelos insignia GPT-4o (reduciendo el costo de entrada de $2.50/MTok a $1.25/MTok) y GPT-4o-mini (reduciendo el costo de entrada de $0.15/MTok a $0.075/MTok) [cite: 19]. En versiones más recientes orientadas a entornos de producción, como GPT-4.1, la tasa de descuento por lectura se incrementa hasta alcanzar el 75% [cite: 17, 19, 20].
La granularidad de OpenAI está estructurada con un umbral de elegibilidad inicial de 1,024 tokens [cite: 17, 18]. Tras superar este límite mínimo, las coincidencias y aciertos de caché se calculan en incrementos o bloques fijos de 128 tokens [cite: 17, 18]. El enrutamiento de la solicitud se realiza basándose en un algoritmo de dispersión (hashing) aplicado sobre los primeros 256 tokens del prompt, lo que permite dirigir las llamadas con prefijos comunes a la misma máquina física de inferencia [cite: 17, 18]. La política de TTL de OpenAI es dinámica e interna, liberando los bloques de memoria generalmente tras un periodo de inactividad de entre 5 y 10 minutos, y garantizando la eliminación definitiva antes de cumplirse una hora del último uso [cite: 8, 18].
DeepSeek (V3 y R1)
La infraestructura de DeepSeek destaca por implementar un sistema de almacenamiento automático basado en almacenamiento distribuido rápido (disco SSD/NVMe optimizado) con un recargo nulo por creación de caché [cite: 21, 22]. El motor calcula de forma nativa los bloques de atención y gestiona de manera eficiente la persistencia bajo un modelo de mejor esfuerzo [cite: 21, 23].
Las tarifas de DeepSeek son las más bajas del sector y sus descuentos de caché resultan altamente agresivos [cite: 24, 25]. Para el modelo basado en procesamiento cognitivo complejo DeepSeek R1, la tarifa estándar de entrada fría (fallo de caché) se sitúa en $0.55/MTok, disminuyendo a $0.14/MTok en caso de acierto de caché, lo que equivale a un descuento del 74.5% [cite: 26, 27]. Para el modelo de propósito general optimizado DeepSeek V4 Flash, el costo estándar de entrada fría es de $0.14/MTok, cayendo a $0.0028/MTok ante un acierto de caché, lo que representa un descuento del 98% [cite: 21, 28].
La granularidad del sistema de DeepSeek es extremadamente fina, dividiendo y alineando el almacenamiento en caché en bloques secuenciales de solo 64 tokens [cite: 22, 29]. Esto maximiza la reutilización de datos incluso en prompts de longitud moderada [cite: 7, 29]. No se requiere configurar ninguna cabecera específica ni gestionar ciclos de vida manuales, ya que el sistema opera de manera nativa en su capa de backend [cite: 21, 29].
Google Gemini (Gemini 1.5 Pro y Gemini 1.5 Flash)
Google implementa una estrategia de almacenamiento de contexto explícita en su familia de modelos Gemini 1.5, la cual está diseñada para interactuar con ventanas de contexto masivas de hasta un millón de tokens [cite: 30, 31]. Los desarrolladores deben crear un recurso de caché persistente independiente mediante llamadas a la API de control de contenidos y luego asociar el identificador del recurso obtenido a las consultas de inferencia subsecuentes [cite: 32, 33].
Para la familia estable Gemini 1.5 Pro y Gemini 1.5 Flash, se establece un requisito de activación riguroso: el documento de contexto largo debe poseer una longitud mínima de 32,768 tokens para ser elegible para la creación de un recurso de caché [cite: 32, 34]. Para contextos que no alcancen esta magnitud, el sistema procesa la solicitud bajo tarifas de entrada lineales estándar [cite: 32, 35]. (Es importante notar que en las versiones 2.5 de Gemini, este límite se reduce a 1,024 tokens en Flash y 2,048 tokens en Pro [cite: 7, 36]).
La facturación de Google se divide en dos componentes: el costo de procesamiento por lectura y una tarifa de retención de almacenamiento por hora [cite: 37, 38]. El procesamiento de tokens bajo caché exitosa recibe un descuento del 75% en la familia Gemini 1.5/2.0 y del 90% en la familia Gemini 2.5/3.1 (reduciendo el costo de entrada de $2.00/MTok a $0.20/MTok en Gemini 3.1 Pro) [cite: 31, 38]. Por otro lado, la tarifa de almacenamiento por hora se prorratea y factura a razón de $1.00/MTok/hora para los modelos Flash y $4.50/MTok/hora para los modelos Pro [cite: 37, 38].
OpenRouter
OpenRouter actúa como un proxy unificado de APIs y traslada las características de almacenamiento en caché de los proveedores subyacentes de manera directa a sus consumidores [cite: 11]. El soporte se expone heredando las propiedades nativas de cada modelo (por ejemplo, permitiendo la inyección de la cabecera cache_control para Claude de Anthropic o detectando de forma automática los aciertos de OpenAI) [cite: 11].
OpenRouter aplica una tarifa de plataforma del 5.5% sobre los costos de uso estándar de los proveedores [cite: 10, 39]. Para asegurar la transparencia operativa, el servicio devuelve un payload enriquecido con metadatos específicos bajo el objeto de respuesta prompt_tokens_details, el cual contiene los campos de auditoría cached_tokens y cache_write_tokens [cite: 11]. El descuento efectivo se traslada de forma íntegra a través del campo cache_discount [cite: 11].
Adicionalmente, OpenRouter implementa un enrutamiento persistente o adherente (sticky routing), asegurando que las solicitudes secuenciales con prefijos idénticos se mantengan asignadas al mismo nodo físico de inferencia para optimizar la tasa de aciertos [cite: 11]. Sin embargo, se debe registrar en el recomendador de Osinergmin que ciertos proveedores secundarios dentro de la red de OpenRouter absorben internamente el descuento de caché sin trasladar el ahorro financiero al usuario final [cite: 40]. Por esta razón, el selector de Osinergmin debe incluir una regla de enmascaramiento para priorizar y fijar proveedores que garanticen el traslado transparente de los descuentos (tales como DeepInfra o Novita) [cite: 40].
2. Modelado Matemático del Costo Efectivo (TCO)
Para estructurar de manera rigurosa las proyecciones financieras en el portal de Osinergmin, se requiere formular una ecuación de costo amortizado. El costo unitario crudo no refleja el costo real de una sesión interactiva o un lote de procesamiento RAG. El Costo Efectivo por Millón de Tokens de Entrada (C 
input_efectivo
​
 ) representa el costo promedio ponderado de procesar un prefijo estático a lo largo de una sesión compuesta por múltiples turnos conversacionales [cite: 15, 41].
Formulación Matemática General
Para una sesión de análisis documental que consta de N interacciones totales, donde un mismo prefijo de longitud M (en millones de tokens) se mantiene constante, el costo efectivo se modela mediante la siguiente ecuación general [cite: 41]:
C 
input_efectivo
​
 = 
N
C 
escritura_cach 
e
ˊ
 
​
 +(N−1)⋅[H⋅C 
lectura_cach 
e
ˊ
 
​
 +(1−H)⋅C 
escritura_cach 
e
ˊ
 
​
 ]
​
 
Donde:
C 
est 
a
ˊ
 ndar
​
 : Costo de procesamiento estándar por millón de tokens de entrada sin el uso de caché [cite: 41].
C 
escritura_cach 
e
ˊ
 
​
 : Costo por millón de tokens para la primera operación de lectura y escritura en la memoria de la caché. Se define mediante la relación de recargo de escritura C 
escritura_cach 
e
ˊ
 
​
 =α⋅C 
est 
a
ˊ
 ndar
​
 , donde α≥1.0 representa el multiplicador de recargo por creación de caché (por ejemplo, α=1.25 para el TTL de 5 minutos en Anthropic [cite: 12, 13], y α=1.0 para OpenAI o DeepSeek [cite: 9, 21]).
C 
lectura_cach 
e
ˊ
 
​
 : Costo de procesamiento por millón de tokens cuando la solicitud resulta en un acierto de caché. Se define mediante la relación de descuento de lectura C 
lectura_cach 
e
ˊ
 
​
 =β⋅C 
est 
a
ˊ
 ndar
​
 , donde β<1.0 representa el multiplicador del descuento por lectura (por ejemplo, β=0.10 para Anthropic [cite: 9, 12], y β=0.50 para OpenAI [cite: 9, 19]).
H∈[0.0,1.0]: Tasa de acierto de caché (Cache Hit Rate), que define la fracción de las N−1 consultas subsiguientes que logran reutilizar con éxito el prefijo almacenado en memoria [cite: 9, 41].
N∈N 
≥1
​
 : Número promedio de consultas en la sesión de chat que intentan explotar el mismo prefijo antes de que expire su persistencia temporal (evaporación del TTL) o se altere el documento de referencia [cite: 9, 41].
Análisis de Sensibilidad y Derivación del Punto de Equilibrio (Breakeven)
La viabilidad financiera del almacenamiento en caché de prompts no es universal y depende críticamente del comportamiento de la tasa de aciertos y del número de consultas [cite: 9]. Para determinar el límite de viabilidad, se establece la condición matemática bajo la cual el costo de procesamiento efectivo con caché es estrictamente menor al costo de procesamiento lineal estándar sin caché:
C 
input_efectivo
​
 <C 
est 
a
ˊ
 ndar
​
 
Sustituyendo los factores multiplicativos α y β en la inecuación se obtiene:
N
α⋅C 
est 
a
ˊ
 ndar
​
 +(N−1)⋅C 
est 
a
ˊ
 ndar
​
 ⋅[H⋅β+(1−H)⋅α]
​
 <C 
est 
a
ˊ
 ndar
​
 
Al simplificar el término constante de costo de entrada estándar C 
est 
a
ˊ
 ndar
​
  en ambos miembros, la condición se reduce a una relación puramente adimensional basada en la física de los multiplicadores:
α+(N−1)⋅[α−H⋅(α−β)]<N
Despejando la tasa de acierto crítica de equilibrio (H 
breakeven
​
 ):
α+(N−1)⋅α−(N−1)⋅H⋅(α−β)<N
N⋅α−N<(N−1)⋅H⋅(α−β)
H 
breakeven
​
 > 
(N−1)⋅(α−β)
N⋅(α−1)
​
 
Este resultado analítico permite deducir tres comportamientos de gran relevancia para el simulador MLOps de Osinergmin:
Comportamiento con Recargo de Escritura Nulo (α=1.0): En los esquemas implementados por OpenAI, DeepSeek y Google Gemini implícito, el multiplicador de escritura es unitario [cite: 9, 21]. Al sustituir α=1.0 en la inecuación, el numerador se reduce a cero, lo que implica que:
H 
breakeven
​
 >0.0
Este resultado demuestra que para OpenAI y DeepSeek, cualquier tasa de acierto superior a 0% genera un ahorro neto de manera inmediata para Osinergmin [cite: 9]. No existe riesgo de incurrir en pérdidas financieras por fallo de caché en estos proveedores [cite: 9, 21].
Comportamiento con Recargo de Escritura de 5 Minutos en Anthropic (α=1.25, β=0.10): Para una conversación típica parametrizada en N=5 turnos [cite: 41], el umbral mínimo de aciertos para rentabilizar la implementación se sitúa en:
H 
breakeven_5m
​
 > 
(5−1)⋅(1.25−0.10)
5⋅(1.25−1)
​
 = 
4⋅1.15
1.25
​
 = 
4.60
1.25
​
 ≈0.2717⟹27.2%
Si la tasa de acierto cae por debajo del 27.2%, el recargo del 25% de la escritura inicial anula el beneficio de los descuentos de lectura, provocando que la operación con caché resulte más costosa que el procesamiento tradicional [cite: 9].
Comportamiento con Recargo de Escritura de 1 Hora en Anthropic (α=2.0, β=0.10): Para una conversación breve de N=2 turnos, el punto de equilibrio requiere una tasa de aciertos irrealizable:
H 
breakeven_1h
​
 > 
(2−1)⋅(2.0−0.10)
2⋅(2.0−1)
​
 = 
1⋅1.90
2.0
​
 ≈1.0526⟹105.3%
Al superar el 100%, queda demostrado matemáticamente que es imposible justificar financieramente el uso de la caché con ventana de 1 hora de Anthropic si la interacción del usuario se limita a solo dos turnos, incluso bajo condiciones de acierto perfecto [cite: 16]. El número mínimo de turnos conversacionales (N 
m 
ı
ˊ
 nimo
​
 ) requeridos para justificar el TTL de 1 hora bajo un escenario de acierto absoluto (H=1.0) se calcula mediante:
N
2.0+(N−1)⋅0.10
​
 <1⟹1.9+0.1⋅N<N⟹1.9<0.9⋅N⟹N>2.11⟹N 
m 
ı
ˊ
 nimo
​
 =3 turnos
Cualquier sesión con una duración inferior a 3 turnos conversacionales generará pérdidas netas utilizando la ventana de retención de 1 hora [cite: 16].
A continuación, se integra una tabla de sensibilidad para evaluar cómo el costo efectivo ponderado de la entrada de Claude 3.5 Sonnet se altera en función de la variación de la tasa de aciertos en una sesión estándar de 5 turnos [cite: 12, 13, 41]:
Tasa de Acierto de Caché (H)
Costo Efectivo Entrada (5m TTL - $ / MTok)
Costo Efectivo Entrada (1h TTL - $ / MTok)
Tasa de Ahorro / Pérdida vs. Estándar (5m TTL)
Tasa de Ahorro / Pérdida vs. Estándar (1h TTL)
0% (Fallo Absoluto) [cite: 9]
$3.75000 [cite: 12, 13]
$6.00000 [cite: 12, 13]
-25.00% (Pérdida) [cite: 9, 16]
-100.00% (Pérdida) [cite: 9, 16]
20%
$3.47400
$5.54400
-15.80% (Pérdida)
-84.80% (Pérdida)
27.2% (Punto de Equilibrio)
$3.00000
$4.76000
0.00% (Equilibrio)
-58.60% (Pérdida)
40%
$2.92200
$4.63200
+2.60% (Ahorro)
-54.40% (Pérdida)
60%
$2.37000
$3.72000
+21.00% (Ahorro)
-24.00% (Pérdida)
80%
$1.81800
$2.80800
+39.40% (Ahorro)
+6.40% (Ahorro)
100% (Acierto Absoluto) [cite: 41]
$1.26600
$1.89600
+57.80% (Ahorro)
+36.80% (Ahorro)
3. Modelado de Latencia en la Fase de Prellenado
La aceleración del tiempo de respuesta constituye el segundo gran pilar del prompt caching [cite: 3, 6, 42]. El procesamiento de prompts extensos sobre modelos autorregresivos introduce una penalización severa en la latencia de inicio que puede degradar drásticamente la experiencia de usuario [cite: 2, 43, 44].
Física de la Inferencia: Prefill (Compute-Bound) vs. Decode (Memory-Bound)
La arquitectura de ejecución de un transformador divide el ciclo de inferencia en dos fases con demandas de hardware radicalmente opuestas:
Fase de Prellenado (Prefill): Ocurre de forma inmediata al recibir el prompt [cite: 2, 45, 46]. El motor de inferencia debe procesar simultáneamente todos los tokens de entrada para calcular el mapa de atención y rellenar las claves y valores iniciales de la memoria de la caché [cite: 2, 6, 46]. Al realizar este proceso de manera masiva y paralela en la GPU, esta fase es de carácter intensivo en cómputo o Compute-Bound [cite: 2, 43, 46]. El hardware se ve limitado por la capacidad de los núcleos tensoriales para realizar multiplicaciones de matrices a alta velocidad, manteniendo el ancho de banda de memoria de la GPU en niveles de baja exigencia [cite: 46]. Esta fase domina por completo el Tiempo al Primer Token (TTFT) [cite: 1, 47].
Fase de Decodificado (Decode): Se ejecuta de forma secuencial y autorregresiva para generar cada token de salida subsecuente [cite: 2, 45, 46]. En cada paso, el modelo debe leer la totalidad de los parámetros de sus capas y el histórico acumulado del KV cache desde la memoria de alta capacidad (HBM) hacia el chip de procesamiento [cite: 2, 6, 46]. Al generar un único token por paso, la intensidad aritmética es extremadamente baja, provocando que esta fase esté limitada estrictamente por el ancho de banda de la memoria de la GPU o Memory-Bandwidth-Bound [cite: 43, 47, 48]. Esta fase define la velocidad de transmisión sostenida o fichas por segundo (TPS) [cite: 1, 49].
Proyección Matemática del TTFT Basada en FLOPS de Inferencia
Para evaluar la reducción de la latencia mediante un modelo analítico, se debe cuantificar la demanda computacional en operaciones de punto flotante de la atención de prellenado [cite: 2]. Para un prompt compuesto por una secuencia de tokens de longitud n, procesado por un modelo con un número de capas L y una dimensión oculta o ancho del canal d, el volumen de FLOPS requeridos se describe mediante la relación matemática [cite: 2]:
FLOPS 
prefill
​
 =2⋅n 
2
 ⋅d⋅L+6⋅n⋅d 
2
 ⋅L
El componente lineal 6⋅n⋅d 
2
 ⋅L modela el volumen de operaciones asociadas a las proyecciones iniciales de los tensores de consulta, clave, valor y la proyección de salida de la atención [cite: 2]. Por otro lado, el componente cuadrático 2⋅n 
2
 ⋅d⋅L modela el cálculo de la matriz de atención causal (el producto de las consultas por la matriz de claves transpuesta y el posterior producto por la matriz de valores) [cite: 2, 50]. Cuando la longitud del prompt de Osinergmin se extiende debido a la inclusión de leyes pesadas o expedientes técnicos (por ejemplo, n>30,000 tokens) [cite: 41], el componente cuadrático n 
2
  domina de manera absoluta la ecuación de cómputo [cite: 44, 48].
El Tiempo al Primer Token sin caché de prompts se proyecta dividiendo la demanda de operaciones entre el rendimiento computacional práctico del hardware dedicado:
TTFT 
sin_cach 
e
ˊ
 
​
 = 
F 
GPU_efectivo
​
 
2⋅n 
2
 ⋅d⋅L+6⋅n⋅d 
2
 ⋅L
​
 +T 
red_cola
​
 
Donde $F_{\text{GPU\_efectivo}}}$ representa el rendimiento real obtenido de los núcleos tensoriales bajo optimizaciones de atención (como FlashAttention) expresado en FLOPS, y T 
red_cola
​
  modela las demoras asociadas a la red de transporte y el tiempo de espera en la cola del despachador [cite: 1, 51].
Al ocurrir un Cache Hit de prompts para un prefijo de longitud n 
cach 
e
ˊ
 
​
 , los tensores de clave y valor para dicha región estática ya se encuentran calculados y pre-cargados en la memoria rápida [cite: 3, 6, 8]. Por lo tanto, el sistema de inferencia salta por completo la fase de proyección lineal y el cálculo de atención interna para ese bloque [cite: 37, 52]. El prellenado se ejecuta de manera exclusiva para los nuevos tokens dinámicos agregados (n 
nuevo
​
 =n−n 
cach 
e
ˊ
 
​
 ) [cite: 3, 48].
La computación de atención para estos nuevos tokens debe realizarse mapeando las consultas de n 
nuevo
​
  contra las claves y valores totales de la secuencia n mediante atención cruzada de prellenado parcial [cite: 2]. Los FLOPS requeridos colapsan a:
FLOPS 
prefill_cached
​
 =2⋅n 
nuevo
​
 ⋅n⋅d⋅L+6⋅n 
nuevo
​
 ⋅d 
2
 ⋅L
Dado que el número de tokens nuevos (la pregunta corta del usuario sobre la ley) es órdenes de magnitud menor que el bloque de contexto almacenado en caché (n 
nuevo
​
 ≪n 
cach 
e
ˊ
 
​
 ), el término cuadrático puro de la longitud de contexto completo n 
2
  desaparece [cite: 17, 48]. El TTFT optimizado se proyecta entonces como:
TTFT 
con_cach 
e
ˊ
 
​
 = 
F 
GPU_efectivo
​
 
2⋅n 
nuevo
​
 ⋅n⋅d⋅L+6⋅n 
nuevo
​
 ⋅d 
2
 ⋅L
​
 +T 
red_cola
​
 
Este modelo matemático demuestra cómo el TTFT pasa de tener un comportamiento cuadrático a mostrar una dependencia lineal amortizada respecto a los tokens dinámicos [cite: 2, 17]. Esto explica por qué los entornos de producción registran caídas del TTFT de hasta un 80% o un 85% para prompts extensos en la nube, reduciendo tiempos de espera de segundos a milisegundos [cite: 7, 8, 17].
Impacto en el Dimensionamiento de la Infraestructura Local MLOps
El modelado del TTFT permite optimizar el dimensionamiento físico del hardware local de Osinergmin utilizando teoría de colas M/M/c bajo la formulación Erlang-C [cite: 51]. Cuando la infraestructura local opera bajo un servidor de inferencia unificado (como vLLM o SGLang) [cite: 53], la capacidad de procesamiento concurrente depende del tiempo promedio de servicio de la máquina física [cite: 51].
El tiempo total de ocupación de un canal de inferencia de la GPU para una consulta RAG es la suma del tiempo de prellenado más el tiempo de decodificación autorregresiva de la respuesta [cite: 45, 47]. En escenarios RAG intensivos donde se procesan documentos extensos para generar respuestas cortas y concisas (como resúmenes regulatorios), la fase de prellenado puede representar entre el 70% y el 90% del tiempo total de la GPU [cite: 50, 53].
Al implementar prompt caching local mediante el mecanismo de almacenamiento automático de bloques de vLLM [cite: 54, 55], el tiempo promedio de servicio decae de manera drástica [cite: 54, 56]. Al reducirse el tiempo de procesamiento en el hardware, el simulador MLOps proyectará un incremento exponencial de la tasa de servicio del servidor (μ), lo que permite tolerar tasas de llegada de solicitudes concurrentes sustancialmente mayores sin provocar la saturación de la memoria KV cache de la GPU y sin derivar las transacciones a colas de espera que incrementen el tiempo de respuesta percibido por el usuario final de Osinergmin [cite: 51].
4. Directrices de Diseño UI/UX y Ergonomía del Selector MLOps
La complejidad matemática del modelado del TCO y la latencia debe ser transparente para los ingenieros de sistemas y tomadores de decisiones de Osinergmin [cite: 57]. La interfaz del simulador MLOps debe estructurarse utilizando principios ergonómicos avanzados que faciliten el análisis comparativo [cite: 57].
Parámetros de Entrada para el Modelado del Escenario
Para parametrizar los cálculos de manera ergonómica, el selector MLOps debe requerir del usuario variables del negocio fáciles de estimar, traduciéndolas internamente en variables analíticas para las ecuaciones de costo y rendimiento:
Frecuencia de Actualización del Corpus Legal o Técnico: Se debe solicitar al usuario que indique con qué periodicidad se modifican los PDFs de referencia del sistema RAG (por ejemplo, actualización diaria, semanal o en tiempo real). El motor MLOps utiliza este parámetro para proyectar la tasa de degradación y expiración forzada de la caché de prompts por invalidez del prefijo estático, ajustando hacia abajo la tasa de aciertos proyectada (H) en función de la volatilidad del contenido [cite: 9, 21].
Longitud Promedio del Prompt del Sistema y Documentación RAG: El usuario ingresa la longitud estimada en número de páginas o palabras de los documentos técnicos consolidados. El sistema realiza la conversión a tokens utilizando tasas estándar por idioma (ej. 1 token ≈ 4 caracteres en inglés o 1.3 tokens por palabra en español con alta densidad terminológica legal) [cite: 29, 30, 38]. Esta variable define la longitud del prefijo n 
cach 
e
ˊ
 
​
  [cite: 57].
Cantidad de Preguntas por Sesión de Consulta (N): Captura el comportamiento del operador humano de Osinergmin al interactuar con el asistente virtual (por ejemplo, estimando si un auditor realiza típicamente entre 5 y 10 preguntas sucesivas sobre el mismo TDR antes de iniciar un nuevo expediente). Esta variable define el parámetro N de la ecuación de TCO [cite: 15, 41].
Cadencia de Interacción Temporal (Tiempo entre Consultas): El usuario define si las consultas ocurren de manera continua o espaciada (por ejemplo, "menos de 3 minutos", "entre 5 y 30 minutos", o "más de una hora"). El motor mapea esta cadencia contra los límites de TTL de los proveedores para evaluar de forma predictiva si la caché de prompts se evaporará antes de la siguiente interacción o si se mantendrá activa gracias a la renovación automática por aciertos de lectura [cite: 8, 9, 15].
Visualización Avanzada de Resultados en el Portal MLOps
El diseño ergonómico de la tabla comparativa de resultados debe evitar la sobrecarga cognitiva, facilitando la toma de decisiones estratégicas mediante las siguientes pautas de presentación visual:
Gráfica Dinámica de Sensibilidad del Costo: Integrar un gráfico interactivo que muestre el costo de procesamiento total proyectado como una función continua de la tasa de aciertos de caché (H) de 0% a 100% [cite: 9, 21]. La gráfica debe incorporar un marcador vertical de color rojo que indique visualmente el punto de equilibrio crítico (H 
breakeven
​
 ) específico de cada modelo [cite: 9]. Esto alertará si el perfil de uso previsto por la organización sitúa la operación en un terreno de ineficiencia de costos [cite: 9].
Presentación Bilateral de TCO (Sin Caché vs. Con Caché): La tabla de resultados debe contrastar de manera directa dos escenarios financieros de forma simultánea. En lugar de limitarse a mostrar el costo óptimo, se debe exponer el costo acumulado bajo una arquitectura lineal sin almacenamiento en caché versus el costo proyectado utilizando la tecnología de caching, detallando los ahorros mensuales esperados en dólares y su equivalente porcentual [cite: 15, 41].
Simulación Dinámica de Latencia Temporal de Inicio (TTFT): Mostrar visualmente dos barras de latencia estimadas para cada modelo. La primera barra representará el tiempo de espera inicial o frío (Turno 1, prellenado completo en GPU) [cite: 45, 47], y la segunda mostrará la latencia esperada para las preguntas subsiguientes (Turnos 2 en adelante, prellenado parcial con acierto de caché de prompts) [cite: 17, 48]. Esto evidenciará el impacto directo del caching en la optimización de los niveles de servicio al usuario [cite: 58, 59].
Indicadores Visuales de Activación de Umbral Técnico: Incluir etiquetas informativas basadas en colores (por ejemplo, verde para activación exitosa y gris para desactivación). Estas etiquetas advertirán si el volumen de tokens de los documentos de Osinergmin supera o no los mínimos requeridos por el proveedor para activar la funcionalidad, previniendo errores de estimación en contextos de documentos ligeros [cite: 11, 14].
5. Caso Práctico de Simulación Numérica
Con el propósito de evaluar la viabilidad financiera de manera cuantitativa, se realiza una simulación comparativa de costos utilizando un escenario de auditoría típico de Osinergmin [cite: 41].
Parámetros Fijos del Escenario de Simulación
El caso de estudio evalúa el comportamiento de los modelos propuestos bajo las siguientes restricciones operativas idénticas [cite: 41]:
Longitud del Prefijo de Entrada Estático (System Prompt + 3 PDFs de bases de licitación): 32,000 tokens [cite: 41].
Longitud de los Nuevos Tokens de Entrada (Pregunta del usuario): Se asume insignificante frente al volumen del documento de RAG para simplificar los cálculos de la simulación del prefijo.
Longitud de los Tokens de Salida por Turno: 1,000 tokens generados [cite: 41].
Estructura de la Interacción: Una sesión de chat compuesta por exactamente 5 turnos conversacionales (N=5) donde el documento de contexto no experimenta cambios [cite: 41].
Tasa de Acierto de Caché (H): Se asume un escenario ideal (H=1.0), donde el usuario interactúa activamente dentro de la ventana de TTL del proveedor, garantizando el éxito del almacenamiento de datos en todas las consultas subsiguientes [cite: 15, 41].
Análisis de Costos por Proveedor y Modelo
Se calcula detalladamente el balance financiero del procesamiento de los 5 turnos conversacionales para cada una de las arquitecturas especificadas, utilizando las tarifas de mercado estandarizadas por millón de tokens [cite: 12, 13, 19, 26, 41].
Claude 3.5 Sonnet (TTL de 5 minutos)
Estructura Tarifaria: Entrada base: $3.00/MTok; Escritura (5m TTL): $3.75/MTok (1.25×); Lectura: $0.30/MTok (0.1×); Salida estándar: $15.00/MTok [cite: 12, 13].
Análisis Tradicional Sin Caché:
Costo de Entrada Acumulado: 32,000 tokens×5 turnos=160,000 tokens⟹0.160 MTok×$3.00=$0.48000 [cite: 41].
Costo de Salida Acumulado: 1,000 tokens×5 turnos=5,000 tokens⟹0.005 MTok×$15.00=$0.07500 [cite: 41].
Costo Total de la Sesión: $0.55500 [cite: 41].
Análisis con Prompt Caching (5m TTL):
Turno 1 (Fase Fría / Creación de Caché): Entrada: 32,000 tokens×$3.75/MTok=$0.12000 [cite: 41]. Salida: 1,000 tokens×$15.00/MTok=$0.01500 [cite: 41]. Costo del Turno 1 = $0.13500 [cite: 41].
Turnos 2 al 5 (Fase Caliente / 4 Lecturas de Caché): Entrada: 32,000 tokens×4 turnos=128,000 tokens⟹0.128 MTok×$0.30/MTok=$0.03840 [cite: 41]. Salida: 1,000 tokens×4 turnos=4,000 tokens⟹0.004 MTok×$15.00/MTok=$0.06000 [cite: 41]. Costo acumulado de los Turnos 2 al 5 = $0.09840 [cite: 41].
Costo Total de la Sesión: $0.23340 [cite: 41].
Ahorro Financiero Obtenido: 57.95% [cite: 41].
Claude 3.5 Sonnet (TTL de 1 hora)
Estructura Tarifaria: Entrada base: $3.00/MTok; Escritura (1h TTL): $6.00/MTok (2.0×); Lectura: $0.30/MTok (0.1×); Salida estándar: $15.00/MTok [cite: 12, 13].
Análisis Tradicional Sin Caché: Costo de Entrada: $0.48000; Costo de Salida: $0.07500; Costo Total de la Sesión: $0.55500 [cite: 41].
Análisis con Prompt Caching (1h TTL):
Turno 1 (Fase Fría / Creación de Caché): Entrada: 32,000 tokens×$6.00/MTok=$0.19200 [cite: 41]. Salida: 1,000 tokens×$15.00/MTok=$0.01500 [cite: 41]. Costo del Turno 1 = $0.20700 [cite: 41].
Turnos 2 al 5 (Fase Caliente / 4 Lecturas de Caché): Entrada: $0.03840 [cite: 41]. Salida: $0.06000 [cite: 41]. Costo acumulado de los Turnos 2 al 5 = $0.09840 [cite: 41].
Costo Total de la Sesión: $0.30540 [cite: 41].
Ahorro Financiero Obtenido: 44.97% [cite: 41].
DeepSeek R1
Estructura Tarifaria: Entrada base (fallo de caché): $0.55/MTok; Escritura (sin recargo): $0.55/MTok; Lectura (acierto de caché): $0.14/MTok; Salida estándar: $2.19/MTok [cite: 26, 27].
Análisis Tradicional Sin Caché:
Costo de Entrada Acumulado: 160,000 tokens⟹0.160 MTok×$0.55=$0.08800 [cite: 41].
Costo de Salida Acumulado: 5,000 tokens⟹0.005 MTok×$2.19=$0.01095 [cite: 41].
Costo Total de la Sesión: $0.09895 [cite: 41].
Análisis con Prompt Caching:
Turno 1 (Fase Fría / Creación de Caché): Entrada: 32,000 tokens×$0.55/MTok=$0.01760 [cite: 41]. Salida: 1,000 tokens×$2.19/MTok=$0.00219 [cite: 41]. Costo del Turno 1 = $0.01979 [cite: 41].
Turnos 2 al 5 (Fase Caliente / 4 Lecturas de Caché): Entrada: 32,000 tokens×4 turnos=128,000 tokens⟹0.128 MTok×$0.14/MTok=$0.01792 [cite: 41]. Salida: 1,000 tokens×4 turnos=4,000 tokens⟹0.004 MTok×$2.19/MTok=$0.00876 [cite: 41]. Costo acumulado de los Turnos 2 al 5 = $0.02668 [cite: 41].
Costo Total de la Sesión: $0.04647 [cite: 41].
Ahorro Financiero Obtenido: 53.04% [cite: 41].
OpenAI GPT-4o
Estructura Tarifaria: Entrada base (fallo de caché): $2.50/MTok; Escritura (sin recargo): $2.50/MTok; Lectura (acierto de caché): $1.25/MTok (0.50×); Salida estándar: $10.00/MTok [cite: 19].
Análisis Tradicional Sin Caché:
Costo de Entrada Acumulado: 160,000 tokens⟹0.160 MTok×$2.50=$0.40000 [cite: 41].
Costo de Salida Acumulado: 5,000 tokens⟹0.005 MTok×$10.00=$0.05000 [cite: 41].
Costo Total de la Sesión: $0.45000 [cite: 41].
Análisis con Prompt Caching:
Turno 1 (Fase Fría / Creación de Caché): Entrada: 32,000 tokens×$2.50/MTok=$0.08000 [cite: 41]. Salida: 1,000 tokens×$10.00/MTok=$0.01000 [cite: 41]. Costo del Turno 1 = $0.09000 [cite: 41].
Turnos 2 al 5 (Fase Caliente / 4 Lecturas de Caché): Entrada: 32,000 tokens×4 turnos=128,000 tokens⟹0.128 MTok×$1.25/MTok=$0.16000 [cite: 41]. Salida: 1,000 tokens×4 turnos=4,000 tokens⟹0.004 MTok×$10.00/MTok=$0.04000 [cite: 41]. Costo acumulado de los Turnos 2 al 5 = $0.20000 [cite: 41].
Costo Total de la Sesión: $0.29000 [cite: 41].
Ahorro Financiero Obtenido: 35.56% [cite: 41].
La siguiente tabla consolida los resultados cuantitativos de la simulación para facilitar la estructuración del motor de recomendación en el selector MLOps de Osinergmin [cite: 41]:
Modelo Evaluado
Costo Total Sin Caché (USD)
Costo Total Con Caché (USD)
Ahorro Financiero Neto (%)
Costo de Entrada Amortizado (C 
input_efectivo
​
  / MTok)
Costo Promedio por Turno (USD)
Claude 3.5 Sonnet (5m TTL) [cite: 41]
$0.55500
$0.23340
57.95%
$0.99000
$0.04668
Claude 3.5 Sonnet (1h TTL) [cite: 41]
$0.55500
$0.30540
44.97%
$1.44000
$0.06108
DeepSeek R1 [cite: 41]
$0.09895
$0.04647
53.04%
$0.22200
$0.00929
GPT-4o [cite: 41]
$0.45000
$0.29000
35.56%
$1.50000
$0.05800
Análisis de Viabilidad y Conclusiones para Osinergmin
La evaluación de los resultados numéricos del caso práctico aporta tres conclusiones estratégicas fundamentales para la toma de decisiones tecnológicas de la entidad:
Disonancia entre Eficiencia Relativa y Costo Absoluto: Claude 3.5 Sonnet bajo la ventana de 5 minutos ofrece el mayor porcentaje de ahorro en el procesamiento de tokens de entrada (57.95%) debido a su alto descuento por acierto de lectura [cite: 12, 41]. Sin embargo, al analizar el costo en términos absolutos, el procesamiento cognitivo de DeepSeek R1 resulta ser cinco veces más económico en el costo total de la sesión ($0.04647 para DeepSeek R1 frente a $0.23340 para Claude 3.5 Sonnet) [cite: 41]. El selector MLOps de Osinergmin debe reflejar de manera clara que la optimización relativa de la arquitectura no debe eclipsar la eficiencia absoluta de las tarifas base de los proveedores de bajo costo [cite: 21, 24].
Impacto de la Elección del TTL en Sesiones Conversacionales: El análisis de sensibilidad demuestra que optar por la ventana de retención de 1 hora en Anthropic en lugar de la ventana de 5 minutos eleva el costo de entrada amortizado de la sesión en un 45.4% ($1.44000/MTok frente a $0.99000/MTok) [cite: 41]. Esto se debe a la duplicación del recargo de escritura fría (2.0×) [cite: 12, 13]. Por lo tanto, el recomendador MLOps debe parametrizar y forzar de forma predeterminada el TTL de 5 minutos para todos los asistentes conversacionales rápidos de la entidad, reservando el TTL de 1 hora únicamente para flujos donde el análisis humano entre preguntas supere estrictamente la barrera de los 5 minutos [cite: 15, 16].
Limitaciones Estructurales de la Caché de OpenAI: OpenAI GPT-4o presenta el menor índice de ahorro relativo en la simulación (35.56%) [cite: 41]. A pesar de poseer la ventaja operativa de no cobrar un recargo por la primera escritura fría de la caché [cite: 9, 10], su multiplicador de lectura conservador del 50% (0.50×) limita significativamente su eficiencia financiera para interacciones prolongadas sobre documentos estáticos extensos [cite: 19, 41]. En consecuencia, el selector de Osinergmin debe priorizar modelos con mayores descuentos de lectura (tales como DeepSeek u Anthropic) cuando el volumen de tokens del documento de RAG supere el umbral de los 30,000 tokens en flujos conversacionales de más de tres turnos [cite: 22, 41].
What Is Time To First Token? How To Run A TTFT & Reduce It | Deepchecks, https://deepchecks.com/glossary/time-to-first-token/
Prefill vs. Decode: Why Long Context Makes Your AI Slow Before It Even Starts Talking, https://bytebell.ai/blog/prefill-vs-decode-long-context-latency
Prompt Caching in Agentic AI Systems | by Amit.Kumar | May, 2026 | Medium, https://unscriptedcoding.medium.com/prompt-caching-in-agentic-ai-systems-1f4b78c65ea5
Goodbye Vector Databases? Gemini 2M Token Long Context and Context Caching Performance & Cost Analysis, https://eastondev.com/blog/en/posts/ai/20260227-gemini-long-context-guide/
How I Cut My LLM Costs by 80% Without Sacrificing Quality. | by Ari Vance - Towards AI, https://pub.towardsai.net/how-i-cut-my-llm-costs-by-80-without-sacrificing-quality-85f8505eec96
How KV Caching Slashes LLM Inference Costs at Scale | DigitalOcean, https://www.digitalocean.com/community/conceptual-articles/how-kv-caching-slashes-llm-inference-costs-at-scale
Prompt Caching Explained: What It Is, What It Isn't, and When to Use It - Medium, https://medium.com/@michael.hannecke/prompt-caching-explained-what-it-is-what-it-isnt-and-when-to-use-it-9f5c6fce7bdb
Prompt Caching Infrastructure: Reducing LLM Costs and Latency - Introl, https://introl.com/blog/prompt-caching-infrastructure-llm-cost-latency-reduction-guide-2025
Prompt Caching in 2026: Cut LLM Costs, Keep Quality - Digital Applied, https://www.digitalapplied.com/blog/prompt-caching-2026-cut-llm-costs-engineering-guide
AI API Pricing Comparison 2026: The Real Cost of GPT-4.1, Claude Sonnet 4.6, and Gemini 2.5 | TokenLab, https://lemondata.cc/en/blog/pricing-comparison
Prompt Caching | Reduce AI Model Costs with OpenRouter, https://openrouter.ai/docs/guides/best-practices/prompt-caching
Anthropic API Pricing: Official Token Rates for Every Claude Model (2026) - PE Collective, https://pecollective.com/tools/anthropic-api-pricing/
Prompt caching - Claude Platform Docs, https://platform.claude.com/docs/en/build-with-claude/prompt-caching
Prompt Caching - LiteLLM Docs, https://docs.litellm.ai/docs/completion/prompt_caching
How prompt caching works in Claude Code (and how to stop wasting tokens) - Reddit, https://www.reddit.com/r/ClaudeAI/comments/1uih6w7/how_prompt_caching_works_in_claude_code_and_how/
Prompt Caching Economics on Fable 5: When the 5-Minute TTL Pays - Developers Digest, https://www.developersdigest.tech/blog/fable-5-prompt-caching-economics
Prompt Caching 201 - OpenAI Developers, https://developers.openai.com/cookbook/examples/prompt_caching_201
Prompt caching with Azure OpenAI in Microsoft Foundry Models, https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/prompt-caching
GPT-4o Pricing 2026: 2.50/10 per 1M Tokens vs GPT-4.1 - PE Collective, https://pecollective.com/tools/gpt-4o-pricing/
OpenAI API Pricing 2026: GPT-4.1 at $2, GPT-5 at $1.25/1M - PE Collective, https://pecollective.com/tools/openai-api-pricing/
DeepSeek pricing 2026: V4, R1, API costs, and how to optimize - CloudZero, https://www.cloudzero.com/blog/deepseek-pricing/
LLM API Cache Hit Math: Why Your DeepSeek Bill Says $4 But the Pricing Says $50, https://ofox.ai/blog/llm-api-cache-hit-math-real-bills-2026/
DeepSeek API Pricing: V4 Flash, V4 Pro, Cache Hit, Cache Miss & Output Costs, https://chat-deep.ai/pricing/
OpenAI vs DeepSeek - a comparison for AI product builders - Solvimon, https://www.solvimon.com/pricing-guides/openai-vs-deepseek
DeepSeek's Low Inference Cost Explained: MoE & Strategy | IntuitionLabs, https://intuitionlabs.ai/articles/deepseek-inference-cost-explained
DeepSeek Pricing 2026: Plans, Costs & Savings, https://checkthat.ai/brands/deepseek/pricing
DeepSeek-R1 Release, https://api-docs.deepseek.com/news/news250120
DeepSeek API: Models, Pricing, and How to Call It (2026) - Morph, https://www.morphllm.com/deepseek-api
DeepSeek Character Limits: Tokens, Context & Output, https://deepseekai.guide/guides/deepseek-character-limits/
Gemini AI Agent Builder Pricing: Explore Affordable AI Solutions - SmythOS, https://smythos.com/developers/agent-integrations/gemini-ai-agent-builder-pricing/
Context caching overview | Gemini Enterprise Agent Platform | Google Cloud Documentation, https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-overview
Feature Request: Support Native Gemini Context Caching · Issue #29818 · NousResearch/hermes-agent - GitHub, https://github.com/NousResearch/hermes-agent/issues/29818
Prompt Caching with OpenAI, Anthropic, and Google Models - PromptHub, https://www.prompthub.us/blog/prompt-caching-with-openai-anthropic-and-google-models
Lowering Your Gemini API Bill: A Guide to Context Caching | by Raheel Siddiqui | Medium, https://rawheel.medium.com/lowering-your-gemini-api-bill-a-guide-to-context-caching-0e1f4d0cb3f8
Lowering Your Gemini API Bill: A Guide to Context Caching - DEV Community, https://dev.to/rawheel/lowering-your-gemini-api-bill-a-guide-to-context-caching-aag
Simon Willison on prompt-caching, https://simonwillison.net/tags/prompt-caching/
Prompt Caching - Helicone OSS LLM Observability, https://docs.helicone.ai/gateway/concepts/prompt-caching
Gemini API Pricing: Full Breakdown of Costs (Jun 2026), https://developer.puter.com/tutorials/gemini-api-pricing/
Pricing - OpenRouter, https://openrouter.ai/pricing
PSA: Some OpenRouter providers are pocketing your prompt cache savings — you could be paying 5x more than you should - Reddit, https://www.reddit.com/r/SillyTavernAI/comments/1te5kj4/psa_some_openrouter_providers_are_pocketing_your/
Untitled, unknown_url
Prompt Caching Explained: How to Cut AI Latency and Cost Without Changing Your Model, https://blog.gopenai.com/prompt-caching-explained-how-to-cut-ai-latency-and-cost-without-changing-your-model-1f8930b79480
What Does “LLMs Are Memory Bandwidth Bound” Really Mean? | by Jimin Lee - Medium, https://medium.com/@jiminlee-ai/what-does-llms-are-memory-bandwidth-bound-really-mean-4a1a57161b53
Prefill vs Decode: LLM Inference Phases Explained - Redis, https://redis.io/blog/prefill-vs-decode/
Optimizing LLM Inference: Fluid-Guided Online Scheduling with Memory Constraints - arXiv, https://arxiv.org/html/2504.11320
Prefill Is Compute-Bound. Decode Is Memory-Bound. Why Your GPU Shouldn't Do Both., https://towardsdatascience.com/prefill-is-compute-bound-decode-is-memory-bound-why-your-gpu-shouldnt-do-both/
Pascal: A Phase-Aware Scheduling Algorithm for Serving Reasoning-based Large Language Models - arXiv, https://arxiv.org/html/2602.11530v1
Observation, Not Prediction: Conversation-Level Disaggregated Scheduling for Agentic Serving - arXiv, https://arxiv.org/html/2606.01839v1
LLM Inference Optimization: Cut Cost & Latency at Every Layer (2026) - MorphLLM, https://www.morphllm.com/llm-inference-optimization
QuoKA: Query-oriented KV selection for Efficient LLM Prefill - arXiv, https://arxiv.org/html/2602.08722
5 steps to triage vLLM performance - Red Hat Developer, https://developers.redhat.com/articles/2026/03/09/5-steps-triage-vllm-performance
The Hidden Bottlenecks in LLM Inference and How to Fix Them - DigitalOcean, https://www.digitalocean.com/community/conceptual-articles/bottlenecks-llm-inference-optimization
Context Engineering for Production AI Agents: KV Cache, Prefix Caching, and Long-Context GPU Economics (2026 Guide) | Spheron Blog, https://www.spheron.network/blog/context-engineering-production-ai-agents-kv-cache-long-context/
Automatic Prefix Caching - vLLM Documentation, https://docs.vllm.ai/en/latest/features/automatic_prefix_caching/
Automatic Prefix Caching - vLLM Documentation, https://docs.vllm.ai/en/stable/design/prefix_caching/
vLLM Optimization Techniques: 5 Practical Methods to Improve Performance - Jarvis Labs, https://jarvislabs.ai/blog/vllm-optimization-techniques
LLM API Pricing 2026 - 20+ Models Compared Per Token - PE Collective, https://pecollective.com/blog/llm-api-pricing-comparison/
Taming Request Imbalance: SLO-Aware Scheduling for Disaggregated LLM Inference, https://arxiv.org/html/2605.02329v1
From Tokens to Layers: Redefining Stall-Free Scheduling for LLM Serving with Layered Prefill - arXiv, https://arxiv.org/html/2510.08055v1