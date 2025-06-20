import os
import sys

from datetime import datetime
diretorio_script = os.path.dirname(os.path.abspath(__file__))
DIR_LOG = os.path.join(diretorio_script,'log')


def log(level, funcao, msg):
    dia_atual = datetime.now()
    tempo = dia_atual.strftime('%Y/%m/%d-%H:%M:%S')
    try:
        pasta_dia = os.path.join(DIR_LOG, dia_atual.strftime('%Y%m%d'))
        if not os.path.exists(pasta_dia):
            os.makedirs(pasta_dia)

        arquivo_atual = os.path.join(pasta_dia, dia_atual.strftime('%Y%m%d_%H') + 'h.log')
        if not os.path.exists(arquivo_atual):
            f = open(arquivo_atual, 'x')
            f.close()
            f = open(arquivo_atual, 'a')
            f.write(f'\n {tempo} -> {level} -> {funcao} - {msg}')
            f.close()
        else:
            f = open(arquivo_atual, 'a')
            f.write(f'\n {tempo} -> {level} -> {funcao} - {msg}')
            f.close()
    except:
        print(f'Erro ao criar log: {str(sys.exc_info()[0])}:{str(sys.exc_info()[1])}')
