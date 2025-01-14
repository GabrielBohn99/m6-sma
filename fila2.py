import queue
import random

a = 1664525
c = 1013904223
M = 2**32
seed = 42

chegada_min = 1
chegada_max = 4
atendimento_fila1_min = 3
atendimento_fila1_max = 4
atendimento_fila2_min = 2
atendimento_fila2_max = 3
total_randoms = 100000

last_random_number = seed

def NextRandom():
    global last_random_number
    last_random_number = (a * last_random_number + c) % M
    return last_random_number / M

def gera_tempo(tempo_min, tempo_max):
    return tempo_min + (tempo_max - tempo_min) * NextRandom()

def simular_fila(num_servidores, capacidade_fila, atendimento_min, atendimento_max, fila_entrada=None):
    fila = queue.Queue(maxsize=capacidade_fila)
    servidores = [0] * num_servidores
    tempo_total = 0
    tempo_estado = [0] * (capacidade_fila + 1)
    perda_clientes = 0
    tempo_atual = 0
    clientes_na_fila = 0
    atendidos = []

    while tempo_atual < total_randoms:
        if fila_entrada:
            if not fila_entrada.empty():
                tempo_chegada = fila_entrada.get()
            else:
                tempo_chegada = gera_tempo(chegada_min, chegada_max)
        else:
            tempo_chegada = gera_tempo(chegada_min, chegada_max)
        
        tempo_atendimento = gera_tempo(atendimento_min, atendimento_max)
        
        if tempo_chegada < tempo_atendimento:
            tempo_atual += tempo_chegada
            if fila.full():
                perda_clientes += 1
            else:
                fila.put(tempo_atual)
                clientes_na_fila += 1
                tempo_estado[clientes_na_fila] += tempo_chegada
        else:
            tempo_atual += tempo_atendimento
            for i in range(num_servidores):
                if servidores[i] <= tempo_atual and not fila.empty():
                    servidores[i] = tempo_atual + tempo_atendimento
                    fila.get()
                    atendidos.append(tempo_atual)
                    clientes_na_fila -= 1
                    tempo_estado[clientes_na_fila] += tempo_atendimento

        tempo_total += max(tempo_chegada, tempo_atendimento)

    print(f"\nSimulação G/G/{num_servidores}/{capacidade_fila}")
    for i in range(capacidade_fila + 1):
        probabilidade = tempo_estado[i] / tempo_total
        print(f"Estado {i} clientes: Tempo acumulado = {tempo_estado[i]}, Probabilidade = {probabilidade:.4f}")
    
    print(f"Clientes perdidos: {perda_clientes}")
    print(f"Tempo global da simulação: {tempo_total:.2f}\n")
    
    return atendidos

if __name__ == "__main__":
    fila1_atendidos = simular_fila(2, 3, atendimento_fila1_min, atendimento_fila1_max)

    simular_fila(1, 5, atendimento_fila2_min, atendimento_fila2_max, fila1_atendidos)