# Poblado en Evolución — Reporte de la Simulación

## 1. Enunciado del problema
# 6. Poblado en Evolución

Se desea conocer la evolución de la población de una determinada región.

## Probabilidad de fallecimiento

La probabilidad de fallecer de una persona distribuye uniforme y se corresponde, según su edad y sexo, con la siguiente tabla:

| Edad     | Hombre | Mujer |
|----------|--------|-------|
| 0-12     | 0.25   | 0.25  |
| 12-45    | 0.10   | 0.15  |
| 45-76    | 0.30   | 0.35  |
| 76-125   | 0.70   | 0.65  |

## Probabilidad de embarazo
La probabilidad de que una mujer se embarace es uniforme y está relacionada con el rango de edad 


| Edad     | Probabilidad de Embarazo
|----------|--------
| 12-15    | 0.2  
| 15-21    | 0.45   
| 21-35    | 0.8   
| 35-45    | 0.4   
| 45-60    | 0.2
| 60-125   | 0.05

## Condiciones para el embarazo

Para que una mujer quede embarazada debe tener pareja y no haber tenido el número máximo de hijos que deseaba tener ella o su pareja en ese momento. El número de hijos que cada persona desea tener distribuye uniforme según la siguiente tabla 

| Número   | Probabilidad |
|----------|--------------|
| 1        | 0.6          |
| 2        | 0.75         |
| 3        | 0.35         |
| 4        | 0.25         |
| 5        | 0.1          |
| más de 5 | 0.05         |

## Formación de parejas
Para que dos personas sean pareja deben estar solas en ese instante y deben desear tener pareja. El desear tener pareja está relacionado con la edad:

| Edad     | Probabilidad de querer pareja |
|----------|-------------------------------|
| 12-15    | 0.6                           |
| 15-21    | 0.65                          |
| 21-35    | 0.8                           |
| 35-45    | 0.6                           |
| 45-60    | 0.5                           |
| 60-125   | 0.2                           |

Si dos personas de diferente sexo están solas y ambas desean tener pareja, entonces la probabilidad de volverse pareja está relacionada con la diferencia de edad:

| Diferencia de edad | Probabilidad de establecer pareja |
|--------------------|-----------------------------------|
| 0-5                | 0.45                              |
| 5-10               | 0.40                              |
| 10-15              | 0.35                              |
| 15-20              | 0.25                              |
| 20 o más           | 0.15                              |

## Ruptura de pareja

Cuando dos personas están en pareja, la probabilidad de que ocurra una ruptura distribuye uniforme y es de **0.2**. Cuando una persona se separa (o enviuda), necesita estar sola (No deseará tener pareja) por un período de tiempo que distribuye exponencial con un parámetro λ relacionado con la edad:

| Edad     | λ          |
|----------|------------|
| 12-15    | 3 meses    |
| 15-21    | 6 meses    |
| 21-35    | 6 meses    |
| 35-45    | 12 meses   |
| 45-60    | 24 meses   |
| 60-125   | 48 meses   |

## Embarazo y nacimientos
Cuando están dadas todas las condiciones y una mujer queda embarazada, puede tener o no un embarazo múltiple. Esto distribuye uniforme acorde a las siguientes probabilidades:

| Número de bebés | Probabilidad |
|----------------|--------------|
| 1              | 0.7           |
| 2              | 0.18         |
| 3              | 0.08         |
| 4              | 0.04         |
| 5              | 0.02         |

La probabilidad del sexo de cada bebé nacido es uniforme: **0.5** para cada sexo.

## Población inicial y simulación
Se asume una población inicial de **M mujeres** y **H hombres**. Cada poblador, en el instante inicial, tiene una edad que distribuye uniforme **U(0, 100)**. Realice un proceso de simulación para determinar cómo evoluciona la población en un período de **100 años**.

---
## 2. Ambigüedades del enunciado
### 2.1 ¿Cuándo se aplican las probabilidades?

El enunciado dice "la probabilidad de fallecer de un hombre de 0–12 años es 0.25". Tres interpretaciones son posibles y producen modelos  distintos:

