import re
import copy

def le_arq_gramatica(fileName):
    with open(fileName, "r") as f:
        vetorLinhas = []
        vetorLinhas = f.readlines()
        f.close()
        return vetorLinhas

def gram_formal(vetorLinhas):
    listaTerminais = []
    listaVariaveis = []
    dictRegras = {}
    contRegras = 0
    gramFormal = {}

    i = 1                               # TERMINALS
    while vetorLinhas[i][0] != '#':
        listaTerminais.append(vetorLinhas[i][vetorLinhas[i].find("[")+2:vetorLinhas[i].find("]")-1])
        i = i+1

    i = i+1                             # VARIABLES
    while vetorLinhas[i][0] != '#':
        listaVariaveis.append(vetorLinhas[i][vetorLinhas[i].find("[")+2:vetorLinhas[i].find("]")-1])
        i = i+1

    i = i+1                             # STARTER SYMBOL
    simbInicial = vetorLinhas[i][vetorLinhas[i].find("[")+2:vetorLinhas[i].find("]")-1]
    i = i+2

    while i < len(vetorLinhas):         # TO FIND PRODUCTIONS
        contRegras += 1
        regra = []
        vetorLinhas[i] = vetorLinhas[i].split(' > ')
        regra.append(vetorLinhas[i][0][vetorLinhas[i][0].find("[")+2:vetorLinhas[i][0].find("]")-1])

        for j, char in enumerate(vetorLinhas[i][1]):
            if(char == '#' or char == '\n'):
                vetorLinhas[i][1] = vetorLinhas[i][1][:j]
                break

        regra.append(re.findall(r'\[ ([^]]*)\ ]', vetorLinhas[i][1]))
        if(len(regra[1]) <= 1):
            regra[1] = ''.join(regra[1])

        if(contRegras <= 1):
            keyRegra = regra[0]
            dictRegras.setdefault(regra[0],[]).append(regra[1])
        else:
            if(regra[0] != keyRegra):
                keyRegra = regra[0]
                dictRegras.setdefault(regra[0],[]).append(regra[1])
            else:
                dictRegras[keyRegra].append(regra[1])
        i = i+1

    gramFormal['V'] = listaVariaveis
    gramFormal['T'] = listaTerminais
    gramFormal['P'] = dictRegras
    gramFormal['S'] = simbInicial
    print(f"Grammar read from file:\n {gramFormal}")
    return gramFormal

def linhas():
    print("---------------------------------------------------------------------------------------------------------------------------")

# ========================================================================== #
def simplificaProdVazias(gram):
# DEFINIÇÕES ÚTEIS
    linhas()

    for k,v in gram.items():
        if k == 'T':
            terminais = v

    for k,v in gram.items():
        if k == 'V':
            variaveis = v

    for k,v in gram.items():
        if k == 'P':
            producoes = v

    for k,v in gram.items():
        if k == 'S':
            inicial = v

#V1 = set() # 1
#terminais = set(terminais) # 2 - converte Terminais para poder aplicar uniao com V1 e definir o alpha
#alpha = V1.union(terminais)
#terminais = list(terminais) # Terminais volta a ser lista para facilitar tratamentos

# algumas definicoes de variaveis para facilitar
    quantidadeTerminais = len(terminais)
    tamanhoKeys = len(producoes.keys())
    tamanhoValues = len(producoes.values())
    listaKeys = list(producoes.keys())
    listaValues = list(producoes.values())

