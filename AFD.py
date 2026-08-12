#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os


if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

class AutomataFinitoDeterminista:
    def __init__(self):
        self.Q = set()           # Conjunto de estados
        self.sigma = set()       # Alfabeto de entrada
        self.f = {}              # Función de transición: (estado, simbolo) -> estado_destino
        self.q0 = None           # Estado inicial
        self.F = set()           # Conjunto de estados finales / de aceptación

    def cargar_configuracion(self, ruta_conf):
        """
        Lee y parsea el archivo de configuración del autómata.
        Soporta encabezados explícitos para Q, SIGMA/ALFABETO, Q0/ESTADO_INICIAL, F/ESTADOS_FINALES y F_TRANSICION/TRANSICIONES.
        """
        if not os.path.exists(ruta_conf):
            raise FileNotFoundError(f"El archivo de configuración '{ruta_conf}' no existe.")

        with open(ruta_conf, 'r', encoding='utf-8') as file:
            lineas = file.readlines()

        seccion_actual = None

        for num_linea, linea_raw in enumerate(lineas, start=1):
            # Limpiar comentarios y espacios
            linea = linea_raw.split('#')[0].strip()
            if not linea:
                continue

            # Detectar encabezados principales
            linea_upper = linea.upper()
            if linea_upper.startswith("Q:") or linea_upper.startswith("ESTADOS:"):
                contenido = linea.split(':', 1)[1].strip()
                self.Q = {s.strip() for s in contenido.split(',') if s.strip()}
                seccion_actual = None
            elif linea_upper.startswith("SIGMA:") or linea_upper.startswith("ALFABETO:"):
                contenido = linea.split(':', 1)[1].strip()
                self.sigma = {s.strip() for s in contenido.split(',') if s.strip()}
                seccion_actual = None
            elif linea_upper.startswith("Q0:") or linea_upper.startswith("ESTADO_INICIAL:"):
                contenido = linea.split(':', 1)[1].strip()
                self.q0 = contenido
                seccion_actual = None
            elif linea_upper.startswith("F:") or linea_upper.startswith("ESTADOS_FINALES:") or linea_upper.startswith("ESTADOS_ACEPTACION:"):
                contenido = linea.split(':', 1)[1].strip()
                self.F = {s.strip() for s in contenido.split(',') if s.strip()}
                seccion_actual = None
            elif linea_upper.startswith("F_TRANSICION:") or linea_upper.startswith("TRANSICIONES:"):
                seccion_actual = "TRANSICIONES"
                partes = linea.split(':', 1)
                if len(partes) > 1 and partes[1].strip():
                    self._parsear_transicion(partes[1].strip(), num_linea)
            elif seccion_actual == "TRANSICIONES":
                self._parsear_transicion(linea, num_linea)

        self.validar_quintupla()

    def _parsear_transicion(self, linea, num_linea):
        """
        Parsea una regla de transición con formato: origen, simbolo -> destino
        """
        if "->" not in linea:
            raise ValueError(f"Sintaxis inválida en línea {num_linea}: '{linea}'. Se esperaba 'origen, simbolo -> destino'.")
        
        izq, destino = linea.split("->")
        izq = izq.strip()
        destino = destino.strip()

        if "," not in izq:
            raise ValueError(f"Sintaxis inválida en línea {num_linea}: '{linea}'. Falta la coma entre origen y símbolo.")
        
        origen, simbolo = izq.split(",", 1)
        origen = origen.strip()
        simbolo = simbolo.strip()

        clave = (origen, simbolo)
        if clave in self.f:
            raise ValueError(f"Error de determinismo en línea {num_linea}: Transición duplicada para ({origen}, '{simbolo}').")

        self.f[clave] = destino

    def validar_quintupla(self):
        """
        Valida las propiedades formales de la quíntupla A = (Q, Σ, f, q0, F).
        """
        if not self.Q:
            raise ValueError("Error en la configuración: El conjunto de estados Q no puede estar vacío.")
        if not self.sigma:
            raise ValueError("Error en la configuración: El alfabeto Σ no puede estar vacío.")
        if not self.q0:
            raise ValueError("Error en la configuración: El estado inicial q0 no ha sido definido.")
        if self.q0 not in self.Q:
            raise ValueError(f"Error formal: El estado inicial q0='{self.q0}' no pertenece a Q={self.Q}.")
        if not self.F.issubset(self.Q):
            estados_invalidos = self.F - self.Q
            raise ValueError(f"Error formal: Los estados finales F={estados_invalidos} no son un subconjunto de Q.")

        # Validar consistencia de las transiciones en f: Q x Σ -> Q
        for (origen, simbolo), destino in self.f.items():
            if origen not in self.Q:
                raise ValueError(f"Error formal en transición f: El estado de origen '{origen}' no pertenece a Q.")
            if simbolo not in self.sigma:
                raise ValueError(f"Error formal en transición f: El símbolo '{simbolo}' no pertenece al alfabeto Σ.")
            if destino not in self.Q:
                raise ValueError(f"Error formal en transición f: El estado destino '{destino}' no pertenece a Q.")

    def procesar_cadena(self, cadena):
        """
        Evalúa una cadena de entrada en el autómata.
        Retorna:
          - aceptada (bool)
          - traza (lista de tuplas (estado_actual, simbolo, estado_siguiente))
          - mensaje_error (str o None si la cadena contiene símbolos ajenos a Σ)
        """
        estado_actual = self.q0
        traza = []

        if cadena == "" or cadena == "ε":
            # Cadena vacía
            es_aceptada = estado_actual in self.F
            return es_aceptada, traza, None

        for idx, simbolo in enumerate(cadena):
            if simbolo not in self.sigma:
                error = f"Carácter inválido '{simbolo}' en posición {idx+1} (no pertenece a Σ={sorted(list(self.sigma))})"
                return False, traza, error

            clave = (estado_actual, simbolo)
            if clave not in self.f:
                # Transición no definida (estado trampa/indefinido)
                error = f"Transición no definida para f({estado_actual}, '{simbolo}')"
                return False, traza, error

            estado_siguiente = self.f[clave]
            traza.append((estado_actual, simbolo, estado_siguiente))
            estado_actual = estado_siguiente

        es_aceptada = estado_actual in self.F
        return es_aceptada, traza, None

    def formatear_traza(self, traza, estado_final):
        """
        Genera una representación visual clara de la secuencia de movimiento.
        """
        if not traza:
            return f"[{self.q0}] (cadena vacía ε)"
        
        pasos = [f"[{traza[0][0]}]"]
        for _, simbolo, sig in traza:
            pasos.append(f"--({simbolo})--> [{sig}]")
        return " ".join(pasos)