- **Por mes**: cada mes el niño tiene 25 % de probabilidad de morir. La probabilidad de llegar vivo a los 12 años sería $(0.75)^{144} \approx 10^{-18}$. Es decir, prácticamente ningún niño sobreviviría a la infancia. Modelo claramente inviable.
- **Por año**: cada año el niño tiene 25 % de probabilidad de morir. Probabilidad de sobrevivir 12 años: $(0.75)^{12} \approx 3 \%$. Sigue siendo catastrófico.
- **Acumulada sobre todo el rango**: hay 25 % de probabilidad de que, durante los 12 años de la infancia, el niño muera en algún momento. Esto da una mortalidad infantil del 25 % en total, dura pero comparable a sociedades pre-industriales y compatible con cualquier modelo demográfico funcional.

La misma duda aparece en la tabla de embarazos. Una probabilidad de 0.80 para mujeres de 21–35 años podría leerse como "80 % de quedar embarazada cada año" (lo cual es altísimo, daría 10+ embarazos por mujer) o como "80 % de tener al menos un embarazo durante los 14 años del rango" (mucho más plausible).

Y otra vez con la ruptura: el enunciado dice escuetamente que la probabilidad de ruptura es 0.20, pero no aclara ni a qué intervalo temporal se refiere ni si depende de la duración de la relación.

### 2.2 Probabilidades que no son distribuciones de probabilidad

Las tablas de "hijos deseados" y "embarazo múltiple" en el enunciado no son distribuciones de probabilidad válidas: sus probabilidades no suman 1.

Para hijos deseados:

$$0.60 + 0.75 + 0.35 + 0.25 + 0.10 + 0.05 = 2.10$$

Para embarazo múltiple:

$$0.70 + 0.18 + 0.08 + 0.04 + 0.02 = 1.02$$

Hay dos lecturas posibles:

1. Son probabilidades **marginales independientes** (p.ej., "60 % de las personas considerarían tener 1 hijo, 75 % considerarían tener 2, etc.", como si fueran preguntas separadas). Pero el enunciado dice explícitamente que se elige **uno** de los valores, así que esta lectura no encaja.
2. Son **proporciones relativas** que hay que **normalizar** para que sumen 1.

La segunda es la que mejor encaja.

### 2.3 La duración del embarazo

El enunciado describe los embarazos como si fueran eventos instantáneos: "la mujer queda embarazada, luego nacen 1–5 bebés". Se asumira una gestación realista: un retraso de 9 meses entre concepción y parto, durante el cual la mujer no puede volver a embarazarse.

### 2.4 "Más de 5 hijos":

La tabla de hijos deseados culmina con la entrada "más de 5 hijos: 0.05". ¿Cuántos hijos son "más de 5"? ¿6? ¿10? 
Las opciones razonables son: fijar 6 o samplear de una uniforme U(6, 10).

### 2.5 ¿"Desear pareja" es un evento o un estado?

La tabla "probabilidad de querer pareja" se puede interpretar de dos maneras:

- **Como estado**: al entrar a un rango de edad, la persona decide una vez si desea pareja. Esa decisión persiste hasta que cambie de rango o salga de un duelo.
- **Como evento mensual**: cada mes, mientras está sola, se reevalúa con la probabilidad del rango. Esto convierte el "deseo" en algo intermitente y poco coherente conceptualmente.

La primera es más natural. Decir que alguien "desea pareja" sugiere algo del orden de los rasgos o la situación vital, no un dado que se tira cada mes.

### 2.6 La mecánica del emparejamiento

El enunciado describe la probabilidad de formar pareja entre dos personas solas que se desean, pero no especifica **cómo se enumeran los pares posibles**. En un mes con 50 hombres y 30 mujeres disponibles, hay 1500 pares teóricos. Pero apenas uno se forma, dos personas dejan de estar disponibles. El orden en que se prueban los pares importa.

Las opciones son varias:

- Barajar ambas listas y probar uno a uno.
- Probar todos los pares y elegir aleatoriamente entre los exitosos.
- Algún esquema de "preferencia" por menor diferencia de edad.

La primera es la más natural si pensamos en encuentros sociales aleatorios. Las otras dos introducen supuestos no presentes en el enunciado.

### 2.7 Los límites de los rangos

¿Una persona con exactamente 12 años cae en el rango 0–12 o en el rango 12–45? El enunciado no aclara, pero las tablas se solapan en los extremos (45 aparece como límite superior de 12–45 y como límite inferior de 45–76). La convención usual es semi-abierta: `[min, max)`. 

### 2.8 La duración del duelo: λ como tasa o como media

