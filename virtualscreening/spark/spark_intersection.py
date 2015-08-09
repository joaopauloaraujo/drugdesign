
import os
import time
import funcoes as func
import ConfigParser as configparser
from pyspark import SparkContext

def main():

    #-----------------------
    # Carregando config.ini
    #-----------------------
    config = configparser.ConfigParser()
    config.read('config.ini')

    path_log          = config.get('Path','path_log')          # path arquivos logs
    path_struc        = config.get('Path','path_struc')        # path arquivos structures
    path_mod          = config.get('Path','path_mod')          # path onde seram gravados os arquivos models
    path_result_tempo = config.get('Path','path_result_tempo') # path ode seram gravados os arquivos de tempo de processamento
    v_affinity        = float(config.get('affinity','valor'))  # affinidade a ser calculada

    #---------------------------------------------------------------------------
    func.rm(path_mod) # Remove path_mod -path onde sera gravado os arquivos model
    #---------------------------------------------------------------------------

    #-------------------------------------------------
    inicio = time.time()  # inicio do calculo do tempo
    #-------------------------------------------------

    # ----- calculo spark -------------------------------------------------------------------------------
    sc = SparkContext('local')
    lines = sc.wholeTextFiles(path_log)
    lines = lines.flatMap(lambda line:func.Maper(line)).filter(lambda line: func.reducer(line,v_affinity))
    #----------------------------------------------------------------------------------------------------

    #----------------------------------------------------
    parcial_01 = time.time() # tempo parcial - map reduce
    #----------------------------------------------------

    lines2 = sc.wholeTextFiles(path_struc)
    lines2 = lines2.flatMap(lambda line:func.Maper_struc(line))
    lines2.intersection(lines)

    scc = sc.parallelize(lines2.collect())
    scc.foreach(lambda line:func.criar_mod_inter(line,path_mod))

    #------------------------------------------
    fim = time.time() # fim do calculo do tempo
    #------------------------------------------

    #-------------------------------------------------------------------------------------------------------
    num = len(os.listdir(os.path.expanduser(path_mod))) # quantidade de arquivos gravados no diretorio model
    #-------------------------------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------------------------------------------
    func.result(inicio,parcial_01,fim,path_mod,path_result_tempo,v_affinity,num,'spark') # gravando os tempos em um arquivo result
    #---------------------------------------------------------------------------------------------------------------------

main()

