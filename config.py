"""Constantes y enums globales de la simulación."""

from enum import Enum


MESES_SIMULACION = 1200  # 100 años
MESES_GESTACION = 9
PROB_RUPTURA_ANUAL = 0.20
PROB_SEXO_BEBE = 0.5  # 50% cada sexo

# Población inicial por defecto
M_MUJERES_INICIAL = 50
H_HOMBRES_INICIAL = 50


class Sexo(Enum):
    HOMBRE = "H"
    MUJER = "M"