La tabla de duelos da valores como "3 meses", "6 meses", "12 meses" etiquetados como λ. En una distribución exponencial, λ tiene una interpretación matemática específica como **tasa**, y la media de la distribución es $1/\lambda$. Pero en el enunciado las unidades están en meses, lo que sugiere que λ representa la **duración promedio**, no la tasa. Si fuera tasa, una "tasa" de 3 meses haría que el duelo promedio fuera $1/3$ de mes, lo que no tendría sentido.

Asumir λ = media es lo consistente con el resto del enunciado.

---

## 3. Decisiones de modelado: cómo se resolvió cada ambigüedad

Una vez identificadas las ambigüedades, había que resolverlas. Esta sección documenta las decisiones tomadas y por qué.

### 3.1 Decisión madre: probabilidades como acumuladas por rango

La interpretación elegida fue que cada probabilidad de la tabla representa el **riesgo total acumulado durante todo el rango de edad** correspondiente. Esto se aplica a mortalidad y a embarazo.

¿Por qué?:

1. **Las otras dos interpretaciones producen modelos absurdos**. Probabilidades mensuales de 0.25 hacen colapsar la simulación en meses. Probabilidades anuales son apenas menos catastróficas.
2. **El enunciado da probabilidades grandes (hasta 0.80)**. Probabilidades grandes "por mes" no tienen sentido para procesos demográficos: nadie tiene 80 % de probabilidad mensual de quedar embarazada (eso significaría 0.8 × 12 ≈ 9.6 embarazos por año).
3. **La interpretación acumulada es la única que cierra dimensionalmente**: cada probabilidad describe un fenómeno asociado a un período (un rango de edad), no a un instante.

La fórmula matemática de la conversión es:

$$P_{\text{rango}} = 1 - (1 - p_{\text{mes}})^N$$

donde N es el número de meses en el rango y $p_{\text{mes}}$ es la probabilidad mensual equivalente. Despejando:

$$p_{\text{mes}} = 1 - (1 - P_{\text{rango}})^{1/N}$$

Aplicando esto a la mortalidad obtenemos probabilidades mensuales muy pequeñas, del orden de 0.1–0.2 %, perfectamente compatibles con cualquier estudio demográfico real:

| Rango (años) | Meses | $P_{\text{rango}}$ H | $p_{\text{mes}}$ H | $P_{\text{rango}}$ M | $p_{\text{mes}}$ M |
|--------------|------:|---------------------:|-------------------:|---------------------:|-------------------:|
| 0–12         |   144 | 0.25                 | 0.00200            | 0.25                 | 0.00200            |
| 12–45        |   396 | 0.10                 | 0.00027            | 0.15                 | 0.00041            |
| 45–76        |   372 | 0.30                 | 0.00096            | 0.35                 | 0.00116            |
| 76–125       |   588 | 0.70                 | 0.00205            | 0.65                 | 0.00179            |

Lo mismo para los embarazos. Cada mujer en pareja tiene una probabilidad mensual modesta de quedar embarazada, que acumulada sobre el rango converge a la probabilidad de la tabla:

| Rango (años) | Meses | $P_{\text{rango}}$ | $p_{\text{mes}}$ |
|--------------|------:|-------------------:|-----------------:|
| 12–15        |    36 | 0.20               | 0.00619          |
| 15–21        |    72 | 0.45               | 0.00831          |
| 21–35        |   168 | 0.80               | 0.00957          |
| 35–45        |   120 | 0.40               | 0.00425          |
| 45–60        |   180 | 0.20               | 0.00124          |
| 60–125       |   780 | 0.05               | 0.0000658        |

Hay un matiz importante: para que esta lógica sea coherente, la probabilidad acumulada de embarazo del rango sólo se realiza si la mujer pasa **todo** el rango con las condiciones favorables (en pareja, no embarazada, ninguno de los dos al máximo de hijos). Si sólo cumple las condiciones la mitad del tiempo, la probabilidad efectiva será proporcionalmente menor — algo que es exactamente lo que pasa en la realidad y emerge naturalmente del modelo.

### 3.2 La probabilidad de ruptura: interpretada como anual

A diferencia de las otras tablas, la ruptura no está vinculada a un rango de edad. Eso elimina la opción "acumulada sobre el rango". Quedan tres lecturas: por mes, por año, o por toda la vida de la pareja.

"Por mes" es muy alta: $1 - (0.8)^{12} \approx 93 \%$ de probabilidad anual de romper, parejas medias de ~5 meses. Insostenible.

