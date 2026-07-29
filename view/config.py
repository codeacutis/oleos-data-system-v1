import os
import sys
caminho_atual = os.path.dirname(os.path.abspath(__file__))
pasta_raiz = os.path.abspath(os.path.join(caminho_atual, '..'))
if pasta_raiz not in sys.path:
    sys.path.append(pasta_raiz)