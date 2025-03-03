# Ant Colony Optimization (ACO)

Este repositório apresenta a implementação de um algoritmo baseado na Otimização por Colônia de Formigas (Ant Colony Optimization - ACO) para resolver problemas de busca de caminhos em grafos.

# Publicado em:
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14962790.svg)](https://doi.org/10.5281/zenodo.14962790)

## Descrição do Algoritmo

O algoritmo ACO é inspirado no comportamento de forrageamento das formigas reais, que usam feromônios para encontrar os caminhos mais eficientes entre a origem e o destino. Nesta implementação, o algoritmo busca o melhor caminho em um grafo, minimizando ou maximizando o custo total conforme a configuração do problema.

### Características:
- Leitura de grafos a partir de arquivos CSV.
- Inicialização de feromônios, custos e desejabilidade.
- Atualização iterativa dos feromônios com evaporação e reforço.
- Critérios de parada baseados no número máximo de iterações ou convergência dos feromônios.
- Visualização do grafo e da convergência do algoritmo.

## Estrutura dos Arquivos
- `aco.py`: Implementação principal do algoritmo ACO.
- `plotar_Grafo.py`: Script para visualização gráfica do grafo e do melhor caminho encontrado.
- `grafo1.csv`, `grafo2.csv`, `grafo3.csv`: Arquivos de grafos de teste, contendo respectivamente 12, 20 e 100 vértices, e 25, 190 e 8020 arestas.

## Dependências
- Python 3.8 ou superior
- Bibliotecas:
  - `matplotlib`
  - `random`
  - `os`
  - `csv`
  - `time`

## Como Executar

1. **Certifique-se de que os arquivos estão organizados na seguinte estrutura:**
   ```
   /caminho/do/projeto/
   |— aco.py
   |— plotar_Grafo.py
   |— grafo1.csv
   |— grafo2.csv
   |— grafo3.csv
   ```

2. **Execute o script `aco.py`:**
   ```bash
   python aco.py
   ```

3. **Parâmetros configuráveis:**
   - Nome do arquivo do grafo (`nomeArquivo`).
   - Parâmetros do algoritmo (como `rho`, `numFormigas` e `maxIter`).
   - Escolha de minimizar ou maximizar o custo (`minimizar`).
   - Opção de plotar os resultados (`plotar`).

## Resultados Esperados

- **Melhor Caminho:** O caminho mais eficiente entre o vértice de origem e o de destino, considerando o custo total.
- **Gráfico de Convergência:** Uma representação da evolução do custo do melhor caminho ao longo das iterações.
- **Visualização do Grafo:** Mostra o grafo com destaque para o melhor caminho encontrado.

## Exemplo de Saída

```plaintext
Processo: 0.00% concluído.
...
Processo: 100.00% concluído.
Melhor caminho encontrado: [1, 5, 8, 10, 12]
Custo total do melhor caminho: 15.8
Tempo: 10.24 segundos.
```

## Notas Adicionais

- Certifique-se de que os arquivos CSV estejam formatados corretamente, com as seguintes colunas: `origem`, `destino`, `custo`.
- A escolha dos parâmetros, como o número de formigas e o fator de evaporação, pode impactar significativamente o desempenho do algoritmo.
