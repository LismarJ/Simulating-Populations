
import random
from dataclasses import dataclass, field
from typing import Optional, Tuple

from config import Sexo
from tablas import TABLA_DESEO_PAREJA
from probabilidades import (
    edad_a,
    buscar_rango,
    obtener_deseo_pareja_prob,
    generar_hijos_deseados,
    generar_duracion_duelo,
)


@dataclass
class Persona:
    id: int
    sexo: Sexo
    edad_meses: int  
    viva: bool = True

    pareja: Optional["Persona"] = field(default=None, repr=False)
    desea_pareja: bool = False
    en_duelo: bool = False
    fin_duelo_mes: int = 0 
    _rango_deseo_actual: Tuple[float, float] = field(default=(0, 0), repr=False)

    # Reproducción
    hijos_deseados: int = 0
    hijos_tenidos: int = 0
    embarazada: bool = False  # solo para mujeres
    mes_concepcion: int = 0

    def __post_init__(self):
        self.hijos_deseados = generar_hijos_deseados()
        self._evaluar_deseo_pareja()

    @property
    def edad_a(self) -> float:
        return edad_a(self.edad_meses)

    @property
    def tiene_pareja(self) -> bool:
        return self.pareja is not None

    @property
    def disponible_para_pareja(self) -> bool:
        return (self.viva
                and not self.tiene_pareja
                and not self.en_duelo
                and self.desea_pareja
                and self.edad_a >= 12)

    def _obtener_rango_actual_deseo(self) -> Tuple[float, float]:
        rango = buscar_rango(TABLA_DESEO_PAREJA, self.edad_a)
        if rango:
            return (rango[0], rango[1])
        return (-1, -1)

    def _evaluar_deseo_pareja(self):
        """Evalúa una vez si desea pareja al entrar en un nuevo rango."""
        rango_actual = self._obtener_rango_actual_deseo()
        if rango_actual != self._rango_deseo_actual:
            self._rango_deseo_actual = rango_actual
            if not self.en_duelo and not self.tiene_pareja:
                prob = obtener_deseo_pareja_prob(self.edad_a)
                self.desea_pareja = random.random() < prob

    def envejecer(self):
        """Incrementa la edad en 1 mes y re-evalúa deseo de pareja si cambió de rango."""
        self.edad_meses += 1
        self._evaluar_deseo_pareja()

    def morir(self, mes_actual: int):
        """Procesa la muerte de la persona."""
        self.viva = False
        if self.pareja is not None:
            pareja = self.pareja
            pareja.pareja = None
            pareja.en_duelo = True
            pareja.desea_pareja = False
            duracion = generar_duracion_duelo(pareja.edad_a)
            pareja.fin_duelo_mes = mes_actual + duracion
            self.pareja = None

    def iniciar_duelo(self, mes_actual: int):
        """Inicia período de duelo tras separación."""
        self.en_duelo = True
        self.desea_pareja = False
        duracion = generar_duracion_duelo(self.edad_a)
        self.fin_duelo_mes = mes_actual + duracion

    def terminar_duelo(self):
        """Termina el período de duelo."""
        self.en_duelo = False
        prob = obtener_deseo_pareja_prob(self.edad_a)
        self.desea_pareja = random.random() < prob
