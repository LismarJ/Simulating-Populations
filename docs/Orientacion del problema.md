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
| 5        | 0.1             |
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
| 35-45    | 12 meses      |
| 45-60    | 24 meses   |
| 60-125   | 48 meses     |

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
