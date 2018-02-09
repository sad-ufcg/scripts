import csv
from getpass import getpass
import math

import controle


def _processa_csv(csv_f, delimiter):
    # HEADER: matr,n1,n2,n3,f
    # CONTROLE ACADEMICO: n1_matr, n2_matr, .. final = f
    data = {}
    # 1 casa decimal, virgulas no lugar de ponto:
    conv = lambda y: ("%.1f" % (math.ceil(10 * float(y)) / 10)).replace('.', ',')
    with open(csv_f, encoding='utf-8-sig', delimiter=delimiter, newline='') as csvfile:
        notas_reader = csv.reader(csvfile)
        header = next(notas_reader)
        for linha in notas_reader:
            matr = linha[0]
            for f, n in zip(header[1:], linha[1:]):
                if n:
                    data[f + "_" + matr] = conv(float(n))
    return data


def processa_csv(codigo, turma, pesos, csv_f, delimiter=';'):
    data = controle.base(codigo, turma, "ProfessorTurmaNotasConfirmar")
    data["notas"] = str(len(pesos))
    data["numNotas"] = str(len(pesos))
    for n, peso in enumerate(pesos):
        data["peso" + str(n + 1)] = str(peso)
    data.update(_processa_csv(csv_f, delimiter))
    return data


def main():
    login_ = input("LOGIN: ")
    senha_ = getpass("SENHA: ")
    # ICC: 1411001
    # LP2: 1411181
    # P2 : 1411168
    data = processa_csv("1411181", "02", [32,12,12,25,20], "notas-lp2.csv")
    jsessionid = controle.login(login_, senha_)
    print(jsessionid)
    print(controle.chamada(data, jsessionid).read())


if __name__ == "__main__":
    main()