"Por toda la vida de la pareja" no tiene sentido como mecanismo iterativo en el bucle de simulación: ¿qué probabilidad mensual le corresponde si no hay duración fija?

"Por año" es lo que queda y es lo razonable: $p_{\text{mes}} = 1 - (0.8)^{1/12} \approx 0.01838$. Las parejas duran en promedio $1/0.01838 \approx 54$ meses, unos 4.5 años. Es un número plausible aunque algo bajo en comparación con datos reales (la duración media del matrimonio en Occidente moderno ronda los 8–11 años).

### 3.3 El deseo de pareja como atributo persistente

Se evalúa una sola vez al entrar a un nuevo rango de edad. Si entra en duelo, el atributo se fuerza a `False` por la duración del duelo. Cuando el duelo termina, se reevalúa una vez con la probabilidad del rango actual.

Una consecuencia interesante: una persona que decide "no quiero pareja" al entrar a un rango de 14 años (digamos 21–35) puede permanecer sola toda esa década y media. Esto refleja una asimetría real: muchas decisiones sobre vínculos son estables y no se reabren cada mes.

### 3.4 Gestación de 9 meses

Se modeló el embarazo como un estado con duración fija. La mujer entra en estado "embarazada" al concebir, conserva ese estado durante 9 meses sin posibilidad de un nuevo embarazo, y al noveno mes ocurre el parto. Si muere durante esos 9 meses, el embarazo desaparece silenciosamente sin generar parto.

Esto sirve para tres cosas:

1. **Espaciar nacimientos**: una mujer no puede tener un embarazo nuevo cada mes; debe esperar al menos 9 meses entre concepciones.
2. **Acoplar mortalidad y fertilidad**: las muertes maternas durante el embarazo reducen los nacimientos, capturando una dinámica realista.
3. **Hacer el modelo demográficamente plausible**: sin gestación, una mujer con pareja en rango 21–35 podría tener 12 partos al año (uno por mes), lo cual es biológicamente imposible.

### 3.5 Emparejamiento: barajar y emparejar uno a uno

Cada mes se construyen las listas de hombres y mujeres disponibles (sola, sin duelo, deseando pareja, mayor de 12 años). Ambas listas se barajan. Se itera sobre la lista de hombres; para cada uno, se itera sobre las mujeres disponibles, se calcula la diferencia de edad, se obtiene la probabilidad correspondiente, y se tira el dado. Si sale exitoso, se forma la pareja y se rompe el ciclo interno. El hombre pasa al siguiente.

Este esquema tiene una propiedad atractiva: el orden de evaluación es aleatorio (por el barajado), así que ningún subconjunto de personas está sistemáticamente favorecido. Y es eficiente: en el peor caso es O(H × M), pero en la práctica termina mucho antes porque los emparejamientos exitosos reducen rápidamente las listas.

### 3.6 "Más de 5 hijos" se mapea a 6

Se eligió 6 como el valor concreto, por dos razones: es el mínimo posible compatible con "más de 5", y la probabilidad de esta categoría es tan baja (~2.4 %) que la elección apenas afecta los resultados.

### 3.7 Convención de intervalos: cerrado-abierto

`[min, max)`. Una persona con exactamente 12.0 años cae en el rango 12–45 (no en 0–12). Esto es consistente con la práctica habitual en estadística y elimina cualquier ambigüedad en los bordes.

### 3.8 Duelo exponencial con λ como media

Se usó `random.expovariate(1/λ)` donde λ es la media en meses, y se redondeó a entero con mínimo 1. Eso da una distribución exponencial con media exactamente λ y varianza $\lambda^2$, lo que produce duelos típicamente cortos pero con cola larga: posible que una persona quede sola durante años después de una ruptura severa.

### 3.9 Granularidad temporal: pasos mensuales

La pregunta de fondo era si usar simulación por intervalos fijos o una FEL (Future Event List) con eventos puntuales programados (muerte, embarazo, ruptura, fin de duelo).

Se eligió **intervalos fijos de 1 mes** por las siguientes razones:

- Los tiempos de duelo y de gestación están naturalmente expresados en meses.
- La conversión de probabilidades acumuladas a probabilidades mensuales es directa.
- El paso mensual es lo suficientemente fino para los procesos biológicos relevantes (concepción, parto) y lo suficientemente grueso para que la simulación de 100 años (1200 pasos) corra en segundos.
- Es más fácil de depurar: en cada mes, el estado de toda la población es observable.

