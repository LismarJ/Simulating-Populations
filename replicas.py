"""Ejecución de múltiples réplicas y estadísticas agregadas."""

import statistics

from config import H_HOMBRES_INICIAL, M_MUJERES_INICIAL
from simulacion import SimulacionPoblado


def ejecutar_replicas(n_replicas: int = 10, n_hombres: int = H_HOMBRES_INICIAL,
                      n_mujeres: int = M_MUJERES_INICIAL, verbose_cada: bool = False):
    """Ejecuta múltiples réplicas y reporta estadísticas."""

    print("\n" + "=" * 70)
    print(f" EJECUCIÓN DE {n_replicas} RÉPLICAS")
    print(f" Población inicial: {n_hombres}H + {n_mujeres}M = {n_hombres + n_mujeres}")
    print("=" * 70)

    resultados_pob_final = []
    resultados_nacimientos = []
    resultados_muertes = []
    resultados_pob_max = []
    pob_anual_acum = {}  # año -> lista de poblaciones

    for i in range(n_replicas):
        sim = SimulacionPoblado(n_hombres=n_hombres, n_mujeres=n_mujeres, seed=i * 42 + 7)
        sim.simular(verbose=verbose_cada)

        pob_final = len(sim.personas_vivas)
        resultados_pob_final.append(pob_final)
        resultados_nacimientos.append(sim.total_nacimientos)
        resultados_muertes.append(sim.total_muertes)
        resultados_pob_max.append(max(sim.hist_poblacion) if sim.hist_poblacion else 0)

        for anio in range(0, 101, 10):
            mes_idx = min(anio * 12, len(sim.hist_poblacion) - 1)
            if mes_idx >= 0:
                if anio not in pob_anual_acum:
                    pob_anual_acum[anio] = []
                pob_anual_acum[anio].append(sim.hist_poblacion[mes_idx])

        if not verbose_cada:
            estado = "EXTINTA" if pob_final == 0 else f"{pob_final} personas"
            print(f"  Réplica {i+1:>2d}/{n_replicas}: {estado} "
                  f"(nac={sim.total_nacimientos}, def={sim.total_muertes})")

    print("\n" + "-" * 70)
    print(" RESUMEN DE RÉPLICAS")
    print("-" * 70)

    def resumen_lista(nombre, datos):
        if not datos:
            return
        media = statistics.mean(datos)
        if len(datos) >= 2:
            desv = statistics.stdev(datos)
            print(f"  {nombre:<30s}: μ={media:>8.1f}  σ={desv:>8.1f}  "
                  f"min={min(datos):>6}  max={max(datos):>6}")
        else:
            print(f"  {nombre:<30s}: {media:>8.1f}")

    resumen_lista("Población final", resultados_pob_final)
    resumen_lista("Total nacimientos", resultados_nacimientos)
    resumen_lista("Total defunciones", resultados_muertes)
    resumen_lista("Población máxima", resultados_pob_max)

    extinciones = sum(1 for p in resultados_pob_final if p == 0)
    print(f"\n  Poblaciones extintas:   {extinciones}/{n_replicas} "
          f"({100*extinciones/n_replicas:.0f}%)")

    print("\n  Evolución promedio por década:")
    for anio in sorted(pob_anual_acum.keys()):
        datos = pob_anual_acum[anio]
        media = statistics.mean(datos)
        max_media = max(statistics.mean(d) for d in pob_anual_acum.values())
        barra = "#" * int(media / max(1, max_media) * 40)
        print(f"    Año {anio:>3d}: {media:>7.1f} personas  {barra}")

    print("=" * 70)