# ETAPA 1: variaveis que constituem producoes vazias
#### Variaveis que geram diretamente V (palavra vazia): A > V;
#### Sucessivamente, variaveis que indiretamente geram V: B > A;
    print("\n***EMPTY PRODUCTIONS SIMPLIFICATION***\n")
    print("FIRST ROUND:")
    print("FIRST SIMPLIFICATION: empty productions\n")

    produzVazia = set() # definicao de Vε

    linhas()
    print(f"Starter list of productions: {producoes}")
    linhas()

    for x in listaKeys:                                                     # para todos elementos da listaKeys
        for z in producoes[x]:                                              # varre as os valores produzidos por esses elementos
            for y in z:                                                     # e para cada elemento y produzido por um x da listaKeys
                if y == 'V':                                                # testa se ele é um simbolo vazio e caso positivo
                    produzVazia.add(x)                                      # o adiciona ao conjunto produzVazia
                    print(f"{x} was added to \"produzVazia\"\n>>>{produzVazia}\n")
                    break

    P0 = copy.deepcopy(producoes)
    produzVazia2 = produzVazia
    listaKeysAux = list(P0.keys())                                          # atualiza a listaKeys com valores dos elementos atuais de 'P'

    if(produzVazia != set()):
        print(f"Variables that directly produces the empty word: {produzVazia}\n")
    else:
        print("There's no variable that produces the empty word directly.")

    lVazios = []
    # sucessivamente
    while True:
        for x in listaKeysAux:                         # para todos os elementos da listaKeys
            for z in P0[x]:                         # varre os valores produzidos por esses elementos
                for y in z:                         # e para cada elemento y produzido por um x da listaKeys
                    if y in produzVazia:            # testa se ele ja pertence ao conjunto das variaveis que produzem palavras vazias
                        lVazios.append(y)
                if(type(z) == list):
                    if(lVazios == z):
                        produzVazia.add(x)
                        print(f"{x} was added to \"produzVazia\"\n>>>{produzVazia}\n")
                elif(type(z) == str and lVazios != []):
                    if(lVazios[0] == z):
                        produzVazia.add(x)
                        print(f"{x} was added to \"produzVazia\"\n>>>{produzVazia}\n")
                lVazios.clear()

        if(produzVazia == produzVazia2):
            break
        else:
            produzVazia2 = produzVazia

    P1 = copy.deepcopy(P0)
    Pn = copy.deepcopy(P1)
    listaKeysAux = list(P1.keys())

    linhas()
    if(produzVazia != set()):
        print(f"Variables that produces the empty word: {produzVazia}")
    else:
        print("No variable produces the empty word.")
    print(f"Productions stays the same: {P1}")
    print("...END OF FIRST ROUND.\n")


# ETAPA 2: exclusao das producoes vazias
##### Considera apenas as producoes NAO-VAZIAS
##### Cada producao cujo lado direito (corpo) possui uma variavel que gera V (palavra vazia)
######## determina uma producao adicional sem essa variavel

    print("...BEGIN OF SECOND ROUND:")

    print(f"Removing the empty word (if it exists)")
    linhas()
    # REMOVER V
    for x in listaKeysAux:
        for z in Pn[x]:
            for y in z:
                if y == 'V':
                    Pn[x].remove(z)
                    print(f"{z} = empty word. Removed from {x} : {Pn[x]}")
                    if Pn[x] == []:
                        print(f"***'V' was the only one production of {x}, hence: {x} was removed.")
                        del Pn[x]
                        break

    Pvazia = copy.deepcopy(Pn)
    Presultantes = copy.deepcopy(Pvazia)
    listaKeysAux = list(Pvazia.keys())

    linhas()
    print(f"Resulting productions: {Pvazia}")
    linhas()
    if(produzVazia != set()):
        print(f"Variables that produces the empty word: {produzVazia}")
    else:
        print("Again, no variable produces the empty word")
    linhas()

