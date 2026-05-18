"""Tablas de probabilidades del modelo (mortalidad, embarazo, pareja, duelo, etc.)."""


# Mortalidad: (edad_min, edad_max, prob_hombre, prob_mujer)
TABLA_MORTALIDAD = [
    (0, 12, 0.25, 0.25),
    (12, 45, 0.10, 0.15),
    (45, 76, 0.30, 0.35),
    (76, 125, 0.70, 0.65),
]

# Embarazo: (edad_min, edad_max, prob_rango)
TABLA_EMBARAZO = [
    (12, 15, 0.20),
    (15, 21, 0.45),
    (21, 35, 0.80),
    (35, 45, 0.40),
    (45, 60, 0.20),
    (60, 125, 0.05),
]

# Deseo de pareja: (edad_min, edad_max, prob)
# Interpretación: al entrar al rango se decide UNA vez si desea pareja
TABLA_DESEO_PAREJA = [
    (12, 15, 0.60),
    (15, 21, 0.65),
    (21, 35, 0.80),
    (35, 45, 0.60),
    (45, 60, 0.50),
    (60, 125, 0.20),
]

# Formación de pareja según diferencia de edad: (dif_min, dif_max, prob)
TABLA_FORMACION_PAREJA = [
    (0, 5, 0.45),
    (5, 10, 0.40),
    (10, 15, 0.35),
    (15, 20, 0.25),
    (20, float("inf"), 0.15),
]

# Hijos deseados: (número, prob_original) → normalizada
_HIJOS_RAW = [(1, 0.60), (2, 0.75), (3, 0.35), (4, 0.25), (5, 0.10), (6, 0.05)]
_SUMA_RAW = sum(p for _, p in _HIJOS_RAW)
TABLA_HIJOS_DESEADOS = [(n, p / _SUMA_RAW) for n, p in _HIJOS_RAW]

# Embarazo múltiple: (num_bebes, prob) → normalizada
_EMB_MULT_RAW = [
    (1, 0.70),
    (2, 0.18),
    (3, 0.08),
    (4, 0.04),
    (5, 0.02),
]
_SUMA_MULT = sum(p for _, p in _EMB_MULT_RAW)
TABLA_EMBARAZO_MULTIPLE = [(n, p / _SUMA_MULT) for n, p in _EMB_MULT_RAW]

# Duelo tras separación/viudez: (edad_min, edad_max, meses)
TABLA_DUELO = [
    (12, 15, 3),
    (15, 21, 6),
    (21, 35, 6),
    (35, 45, 12),
    (45, 60, 24),
    (60, 125, 48),
]
