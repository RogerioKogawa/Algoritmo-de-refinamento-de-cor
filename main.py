#Para executar esse código basta colocar a ordem da matriz no primeiro input
#E as matrizes no segundo e terceiro input(Siga as instruções na função montar_matriz)

import time


#Essa função recebe a matriz inteira, copie cole uma matriz(uma por vez) 
 #e pressione enter, pressione enter de novo para mandar uma linha em branco
#Exemplo com o grafo da lista 3:

# Seja a matriz
# 0101
# 1010
# 0101
# 1010
#Coloque desta forma:
## 0101
# 1010
# 0101
# 1010
#E pressioe enter
#Pressione enter de novo para mandar um input vazio
def montar_matriz(ordem_matriz):
    #Para ler a matriz de uma vez, ao invés de linha por linha utilizei o iter
    #O iter vai fazer uma iteração com o input e vai para quando chegar uma string
    #vazia, por isso é preciso pressionar enter duas vezes, um aviso sera mostrado 
    #após digitar a primeira matriz ser salva
    matriz = list(iter(input, ''))
    matriz_resultante = []

    for i in range(ordem_matriz):
        linha_atual = []
        for j in range(ordem_matriz):
            linha_atual.append(matriz[i][j])
        matriz_resultante.append(linha_atual)
    return matriz

#Depois de calcular a matriz temos essa função que vai calcular as arestas
#Ela percorre toda a matriz e caso o valor seja 1, quer dizer que tem uma aresta
#Então a função armazena essa aresta numa tupla, é preciso adicionar 1 pois a numeração
#seguida começa em 1, ja o loop começa em 0, antes de armazenar eu dou um sorted na tupla
#para ficar mais facil no manuseio desse dado posteriormente, antes de retornar todas as 
#arestas em dou um sorted agora na lista, que é ajustada de maneira lexicográfica
#o conjunto_arestas precisar do set() para não repetir arestas pois o grafo é não ordenado
#Caso n tenha ele a função armazenaria (1,2) e (2,1) por exemplo, e isso é uma redundância.
def arestas_matriz(matriz):
  conjunto_arestas = set()
  
  for i in range(0, len(matriz[0])):
    for j in range(0, len(matriz[0])):
      if matriz[i][j] == "1":
        aresta = tuple(sorted((i+1, j+1)))
        conjunto_arestas.add(aresta)
  return sorted(conjunto_arestas)

def calcular_grau_vertices(conjunto_arestas):
    conjunto_grau_vertices = []
    num_vertices = ordem_matriz 

    for vertice_atual in range(1, num_vertices + 1):
        grau_vertice = 0
        #Calcula quantas vezes o numero do vertice aparece no conjunto de tuplas
        #Como não existem loops(x,x) não é preciso se preocupar numa contagem duplicada
        for x, y in conjunto_arestas:
            if x == vertice_atual:
                grau_vertice += 1
            if y == vertice_atual:
                grau_vertice += 1
        #Armazena o grau do vertice no conjunto_grau vertice como uma tupla
        #em que o primeiro valor identifica o vertice e o segundo é o seu grau
        conjunto_grau_vertices.append((vertice_atual, grau_vertice))
    return conjunto_grau_vertices


#Aqui começa o algoritmo de color refinement, na primeira vez eu vou atribuir uma cor
#igual para os vertices de mesmo grau e depois vou implementar uma coloração de acordo
#com a vizinhança

#Vamos considerar numeros inteiros positivos como cores, em que 0 é uma cor e 1 é uma 
#cor diferente de 0
def colorir_vertices_primeira_vez(grau_vertices):   
  grau_para_cor_map = {}
  proxima_cor_disponivel = 0
  vertices_coloridos = []
  for vertice, grau in grau_vertices:
    if grau not in grau_para_cor_map:
      grau_para_cor_map[grau] = proxima_cor_disponivel
      proxima_cor_disponivel += 1 
            
    cor_do_vertice = grau_para_cor_map[grau]
    vertices_coloridos.append((vertice, cor_do_vertice))
  return vertices_coloridos