# REMOVER INDIRETAMENTE VAZIAS
    print("Exchanging variables that generates the empty element:\n")

    alfa = []
    for x in listaKeysAux:
        for i, prod in enumerate(Pvazia[x]):            # itera índice e produção
            if(type(prod) == list):
                for k, y in enumerate(prod[:]):         # prod[:] cria uma cópia da prod original porque senão o remove() interfere no loop
                    if y in produzVazia:
                        if(prod[:k] != []):
                            for v in prod[:k]:
                                alfa.append(v)
                        if(prod[k+1:] != []):
                            for v in prod[k+1:]:
                                alfa.append(v)

                        if(len(alfa) >= 2):
                            if(alfa[:] not in Pvazia[x]):
                                Pvazia[x].append(alfa[:])
                                print(f"Production {alfa} is now a subset of {x}: {Pvazia[x]}")
                        else:
                            if(alfa[0] not in Pvazia[x]):
                                Pvazia[x].append(alfa[0])
                                print(f"Production '{alfa[0]}' is now a subset of {x}: {Pvazia[x]}")

                        alfa.clear()

    print("\n...END OF SECOND ROUND.")
    linhas()
    gram['P'] = copy.deepcopy(Pvazia)

    # ETAPA 3: geracao de V (palavra vazia), se necessário
    print("\nROUND THREE:")
    if gram['S'] in produzVazia:        # se a variável inicial produz o elemento vazio,
        gram['P'][gram['S']].append('V')      # adiciona prod. vazia a suas produções
        print(f"Adding the empty production 'V' as subset of {gram['S']}: {gram['P'][gram['S']]}\n")
    else:
        print("It is not necessary to add the empty production.\n")

    print(f"Grammar after empty words simplification:\n{gram}")
    linhas()
    return gram

# =========================================================================== #
def simplificaProdUnitarias(gram):
    print('\n***Null productions simplification***\n')
    for k,v in gram.items():
        if k == 'T':
            terminais = v

    for k,v in gram.items():
        if k == 'V':
            variaveis = v

    for k,v in gram.items():
        if k == 'P':
            producoes = v

    for k,v in gram.items():
        if k == 'S':
            inicial = v

    #V1 = set() # 1
    #terminais = set(terminais) # 2 - converte Terminais para poder aplicar uniao com V1 e definir o alpha
    #alpha = V1.union(terminais)
    #terminais = list(terminais) # Terminais volta a ser lista para facilitar tratamentos

    # algumas definicoes de variaveis para facilitar
    quantidadeTerminais = len(terminais)
    tamanhoKeys = len(producoes.keys())
    tamanhoValues = len(producoes.values())
    listaKeys = list(producoes.keys())
    listaValues = list(producoes.values())

    # função que simplifica produções que substituem variáveis

    print(f"Current productions: {gram['P']}\n")

# dictFechos: dicionário que contem os fechos transitivos; P1: cópia do dicionário de produções
    dictFechos = {}
    dictFechos2 = {}
    P1 = gram['P']

# etapa 1: para cada produção de cada chave contida nas produções, verifica se ela é do tipo A -> A e remove se tiver
    while True:
        for key in listaKeys:
            if key not in dictFechos:
                dictFechos[key] = []
            for prod in gram['P'][key]:
                if(key == prod):
                    gram['P'][key].remove(prod)
                else:
                    if prod in variaveis:                 	  # se a prod. for apenas uma variável,
                        if prod not in dictFechos[key]:		  # e não estiver ainda do fecho
                            dictFechos[key].append(prod)      # põe ela no fecho
                            print(f"Current: {dictFechos}")                # print do passo intermediário
                            P1[key].remove(prod)              # e a remove de P1

            if not dictFechos[key]:                       # se não houver prods. com 1 variável na chave, deleta lista vazia de dictFechos
                del dictFechos[key]

        if(dictFechos == dictFechos2):
            break
        else:
            dictFechos2 = dictFechos

    for key in dictFechos:                            # etapa 2: itera sobre o dictFecho
        for varFecho in dictFechos[key]:
            if varFecho in listaKeys:
                for prodFecho in gram['P'][varFecho]:
                    if prodFecho not in variaveis:        # se a prod. não for apenas uma variável,
                        P1[key].append(prodFecho)         # passa ela para P1, substituindo a prod. de uma variável
                        print(f"The production {prodFecho} is now a subset of {key}: {P1[key]}")                        # print da prod. nova

    gram['P'] = P1                                    # troca as prods. origina	is de "gram" pelas simplificadas em P1
    print(f"Grammar after null productions simplification:\n{gram}")
    return gram

