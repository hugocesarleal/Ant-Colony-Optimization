import os
import csv
import time
import random
import matplotlib.pyplot as plt
from plotar_Grafo import plotarGrafo 

def inicializarListas(nomeArquivo, feromonioInicial, minimizar):
    arestas = []
    custo = []
    desejabilidade = []
    feromonio = []

    try:
        with open(nomeArquivo, mode='r') as arquivo:
            leitorCsv = csv.DictReader(arquivo, delimiter='\t')
            for linha in leitorCsv:
                origem = int(linha['origem'])
                destino = int(linha['destino'])
                peso = float(linha['custo'])
                arestas.append((origem, destino))
                custo.append(peso)
                
                if minimizar:
                    desejabilidade.append(1 / peso if peso > 0 else 0)
                else:
                    desejabilidade.append(peso if peso > 0 else 0)

                feromonio.append(feromonioInicial)

        fim = max(max(origem, destino) for origem, destino in arestas)

    except FileNotFoundError:
        print(f"Arquivo {nomeArquivo} não encontrado.")
        return None, None, None, None, None
    except KeyError as e:
        print(f"Erro: coluna {e} não encontrada no arquivo CSV.")
        return None, None, None, None, None
    except ValueError as e:
        print(f"Erro ao converter valor: {e}")
        return None, None, None, None, None

    return arestas, custo, desejabilidade, feromonio, fim

def funcaoObjetivo(caminho, arestas, custo):
    custoTotal = 0
    for i in range(len(caminho) - 1):
        for j, (origem, destino) in enumerate(arestas):
            if (origem == caminho[i] and destino == caminho[i + 1]) or (origem == caminho[i + 1] and destino == caminho[i]):
                custoTotal += custo[j]
                break
    return custoTotal

def aco(numFormigas, inicio, fim, arestas, custo, desejabilidade, feromonio, rho, maxIter, minimizar):
    melhorCaminho = []
    melhorCusto = float('inf') if minimizar else float('-inf')
    custosMelhores = []  # Lista para registrar os custos do melhor caminho

    for iteracao in range(maxIter):
        print(f"Progresso: {((iteracao + 1) / maxIter * 100):.2f}% concluído", end='\r')

        caminhosFormigas = []
        custosFormigas = []
        todasArestasPercorridas = []

        feromonioAnterior = feromonio[:]

        for f in range(numFormigas):
            verticeAtual = inicio
            visitados = {verticeAtual}
            caminho = [verticeAtual]
            arestasPercorridas = []

            while verticeAtual != fim:
                arestasViaveis = []
                probabilidades = []

                # Construção de caminhos
                for i, (origem, destino) in enumerate(arestas):
                    if origem == verticeAtual or destino == verticeAtual:
                        proximoVertice = destino if origem == verticeAtual else origem
                        if proximoVertice not in visitados:
                            arestasViaveis.append((verticeAtual, proximoVertice, custo[i], desejabilidade[i], feromonio[i]))

                if arestasViaveis:
                    somatorio = sum(fero * des for _, _, _, des, fero in arestasViaveis)

                    if somatorio > 0:
                        for _, _, _, des, fero in arestasViaveis:
                            probabilidades.append((fero * des) / somatorio)

                        escolhida = random.choices(arestasViaveis, weights=probabilidades, k=1)[0]

                        verticeAtual = escolhida[1]
                        visitados.add(verticeAtual)
                        caminho.append(verticeAtual)
                        arestasPercorridas.append(escolhida)
                    else:
                        break
                else:
                    break

            if verticeAtual == fim:
                custoTotal = funcaoObjetivo(caminho, arestas, custo)
                caminhosFormigas.append(caminho)
                custosFormigas.append(custoTotal)
                todasArestasPercorridas.extend(arestasPercorridas)

        # Atualização do melhor caminho
        if custosFormigas:
            melhorCustoIteracao = min(custosFormigas) if minimizar else max(custosFormigas)

            if (minimizar and melhorCustoIteracao < melhorCusto) or (not minimizar and melhorCustoIteracao > melhorCusto):
                melhorCusto = melhorCustoIteracao
                melhorCaminho = caminhosFormigas[custosFormigas.index(melhorCustoIteracao)]

        # Salvar o custo do melhor caminho da iteração
        custosMelhores.append(melhorCusto)

        # Evaporação do feromônio
        for i in range(len(feromonio)):
            feromonio[i] *= (1 - rho)

        # Adicionando feromônio com base nas arestas percorridas
        for caminho, custoTotal in zip(caminhosFormigas, custosFormigas):
            delta_feromonio = (1 / custoTotal) if minimizar else custoTotal
            for i in range(len(caminho) - 1):
                origem, destino = caminho[i], caminho[i + 1]
                for j, (o, d) in enumerate(arestas):
                    if (o == origem and d == destino) or (o == destino and d == origem):
                        feromonio[j] += delta_feromonio

        # Critério de parada com base na diferença de feromônio
        diferencaFeromonio = max(abs(f - a) for f, a in zip(feromonio, feromonioAnterior))
        if diferencaFeromonio < 0.1:
            print(f"Criterio de parada atingido: diferença de feromônio menor que 0.001 na iteração {iteracao + 1}.")
            break

    return melhorCaminho, melhorCusto, feromonio, custosMelhores

if __name__ == "__main__":

    inicio = time.time()

    nomeArquivo = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'grafo2.csv')

    feromonioInicial = 0.1
    rho = 0.7
    numFormigas = 40
    maxIter = 500
    minimizar = False
    plotar = True
    arestas, custo, desejabilidade, feromonio, fim = inicializarListas(nomeArquivo, feromonioInicial, minimizar)

    if arestas:
        melhorCaminho, melhorCusto, feromonio, custosMelhores = aco(numFormigas, 1, fim, arestas, custo, desejabilidade, feromonio, rho, maxIter, minimizar)
        print(f"Melhor caminho encontrado: {melhorCaminho}")
        print(f"Custo total do melhor caminho: {melhorCusto}")

        fim = time.time()

        print(f"Tempo: {fim-inicio} segundos.")

        if plotar:
            # Plotar gráfico de convergência
            
            plt.plot(custosMelhores)
            plt.title("Convergência do ACO")
            plt.xlabel("Iterações")
            plt.ylabel("Custo do Melhor Caminho")
            plt.grid()
            plt.show()

            plotarGrafo(arestas, melhorCaminho)