# Autómata Finito Determinista (AFD) en Python
**Implementación, Simulación y Análisis Basado en el Ejercicio 3.16 del Libro de Aho**

*Trabajo Práctico para la Asignatura de Teoría de la Computación / Compiladores (5to Semestre Universitario)*

---

## 1. Introducción

El presente proyecto consiste en el desarrollo e implementación de un simulador genérico de **Autómatas Finitos Deterministas (AFD)** escrito en Python (`AFD.py`). El simulador permite configurar cualquier autómata mediante un archivo de texto de configuración (`conf.txt`) y evaluar secuencialmente un conjunto de cadenas de entrada provistas en `cadenas.txt`.

Para validar el funcionamiento del autómata, se toman como caso de estudio los modelos formales descritos en el **Ejercicio 3.16 (Página 149)** del libro clásico de referencia: *Compiladores: Principios, Técnicas y Herramientas* de Alfred V. Aho, Sethi y Ullman. El programa determina si cada cadena pertenece al lenguaje formal aceptado por el autómata y genera la secuencia completa de movimiento (traza de estados).

---

## 2. Fundamento Teórico

### 2.1 Definición Formal del Autómata Finito Determinista (AFD)

Un **Autómata Finito Determinista** es un modelo matemático de computación que reconoce lenguajes regulares. Formalmente, un AFD se define como una **quíntupla**:

$$A = (Q, \Sigma, f, q_0, F)$$

Donde:
* **$Q$**: Conjunto finito de estados ($Q = \{q_0, q_1, \dots, q_n\}$).
* **$\Sigma$**: Alfabeto de entrada (conjunto finito de símbolos permitidos).
* **$f : Q \times \Sigma \to Q$**: Función total de transición, la cual asigna a cada par (estado actual, símbolo leído) un único estado siguiente.
* **$q_0 \in Q$**: Estado inicial desde el cual comienza el procesamiento de la cadena.
* **$F \subseteq Q$**: Conjunto de estados finales o de aceptación.

```
                  ┌───────────────────────────────┐
                  │    Entrada: Símbolo (a ∈ Σ)   │
                  └───────────────┬───────────────┘
                                  │
                                  ▼
┌──────────────────┐      ┌───────────────┐      ┌──────────────────┐
│  Estado Actual   ├─────►│   Función f   ├─────►│ Estado Siguiente │
│     (q ∈ Q)      │      │ (Q x Σ ──► Q) │      │     (q' ∈ Q)     │
└──────────────────┘      └───────────────┘      └──────────────────┘
```

### 2.2 Determinismo vs. No Determinismo (AFD vs. AFND)
En un autómata determinista (**AFD**), para un estado $q$ y un símbolo $a$, existe **exactamente una única transición** $f(q, a) = q'$. No existen ambigüedades ni transiciones vacías ($\epsilon$). En contraste, un autómata no determinista (**AFND**) puede tener múltiples caminos posibles o transiciones $\epsilon$. 

El **Algoritmo de Thompson** (mencionado como Algoritmo 3.3 en la literatura de Aho) permite construir un AFND a partir de una expresión regular, el cual posteriormente se convierte a un **AFD equivalente** mediante la *Construcción de Subconjuntos*.

---

## 3. Análisis del Ejercicio 3.16 (Libro de Aho, Pág. 149)

El Ejercicio 3.16 solicita construir autómatas y mostrar la secuencia de movimientos al procesar la cadena de entrada **`ababbab`** para las siguientes expresiones regulares:

1. **Inciso a)**: $(a \mid b)^*$
   * **Descripción**: Acepta cualquier combinación de $a$ y $b$, incluyendo la cadena vacía $\epsilon$. Es el lenguaje universal sobre $\Sigma = \{a, b\}$.
2. **Inciso b)**: $(a^* \mid b^*)^*$
   * **Descripción**: Equivalente a la expresión del inciso a), acepta cualquier secuencia de $a$ y $b$.
3. **Inciso c)**: $((\epsilon \mid a) b^*)^*$
   * **Descripción**: De igual forma, genera cualquier cadena sobre el alfabeto $\{a, b\}^*$.
