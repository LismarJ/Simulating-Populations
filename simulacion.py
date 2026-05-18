"""Motor de simulación del poblado."""

import random
import statistics
from typing import List

from config import (
    Sexo,
    MESES_SIMULACION,
    MESES_GESTACION,
    PROB_RUPTURA_ANUAL,
    PROB_SEXO_BEBE,
    H_HOMBRES_INICIAL,
    M_MUJERES_INICIAL,
)
from persona import Persona
from probabilidades import (
    prob_mensual,
    obtener_prob_muerte_mensual,
    obtener_prob_embarazo_mensual,
    obtener_prob_formacion_pareja,
    generar_num_bebes,
)


class SimulacionPoblado:

    def __init__(self, n_hombres: int = H_HOMBRES_INICIAL,
                 n_mujeres: int = M_MUJERES_INICIAL, seed: int = None):
        if seed is not None:
            random.seed(seed)

        self.mes_actual = 0
        self.siguiente_id = 0
        self.personas: List[Persona] = []

        # Estadísticas por mes
        self.hist_poblacion: List[int] = []
        self.hist_nacimientos: List[int] = []
        self.hist_muertes: List[int] = []
        self.hist_parejas: List[int] = []
        self.hist_hombres: List[int] = []
        self.hist_mujeres: List[int] = []

        # Contadores globales
        self.total_nacimientos = 0
        self.total_muertes = 0
        self.total_parejas_formadas = 0
        self.total_rupturas = 0

        self._inicializar_poblacion(n_hombres, n_mujeres)

    def _nuevo_id(self) -> int:
        self.siguiente_id += 1
        return self.siguiente_id

    def _inicializar_poblacion(self, n_hombres: int, n_mujeres: int):
        """Crea la población inicial con edades U(0, 100)."""
        for _ in range(n_hombres):
            edad_anios = random.uniform(0, 100)
            edad_meses = int(edad_anios * 12)
            p = Persona(id=self._nuevo_id(), sexo=Sexo.HOMBRE, edad_meses=edad_meses)
            self.personas.append(p)

        for _ in range(n_mujeres):
            edad_anios = random.uniform(0, 100)
            edad_meses = int(edad_anios * 12)
            p = Persona(id=self._nuevo_id(), sexo=Sexo.MUJER, edad_meses=edad_meses)
            self.personas.append(p)

    @property
    def personas_vivas(self) -> List[Persona]:
        return [p for p in self.personas if p.viva]

    @property
    def num_parejas(self) -> int:
        count = sum(1 for p in self.personas_vivas if p.tiene_pareja)
        return count // 2  # cada pareja se cuenta dos veces

    def _paso_envejecer(self):
        for p in self.personas_vivas:
            p.envejecer()

   
    def _paso_mortalidad(self) -> int:
        muertes = 0
        for p in list(self.personas_vivas):
            prob = obtener_prob_muerte_mensual(p.edad_a, p.sexo)
            if random.random() < prob:
                p.morir(self.mes_actual)
                muertes += 1
        return muertes

   
    def _paso_fin_duelo(self):
        for p in self.personas_vivas:
            if p.en_duelo and self.mes_actual >= p.fin_duelo_mes:
                p.terminar_duelo()

    def _paso_formacion_parejas(self) -> int:
        hombres_disp = [p for p in self.personas_vivas
                        if p.sexo == Sexo.HOMBRE and p.disponible_para_pareja]
        mujeres_disp = [p for p in self.personas_vivas
                        if p.sexo == Sexo.MUJER and p.disponible_para_pareja]

        random.shuffle(hombres_disp)
        random.shuffle(mujeres_disp)

        parejas_formadas = 0
        mujeres_emparejadas = set()

        for h in hombres_disp:
            if h.tiene_pareja:
                continue
            for m in mujeres_disp:
                if m.id in mujeres_emparejadas or m.tiene_pareja:
                    continue

                dif_edad = abs(h.edad_a - m.edad_a)
                prob = obtener_prob_formacion_pareja(dif_edad)

                if random.random() < prob:
                    h.pareja = m
                    m.pareja = h
                    h.desea_pareja = False
                    m.desea_pareja = False
                    mujeres_emparejadas.add(m.id)
                    parejas_formadas += 1
                    break

        return parejas_formadas


    def _paso_rupturas(self) -> int:
        p_rup_mensual = prob_mensual(PROB_RUPTURA_ANUAL, 12)

        rupturas = 0
        parejas_procesadas = set()

        for p in self.personas_vivas:
            if p.tiene_pareja and p.id not in parejas_procesadas:
                pareja = p.pareja
                parejas_procesadas.add(p.id)
                parejas_procesadas.add(pareja.id)

                if random.random() < p_rup_mensual:
                    p.pareja = None
                    pareja.pareja = None
                    p.iniciar_duelo(self.mes_actual)
                    pareja.iniciar_duelo(self.mes_actual)
                    rupturas += 1

        return rupturas

     
    def _paso_embarazos(self):
        for p in self.personas_vivas:
            if (p.sexo == Sexo.MUJER
                    and p.tiene_pareja
                    and not p.embarazada
                    and p.edad_a >= 12):

                # Ninguno de los dos debe haber alcanzado su PROPIO máximo deseado.
                if p.hijos_tenidos >= p.hijos_deseados:
                    continue
                if p.pareja.hijos_tenidos >= p.pareja.hijos_deseados:
                    continue

                prob = obtener_prob_embarazo_mensual(p.edad_a)
                if random.random() < prob:
                    p.embarazada = True
                    p.mes_concepcion = self.mes_actual

   
    def _paso_nacimientos(self) -> int:
        nacimientos = 0

        for p in list(self.personas_vivas):
            if p.embarazada and (self.mes_actual - p.mes_concepcion) >= MESES_GESTACION:
                num_bebes = generar_num_bebes()

                for _ in range(num_bebes):
                    sexo_bebe = Sexo.HOMBRE if random.random() < PROB_SEXO_BEBE else Sexo.MUJER
                    bebe = Persona(
                        id=self._nuevo_id(),
                        sexo=sexo_bebe,
                        edad_meses=0
                    )
                    self.personas.append(bebe)
                    nacimientos += 1

                p.hijos_tenidos += num_bebes
                if p.pareja is not None and p.pareja.viva:
                    p.pareja.hijos_tenidos += num_bebes

                p.embarazada = False

        return nacimientos

   
    # BUCLE PRINCIPAL
   
    def simular(self, verbose: bool = True):
        """Ejecuta la simulación completa."""
        if verbose:
            print("=" * 70)
            print(" SIMULACIÓN: POBLADO EN EVOLUCIÓN")
            print(f" Población inicial: {len(self.personas)} "
                  f"({H_HOMBRES_INICIAL}H / {M_MUJERES_INICIAL}M)")
            print(f" Duración: {MESES_SIMULACION} meses ({MESES_SIMULACION // 12} años)")
            print("=" * 70)

        for mes in range(MESES_SIMULACION):
            self.mes_actual = mes

            self._paso_envejecer()

            muertes = self._paso_mortalidad()
            self.total_muertes += muertes

            self._paso_fin_duelo()

            nuevas_parejas = self._paso_formacion_parejas()
            self.total_parejas_formadas += nuevas_parejas

            rupturas = self._paso_rupturas()
            self.total_rupturas += rupturas

            self._paso_embarazos()

            nacimientos = self._paso_nacimientos()
            self.total_nacimientos += nacimientos

            # Registrar estadísticas
            vivas = self.personas_vivas
            n_vivos = len(vivas)
            n_h = sum(1 for p in vivas if p.sexo == Sexo.HOMBRE)
            n_m = sum(1 for p in vivas if p.sexo == Sexo.MUJER)

            self.hist_poblacion.append(n_vivos)
            self.hist_nacimientos.append(nacimientos)
            self.hist_muertes.append(muertes)
            self.hist_parejas.append(self.num_parejas)
            self.hist_hombres.append(n_h)
            self.hist_mujeres.append(n_m)

            # Reporte cada 10 años
            if verbose and (mes + 1) % 120 == 0:
                anio = (mes + 1) // 12
                print(f"  Año {anio:>3d}: Pob={n_vivos:>5d} "
                      f"(H={n_h:>4d}, M={n_m:>4d}) | "
                      f"Parejas={self.num_parejas:>3d} | "
                      f"Nac(año)={sum(self.hist_nacimientos[-120:]):>4d} | "
                      f"Def(año)={sum(self.hist_muertes[-120:]):>4d}")

            if n_vivos == 0:
                if verbose:
                    print(f"\n  ¡Población extinta en el mes {mes} "
                          f"(año {mes / 12:.1f})!")
                break

        if verbose:
            self._imprimir_resumen()

   
    # RESUMEN FINAL
   
    def _imprimir_resumen(self):
        vivas = self.personas_vivas
        print("\n" + "=" * 70)
        print(" RESUMEN FINAL")
        print("=" * 70)

        print(f"\n  Población final:        {len(vivas)}")
        print(f"  Hombres vivos:          {sum(1 for p in vivas if p.sexo == Sexo.HOMBRE)}")
        print(f"  Mujeres vivas:          {sum(1 for p in vivas if p.sexo == Sexo.MUJER)}")
        print(f"  Parejas activas:        {self.num_parejas}")

        print(f"\n  Total nacimientos:      {self.total_nacimientos}")
        print(f"  Total defunciones:      {self.total_muertes}")
        print(f"  Crecimiento neto:       {self.total_nacimientos - self.total_muertes}")
        print(f"  Total parejas formadas: {self.total_parejas_formadas}")
        print(f"  Total rupturas:         {self.total_rupturas}")

        if vivas:
            edades = [p.edad_a for p in vivas]
            print(f"\n  Edad promedio:          {statistics.mean(edades):.1f} años")
            print(f"  Edad mediana:           {statistics.median(edades):.1f} años")
            print(f"  Persona más joven:      {min(edades):.1f} años")
            print(f"  Persona más vieja:      {max(edades):.1f} años")

        if vivas:
            print("\n  Distribución por rango de edad:")
            rangos = [(0, 12), (12, 18), (18, 30), (30, 45), (45, 60), (60, 76), (76, 125)]
            for rmin, rmax in rangos:
                count = sum(1 for p in vivas if rmin <= p.edad_a < rmax)
                barra = "#" * (count * 40 // len(vivas)) if vivas else ""
                print(f"    {rmin:>3d}-{rmax:<3d}: {count:>4d} ({100*count/len(vivas):5.1f}%) {barra}")

        if self.hist_poblacion:
            pob_max = max(self.hist_poblacion)
            pob_min = min(self.hist_poblacion)
            mes_max = self.hist_poblacion.index(pob_max)
            mes_min = self.hist_poblacion.index(pob_min)
            print(f"\n  Población máxima:       {pob_max} (año {mes_max/12:.1f})")
            print(f"  Población mínima:       {pob_min} (año {mes_min/12:.1f})")

        print("=" * 70)
