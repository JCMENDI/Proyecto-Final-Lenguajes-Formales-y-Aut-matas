# Proyecto-Final-Lenguajes-Formales-y-Autómatas
Este es el repositorio del proyecto final sobre autómatas, y máquina de Turing, elaborado y creado por el estudiante de 3er año José Carlos Mendizábal Huertas - 1077222

# Máquina de Turing de Dos Cintas
## Proyecto de Lenguajes Formales y de Programación

### Descripción del Proyecto
Este proyecto implementa una Máquina de Turing de dos cintas que procesa y valida cadenas según la expresión regular L = {abaab*#ab*}. La máquina es capaz de procesar las cadenas tanto de izquierda a derecha como de derecha a izquierda.

### Especificación Formal de la Máquina
La máquina de Turing está definida formalmente como:
```
M = (Q, Σ, Γ, δ, q0, B, F)

Donde:
Q = {q0, q1, q2, q3, q4, q5, qn}  // Conjunto de estados
Σ = {a, b}                        // Alfabeto de entrada
Γ = {a, b, *, #, B}              // Alfabeto de la cinta (incluye blank 'B')
q0 = q0                          // Estado inicial
F = {qn}                         // Estados de aceptación
B = B                            // Símbolo blank
```

### Tabla de Símbolos
| Símbolo | Descripción |
|---------|-------------|
| *       | Asterisco (símbolo especial) |
| #       | Separador |
| B       | Símbolo blank |

### Funcionamiento de las Dos Cintas
1. **Primera Cinta**: Lee los símbolos en posiciones impares
2. **Segunda Cinta**: Lee los símbolos en posiciones pares

### Tablas de Transición

#### Transiciones de Izquierda a Derecha
| Estado Actual | Símbolo1 | Símbolo2 | Siguiente Estado | Movimiento |
|--------------|----------|-----------|------------------|------------|
| q0           | a        | b         | q1              | D/D        |
| q1           | a        | a         | q2              | D/D        |
| q2           | b        | *         | q3              | D/D        |
| q2           | b        | #         | q3              | D/D        |
| q3           | *        | *         | q3              | D/D        |
| q3           | *        | #         | q4              | D/D        |
| q3           | #        | *         | q4              | D/D        |
| q3           | #        | a         | q4              | D/D        |
| q4           | a        | b         | q5              | D/D        |
| q5           | *        | *         | q5              | D/D        |
| q5           | B        | B         | qn              | D/D        |

#### Transiciones de Derecha a Izquierda
| Estado Actual | Símbolo1 | Símbolo2 | Siguiente Estado | Movimiento |
|--------------|----------|-----------|------------------|------------|
| q0           | b        | a         | q1              | I/I        |
| q1           | a        | a         | q2              | I/I        |
| q2           | b        | a         | q3              | I/I        |
| q3           | *        | *         | q3              | I/I        |
| q3           | #        | *         | q4              | I/I        |
| q4           | b        | a         | q5              | I/I        |
| q5           | *        | *         | q5              | I/I        |
| q5           | B        | B         | qn              | I/I        |

### Ejemplos de Cadenas Válidas

#### De Izquierda a Derecha
```
abaab#ab
abaab*#ab*
abaab**#ab**
abaab#ab*
abaab*#ab
abaab***#ab*
abaab**#ab**
abaab*#ab***
abaab****#ab
abaab#ab****
```

#### De Derecha a Izquierda
```
ba#baaba
*ba#*baaba
**ba#**baaba
*ba#baaba
ba#*baaba
*ba#***baaba
**ba#**baaba
***ba#*baaba
ba#****baaba
****ba#baaba
```

### Proceso de Validación
Para cada cadena, la máquina:
1. Divide la entrada en dos cintas
2. Procesa los símbolos según la dirección elegida
3. Muestra el estado de las cintas en cada paso
4. Genera una tabla de transiciones
5. Determina si la cadena es válida o no

### Estructura del Código

#### Clases Principales
```python
class TuringMachine:
    def __init__(self):
        # Inicialización de la máquina
        
    def _create_transitions(self):
        # Definición de las transiciones
        
    def procesar_cadena(self, cadena, direccion):
        # Procesamiento de cadenas
        
    def validar_cadena(self, cadena, direccion):
        # Validación de cadenas
```

#### Métodos Importantes
1. `procesar_cadena`: Método principal que maneja el procesamiento de cada cadena
2. `validar_cadena`: Verifica si una cadena cumple con el patrón
3. `mostrar_estado_cintas`: Visualiza el estado actual de las cintas
4. `generar_arbol_derivacion`: Genera el árbol de derivación de la cadena

### Ejemplo de Ejecución

Para una cadena como "abaab#ab":
```
Procesando cadena: abaab#ab
Dirección: Izquierda a Derecha

Estado actual de las cintas:
Cinta 1: [a]  a  b  #  b
Cinta 2: [b]  a  *  a

Estado: q0 -> q1, Leyendo: a,b, Movimiento: D/D
...
```

### Requisitos e Instalación
1. Python 3.x
2. Biblioteca `tabulate` para formateo de tablas

```bash
pip install tabulate
```

### Uso del Programa
1. Crear un archivo `cadenas.txt` con las cadenas a procesar
2. Ejecutar el programa:
```bash
python nombre_del_script.py
```
3. Para cada cadena, elegir la dirección de procesamiento (I/D)

### Limitaciones
- Las cadenas deben seguir el patrón L = {abaab*#ab*}
- Los símbolos especiales son * y #
- La cadena debe tener exactamente un separador #

### Conclusiones
Esta implementación demuestra el funcionamiento de una Máquina de Turing de dos cintas, capaz de procesar cadenas en ambas direcciones y manejar símbolos especiales. La visualización paso a paso y las tablas de transición proporcionan una clara comprensión del proceso de validación.