# =========================================================================== #
def simplificaSimbInuteis(gram):
    linhas()
    print("\n***Useless Symbols Simplification***\n")

    for k,v in gram.items():
        if k == 'T':
            terminais = v

    for k,v in gram.items():
        if k == 'V':
            variaveis = v

    for k,v in gram.items():
        if k == 'P':
            producoes = v

    for k,v in gram.items():
        if k == 'S':
            inicial = v

    #Devolve true caso seja não terminal
    def nao_terminal(s):
        for x in variaveis:
            if x == s:
                return True
        return False

    print("1st:")
    #Acha a produção do simbolo inicial
    for k,v in producoes.items():
        if k == 'S':
            prodinicial = v

    V1 = []
    # algumas definicoes de variaveis para facilitar
    listaKeys = list(producoes.keys())

    len_aux = -1
    while len_aux != len(V1):
        len_aux = len(V1)
        for x in producoes:
            for y in producoes[x]:
                aux = 1
                for z in y:
                    if nao_terminal(z) and z not in V1:
                        aux = 0
                        break
                if aux == 1 and x not in V1:
                    V1.append(x)
                    #print(V1)
                    break

    print(f">>> V1 (all the variables that produces terminals):\n{V1}.")

    # IMPLEMENTANDO O ALGORITMO PARA REMOVER SIMBOLOS NAO PERTENCENTES A V1 DAS PRODUCOES E GERAR P1
    # Lembrando que V1 sao todas as VARIAVEIS que produzem terminais diretamente
    # Remove todas as produções que possuam um elemento não presente em V1

    varAux = list(variaveis)
    for x in variaveis:
        if x not in V1:
            if x in listaKeys:
                del producoes[x]
                varAux.remove(x)
            for v in varAux:
                for z in producoes[v]:
                    for y in z:
                        if(y == x):
                            #print(f"{producoes[x]}")
                            #print(f"{prodinicial}")
                            producoes[v].remove(z)
                            break
    variaveis = V1
    P1 = producoes
    print(f">>> P1 (all productions that generates terminals starting from the first production):\n{P1}.")

    ###########################################################################

    #Devolve true se um simbolo é terminal
    def terminal(s):
        for terminal in terminais:
            if terminal == s:
                return True
        return False

    print("\n2nd:")

    V2 = [inicial]
    T2 = []
    print("What we have until now:")
    print(f"V2 = {V2}\nP1 = {P1}")
    #print(producoes)

    def lista_ou_string(elemento):
        if type(elemento) == type([]):
            return True
        else:
            return False

    tV = -1
    tT = -1
    while len(V2) != tV or len(T2) != tT:
        tV = len(V2)
        tT = len(T2)
        for x in V2:
            for y in producoes[x]:
                #print(y)
                if lista_ou_string(y):
                    for z in y:
                        if nao_terminal(z) and not z in V2:
                            V2.append(z)
                        elif terminal(z) and not z in T2:
                            T2.append(z)
                else:
                    if nao_terminal(y) and not y in V2:
                        V2.append(y)
                    elif terminal(y) and not y in T2:
                        T2.append(y)

    print(f"Non-terminal with useless productions: {V2}")
    listaKeys = list(producoes.keys())
    #print(producoes.keys())
    P2 = {}
    for x in listaKeys:
        if x not in V2:
            del producoes[x]
        else:
            for y in producoes[x]:
                #print(producoes[x])
                #print(y)
                for z in y:
                   # print(z)
                    if (nao_terminal(z) and not z in V2 or
                            terminal(z) and not z in T2):
                        producoes[x].remove(y)
                        break

    P2 = producoes
    print(f"Useful productions: {P2}")

    variaveis = V2
    terminais = T2
    gram['P'] = P2
    gram['V'] = V2
    gram['T'] = T2
    print(f"\nGrammar after useless symbols simplification:\n{gram}")
    return gram

