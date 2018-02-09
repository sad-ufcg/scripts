import csv
from getpass import getpass
import math

import controle


def _processa_csv(csv_f, delimiter):
    aulas = []
    with open(csv_f, encoding='utf-8-sig', delimiter=delimiter, newline='') as csvfile:
        aulas_reader = csv.reader(csvfile)
        for linha in aulas_reader:
            aulas.append((linha[0], linha[1]))
    return aulas


def processa_csv(codigo, turma, csv_f, delimiter=';'):
    data = controle.base(codigo, turma, 'ProfessorTurmaAulasConfirmar')
    data["numAulas"] = str(len(aulas))
    aulas = _processa_csv(csv_f, delimiter)
    n = 0
    for d, a in aulas:
        data["d_" + str(n + 1)] = str(d)  # 03/05/2017
        data["h_" + str(n + 1)] = "2"
        data["a_" + str(n + 1)] = a.encode('iso8859-15')
        n += 1
    return data


def main():
    login_ = input("LOGIN: ")
    senha_ = getpass("SENHA: ")
    jsessionid = controle.login(login_, senha_)
    data = processa_csv("1411181", "02", 'aulas_lp2.csv')
    controle.chamada(data, jsessionid)
