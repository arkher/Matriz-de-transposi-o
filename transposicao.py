import math

def clear(n=300):
    for i in range(n):
        print()

def valida_chave(chave):
    '''
        Realiza o tratamento de chaves inválidas e realiza a requisição
        de uma nova, caso esta o seja.
    '''
    chave_invalida = True
    
    while(chave_invalida):
        # o método set() transforma em uma estrutura de conjunto
        chave_set = set(chave.copy())

        # se a chave possui realmente 7 números distintos
        if(len(chave_set)==len(chave)) :
            chave_invalida = False
        else:
            print('por favor, digite uma chave válida')
            chave = [int(i) for i in input().split(' ')]

def open_arq(path='texto_teste.txt'):
    # leitura do arquivo de texto
    try:
        arq = open(path, 'r', encoding='utf8')
        texto = arq.read()
        arq.close()
        return texto
    except:
        print("erro na leitura do arquivo")
        quit()

def get_dictionary(texto, key_size, qtd_linhas):
    '''
        dicionario de linhas 
        (cada posição do dicionario é um indice 
        para uma linha do texto)
    '''
    dic_linhas = {}
    
    for i in range(qtd_linhas):
        dic_linhas[i] = []
    
    # preenchimento do dicionario
    count = 0
    col = 0
    for i in range(len(texto)):
        if(count>=key_size):
            count = 0
            col += 1    
        dic_linhas[col].append(texto[i])
        count += 1

    # preenchimento dos espaços vazios 
    ini = 97
    while(len(dic_linhas[list(dic_linhas.keys())[-1]])<key_size):
        dic_linhas[list(dic_linhas.keys())[-1]].append(chr(ini))
        ini += 1
    
    return dic_linhas

def encryp(dic_linhas, texto, chave, path_out='texto_criptografado.txt'):    
    '''
        Realiza a criptografia por transposição
    '''
    # texto criptografado
    texto_crip = ""

    # ordem das colunas 
    ordem = [chave.index(i+1)+1 for i in range(len(chave))]

    # criptografia: coloca as linhas no dicionário 
    # baseado nos valores da chave
    for k in ordem:
        for i in range(len(dic_linhas)):
            texto_crip += dic_linhas[i][k-1] 

    # salva o arquivo de saída
    arq_crip = open(path_out,'w', encoding='utf8')
    arq_crip.write(texto_crip)
    arq_crip.close()
    return texto_crip

def decryp(chave, path_crip, key_size=7, texto_crip=''):
    '''
        Realiza a descriptografia
    '''
    if(texto_crip==''):
        texto_crip = open_arq(path_crip)
    qtd_linhas = math.ceil(len(texto_crip)/key_size)
    texto_descrip = ""
    count_letras = 0
    # descriptografia: inverte o processo de criptografia
    for k in range(qtd_linhas):
        for i in chave:
            texto_descrip += texto_crip[(i-1)*qtd_linhas+count_letras]
        count_letras+=1
    
    # salva o arquivo de saída
    return texto_descrip

def save_arc(text, path_decrip):
    # salva um arquivo qualquer
    arq_descrip = open(path_decrip,'w', encoding='utf8')
    arq_descrip.write(text)
    arq_descrip.close()

def run(path, path_out_encryp, path_out_decryp, chave, key_size = 7):
    n_estagios = 3
    
    print('| (1) - criptografar | (2) - descriptografar | (3) - sair |')
    entrada = int(input())
    while(entrada!=3):
        
        # abre o arquivo, cria o dicionário de linhas e criptografa (3 vezes) 
        # e salva o arquivo criptografado
        if(entrada==1):
            texto = open_arq(path)
            qtd_linhas = math.ceil(len(texto)/key_size)
            dicionario = get_dictionary(texto,key_size,qtd_linhas)
            
            texto_crip = encryp(dicionario, texto, chave, path_out_encryp)
            for i in range(n_estagios-1):
                dicionario = get_dictionary(texto_crip,key_size,qtd_linhas)
                texto_crip = encryp(dicionario, texto_crip, chave, path_out_encryp)
            clear()
            print('arquivo salvo!')
        elif(entrada==2):
            texto_decrip = decryp(chave, path_out_encryp, key_size)
            for i in range(n_estagios-1):
                texto_decrip = decryp(chave, path_out_decryp, key_size, texto_decrip)
            save_arc(texto_decrip, path_out_decryp)
            clear()
            print('arquivo salvo!')
        elif(entrada==3):
            clear()
            print('obrigado')
            break
        else:
            print('por favor, digite uma entrada válida')
        print('| (1) - criptografar | (2) - descriptografar | (3) - sair |')    
        entrada = int(input())

if __name__=='__main__':
    print('digite o caminho para acessar o arquivo de teste')
    print('ex.: ./teste.txt')
    path = input()
    
    print('digite o caminho do arquivo criptografado')
    print('ex.: ./teste_saida.txt')
    path_out_encryp = input()

    print('digite o caminho do arquivo descriptografado')
    print('ex.: ./teste_saida.txt')
    path_out_decryp = input()

    print('digite a chave de criptografia com valores intercalados por espaço')
    chave = [int(i) for i in input().split(' ')]
    valida_chave(chave)
    run(path, path_out_encryp, path_out_decryp, chave)