# =========================================================================== #
def transformaFNC(gram):
    #Transformação em FNC
    linhas()
    print("\n***TRANSFORMING INTO CHOMSKY NORMAL FORM***\n")

    for k,v in gram.items():
        if k == 'T':
            terminais = v

    for k,v in gram.items():
        if k == 'V':
            variaveis = v

    for k,v in gram.items():
        if k == 'P':
            producoes = v

    for k,v in gram.items():
        if k == 'S':
            inicial = v

    def nao_terminal(s):
        for x in variaveis:
            if x == s:
                return True
        return False

    def terminal(s):
        for terminal in terminais:
            if terminal == s:
                return True
        return False

    print("round 1: simplification is ready\n")
    print("round 2:")
    #Etapa 2: Garantir que o lado direito da produção possui apenas não terminais
    variaveis_aux = []   #variaveis geradas
    lAux = []

    for x in producoes:
        for m, y in enumerate(producoes[x]):
            if type(y) == list and len(y) >= 2:  #Caso a produção tenha mais de 2 elementos
                for k, elem in enumerate(y):
                    if terminal(elem):  #Se houver terminal na produção substituir por não terminal(da forma Cz)
                        if not elem in variaveis_aux:
                            variaveis_aux.append(elem)

                        for el in y[:k]:
                            #if el in variaveis:
                            lAux.append(el)
                        lAux.append(''.join(['C', elem]))
                        for el in y[k+1:]:
                            #if el in variaveis:
                            lAux.append(el)

                        y.clear()
                        for var in lAux[:]:
                            y.append(var)
                        lAux.clear()
        print(f"Productions of {x} with variables and symbols now has only variables: {producoes[x]}")

    for x in variaveis_aux:  #Adicionar as novas variaveis à gramática e produção
        variaveis.append('C'+x)
        producoes['C'+x] = [x]

    print(f"\nCurrent variables: {variaveis}")
    print(f"Current productions: {producoes}")

    print("\nround 3:")
    #Etapa 3: Garantir que lado direito da produção possui apenas 2 variáveis
    variaveis_aux = []
    for x in producoes:
        for m, y in enumerate(producoes[x]):
            #print(y)
            while type(y) == list and len(y) >= 3:  #Enquanto o tamanho da produção for maior que 2
                for j in range(0, len(y), 2): #Pega duas variaveis para concatenar e transformar em 1
                    try:
                        aux1 = y[j]
                        aux2 = y[j+1]
                    except IndexError: #A não ser que o índice não exista
                        break

                    if (not ('C'+aux1+aux2 in variaveis or [aux1, aux2] in variaveis_aux)):
                        variaveis_aux.append([aux1, aux2])

                    lAux.append(''.join(['C', aux1, aux2]))
                    for el in y[j+2:]:
                        lAux.append(el)

                    y.clear()
                    for var in lAux[:]:
                        y.append(var)
                    lAux.clear()
        print(f"Productions of 3 or more variables of {x} was shrinked into: {producoes[x]}")

    for x in variaveis_aux:  #Adicionar as novas variaveis à gramática e produção
        variaveis.append('C'+x[0]+x[1])
        producoes['C'+x[0]+x[1]] = [x]

    gram['P'] = producoes
    gram['V'] = variaveis
    print(f"\nGrammar in Chomsky Normal Form:\n{gram}\n")
    return gram

# =========================================================================== #

class Nodo:                         # TAD da árvore de derivação
    def __init__(self,chave):
        self.esq = None
        self.dir = None
        self.val = chave