La FEL sería más eficiente para poblaciones muy grandes, pero para 100–500 personas el costo computacional es despreciable y la simplicidad gana.

---

## 4. La implementación: arquitectura y flujo

El proyecto está dividido en siete archivos, cada uno con una responsabilidad bien delimitada:

| Archivo                                           | Qué contiene                                                            |
|---------------------------------------------------|-------------------------------------------------------------------------|
| [config.py](../config.py)                         | Constantes globales (duración de la sim, meses de gestación, sexos)     |
| [tablas.py](../tablas.py)                         | Tablas de probabilidad transcritas del enunciado, con normalizaciones   |
| [probabilidades.py](../probabilidades.py)         | Funciones de consulta y la conversión rango → mensual                   |
| [persona.py](../persona.py)                       | Modelo de una persona individual con su ciclo de vida                   |
| [simulacion.py](../simulacion.py)                 | Motor `SimulacionPoblado` con el bucle principal                        |
| [replicas.py](../replicas.py)                     | Ejecución de múltiples réplicas y agregación estadística                |
| [poblado_simulacion.py](../poblado_simulacion.py) | Punto de entrada                                                        |

### 4.1 La clase `Persona`

Cada poblador es una instancia de `Persona` con los siguientes atributos:

- **Identidad**: `id`, `sexo`, `edad_meses`, `viva`.
- **Estado de pareja**: `pareja` (referencia bidireccional a otra `Persona`), `desea_pareja`, `en_duelo`, `fin_duelo_mes`.
- **Memoria de rango**: `_rango_deseo_actual`, usado para detectar cuándo la persona cambia de rango etario y disparar una nueva evaluación del deseo de pareja.
- **Reproducción**: `hijos_deseados`, `hijos_tenidos`.
- **Embarazo** (sólo mujeres): `embarazada`, `mes_concepcion`.

La persona expone métodos para envejecer (incrementar la edad y reevaluar deseos si cambió de rango), morir (con propagación del estado de viudez a la pareja sobreviviente), iniciar duelo y terminar duelo.

### 4.2 El bucle principal

Cada mes (de 0 a 1199) se ejecutan siete fases en orden:

```text
1.  Envejecer:         edad_meses += 1; si cambia de rango etario,
                       reevaluar el deseo de pareja
2.  Mortalidad:        cada persona viva tira U; si U < p_mes(edad, sexo)
                       → muere; si tenía pareja, la pareja inicia duelo
3.  Fin de duelo:      personas cuyo fin_duelo_mes ya pasó salen del duelo
                       y reevalúan su deseo de pareja
4.  Formación pareja:  emparejar disponibles por diferencia de edad
5.  Rupturas:          cada pareja tira U; si U < p_rup_mensual
                       → se separan e inician duelo
6.  Embarazos:         cada mujer apta tira U; si U < p_embarazo_mensual
                       → queda embarazada (mes_concepcion = mes_actual)
7.  Nacimientos:       cada mujer con 9 meses de gestación cumplidos
                       da a luz (1–5 bebés, sexo 50/50, edad 0)
```

El orden importa: ubicar la mortalidad antes que las rupturas asegura que las personas que mueren no participen en las rupturas del mismo mes. Ubicar los embarazos antes que los nacimientos es solo cuestión de claridad: un embarazo concebido este mes no puede nacer este mismo mes (siempre hay un delta de al menos 9 meses).

### 4.3 Manejo de estado bidireccional

Las parejas son referencias bidireccionales: si A tiene a B como pareja, B tiene a A. Cuando A muere, el método `morir` rompe ambos lados del vínculo: pone `B.pareja = None`, marca a B como en duelo, calcula su tiempo de fin de duelo, y sólo entonces marca a A como muerto y limpia `A.pareja = None`. El orden de las operaciones evita estados inconsistentes (un huérfano apuntando a un muerto).

---
## 6. Resultados experimentales

La simulación se ejecutó con la configuración por defecto: 50 hombres, 50 mujeres, edades iniciales U(0, 100), 100 años (1200 meses) de evolución.

El resumen final de esta corrida individual:

```text
======================================================================
 RESUMEN FINAL
======================================================================

  Población final:        15
  Hombres vivos:          6
  Mujeres vivas:          9
  Parejas activas:        1

  Total nacimientos:      19
  Total defunciones:      104
  Crecimiento neto:       -85
  Total parejas formadas: 112
  Total rupturas:         102

  Edad promedio:          83.6 años
  Edad mediana:           80.9 años
  Persona más joven:      39.4 años
  Persona más vieja:      122.8 años

  Distribución por rango de edad:
      0-12 :    0 (  0.0%)
     12-18 :    0 (  0.0%)
     18-30 :    0 (  0.0%)
     30-45 :    1 (  6.7%) ##
     45-60 :    2 ( 13.3%) #####
     60-76 :    4 ( 26.7%) ##########
     76-125:    8 ( 53.3%) #####################

  Población máxima:       98 (año 0.0)
  Población mínima:       15 (año 98.5)
======================================================================
```

De 100 personas iniciales sólo quedan 15 al final, y la pirámide está completamente invertida: el 80 % de los sobrevivientes tiene más de 60 años. No hay ningún sobreviviente menor de 30. La única pareja activa al final es una excepción, no una norma.

### 6.2 Evolución década a década

Para entender cómo se llegó a ese estado, conviene mirar la evolución temporal:

| Año | Población | Hombres | Mujeres | Parejas | Nac/año | Def/año |
|----:|----------:|--------:|--------:|--------:|--------:|--------:|
| 10  | 91        | 43      | 48      | 5       | 7       | 16      |
| 20  | 83        | 42      | 41      | 8       | 4       | 12      |
| 30  | 72        | 35      | 37      | 7       | 0       | 11      |
| 40  | 59        | 29      | 30      | 5       | 5       | 18      |
| 50  | 50        | 27      | 23      | 4       | 2       | 11      |
| 60  | 40        | 24      | 16      | 3       | 0       | 10      |
| 70  | 35        | 20      | 15      | 2       | 1       | 6       |
| 80  | 26        | 12      | 14      | 1       | 0       | 9       |
| 90  | 18        | 8       | 10      | 0       | 0       | 8       |
| 100 | 15        | 6       | 9       | 1       | 0       | 3       |

El declive no es abrupto. La población pierde alrededor de 10 personas cada década, con un ritmo que se mantiene  constante. Los nacimientos nunca compensan las defunciones: el mejor año tiene 7 nacimientos, pero las defunciones rondan los 10–18 anuales.

Hay un detalle que vale la pena notar: el número de parejas activas oscila entre 1 y 8 durante toda la simulación, con un pico en la segunda década y un declive a partir de ahí. Después del año 80 prácticamente no hay parejas, lo cual cierra cualquier posibilidad de nacimientos nuevos.

### 6.3 Agregado de 10 réplicas

Para reducir el ruido de una única semilla, se ejecutaron 10 réplicas con semillas distintas. Los resultados:

| Métrica            | Media (μ) | Desv. estándar (σ) | Mínimo | Máximo |
|--------------------|----------:|-------------------:|-------:|-------:|
| Población final    | 19.7      | 6.7                | 10     | 27     |
| Total nacimientos  | 35.1      | 13.1               | 16     | 51     |
| Total defunciones  | 115.4     | 7.2                | 104    | 125    |
| Población máxima   | 104.5     | 3.2                | 99     | 108    |

Ninguna de las 10 réplicas terminó en extinción total. Todas declinaron significativamente, con poblaciones finales entre 10 y 27 (μ ≈ 20). La variabilidad es moderada (σ/μ ≈ 34 % para población final, ≈ 37 % para nacimientos), lo que indica que el modelo es estocásticamente estable: el destino "decadencia sin extinción" se repite en todas las trayectorias.

La evolución promediada por década:

```text
  Año   0:   99.9 personas  ########################################
  Año  10:   98.5 personas  #######################################
  Año  20:   92.7 personas  #####################################
  Año  30:   83.4 personas  #################################
  Año  40:   71.4 personas  ############################
  Año  50:   60.4 personas  ########################
  Año  60:   49.9 personas  ###################
  Año  70:   40.8 personas  ################
  Año  80:   32.7 personas  #############
  Año  90:   26.5 personas  ##########
  Año 100:   19.7 personas  #######
```

El perfil es una curva que recuerda al decaimiento exponencial, con un punto de inflexion alrededor del año 30. Antes de ese punto el declive es lento (la primera década pierde apenas 1.5 personas); después se acelera (de la década 30 a la 40 se pierden ~12 personas).

---

## 7. Discusión: 