def main():
    print("=" * 70)
    print("      Simulador de AFD")
    print("         Quíntupla Formal: A = (Q, Σ, f, q0, F)")
    print("=" * 70)

    if len(sys.argv) < 3:
        print("\nUso correcto:")
        print("  python AFD.py <archivo_configuracion> <archivo_cadenas>")
        print("\nEjemplo:")
        print("  python AFD.py conf.txt cadenas.txt\n")
        sys.exit(1)

    ruta_conf = sys.argv[1]
    ruta_cadenas = sys.argv[2]

    afd = AutomataFinitoDeterminista()

    # 1. Cargar autómata
    try:
        afd.cargar_configuracion(ruta_conf)
        print(f"\n[+] Autómata cargado exitosamente desde '{ruta_conf}'")
        print(f"    - Q (Estados): {sorted(list(afd.Q))}")
        print(f"    - Σ (Alfabeto): {sorted(list(afd.sigma))}")
        print(f"    - q0 (Estado Inicial): {afd.q0}")
        print(f"    - F (Estados Finales): {sorted(list(afd.F))}")
        print(f"    - Total de reglas en f: {len(afd.f)}")
    except Exception as e:
        print(f"\n[!] Error al cargar la configuración: {e}")
        sys.exit(1)

    # 2. Leer cadenas
    if not os.path.exists(ruta_cadenas):
        print(f"\n[!] Error: El archivo de cadenas '{ruta_cadenas}' no existe.")
        sys.exit(1)

    with open(ruta_cadenas, 'r', encoding='utf-8') as f_cadenas:
        lineas_cadenas = [linea.strip() for linea in f_cadenas.readlines()]

    print(f"\n[+] Procesando cadenas desde '{ruta_cadenas}'...\n")
    print("-" * 70)

    total = 0
    aceptadas = 0
    rechazadas = 0
    errores = 0

    for idx, cadena in enumerate(lineas_cadenas, start=1):
        # Ignorar líneas vacías o de comentarios en cadenas.txt
        if not cadena or cadena.startswith("#"):
            continue

        total += 1
        es_aceptada, traza, error = afd.procesar_cadena(cadena)

        cadena_disp = f"'{cadena}'" if cadena != "" else "ε (cadena vacía)"

        if error:
            errores += 1
            verdicto = "RECHAZADA (ERROR)"
            print(f"Cadena #{idx:02d}: {cadena_disp:<20} | Resultado: {verdicto}")
            print(f"  └─ Detalle: {error}")
        else:
            if es_aceptada:
                aceptadas += 1
                verdicto = "ACEPTADA  [✓]"
            else:
                rechazadas += 1
                verdicto = "RECHAZADA [✗]"

            traza_str = afd.formatear_traza(traza, None)
            print(f"Cadena #{idx:02d}: {cadena_disp:<20} | Resultado: {verdicto}")
            print(f"  └─ Traza de movimientos: {traza_str}")

        print("-" * 70)

    print("                        RESUMEN DE EVALUACIÓN")
    print(f" Total de cadenas evaluadas: {total}")
    pct_ac = (aceptadas / total * 100) if total > 0 else 0
    pct_re = (rechazadas / total * 100) if total > 0 else 0
    print(f" Cadenas ACEPTADAS         : {aceptadas} ({pct_ac:.1f}%)")
    print(f" Cadenas RECHAZADAS        : {rechazadas} ({pct_re:.1f}%)")
    print(f" Cadenas con Error/Inválida: {errores}")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