def arvorePrefix(node, nodeAnt, coords, posDerivacao, palavra, esqOuDir, geraTerminal):
    if node:
        if(nodeAnt.esq.val == node.val and esqOuDir == 'esq'):      # se é filho esquerdo de uma variável
            print(f'     {node.val}', end='')                       # printa-o
            colunaNodeEsq = coords[nodeAnt.val][posDerivacao][0][1][0]      # guarda coluna e linha dele
            linhaNodeEsq = coords[nodeAnt.val][posDerivacao][0][1][1]

            if(geraTerminal == 0):              # ou seja, a variável está na linha 0 da tabela e deriva um terminal
                node.esq = Nodo(palavra[colunaNodeEsq])     # insere terminal na árvore
                print(f'     {palavra[colunaNodeEsq]}')     # e printa-o
            else:
                for deriva in coords[node.val]:             # se a variável é do tipo A -> BC, percorre todas suas produções desse tipo (que estão no dicionário coords)
                    for k in range(1,linhaNodeEsq+1):
                        if((colunaNodeEsq, k-1) == deriva[0][1] and (colunaNodeEsq+k, linhaNodeEsq-k) == deriva[1][1]):     # se as coordenadas conferem, achou a produção (usei o mesmo esquema
                            #print(f"---{deriva[0][1]}    {deriva[1][1]}---")                                               do algoritmo CYK, s = linhaNodeEsq e r = colunaNodeEsq
                            node.esq = Nodo(deriva[0][0])       # insere filhos na árvore
                            node.dir = Nodo(deriva[1][0])
                            print(f'     ----->     derives {node.esq.val} at left and {node.dir.val} at right')   # printa-os
                            novaPos = coords[node.val].index(deriva)                                                # guarda o index da produção que está em coords
                            arvorePrefix(node.esq, node, coords, novaPos, palavra, 'esq', deriva[0][1][1])          # e chama a função recursiva para os filhos esq. e dir.
                            arvorePrefix(node.dir, node, coords, novaPos, palavra, 'dir', deriva[1][1][1])

        elif(nodeAnt.dir.val == node.val and esqOuDir == 'dir'):        # se é filho direito de uma variável (daqui para baixo é análogo a acima)
            print(f'     {node.val}', end='')
            colunaNodeDir = coords[nodeAnt.val][posDerivacao][1][1][0]
            linhaNodeDir = coords[nodeAnt.val][posDerivacao][1][1][1]

            if(geraTerminal == 0):
                node.dir = Nodo(palavra[colunaNodeDir])
                print(f'     {palavra[colunaNodeDir]}')

            else:
                for deriva in coords[node.val]:
                    for k in range(1,linhaNodeDir+1):
                        if((colunaNodeDir, k-1) == deriva[0][1] and (colunaNodeDir+k, linhaNodeDir-k) == deriva[1][1]):
                            #print(f"---{deriva[0][1]}    {deriva[1][1]}---")
                            node.esq = Nodo(deriva[0][0])
                            node.dir = Nodo(deriva[1][0])
                            print(f'     ----->     derives {node.esq.val} at left and {node.dir.val} at right')
                            novaPos = coords[node.val].index(deriva)
                            arvorePrefix(node.esq, node, coords, novaPos, palavra, 'esq', deriva[0][1][1])
                            arvorePrefix(node.dir, node, coords, novaPos, palavra, 'dir', deriva[1][1][1])

