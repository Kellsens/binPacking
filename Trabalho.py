import random
import copy
import math
import time

def inicial_guloso(items,params):
    inicial = [-1 for x in range(int(params[1]))]
    bins = [0 for x in range(int(params[1]))]

    items_local = copy.copy(items)

    items_local = sorted(enumerate(items_local), key=lambda x:x[1],reverse=True)
    for index, peso in items_local:
        ctd = 0
        busca = True
        while busca:
            if bins[ctd]+peso < params[0]:
                inicial[index] = ctd
                bins[ctd] = bins[ctd] + peso
                busca = False
            ctd = ctd + 1
        pass

    return [inicial,bins]

def f_obj(bins):
    saida = 0
    ctd = 0
    while ctd < len(bins):
        saida = saida + math.pow(bins[ctd],2)
        ctd = ctd + 1
    return saida

def f_obj_num_bins(solucao):
    lista = list()
    for i in solucao:
        if i not in lista:
            lista.append(i)
    return len(lista)

def realocar_1(s_inicial,bin,pesos,params):

    bin_estrela = copy.copy(bin)

    fobj_original = f_obj(bin)
    fobj_estrela = fobj_original

    solucao = copy.copy(s_inicial)
    s_estrela = copy.copy(s_inicial)

    for i,j in enumerate(solucao):
        for k in range(len(bin)):
            if (k != j) and (bin[k] + pesos[i] <= params[0]) and (bin[k] > 0) :
                nova_fobj = fobj_original - math.pow(bin[j],2) - math.pow(bin[k],2) + math.pow((bin[j]-pesos[i]),2) + math.pow((bin[k]+pesos[i]),2)
                if nova_fobj > fobj_estrela:
                    s_estrela = copy.copy(s_inicial)
                    s_estrela[i] = k
                    fobj_estrela = nova_fobj
                    bin_estrela = copy.copy(bin)
                    bin_estrela[j] = bin[j] - pesos[i]
                    bin_estrela[k] = bin[k] + pesos[i]

    return [s_estrela, bin_estrela]

def realoca_1_rand(s_inicial,bin,pesos,params):
    loop = True
    itermax = 1000
    iter = 0
    while loop:
        item = random.randrange(int(params[1]))
        bin_item = s_inicial[item]
        bin_novo = random.randrange(int(params[1]))
        iter = iter + 1
        if (bin_item != bin_novo) and (bin[bin_novo] != 0) and ((bin[bin_novo]+pesos[item]) <= params[0]):
            nova_solucao = copy.copy(s_inicial)
            nova_solucao[item] = bin_novo
            loop = False
        if iter == itermax:
            nova_solucao = copy.copy(s_inicial)
            loop = False
    novo_bin = [0 for x in range(len(nova_solucao))]
    for i, j in enumerate(nova_solucao):
        novo_bin[j] = novo_bin[j] + pesos[i]
    return [nova_solucao,novo_bin]

def trocar_2(s_inicial, bin, pesos, params):

    fobj_original = f_obj(bin)
    fobj_estrela = fobj_original

    solucao = copy.copy(s_inicial)
    s_estrela = copy.copy(s_inicial)
    bin_estrela = copy.copy(bin)

    for i, j in enumerate(solucao):
        for k in range(i+1,len(solucao)):
            if (j != solucao[k]) and (bin[solucao[k]] + pesos[i] - pesos[k] <= params[0]) and (bin[j] + pesos[k] - pesos[i] <= params[0]):
                nova_fobj = fobj_original - math.pow(bin[j], 2) - math.pow(bin[solucao[k]], 2) + math.pow((bin[j]-pesos[i]+pesos[k]),2) + math.pow((bin[solucao[k]]+pesos[i]-pesos[k]), 2)
                if nova_fobj > fobj_estrela:
                    s_estrela = copy.copy(s_inicial)
                    s_estrela[i] = solucao[k]
                    s_estrela[k] = j
                    fobj_estrela = nova_fobj
                    bin_estrela = copy.copy(bin)
                    bin_estrela[j] = bin[j] - pesos[i] + pesos[k]
                    bin_estrela[solucao[k]] = bin[solucao[k]] + pesos[i] - pesos[k]
    return [s_estrela, bin_estrela]