#Essa é a segunda etapa de refinamento, que muda a cor de um vertice se no seu grupo
#(mesmo grau inicialmente) se os vizinhos de cada um tiver cores difentes ou em quantidades
#diferentes
def refinar_cores(vertices_coloridos_atuais, conjunto_arestas, ordem_matriz):
    # Inicializa a lista de cores atuais: posição i representa o vértice (i+1)
    cores_atuais = [0] * ordem_matriz
    for vertice, cor in vertices_coloridos_atuais:
        cores_atuais[vertice - 1] = cor

    while True:
        novas_cores = [-1] * ordem_matriz  # Nova coloração
        rotulos = []  # Lista de pares: (cor_atual, cores_vizinhos) para cada vértice

        for i in range(ordem_matriz):
            vizinhos = []
            vertice = i + 1

            for aresta in conjunto_arestas:
                if aresta[0] == vertice:
                    vizinhos.append(aresta[1])
                elif aresta[1] == vertice:
                    vizinhos.append(aresta[0])

            cores_vizinhos = [cores_atuais[v - 1] for v in vizinhos]
            cores_vizinhos.sort()

            rotulo = (cores_atuais[i], cores_vizinhos)
            rotulos.append(rotulo)

        # Agora damos uma nova cor para cada grupo de vértices com o mesmo rótulo
        cores_dadas = []
        nova_cor = 0

        for i in range(ordem_matriz):
            if rotulos[i] not in cores_dadas:
                cores_dadas.append(rotulos[i])
                # Todos os vértices com esse rótulo recebem a mesma cor
                for j in range(ordem_matriz):
                    if rotulos[j] == rotulos[i]:
                        novas_cores[j] = nova_cor
                nova_cor += 1

        # Verifica se as cores mudaram
        if novas_cores == cores_atuais:
            break  
        else:
            cores_atuais = novas_cores  

    resultado_final = []
    for i in range(ordem_matriz):
        resultado_final.append((i + 1, cores_atuais[i]))

    return resultado_final



inicio_tempo = time.process_time()
#Insira o primeiro valor antes do grafo(matriz de incidência), que indica o seu tamanho(ordem)
print("Digite a ordem da matriz")
ordem_matriz = int(input())
#gera a matriz, siga as instruções da função montar_matriz
print("Digite a primeira matriz: ")
matriz = montar_matriz(ordem_matriz)
print("Primeira matriz armazenada")
#calcula as arestas da matriz
conjunto_arestas = arestas_matriz(matriz)
#Cria uma variavel que enumera todos os vertices
conjunto_vertices= [i for i in range(ordem_matriz)]
grau_vertices = calcular_grau_vertices(conjunto_arestas)

#implementa o algoritmo de color refinement
vertices_coloridos_atuais = colorir_vertices_primeira_vez(grau_vertices)
vertices_coloridos_finais = refinar_cores(vertices_coloridos_atuais, conjunto_arestas, ordem_matriz)


#Repete o processo para a segunda matriz, não é preciso inserir a ordem da matriz novamente
print("Insira agora a segunda matriz:")
matriz2 = montar_matriz(ordem_matriz)
print("Segunda matriz armazenada")
conjunto_arestas2 = arestas_matriz(matriz2)
grau_vertices2 = calcular_grau_vertices(conjunto_arestas2)
vertices_coloridos_iniciais2 = colorir_vertices_primeira_vez(grau_vertices2)
vertices_coloridos_finais2 = refinar_cores(vertices_coloridos_iniciais2, conjunto_arestas2, ordem_matriz)

fim_tempo = time.process_time()
#Calcula o tempo total arredondando com 3 casas decimais
tempo_total = fim_tempo - inicio_tempo

cores1 = sorted([cor for m, cor in vertices_coloridos_finais])
cores2 = sorted([cor for n, cor in vertices_coloridos_finais2])

print("|V|     ++++/----  CPU time")
if cores1 == cores2:
  print(f"{ordem_matriz}) n = {ordem_matriz} +++ {tempo_total}")
else:
  print(f"{ordem_matriz}) n = {ordem_matriz} --- {tempo_total}")


