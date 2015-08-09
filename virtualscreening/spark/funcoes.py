import os

def Maper(file_comp):
    saida = []
    file = file_comp[1].strip().split('\n')
    filename = file_comp[0]
    filename = os.path.basename(filename)
    filename = filename.replace(".log","")
    for line in file:
        if(len(line) > 0):
            words = line.split()
            if(words[0].isdigit()):
                saida.append(filename + '_' + words[0] + '\t' + words[1])
    return saida

def Maper_struc(file_comp):
    saida = []
    file = file_comp[1].strip().split('ENDMDL')
    filename = file_comp[0]
    filename = os.path.basename(filename)
    filename = filename.replace(".log","")
    for line in file:
        if(len(line) > 0):
            words = line.split()
            saida.append(filename + '_' + words[1] + '\t' + line)

    return saida

def reducer(file_comp,valor):
    ID, affinity = file_comp.split('\t', 1)
    affinity = float(affinity)
    if(affinity <= valor):
        return True
    return False

def criar_mod_inter(line,path_m):
    filename, model = line.split('\t')
    write = open(path_m + filename, "w")
    write.writelines(model)
    write.close()

def criar_mod_p(line,path_s,path_m):
    path_struc = path_s
    path_mod = path_m
    flag = False
    line = line.strip()
    ID, affinity = line.split('\t', 1)
    filename = ID[0:ID.rfind('_')]
    model    = ID[len(filename)+ 1 :len(ID)]
    _read  = open(path_struc + filename + ".pdbqt", "r")
    a = _read.readlines()
    b = []
    _read.close()
    for line in a:
        s = line.split()
        if(s[0] == "MODEL" and s[1] == model):
            flag = True
        if (flag):
            b.append(line)
            if (line.find("ENDMDL") > -1):
                _write = open(path_mod + filename + "_" + model + ".pdbqt", "w")
                _write.writelines(b)
                _write.close()
                break

def criar_mod(reducer,path_s,path_m):
    flag = False
    path_struc = path_s
    path_mod = path_m
    for line in reducer:
        line = line.strip()
        ID, affinity = line.split('\t', 1)
        filename = ID[0:ID.rfind('_')]
        model = ID[len(filename)+ 1 :len(ID)]
        fpdbqt = open(path_struc + filename + ".pdbqt", "r")
        for line in fpdbqt:
            s = line.split()
            if(s[0] == "MODEL" and s[1] == model and flag == False):
                arq = open(path_mod + filename + "_" + model + ".pdbqt", "w")
                arq.writelines(line)
                flag = True
            if (flag == True and s[0] <> "MODEL"):
                arq.writelines(line)
                if (line.find("ENDMDL") > -1):
                    flag = False
                    arq.close()
        fpdbqt.close()

def saida(lista,path_result):
    arq = open(path_result, 'w')
    for line in lista:
        arq.writelines(line)
    arq.close()

def rm(path_local):
    list_arqs = os.listdir(os.path.expanduser(path_local))
    for linha in list_arqs:
        os.remove(path_local + linha)

def result(_inicio,_parcial,_fim,_path_mod,_path_result_tempo,_v_affinity,_num,_name):
    tempos = []
    tempos.append('*********************')
    tempos.append('********' + _name.upper() +'********')
    tempos.append('*********************')

    tempos.append('\n\nMAP E REDUCE\nTEMPO:\t' + str(_parcial - _inicio) )
    tempos.append('\n\nCRIANDO ARQUIVO MODE LOCAL\nTEMPO:\t'  + str(_fim - _parcial) )
    tempos.append('\n\nTEMPO TOTAL\nTEMPO:\t'  + str(_fim - _inicio) )
    tempos.append('\n\nAffinity: ' + str(_v_affinity))
    tempos.append('\n\nQuantidade de Arquivos gravados no diretorio >>')
    tempos.append('\n' + _path_mod)
    tempos.append('\nQtd: ' + str(_num))

    path_result_tempo = _path_result_tempo + _name + '/' +'result_affinity' + str(_v_affinity) + '.txt'
    saida(tempos,path_result_tempo)

    print "************"
    print "SUCESSO !!! "
    print "************"