Los resultados son consistentes con las probabilidades dadas y con la condición inicial U(0, 100). La simulación muestra es que el sistema descrito por el enunciado **no es una población biológicamente sostenible**.

### 7.1 ¿Cuánto declive es razonable esperar?

Hagamos un análisis de sobre-mesa. La población inicial es uniforme en [0, 100]. Eso significa que aproximadamente:

- 12 % de las personas (12 en total) son niños menores de 12 años.
- 33 % (33 en total) están en el rango fértil amplio 12–45.
- 31 % (31 personas) están en 45–76.
- 24 % (24 personas) tienen más de 76 años.

Sólo las mujeres entre 12 y 45 años pueden producir hijos. Eso son ~16 mujeres iniciales. Pero la "fertilidad alta" ocurre sólo en 21–35, que abarca ~7 mujeres. Y estas 7 mujeres sólo permanecen en ese rango unos 14 años cada una.

Si pensamos en términos de "person-years fértiles totales" disponibles durante los 100 años de simulación, salen unos 14 × 7 ≈ 100 años de fertilidad prima de las mujeres iniciales, más los aportes de las mujeres que entran al rango después (las niñas iniciales más las hijas nacidas durante la simulación, lo cual es relativamente poco).

Una mujer con pareja todo el tiempo en rango 21–35 tendría aproximadamente $1 - (1 - 0.00957)^{168} \approx 80 \%$ de probabilidad de al menos un embarazo. Pero como las parejas duran sólo 4.5 años y luego hay un duelo de 6–12 meses, las mujeres pasan típicamente entre 30 % y 50 % de su vida fértil sin pareja, lo que reduce los embarazos efectivos a la mitad o un tercio.

Multiplicando: la cantidad esperada de embarazos es del orden de 0.4 × 16 mujeres × 1 embarazo posible ≈ 6 embarazos durante toda la simulación, con un promedio de 1.56 bebés por embarazo (calculando la media de la tabla de embarazo múltiple) ≈ 10 bebés. Pero la simulación produce 35 nacimientos en promedio. La diferencia se debe a embarazos múltiples adicionales en la vida de cada mujer (algunas tienen 2 ó 3 embarazos, no sólo 1) y a los hijos de mujeres que entran al rango fértil más tarde. El orden de magnitud (decenas, no centenas) es correcto.

Y las defunciones: de las 135 personas que pasan por la simulación (100 iniciales + 35 nacidas), mueren 115. Eso es una tasa de supervivencia del 15 %. Dado que la edad inicial promedio es 50 años y la simulación dura 100 años, mucha gente envejece hasta entrar en el rango de altísima mortalidad. La cuenta cierra.


### 7.2 La causa del declive:

La condición inicial U(0, 100) es el primer y principal causante. Las poblaciones reales no tienen esa estructura: típicamente hay una pirámide demográfica, con base ancha (muchos niños) y cumbre estrecha (pocos ancianos). En este modelo, comenzamos con tantos ancianos como adolescentes, y tantos adultos jóvenes como adultos mayores. Esa estructura es típica de una población **que ya está envejecida** y declinando, no de una población joven.

Por cada réplica se forman ~110 parejas y se rompen ~102. Es decir, casi todas las parejas que se forman se disuelven antes de los 100 años. Pero el dato más jugoso es la **tasa de embarazos por pareja**: 35 nacimientos en 110 parejas ≈ 0.32 nacimientos por pareja.

Las parejas son mayoritariamente estériles, no porque no quieran hijos, sino porque no duran lo suficiente o porque se forman entre personas fuera del rango fértil. Si las parejas duraran el doble (probabilidad de ruptura anual = 0.10 en lugar de 0.20), la duración media saltaría a ~9 años, y la fertilidad por pareja crecería desproporcionadamente — quizá ×2 o ×3. **La duración de la pareja es el parámetro de mayor apalancamiento en este modelo**.

### 7.3 Paralelo con poblaciones reales

El comportamiento simulado se parece a una superposición de patologías demográficas:

- **Baja fertilidad**, similar a la de Japón, Italia o Corea del Sur contemporáneos.
- **Mortalidad pre-moderna**, similar a la Europa del siglo XIX.
- **Población inicial envejecida**, parecida a la situación de muchos países desarrollados después del baby boom.
- **Sin migración**, una sociedad cerrada.

En la realidad, nunca coexisten estas cuatro condiciones. Las sociedades de baja fertilidad tienen mortalidad baja; las de mortalidad alta tienen fertilidad alta como mecanismo compensatorio. 

