# Poblado en Evolución — Reporte de la Simulación

 Poblado en Evolución

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


##  Cómo ejecutar el proyecto

Desde la raíz del proyecto:

```bash
python poblado_simulacion.py
```

Esto ejecuta:

1. Una simulación individual detallada con `seed=42`, 50 hombres y 50 mujeres iniciales, mostrando estado cada 10 años y un resumen final.
2. 10 réplicas con semillas distintas (`seed = i * 42 + 7`), reportando estadísticas agregadas: media, desviación, mínimo, máximo, distribución por década, número de extinciones.

Para variar los parámetros, basta con editar la llamada en [poblado_simulacion.py](../poblado_simulacion.py) o cambiar las constantes en [config.py](../config.py).

### Estructura de archivos

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


## La implementación: arquitectura y flujo

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


### El bucle principal

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

##  Conclusiones

**Primera**: El modelo demográfico depende críticamente de cómo se interpretan las probabilidades temporalmente. El enunciado de este problema deja esa interpretación al lector, y la única lectura que produce dinámicas no triviales es la acumulada por rango. 

**Segunda**: el modelo describe una población en declive porque las probabilidades dadas no soportan una población estable a partir de la condición inicial U(0, 100). El resultado es robusto a las semillas: ninguna réplica se extingue, pero todas declinan ~80 % en 100 años. La estructura inicial domina el destino del sistema durante al menos las primeras décadas.

**Tercera**: la palanca de mayor sensibilidad es la duración de las parejas. Una baja en la probabilidad de ruptura de 0.20 a 0.10 anual probablemente cambiaría el modelo de "declinante" a "estable" o incluso "creciente", sin tocar ninguna otra probabilidad. Esto es consistente con la demografía real: las sociedades con vínculos familiares más estables tienden a tener mayor reposición generacional.

El modelo muestra cómo procesos individuales (nacer, envejecer, emparejarse, morir) se agregan en dinámicas poblacionales que pueden ser contraintuitivas. Y muestra también que las decisiones de modelado, lejos de ser detalles técnicos, son las que determinan el resultado.

---
