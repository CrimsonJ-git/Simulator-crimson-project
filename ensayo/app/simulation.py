from PySpice.Spice.Parser import SpiceParser
from PySpice.Spice.NgSpice.Shared import NgSpiceShared
import numpy as np
from .Aleatory.events import event
import os
#parser =SpiceParser(path= "simulation/circuit.cir")
class Simulator:
    
    def __init__(self,path):
        self.path = path
        self.transient_analysis = None

    def change(self, resistor, valor=None):  # Agregamos 'self' como primer argumento
        try:
            with open(self.path, 'r') as file:
                lines = file.readlines()

            with open(self.path, 'w') as file:
                for line in lines:
                    if line.startswith(resistor):
                        # Cambiar el valor del resistor
                        partes = line.split()
                        partes[3] = str(valor)  # Asumimos que el valor está en la posición 3
                        line = ' '.join(partes) + '\n'
                    file.write(line)

            #print("Resistor cambiado con éxito.")
            return self.path  # Devolver el path actualizado

        except FileNotFoundError:
            print(f"Archivo {self.path} no encontrado.")
            return None
        except Exception as e:
            print(f"Error al cambiar el resistor: {e}")
            return None
        
    def reset_simulator(self):
        self.transient_analysis = None
        self.circuit = None

    def analysis(self):
        if self.transient_analysis is not None:
            self.reset_simulator()
        parser = SpiceParser(self.path)
        circuit = parser.build_circuit()
        simulator = circuit.simulator(temperature=25, nominal_temperature=25)
        self.transient_analysis = simulator.transient(step_time=0.1, end_time=100)
        return self.transient_analysis        
    
    def switch_all(self):
        resistores = ['R1', 'R2', 'R3', 'R4']
        for resistor in resistores:
            resultado = event()
            if resultado == 'A':
                value = np.random.randint(1500,2000)
                self.change(resistor,value)
            elif resultado == 'B':
                value = np.random.randint(5000,9000)
                self.change(resistor,value)
            else:
                value = np.random.randint(500,1000)
                self.change(resistor,value)
        print("todos los valores cambiados")
        return self.path

    def restart_all(self):
        resistores = ['R1', 'R2', 'R3', 'R4']
        for resistor in resistores:
            self.change(resistor,2000)
        print("All resistances changed to standar work values")
        return self.path   

    def get_values(self):
    # Ejecutar el análisis y obtener los datos
        analysis = self.analysis()
        registro ={}
        # Imprimir nodos
        try:
            for node_name, node_data in analysis.nodes.items():
                node_array = np.array(node_data)  
                node_rms = np.sqrt(np.mean(node_array**2))  # Calcular el RMS
                registro[node_name] = node_rms
        except AttributeError:
            print("El análisis no contiene información sobre nodos.")
        
        
        try:
            for branch_name, branch_data in analysis.branches.items():
                branch_array = np.array(branch_data)
                branch_rms = np.sqrt(np.mean(branch_array**2))  # Calcular el RMS
                registro[branch_name] = branch_rms
        except AttributeError:
            print("El análisis no contiene información sobre ramas.")
        return registro

    def source_data(self,Vs='vsource', current='vs'):
        analysis = self.transient_analysis 
        # Obtener las señales de voltaje y corriente
        Vs = np.array(analysis[Vs].data)  # Tensión de la fuente
        Is = np.array(analysis[current].data)  # Corriente a través de la fuente
        
        # Realizar la FFT y obtener las fases
        phase_Vs = np.angle(np.fft.fft(Vs))  # Fase de la tensión
        phase_Is = np.angle(np.fft.fft(Is))  # Fase de la corriente
        
        # Calcular el desfase entre la tensión y la corriente
        dphase =phase_Vs - phase_Is  # Diferencia de fases entre tensión y corriente
        dphase_degrees = np.degrees(np.mean(dphase))  # Convertir a grados
        
        # Calcular el RMS (valor eficaz) de la tensión y corriente
        Vs_rms = np.sqrt(np.mean(Vs**2))  # RMS de la tensión
        Is_rms = np.sqrt(np.mean(Is**2))  # RMS de la corriente
        
        # Calcular la potencia aparente, activa, reactiva y el factor de potencia
        aparente = Vs_rms * Is_rms
        activa = aparente * np.cos(np.radians(dphase_degrees))  # Convertir el desfase a radianes
        reactiva = aparente * np.sin(np.radians(dphase_degrees))  # Convertir el desfase a radianes
        factor = np.cos(np.radians(dphase_degrees))  # Factor de potencia
        
        # Resultados
        resultados = {
            'activa': activa,
            'reactiva': reactiva,
            'factor': factor,
            'aparente': aparente,
        }
        
        return resultados
    def machine_data(self,V,current):
        analysis = self.transient_analysis  
        #you can use : (Vo_1,l1)(Vo_2,l2)(Vo_3,l3)(Vo_4,l4)

        # Obtener las señales de voltaje y corriente
        Vs = np.array(analysis[V].data)  # Tensión de la fuente
        Is = np.array(analysis[current].data)  # Corriente a través de la fuente
        
        # Realizar la FFT y obtener las fases
        phase_Vs = np.angle(np.fft.fft(Vs))  # Fase de la tensión
        phase_Is = np.angle(np.fft.fft(Is))  # Fase de la corriente
        
        # Calcular el desfase entre la tensión y la corriente
        dphase = np.absolute(phase_Vs - phase_Is)  # Diferencia de fases entre tensión y corriente
        dphase_degrees = np.degrees(np.mean(dphase))  # Convertir a grados
        
        # Calcular el RMS (valor eficaz) de la tensión y corriente
        Vs_rms = np.sqrt(np.mean(Vs**2))  # RMS de la tensión
        Is_rms = np.sqrt(np.mean(Is**2))  # RMS de la corriente
        
        # Calcular la potencia aparente, activa, reactiva y el factor de potencia
        aparente = Vs_rms * Is_rms
        activa = aparente * np.cos(np.radians(dphase_degrees))  # Convertir el desfase a radianes
        reactiva = aparente * np.sin(np.radians(dphase_degrees))  # Convertir el desfase a radianes
        factor = np.cos(np.radians(dphase_degrees))  # Factor de potencia
        
        # Resultados
        resultados = {
            'activa': activa,
            'reactiva': reactiva,
            'factor': factor,
            'aparente': aparente,
        }    
        return resultados


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
netlist_path = os.path.join(BASE_DIR,'app', 'netlist', 'circuit.cir')
sim = Simulator(netlist_path)