4. **Inciso d)**: $(a \mid b)^* a b b (a \mid b)^*$
   * **Descripción**: Es el autómata de patrón estructurado. Acepta todas las cadenas sobre $\{a, b\}$ que contienen la subcadena continua **`abb`**.

### Autómata Determinista para el Inciso d) $(a \mid b)^* a b b (a \mid b)^*$

Para detectar la subcadena `abb`, el autómata requiere 4 estados con las siguientes funciones de memoria:
* **$q_0$**: Estado inicial. No se ha detectado ningún prefijo de `abb`.
* **$q_1$**: Se ha leído el primer carácter `'a'`.
* **$q_2$**: Se ha leído la secuencia `'ab'`.
* **$q_3$**: Estado final / aceptación ($F = \{q_3\}$). Se ha leído la subcadena `'abb'`. Una vez alcanzado este estado, permanece en $q_3$ (estado trampa de aceptación).

```
                      +--- b ---+
                      |         |
                      v         |
(Inicio) ===> (( q0 )) --- a ---> [ q1 ] --- b ---> [ q2 ] --- b ---> ((( q3 ★ )))
                ^                   |                 |                  ^     |
                |                   +------- a -------+                  + a,b +
                |                   v                                    
                +------------------- a ------------------+ (Regreso a q1 si lee 'a')
```

---

## 4. Estructura del Proyecto

El repositorio está organizado con los siguientes archivos:

```text
AFD-Python/
│
├── AFD.py                           # Simulador principal del Autómata (Python 3)
├── conf.txt                         # Configuración del autómata d) (por defecto)
├── conf_a.txt                       # Configuración para inciso a) (a|b)*
├── conf_b.txt                       # Configuración para inciso b) (a*|b*)*
├── conf_c.txt                       # Configuración para inciso c) ((ε|a)b*)*
├── conf_d.txt                       # Configuración para inciso d) (a|b)*abb(a|b)*
├── cadenas.txt                      # Cadenas de prueba (incluye 'ababbab')
├── generate_diagrams.py             # Script auxiliar para generar gráficas PNG
├── diagrama_afd_ejercicio3_16d.png  # Diagrama de estados generado
├── resultados_ejercicio3_16.png     # Gráfica estadística de evaluación
└── README.md                        # Documentación detallada del proyecto
```

---

## 5. Formato de Archivos de Configuración y Cadenas

### 5.1 Formato del Archivo `conf.txt`

El archivo de configuración refleja de forma transparente la quíntupla formal $A = (Q, \Sigma, f, q_0, F)$:

```ini
# Q: Conjunto de estados
Q: q0, q1, q2, q3

# Σ: Alfabeto de entrada
SIGMA: a, b

# q0: Estado inicial (q0 ∈ Q)
Q0: q0

# F: Conjunto de estados finales (F ⊆ Q)
F: q3

# f: Función total de transición (origen, simbolo -> destino)
F_TRANSICION:
q0, a -> q1
q0, b -> q0
q1, a -> q1
q1, b -> q2
q2, a -> q1
q2, b -> q3
q3, a -> q3
q3, b -> q3
```

### 5.2 Formato del Archivo `cadenas.txt`

Cada línea no vacía representa una cadena a ser evaluada por el autómata. Las líneas que inician con `#` son ignoradas.

```text
ababbab
abb
aabbab
babb
ababbabb
ab
baba
a
b
ε
ababbx
```

---

## 6. Resultados de la Evaluación (Caso de Estudio `ababbab`)

Al ejecutar el autómata con el comando `python AFD.py conf.txt cadenas.txt`, se obtiene la evaluación detallada:

### Traza de Movimientos de la Cadena Requerida `ababbab`:

$$q_0 \xrightarrow{a} q_1 \xrightarrow{b} q_2 \xrightarrow{a} q_1 \xrightarrow{b} q_2 \xrightarrow{b} q_3 \xrightarrow{a} q_3 \xrightarrow{b} q_3 \quad (\text{Resultado: ACEPTADA } [✓])$$

### Tabla de Resultados Generales:

| # | Cadena | Subcadena `abb` Presente? | Estado Final Alcanzado | Verdicho |
|---|--------|---------------------------|------------------------|----------|
| 1 | `ababbab` | **Sí** | $q_3 \in F$ | **ACEPTADA [✓]** |
| 2 | `abb` | **Sí** | $q_3 \in F$ | **ACEPTADA [✓]** |
| 3 | `aabbab` | **Sí** | $q_3 \in F$ | **ACEPTADA [✓]** |
| 4 | `babb` | **Sí** | $q_3 \in F$ | **ACEPTADA [✓]** |
| 5 | `ababbabb` | **Sí** | $q_3 \in F$ | **ACEPTADA [✓]** |
| 6 | `ab` | No | $q_2 \notin F$ | **RECHAZADA [✗]** |
| 7 | `baba` | No | $q_1 \notin F$ | **RECHAZADA [✗]** |
| 8 | `a` | No | $q_1 \notin F$ | **RECHAZADA [✗]** |
| 9 | `b` | No | $q_0 \notin F$ | **RECHAZADA [✗]** |
| 10 | `ε` | No | $q_0 \notin F$ | **RECHAZADA [✗]** |
| 11 | `ababbx` | Inválida ($x \notin \Sigma$) | N/A | **RECHAZADA (ERROR)** |

---

## 7. Gráficas y Diagramas Visuales

### 7.1 Diagrama de Transición de Estados ($A = (Q, \Sigma, f, q_0, F)$)

![Diagrama de Estados AFD](diagrama_afd_ejercicio3_16d.png)

### 7.2 Gráfica de Distribución de Resultados

![Gráfica de Resultados](resultados_ejercicio3_16.png)

---

## 8. Guía de Ejecución Paso a Paso

### 8.1 Requisitos Previos

Asegúrate de contar con Python 3 instalado en tu sistema:
```bash
python --version   # O python3 --version
```

Para generar las gráficas visuales (opcional), instala las librerías necesarias:
```bash
pip install matplotlib networkx
```

---

### 8.2 Ejecución en Windows (PowerShell / CMD)

1. Abre la consola de **PowerShell** o **Símbolo del sistema (CMD)**.
2. Navega hasta la carpeta del proyecto:
   ```powershell
   cd C:\Ruta\A\Tu\Carpeta\AFD-Python
   ```
3. Ejecuta el autómata pasando los archivos `conf.txt` y `cadenas.txt`:
   ```powershell
   python AFD.py conf.txt cadenas.txt
   ```
4. Para probar cualquier otra configuración (por ejemplo, el inciso d explícito):
   ```powershell
   python AFD.py conf_d.txt cadenas.txt
   ```
5. Para regenerar los diagramas y gráficas visuales:
   ```powershell
   python generate_diagrams.py
   ```

---

### 8.3 Ejecución en Linux / macOS (Terminal Bash/Zsh)

1. Abre tu terminal.
2. Clona o navega hasta el directorio del proyecto:
   ```bash
   cd ~/Ruta/A/Tu/Carpeta/AFD-Python
   ```
3. Asegura permisos de ejecución (opcional):
   ```bash
   chmod +x AFD.py generate_diagrams.py
   ```
4. Ejecuta el simulador con Python 3:
   ```bash
   python3 AFD.py conf.txt cadenas.txt
   ```
5. Para probar las configuraciones de otros incisos:
   ```bash
   python3 AFD.py conf_a.txt cadenas.txt
   python3 AFD.py conf_b.txt cadenas.txt
   python3 AFD.py conf_c.txt cadenas.txt
   ```
6. Genera las gráficas en Linux:
   ```bash
   python3 generate_diagrams.py
   ```

---

## 9. Conclusión

El simulador desarrollado en Python demuestra cómo la representación formal de un **Autómata Finito Determinista mediante su quíntupla $A = (Q, \Sigma, f, q_0, F)$** se traduce eficientemente en estructuras de datos de código (conjuntos y diccionarios). La solución permite analizar patrones lingüísticos de forma determinista en tiempo $O(n)$, siendo $n$ la longitud de la cadena de entrada, garantizando un recorrido sin ambigüedades.
