"""Funciones auxiliares y de consulta sobre las tablas de probabilidad."""

import random

from config import Sexo
from tablas import (
    TABLA_MORTALIDAD,
    TABLA_EMBARAZO,
    TABLA_DESEO_PAREJA,
    TABLA_FORMACION_PAREJA,
    TABLA_HIJOS_DESEADOS,
    TABLA_EMBARAZO_MULTIPLE,
    TABLA_DUELO,
)


def prob_mensual(p_rango: float, meses_rango: int) -> float:
    """Convierte probabilidad acumulada del rango a probabilidad por mes."""
    if meses_rango <= 0 or p_rango <= 0:
        return 0.0
    if p_rango >= 1.0:
        return 1.0
    return 1.0 - (1.0 - p_rango) ** (1.0 / meses_rango)


def edad_a(edad_meses: int) -> float:
    """Convierte meses a años."""
    return edad_meses / 12.0


def buscar_rango(tabla, edad_anios: float):
    """Busca en una tabla por rango de edad [min, max)."""
    for entrada in tabla:
        if entrada[0] <= edad_anios < entrada[1]:
            return entrada
    return None


def obtener_prob_muerte_mensual(edad_anios: float, sexo: Sexo) -> float:
    """Probabilidad mensual de muerte según edad y sexo."""
    rango = buscar_rango(TABLA_MORTALIDAD, edad_anios)
    if rango is None:
        return 1.0  # edad >= 125, muerte segura
    edad_min, edad_max, p_h, p_m = rango
    meses = int((edad_max - edad_min) * 12)
    p = p_h if sexo == Sexo.HOMBRE else p_m
    return prob_mensual(p, meses)


def obtener_prob_embarazo_mensual(edad_anios: float) -> float:
    """Probabilidad mensual de embarazo según edad."""
    rango = buscar_rango(TABLA_EMBARAZO, edad_anios)
    if rango is None:
        return 0.0
    edad_min, edad_max, p = rango
    meses = int((edad_max - edad_min) * 12)
    return prob_mensual(p, meses)


def obtener_deseo_pareja_prob(edad_anios: float) -> float:
    """Probabilidad de desear pareja al entrar en un rango."""
    rango = buscar_rango(TABLA_DESEO_PAREJA, edad_anios)
    if rango is None:
        return 0.0
    return rango[2]


def obtener_prob_formacion_pareja(dif_edad: float) -> float:
    """Probabilidad de formar pareja según diferencia de edad."""
    for dmin, dmax, p in TABLA_FORMACION_PAREJA:
        if dmin <= dif_edad < dmax:
            return p
    return 0.15  # 20+ años de diferencia


def obtener_tiempo_duelo(edad_anios: float) -> float:
    """Tiempo promedio (en meses) para la distribución exponencial del duelo."""
    rango = buscar_rango(TABLA_DUELO, edad_anios)
    if rango is None:
        return 48  # default para edades extremas
    return rango[2]


def generar_hijos_deseados() -> int:
    """Genera el número de hijos deseados según tabla normalizada."""
    u = random.random()
    acum = 0.0
    for n, p in TABLA_HIJOS_DESEADOS:
        acum += p
        if u < acum:
            return n
    return 6  # más de 5


def generar_num_bebes() -> int:
    """Genera el número de bebés en un parto."""
    u = random.random()
    acum = 0.0
    for n, p in TABLA_EMBARAZO_MULTIPLE:
        acum += p
        if u < acum:
            return n
    return 1


def generar_duracion_duelo(edad_anios: float) -> int:
    """Genera duración del duelo en meses (exponencial)."""
    lam = obtener_tiempo_duelo(edad_anios)
    duracion = random.expovariate(1.0 / lam)
    return max(1, int(round(duracion)))