La interpretación de las probabilidades como acumuladas por rango fue la decisión más cargada de consecuencias. Si hubiéramos interpretado los mismos números como "probabilidades anuales" o, peor, "mensuales", la simulación habría colapsado en cuestión de semanas simuladas. La interpretación elegida es la **única que produce dinámicas no triviales**. 

---

## 8. Limitaciones y posibles mejoras

El modelo, aunque funcional, tiene puntos débiles que valdría la pena revisar.

### 8.1 La condición inicial

El cambio más impactante sería abandonar U(0, 100) y partir de una **pirámide demográfica realista**. Por ejemplo, una distribución triangular con base en 0 (muchos niños) y vértice en 100 (pocos ancianos). Con una pirámide así, los primeros 30 años de simulación tendrían muchas más mujeres entrando en edad fértil, y la dinámica sería sustancialmente distinta. Es probable que con una pirámide adecuada la población se estabilizara o creciera.

### 8.2 Período post-parto

El modelo actual permite que una mujer quede embarazada el mes siguiente del parto. En la realidad, hay un período de infertilidad post-parto de 6 a 24 meses, dependiendo de factores como la lactancia. Agregar este detalle reduciría aún más la natalidad pero la haría más realista.

### 8.3 Edad mínima de embarazo

El modelo permite embarazos desde los 12 años con probabilidad 0.20 (de la tabla). Aunque en la práctica casi no ocurren (porque las niñas de 12 raramente tienen pareja), el sistema podría incorporar restricciones más fuertes: probabilidad de pareja entre edades muy disímiles tendiendo a cero.

### 8.4 Inmigración

Una pequeña tasa de inmigración (digamos, 5 personas jóvenes nuevas por año) podría compensar el declive estructural y producir poblaciones estables. Sin esto, el modelo es un sistema cerrado condenado al declive.

---

## 9. Conclusiones

**Primera**: El modelo demográfico depende críticamente de cómo se interpretan las probabilidades temporalmente. El enunciado de este problema deja esa interpretación al lector, y la única lectura que produce dinámicas no triviales es la acumulada por rango. 

**Segunda**: el modelo describe una población en declive porque las probabilidades dadas no soportan una población estable a partir de la condición inicial U(0, 100). El resultado es robusto a las semillas: ninguna réplica se extingue, pero todas declinan ~80 % en 100 años. La estructura inicial domina el destino del sistema durante al menos las primeras décadas.

**Tercera**: la palanca de mayor sensibilidad es la duración de las parejas. Una baja en la probabilidad de ruptura de 0.20 a 0.10 anual probablemente cambiaría el modelo de "declinante" a "estable" o incluso "creciente", sin tocar ninguna otra probabilidad. Esto es consistente con la demografía real: las sociedades con vínculos familiares más estables tienden a tener mayor reposición generacional.

El modelo muestra cómo procesos individuales (nacer, envejecer, emparejarse, morir) se agregan en dinámicas poblacionales que pueden ser contraintuitivas. Y muestra también que las decisiones de modelado, lejos de ser detalles técnicos, son las que determinan el resultado.

---

## 10. Cómo ejecutar el proyecto

Desde la raíz del proyecto:

```bash
python poblado_simulacion.py
```

Esto ejecuta:

1. Una simulación individual detallada con `seed=42`, 50 hombres y 50 mujeres iniciales, mostrando estado cada 10 años y un resumen final.
2. 10 réplicas con semillas distintas (`seed = i * 42 + 7`), reportando estadísticas agregadas: media, desviación, mínimo, máximo, distribución por década, número de extinciones.

Para variar los parámetros, basta con editar la llamada en [poblado_simulacion.py](../poblado_simulacion.py) o cambiar las constantes en [config.py](../config.py).

### 10.1 Estructura de archivos

```text
.
├── config.py              # Constantes globales (duración, gestación, sexos)
├── tablas.py              # Tablas de probabilidad del enunciado
├── probabilidades.py      # Funciones de consulta y conversión rango → mensual
├── persona.py             # Modelo de Persona con su ciclo de vida
├── simulacion.py          # Motor SimulacionPoblado con el bucle principal
├── replicas.py            # Ejecución de múltiples réplicas y agregación
├── poblado_simulacion.py  # Punto de entrada
└── docs/
    ├── Orientacion del problema.md
    └── reporte.md         # Este documento
```