def troca_2_random(s_inicial, bin, pesos, params):
    loop = True
    while loop:
        item1 = random.randrange(int(params[1]))
        item2 = random.randrange(int(params[1]))
        if(item1 != item2) and (s_inicial[item1] != s_inicial[item2]) and (bin[s_inicial[item1]]-pesos[item1]+pesos[item2] <= params[0]) and (bin[s_inicial[item2]]-pesos[item2]+pesos[item1] <= params[0]):
            nova_solucao = copy.copy(s_inicial)
            nova_solucao[item1] = s_inicial[item2]
            nova_solucao[item2] = s_inicial[item1]
            loop = False
    novo_bin = [0 for x in range(len(nova_solucao))]
    for i, j in enumerate(nova_solucao):
        novo_bin[j] = novo_bin[j] + pesos[i]
    return [nova_solucao,novo_bin]

def vnd(s_inicial,bins,pesos,params):
    s_atual = copy.copy(s_inicial)
    bin_atual = copy.copy(bins)
    k = 1
    while k <= 2:
        if k == 1:
            saida = realocar_1(s_atual,bin_atual,pesos,params)
            vizinho = copy.copy(saida[0])
            bin_vizinho = copy.copy(saida[1])
        if k == 2:
            saida = trocar_2(s_atual, bin_atual, pesos, params)
            vizinho = copy.copy(saida[0])
            bin_vizinho = copy.copy(saida[1])
        if vizinho != s_atual:
            s_atual = copy.copy(vizinho)
            bin_atual = bin_vizinho
            k = 1
        else:
            k = k +1
    return [s_atual,bin_atual]

def gvns(s_inicial,bins,pesos,params):
    t_inicial = int(round(time.time() * 1000))
    iter_max = 1000
    s_atual = copy.copy(s_inicial)
    bin_atual = copy.copy(bins)
    iter_sem_melhoras = 0
    iter = 0
    melhor_caso = math.ceil(sum(pesos)/params[0])
    ultima_fobj = f_obj_num_bins(s_atual)
    while iter_sem_melhoras < 50 and f_obj_num_bins(s_atual) != melhor_caso and iter < iter_max:
        k = 1
        while k <= 2:
            if k == 1:
                random = realoca_1_rand(s_atual,bin_atual,pesos,params)
                s_random = copy.copy(random[0])
                bin_random = copy.copy(random[1])
                saida = vnd(s_random,bin_random,pesos,params)
                vizinho = copy.copy(saida[0])
                bin_vnd = copy.copy(saida[1])
            if k == 2:
                random = troca_2_random(s_atual,bin_atual,pesos,params)
                s_random = copy.copy(random[0])
                bin_random = copy.copy(random[1])
                saida = vnd(s_random,bin_random,pesos,params)
                vizinho = copy.copy(saida[0])
                bin_vnd = copy.copy(saida[1])
            if f_obj(bin_vnd) > f_obj(bin_atual):
                s_atual = copy.copy(vizinho)
                bin_atual = copy.copy(bin_vnd)
                iter_sem_melhoras = 0
                k = 1
            else:
                k = k +1
        if ultima_fobj == f_obj_num_bins(s_atual):
            iter_sem_melhoras = iter_sem_melhoras + 1
        else:
            ultima_fobj = f_obj_num_bins(s_atual)
        iter = iter + 1
    t_final = int(round(time.time() * 1000)) - t_inicial
    return [s_atual,f_obj_num_bins(s_atual),f_obj(bin_atual),t_final]

