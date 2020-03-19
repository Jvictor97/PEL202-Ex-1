#!/usr/bin/env python
# coding: utf-8

# # Exercício 1 - Busca em Largura (BFS) e Busca em Profundidade (DFS)

# ## Classes com as estruturas de dados para os algoritmos

# #### Classe State (ou Nó)
# Guarda referências para o nó pai e os nós filhos

# In[2]:


class State:
    def __init__(self, water_on_3 = 0, water_on_4 = 0):
        self.water_on_3 = water_on_3  # inicializa o atributo water_on_3 (quantidade de água no jarro de 3L)
        self.water_on_4 = water_on_4 # inicializa o atributo water_on_4 (quantidade de água no jarro de 4L)
        self.parent = None # inicializa a referência para o nó pai como None
        self.children = [] # inicializa as referências para os nós filhos como um array vazio
    
    def update(self, water_on_3, water_on_4): # atualiza a quantidade de água nos jarros
        self.water_on_3 = water_on_3
        self.water_on_4 = water_on_4
        
    def is_final_state(self): # verifica se o estado do nó atual é o estado final (2, 0)
        return self.water_on_3 == 2 and self.water_on_4 == 0
    
    def get_value(self): # retorna o valor do estado atual (água no jarro de 3L, água no jarro de 4L)
        return self.water_on_3, self.water_on_4


# #### Classe Base
# Possui as funções básicas de inicialização, busca por índice e exibição dos conteúdos da Fila e Pilha

# In[3]:


class Base():
    def __init__(self, first_element = None):
        # inicializa o vetor como um vetor vazio ou com o primeiro elemento, se houver
        self.array = [first_element] if first_element is not None else [] 
        self.length = 0 # inicializa o atributo de comprimento
    def __getitem__(self, index): # retorna o conteúdo do array na posição especificada (sobrecarga do operador [i])
        if index < len(self.array):
            return self.array[index]
    def show(self): # Exibe o conteúdo do array
        print(self.array)


# #### Classe Pilha
# Funções:
# - push: adiciona um item no topo da pilha
# - pop: remove e retorna o item no topo da pilha

# In[4]:


class Stack(Base):
    def push(self, value):
        self.array.append(value)
        self.length += 1
        return self.array[:]
    def pop(self):
        if(len(self.array) > 0):
            self.length -= 1
            return self.array.pop()


# #### Classe Fila
# Funções:
# - enqueue: adiciona um item no fim da fila
# - dequeue: remove e retorna o item na primeira posição da fila

# In[5]:


class Queue(Base):
    def enqueue(self, value):
        self.array.append(value);
        self.length += 1
        return self.array[:]
    def dequeue(self):
        if(len(self.array) > 0):
            self.length -= 1
            return self.array.pop(0)


# ## Operações
# 
# - fill_3: enche o jarro de 3L
# - empty_3: esvazia o jarro de 3L
# - fill_4: enche o jarro de 4L
# - empty_4: esvazia o jarro de 4L
# - transfer_3_4: transfere o conteúdo do jarro de 3L para o jarro de 4L
# - transfer_4_3: transfere o conteúdo do jarro de 4L para o jarro de 3L

# In[6]:


def fill_3(water_on_3, water_on_4):
    return 3, water_on_4

def empty_3(water_on_3, water_on_4):
    return 0, water_on_4

def fill_4(water_on_3, water_on_4):
    return water_on_3, 4

def empty_4(water_on_3, water_on_4):
    return water_on_3, 0

def transfer_3_4(water_on_3, water_on_4):
    total_water = water_on_3 + water_on_4 
    return (total_water - 4, 4) if (total_water > 3) else (0, total_water)

def transfer_4_3(water_on_3, water_on_4):
    total_water = water_on_3 + water_on_4 
    return (3, total_water - 3) if (total_water > 3) else (total_water, 0)


# #### Função para exibir o resultado da busca

# In[7]:


def print_result(state):
    way = [] # inicializa o vetor do caminho a ser realizado na árvore de estados
    print('Resultado:')
    while(state.parent is not None): # Itera do nó final (folha) até o nó raiz através da referência para o pai
        way.insert(0, state.get_value()) # Insere no vetor do caminho o estado atual
        state = state.parent # Atualiza o estado atual com o nó pai
    way.insert(0, state.get_value()) # Insere o valor do nó raiz
    print(way) 


# ### Algoritmo de Busca em Largura (BFS)
# Utiliza internamente uma estrutura de fila para visitar os nós da árvore de estados

# In[8]:


def bfs(q, visited_states):
    if q is None and visited_states is None: # Caso seja a primeira execução do algoritmo inicializa os parâmetros
        visited_states = [] # Inicializa os estados visitados
        q = Queue(State(0,0)) # Inicializa a fila com o estado inicial
    state = q.dequeue() # Remove e recebe o estado do início da fila
    if(state.get_value() in visited_states): # Se o estado já foi visitado chama novamente a recursão sem gerar os filhos
        return bfs(q, visited_states)
    elif(state.is_final_state()): # Se o estado é o estado final exibe o resultado e para a recursão (caso base)
        print_result(state)
        return
    else:
        # Não é estado final, então gera os estados filhos
        visited_states.append(state.get_value()) # Atualiza o vetor de estados visitados com o estado atual
        # Vetor de funções com as operações para gerar os nós filhos
        operations = [fill_3, empty_3, fill_4, empty_4, transfer_3_4, transfer_4_3] 
        print(state.get_value()) # Exibe o estado atual
        for operation in operations: # Itera sobre todas as operações
            new_state = State(*operation(*state.get_value())) # Gera o filho com base no valor do pai
            new_state.parent = state # Guarda a referência para o nó pai
            q.enqueue(new_state) # Adiciona o filho gerado ao fim da fila
        return bfs(q, visited_states) # Executa o passo recursivo


# ### Algoritmo de Busca em Profundidade (DFS)
# Utiliza internamente uma pilha para visitar os nós da árvore de estados

# In[9]:


def dfs(stack, visited_states):
    if stack is None and visited_states is None:  # Caso seja a primeira execução do algoritmo inicializa os parâmetros
        visited_states = [] # Inicializa os estados visitados
        stack = Stack(State(0,0)) # Inicializa a pilha com o estado inicial
    state = stack.pop() # Remove e retorna o estado do topo da pilha
    if(state.get_value() in visited_states): # Se o estado já foi visitado chama novamente a recursão sem gerar os filhos
        return dfs(stack, visited_states) 
    elif(state.is_final_state()): # Se o estado é o estado final exibe o resultado e para a recursão (caso base)
        print_result(state)
        return
    else: # Não é estado final, então gera os estados filhos
        visited_states.append(state.get_value()) # Atualiza o vetor de estados visitados com o estado atual
        # Vetor de funções com as operações para gerar os nós filhos
        operations = [fill_3, empty_3, fill_4, empty_4, transfer_3_4, transfer_4_3]
        operations.reverse() # Inverte a ordem das operações (para visitar os estados da árvore pelo ramo da esquerda)
        print(state.get_value()) # Exibe o estado atual

        for operation in operations: # Itera sobre todas as operações
            new_state = State(*operation(*state.get_value())) # Gera o filho com base no valor do pai
            new_state.parent = state # Guarda a referência para o nó pai
            stack.push(new_state) # Adiciona o filho no topo da pilha
        return dfs(stack, visited_states) # Executa o passo recursivo


# In[10]:


def main(): # Função principal, executa as duas buscas e exibe o resultado obtido
    print('Busca em Largura')
    print('Caminho da Busca:')
    bfs(None, None) # Chamada inicial do BFS enviando os argumentos como None
    
    print('\nBusca em Profundidade')
    print('Caminho da Busca')
    dfs(None, None) # Chamada inicial do DFS enviando os argumentos como None


# In[11]:


main()

