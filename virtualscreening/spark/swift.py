import swiftclient
import os
'''
authurl  = 'https://dal05.objectstorage.softlayer.net/v1/AUTH_00b5108b-e123-4ae2-8fa5-d41204677bde'
username = '7354c34f7dd3c69ae4751c2bf6ece37536dac238'
password = '9723efc1ef0fd6cc32f8c464d139edf3a63464f054977b0dbfab38b9ab8a'
token = 'AUTH_tk7e973727de5f494a87887184ad4f22aa'
token = 'AUTH_tk7c99f26eb484441482100c87c575018e'
AUTH_tk7c99f26eb484441482100c87c575018e
'''

def carregar(path_local):
    list_arqs = os.listdir(os.path.expanduser(path_local))
    for linha in list_arqs:
        arquivo = open(path_local + linha, "r")
        arq = arquivo.read()
        arquivo.close()
        swiftclient.put_object(authurl,token,'testestructures',linha,arq)

authurl  = 'https://dal05.objectstorage.softlayer.net/v1/AUTH_00b5108b-e123-4ae2-8fa5-d41204677bde'
username = '7354c34f7dd3c69ae4751c2bf6ece37536dac238'
password = '9723efc1ef0fd6cc32f8c464d139edf3a63464f054977b0dbfab38b9ab8a'
token = 'AUTH_tkd81b30065c9340ceba91f3d7bda880a5'

path_local = '/home/joao/Git/TCC/drugdesign/virtualscreening/spark/'

#swiftclient.put_container(authurl,token,'log_teste')

carregar(path_local)