def ils(s_inicial,bins,pesos,params,tipo_busca):
    t_inicial = int(round(time.time() * 1000))
    s_atual = copy.copy(s_inicial)
    bin_atual = copy.copy(bins)
    iter_sem_melhora = 0
    melhor_caso = math.ceil(sum(pesos) / params[0])
    while iter_sem_melhora < 50 and f_obj_num_bins(s_atual) != melhor_caso:
        if tipo_busca == 1:
            novo_random_1 = troca_2_random(s_atual, bin_atual, pesos, params)
            s_random_1 = copy.copy(novo_random_1[0])
            bin_random_1 = copy.copy(novo_random_1[1])
            novo_random = troca_2_random(s_random_1, bin_random_1, pesos, params)
            s_random = copy.copy(novo_random[0])
            bin_random = copy.copy(novo_random[1])

        if tipo_busca == 2:
            novo_random_1 = realoca_1_rand(s_atual, bin_atual, pesos, params)
            s_random_1 = copy.copy(novo_random_1[0])
            bin_random_1 = copy.copy(novo_random_1[1])
            novo_random = realoca_1_rand(s_random_1, bin_random_1, pesos, params)
            s_random = copy.copy(novo_random[0])
            bin_random = copy.copy(novo_random[1])

        if tipo_busca == 1:
            s_anterior = copy.copy(s_random)
            saida = realocar_1(s_random, bin_random, pesos, params)
            s_linha = saida[0]
            s_bin = saida[1]
            while s_linha != s_anterior:
                s_anterior = copy.copy(s_linha)
                saida = realocar_1(s_linha,s_bin,pesos,params)
                s_linha = copy.copy(saida[0])
                s_bin = copy.copy(saida[1])

        if tipo_busca == 2:
            s_anterior = copy.copy(s_random)
            saida = trocar_2(s_random, bin_random, pesos, params)
            s_linha = copy.copy(saida[0])
            s_bin = copy.copy(saida[1])
            while s_linha != s_anterior:
                s_anterior = copy.copy(s_linha)
                saida = trocar_2(s_linha,s_bin,pesos,params)
                s_linha = copy.copy(saida[0])
                s_bin = copy.copy(saida[1])

        if f_obj(s_bin) > f_obj(bin_atual):
            s_atual = copy.copy(s_linha)
            bin_atual = copy.copy(s_bin)
            iter_sem_melhora = 0
        else:
            iter_sem_melhora = iter_sem_melhora + 1
    t_final = int(round(time.time() * 1000)) - t_inicial
    return [s_atual,f_obj_num_bins(s_atual),f_obj(bin_atual),t_final]


#======Main======#

items = list()
params = list()
solucoes = list()
bins = list()

ctd_prob = 0
i=0
j=0

linha_param = ""

arq = 'binpack1.txt'

with open(arq) as f:
    next(f)
    for line in f:
        if line.find('u') == True or line.find('t') == True:
            linha_param = line #f.readline()
            linha_param = linha_param.replace('\n', '')
            linha_param = linha_param.split(' ')
            params.append(list())
            for i in linha_param:
                if i != '' and type(i) == int:
                    params[ctd_prob].append(float(i))
            items.append(list())
            ctd_prob = ctd_prob + 1
        else:
            if len(line.split(' ')) == 1:
                if ctd_prob > 0:
                    items[ctd_prob-1].append(float(line.replace('\n', '')))
f.close()

S_ILS1 = list()
S_ILS2 = list()
S_GVNS = list()

for i in range(len(params)):
    s_inicial = inicial_guloso(items[i],params[i])
    solucoes.append(s_inicial[0])
    bins.append(s_inicial[1])
    S_ILS1.append(ils(solucoes[i],bins[i],items[i],params[i],1))
    S_ILS2.append(ils(solucoes[i],bins[i],items[i],params[i],2))
    S_GVNS.append(gvns(solucoes[i],bins[i],items[i],params[i]))
    pass

f = open('S_'+arq,'w')

for i in range(len(params)):
    f.write('ILS 1 | #bins '+str(S_ILS1[i][1])+' | Peso Total '+str(S_ILS1[i][2])+' | Tempo(ms) '+str(S_ILS1[i][3])+'\n')
f.write('\n\n')
for i in range(len(params)):
    f.write('ILS 2 | #bins '+str(S_ILS2[i][1])+' | Peso Total '+str(S_ILS2[i][2])+' | Tempo(ms) '+str(S_ILS2[i][3])+'\n')
f.write('\n\n')
for i in range(len(params)):
    f.write('GVNS | #bins '+str(S_GVNS[i][1])+' | Peso Total '+str(S_GVNS[i][2])+' | Tempo(ms) '+str(S_GVNS[i][3])+'\n')
f.close()
