from collections import deque
import time
from tabulate import tabulate

class TuringMachine:
    def __init__(self):
        # Definición formal de la Máquina de Turing
        self.formal_definition = {
            'Q': {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'qn'},
            'Σ': {'a', 'b', '*', '#'},
            'Γ': {'a', 'b', '*', '#', 'B'},
            'q0': 'q0',
            'F': {'qn'},
            'B': 'B',
            'δ': self._create_transitions()
        }
        
        self.resultados = {
            'D': {'validas': [], 'invalidas': []},
            'I': {'validas': [], 'invalidas': []}
        }

    def _create_transitions(self):
        return {
            'derecha': {
                # Estado q0 - Verifica el patrón inicial "abaab"
                ('q0', 'a', 'b'): ('q1', 'D', 'D'),  # Lee 'ab'
                ('q1', 'a', 'a'): ('q2', 'D', 'D'),  # Lee 'aa'
                ('q2', 'b', '*'): ('q3', 'D', 'D'),  # Lee 'b*'
                ('q2', 'b', '#'): ('q3', 'D', 'D'),  # Lee 'b#'
                ('q3', '*', '*'): ('q3', 'D', 'D'),  # Lee '**'
                ('q3', '*', '#'): ('q4', 'D', 'D'),  # Lee '*#'
                ('q3', '#', '*'): ('q4', 'D', 'D'),  # Lee '#*'
                ('q3', '#', 'a'): ('q4', 'D', 'D'),  # Lee '#a'
                ('q4', 'a', 'b'): ('q5', 'D', 'D'),  # Lee 'ab'
                ('q5', '*', '*'): ('q5', 'D', 'D'),  # Lee '**'
                ('q5', '*', 'B'): ('qn', 'D', 'D'),  # Fin con *
                ('q5', 'B', '*'): ('qn', 'D', 'D'),  # Fin con *
                ('q5', 'B', 'B'): ('qn', 'D', 'D')   # Fin sin *
            },
            'izquierda': {
                # Transiciones específicas para dirección izquierda
                ('q0', 'b', 'a'): ('q1', 'I', 'I'),    # Inicio con ba del final
                ('q1', 'a', 'a'): ('q2', 'I', 'I'),    # Lee aa
                ('q2', 'b', 'a'): ('q3', 'I', 'I'),    # Lee ba
                ('q3', '*', '*'): ('q3', 'I', 'I'),    # Lee asteriscos después de baaba
                ('q3', '#', '*'): ('q4', 'I', 'I'),    # Lee el separador #
                ('q4', 'b', 'a'): ('q5', 'I', 'I'),    # Lee ba antes del #
                ('q5', '*', '*'): ('q5', 'I', 'I'),    # Lee asteriscos antes de ba
                ('q5', 'B', 'B'): ('qn', 'I', 'I')     # Final
            }
        }
    
    def validar_cadena(self, cadena, direccion):
        if direccion == 'D':
            return self.validar_izquierda_derecha(cadena)
        else:
            return self.validar_derecha_izquierda(cadena)

    def validar_izquierda_derecha(self, cadena):
        try:
            # 1. Debe comenzar con "abaab"
            if not cadena.startswith("abaab"):
                return False

            # 2. Encontrar la posición del #
            pos_hash = cadena.find('#')
            if pos_hash == -1:
                return False

            # 3. Entre "abaab" y "#" solo puede haber asteriscos
            seccion_media = cadena[5:pos_hash]
            if not all(c == '*' for c in seccion_media):
                return False

            # 4. Después del # debe venir "ab"
            resto = cadena[pos_hash + 1:]
            if not resto.startswith("ab"):
                return False

            # 5. Después de "ab" solo puede haber asteriscos
            final = resto[2:]
            if not all(c == '*' for c in final):
                return False

            return True
        except:
            return False

    def validar_derecha_izquierda(self, cadena):
        try:
            # 1. Separar la cadena por el #
            partes = cadena.split('#')
            if len(partes) != 2:
                return False
            
            parte_izq, parte_der = partes
            
            # 2. La parte derecha debe ser "baaba"
            if not parte_der.endswith("baaba"):
                return False
            
            # 3. Los caracteres antes de "baaba" en la parte derecha deben ser asteriscos
            asteriscos_der = parte_der[:-5]
            if not all(c == '*' for c in asteriscos_der):
                return False
            
            # 4. La parte izquierda debe terminar en "ba"
            if not parte_izq.endswith("ba"):
                return False
            
            # 5. Los caracteres antes de "ba" en la parte izquierda deben ser asteriscos
            asteriscos_izq = parte_izq[:-2]
            if not all(c == '*' for c in asteriscos_izq):
                return False
            
            return True
        except:
            return False

    def mostrar_especificacion_formal(self):
        print("\nEspecificación Formal de la Máquina de Turing de 2 Cintas:")
        print("=" * 60)
        print("M = (Q, Σ, Γ, δ, q0, B, F)")
        print("-" * 60)
        print(f"Q = {self.formal_definition['Q']}")
        print(f"Σ = {self.formal_definition['Σ']}")
        print(f"Γ = {self.formal_definition['Γ']}")
        print(f"q0 = {self.formal_definition['q0']}")
        print(f"B = {self.formal_definition['B']}")
        print(f"F = {self.formal_definition['F']}")

    def mostrar_lectura_paso_a_paso(self, cinta1, cinta2, direccion):
        print("\nLectura paso a paso de las cintas:")
        print("=" * 50)
        
        # Asegurar que ambas cintas tengan la misma longitud
        max_len = max(len(cinta1), len(cinta2))
        cinta1 = cinta1 + ['B'] * (max_len - len(cinta1))
        cinta2 = cinta2 + ['B'] * (max_len - len(cinta2))
        
        # Mostrar estado inicial
        print("\nEstado inicial de las cintas:")
        print("Cinta 1:", " ".join(cinta1))
        print("Cinta 2:", " ".join(cinta2))
        
        for i in range(max_len):
            print(f"\nPaso {i + 1}:")
            if direccion == 'D':
                pos = i
                print(f"Leyendo de izquierda a derecha - Posición {pos}")
            else:
                pos = max_len - 1 - i
                print(f"Leyendo de derecha a izquierda - Posición {pos}")
            
            print(f"Leyendo de Cinta 1: {cinta1[pos]}")
            print(f"Leyendo de Cinta 2: {cinta2[pos]}")
            self._mostrar_estado_cintas(cinta1, cinta2, pos)
            time.sleep(0.5)

    def _mostrar_estado_cintas(self, cinta1, cinta2, pos):
        def format_cinta(cinta, pos):
            return ' '.join([f"[{c}]" if i == pos else f" {c} " for i, c in enumerate(cinta)])
        
        print("\nEstado actual de las cintas:")
        print("Cinta 1:", format_cinta(cinta1, pos))
        print("Cinta 2:", format_cinta(cinta2, pos))

    def generar_arbol_derivacion(self, cadena):
        print(f"\nÁrbol de derivación para '{cadena}':")
        print("S")
        self._generar_arbol_rec(cadena, 1)

    def _generar_arbol_rec(self, cadena, nivel):
        if not cadena:
            return
        print("  " * nivel + "|")
        print("  " * nivel + f"+- {cadena[0]}")
        self._generar_arbol_rec(cadena[1:], nivel + 1)

    def procesar_cadena(self, cadena, direccion):
        print(f"\nProcesando cadena: {cadena}")
        print(f"Dirección: {'Izquierda a Derecha' if direccion == 'D' else 'Derecha a Izquierda'}")
        
        es_valida = self.validar_cadena(cadena, direccion)
        tabla_transicion = []
        tabla_transicion.append(['Estado', 'Símbolo1', 'Símbolo2', 'Siguiente Estado', 'Movimiento'])
        
        # Preparar las cintas
        if direccion == 'I':
            partes = cadena.split('#')
            if len(partes) == 2:
                cinta1 = [c for i, c in enumerate(cadena) if i % 2 == 0]
                cinta2 = [c for i, c in enumerate(cadena) if i % 2 == 1]
                parte_izq, parte_der = partes
                
                print("\nLectura paso a paso de las cintas:")
                print("=" * 50)
                
                estado_actual = 'q0'
                
                # Procesar 'baaba' desde el final
                if parte_der.endswith('baaba'):
                    self._mostrar_estado_cintas(cinta1, cinta2, len(cinta1)-1)
                    tabla_transicion.append(['q0', 'b', 'a', 'q1', 'I/I'])
                    estado_actual = 'q1'
                    time.sleep(0.5)
                    
                    self._mostrar_estado_cintas(cinta1, cinta2, len(cinta1)-2)
                    tabla_transicion.append(['q1', 'a', 'a', 'q2', 'I/I'])
                    estado_actual = 'q2'
                    time.sleep(0.5)
                    
                    self._mostrar_estado_cintas(cinta1, cinta2, len(cinta1)-3)
                    tabla_transicion.append(['q2', 'b', 'a', 'q3', 'I/I'])
                    estado_actual = 'q3'
                    time.sleep(0.5)
                
                # Procesar asteriscos antes de baaba
                asteriscos_der = parte_der[:-5].count('*')
                if asteriscos_der > 0:
                    for i in range(asteriscos_der):
                        self._mostrar_estado_cintas(cinta1, cinta2, len(cinta1)-4-i)
                        tabla_transicion.append(['q3', '*', '*', 'q3', 'I/I'])
                        time.sleep(0.5)
                
                # Procesar separador #
                pos_hash = cadena.find('#')
                self._mostrar_estado_cintas(cinta1, cinta2, pos_hash//2)
                tabla_transicion.append(['q3', '#', '*', 'q4', 'I/I'])
                estado_actual = 'q4'
                time.sleep(0.5)
                
                # Procesar 'ba' antes del #
                if parte_izq.endswith('ba'):
                    self._mostrar_estado_cintas(cinta1, cinta2, (pos_hash//2)-1)
                    tabla_transicion.append(['q4', 'b', 'a', 'q5', 'I/I'])
                    estado_actual = 'q5'
                    time.sleep(0.5)
                
                # Procesar asteriscos iniciales
                asteriscos_izq = parte_izq[:-2].count('*')
                if asteriscos_izq > 0:
                    for i in range(asteriscos_izq):
                        self._mostrar_estado_cintas(cinta1, cinta2, (pos_hash//2)-2-i)
                        tabla_transicion.append(['q5', '*', '*', 'q5', 'I/I'])
                        time.sleep(0.5)
                
                # Estado final
                self._mostrar_estado_cintas(cinta1, cinta2, 0)
                tabla_transicion.append(['q5', 'B', 'B', 'qn', 'I/I'])
                time.sleep(0.5)
        else:
            # Procesamiento dirección derecha
            cinta1 = [c for i, c in enumerate(cadena) if i % 2 == 0]
            cinta2 = [c for i, c in enumerate(cadena) if i % 2 == 1]
            
            print("\nLectura paso a paso de las cintas:")
            print("=" * 50)
            
            estado_actual = 'q0'
            idx = 0
            
            while idx < max(len(cinta1), len(cinta2)) and estado_actual != 'qn':
                self._mostrar_estado_cintas(cinta1, cinta2, idx)
                time.sleep(0.5)
                
                s1 = cinta1[idx] if idx < len(cinta1) else 'B'
                s2 = cinta2[idx] if idx < len(cinta2) else 'B'
                
                transicion_key = (estado_actual, s1, s2)
                transiciones = self.formal_definition['δ']['derecha']
                
                if transicion_key in transiciones:
                    siguiente_estado, mov1, mov2 = transiciones[transicion_key]
                    tabla_transicion.append([
                        estado_actual,
                        s1,
                        s2,
                        siguiente_estado,
                        f"{mov1}/{mov2}"
                    ])
                    estado_actual = siguiente_estado
                else:
                    if not es_valida:
                        tabla_transicion.append([
                            estado_actual,
                            s1,
                            s2,
                            'ERROR',
                            '-'
                        ])
                    break
                
                idx += 1
            
            if es_valida and estado_actual != 'qn':
                self._mostrar_estado_cintas(cinta1, cinta2, idx)
                tabla_transicion.append([estado_actual, 'B', 'B', 'qn', 'D/D'])
                time.sleep(0.5)
        
        # Mostrar proceso
        print("\nProceso de la cinta:")
        for t in tabla_transicion[1:]:
            print(f"Estado: {t[0]} -> {t[3]}, Leyendo: {t[1]},{t[2]}, Movimiento: {t[4]}")
        
        if es_valida:
            self.resultados[direccion]['validas'].append(cadena)
        else:
            self.resultados[direccion]['invalidas'].append(cadena)
        
        return es_valida, tabla_transicion

    def mostrar_resumen(self):
        print("\n" + "="*80)
        print("RESUMEN DE PROCESAMIENTO DE CADENAS")
        print("="*80)
        
        # Resumen dirección derecha
        print("\nCadenas procesadas de Izquierda a Derecha (D):")
        print("-"*60)
        print(f"Total de cadenas válidas: {len(self.resultados['D']['validas'])}")
        if self.resultados['D']['validas']:
            print("\nCadenas válidas:")
            for cadena in self.resultados['D']['validas']:
                print(f"✓ {cadena}")
        
        print(f"\nTotal de cadenas inválidas: {len(self.resultados['D']['invalidas'])}")
        if self.resultados['D']['invalidas']:
            print("\nCadenas inválidas:")
            for cadena in self.resultados['D']['invalidas']:
                print(f"✗ {cadena}")
        
        # Resumen dirección izquierda
        print("\nCadenas procesadas de Derecha a Izquierda (I):")
        print("-"*60)
        print(f"Total de cadenas válidas: {len(self.resultados['I']['validas'])}")
        if self.resultados['I']['validas']:
            print("\nCadenas válidas:")
            for cadena in self.resultados['I']['validas']:
                print(f"✓ {cadena}")
        
        print(f"\nTotal de cadenas inválidas: {len(self.resultados['I']['invalidas'])}")
        if self.resultados['I']['invalidas']:
            print("\nCadenas inválidas:")
            for cadena in self.resultados['I']['invalidas']:
                print(f"✗ {cadena}")
                # Continuación del método mostrar_resumen
        # Estadísticas generales
        total_cadenas = sum(len(v['validas']) + len(v['invalidas']) for v in self.resultados.values())
        total_validas = sum(len(v['validas']) for v in self.resultados.values())
        
        print("\nEstadísticas Generales:")
        print("-"*60)
        print(f"Total de cadenas procesadas: {total_cadenas}")
        print(f"Total de cadenas válidas: {total_validas}")
        print(f"Total de cadenas inválidas: {total_cadenas - total_validas}")
        if total_cadenas > 0:
            print(f"Porcentaje de validez: {(total_validas/total_cadenas)*100:.2f}%")

def procesar_archivo_cadenas(nombre_archivo):
    maquina = TuringMachine()
    todas_las_tablas = []
    
    # Mostrar especificación formal de la máquina
    maquina.mostrar_especificacion_formal()
    
    try:
        with open(nombre_archivo, 'r') as archivo:
            cadenas = archivo.read().splitlines()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {nombre_archivo}")
        return
    
    for i, cadena in enumerate(cadenas, 1):
        print(f"\n{'='*60}")
        print(f"Procesando cadena {i}: {cadena}")
        
        while True:
            direccion = input("Elegir dirección (I/D): ").upper()
            if direccion in ['I', 'D']:
                break
            print("Por favor, ingrese 'I' para izquierda o 'D' para derecha.")
        
        maquina.generar_arbol_derivacion(cadena)
        es_valida, tabla = maquina.procesar_cadena(cadena, direccion)
        todas_las_tablas.append((cadena, tabla, es_valida))
        
        print(f"\nLa cadena es {'válida' if es_valida else 'inválida'}")
    
    # Mostrar resumen final
    maquina.mostrar_resumen()
    
    # Mostrar todas las tablas de transición
    print("\n\nTABLAS DE TRANSICIÓN DE TODAS LAS CADENAS:")
    for cadena, tabla, es_valida in todas_las_tablas:
        print(f"\nCadena: {cadena} ({'válida' if es_valida else 'inválida'})")
        print("-" * 70)
        # Usar tabulate para una mejor presentación
        print(tabulate(tabla, headers="firstrow", tablefmt="grid"))

if __name__ == "__main__":
    procesar_archivo_cadenas('cadenas.txt')