def CYK(gram, palavra):
    print("\n***CYK PARSER***\n")
    n = len(palavra)
    # tabela em forma de dicionário
    tabela = [[[] for x in range(n)] for y in range(n)]
    # Dicionário p/ a árvore de derivação (guarda linha e coluna dos elementos da tabela que causaram a inserção de outro)
    coords = {}
    # Acrescentar a tabela produções do tipo A -> ar, com a sentença a1a2...an
    for r in range(1,n+1):
        for A in gram['V']:
            if(palavra[r-1] in gram['P'][A]):
                tabela[r-1][0].append(A)
                #print(tabela)

    # Deleta os quadrados da tabela (listas vazias) que não serão usados
    for p in range(n-1,0,-1):
        for q in range(n-1, n-p-1, -1):
            del tabela[p][q]

    # Acrescentar a tabela de produções do tipo A -> BC
    for s in range(2,n+1):
        for r in range(1, n-s+1+1):
            print(f"\n- Fulfilling line {s-1}, row {r-1}. Current Table:")
            print(tabela, '\n')
            for k in range(1,s):
                for A in gram['V']:
                    for prod in gram['P'][A]:
                        if(type(prod) == list):
                            if (len(prod) == 2):
                                B = prod[0]
                                C = prod[1]
                                print(f'Production of {A}: {B} and {C}')
                                print(f'{B} is in {tabela[r-1][k-1]} and {C} is in {tabela[r+k-1][s-k-1]}?')
                                if B in tabela[r-1][k-1] and C in tabela[r+k-1][s-k-1]:
                                    if A not in tabela[r-1][s-1]:
                                        tabela[r-1][s-1].append(A)
                                        coords.setdefault(A,[]).append([[B, (r-1, k-1)], [C, (r+k-1, s-k-1)]])      # guarda as coordenadas das variáveis no dicionário coords
                                        print(f'* YES - inserting  {A} in line {s}, row {r} *')
                                        print(tabela)
                                else:
                                    print('NOPE')
    print(f'Final table: {tabela}')
    if(gram['S'] not in tabela[0][n-1]):
        print('\nThis input is not accepted.\n')
    else:
        print('\nThis input is accepted.\n')
        linhas()

        print('\nCoordinates of productions in the format A -> BC in the table:')
        print(coords)       # marquei as coordenadas da tabela (linha e coluna começando por 0) para cada produção A -> BC da tabela
        print('\nWord derivation tree, variables in the left row, terminals in the right row:\n')
        if(coords == {}):       # se S -> terminal
            print(f"[{gram['S']}\n{palavra}\n")
        else:
            raiz = Nodo(gram['S'])
            derivacaoInicial = len(coords[raiz.val])-1      # derivação inicial é a de S que está na última linha
            print(f'     {raiz.val}', end='')               # começa a printar a árvore
            raiz.esq = Nodo(coords[raiz.val][derivacaoInicial][0][0])       # filhos esq. e dir. da raiz
            raiz.dir = Nodo(coords[raiz.val][derivacaoInicial][1][0])
            #print(raiz.esq.val)
            #print(raiz.dir.val)
            print(f'     ----->     derives {raiz.esq.val} at left and {raiz.dir.val} at right')       #printa as variáveis geradas por S
            linEsq = coords[raiz.val][derivacaoInicial][0][1][1]        # guarda a linha da tabela onde estão essas variáveis para saber se geram terminais ou não
            linDir = coords[raiz.val][derivacaoInicial][1][1][1]

            arvorePrefix(raiz.esq, raiz, coords, derivacaoInicial, palavra, 'esq', linEsq)      # chamadas da função recursiva para filhos esq. e dir.
            arvorePrefix(raiz.dir, raiz, coords, derivacaoInicial, palavra, 'dir', linDir)

            print('\n')

    # Formatando a tabela diagonal
    quantColunas = len(tabela)
    quantLinhas = quantColunas
    coluna = 0
    counter = 1 # incremento em 1 para printar colunas
    linhas()
    print("\nTriangular Table:\n")
    while counter <= quantColunas:
        while coluna < counter:
          print(f'{tabela[coluna][quantLinhas-1]}\t', end='')
          coluna = coluna + 1
        print('\n')
        coluna = 0
        counter = counter + 1
        quantLinhas = quantLinhas - 1
    for symb in palavra:
        print(f'{symb}\t', end='')
    print('\n')

# =========================================================================== #
# MAIN

nomeArq = input('Type the grammar file name (without .txt): ')
nomeArq = nomeArq + '.txt'
vetorLinhas = le_arq_gramatica(nomeArq)
gram = gram_formal(vetorLinhas)
gram = simplificaProdVazias(gram)
gram = simplificaProdUnitarias(gram)
gram = simplificaSimbInuteis(gram)
gram = transformaFNC(gram)
linhas()
palavra = input('Type the sentence to parse <CYK> with spaces between terminals: ')
CYK(gram, palavra.split( ))
linhas()
print('\n')
