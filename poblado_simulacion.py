"""Punto de entrada de la simulación del poblado."""

from simulacion import SimulacionPoblado
from replicas import ejecutar_replicas


if __name__ == "__main__":
    # --- Ejecución simple (1 réplica detallada) ---
    print("\n>>> SIMULACIÓN INDIVIDUAL DETALLADA <<<\n")
    sim = SimulacionPoblado(n_hombres=50, n_mujeres=50, seed=42)
    sim.simular(verbose=True)

    # --- Ejecución con múltiples réplicas ---
    print("\n\n>>> MÚLTIPLES RÉPLICAS <<<\n")
    ejecutar_replicas(n_replicas=10, n_hombres=50, n_mujeres=50)
