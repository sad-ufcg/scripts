import csv
from getpass import getpass
import math

import controle


def _processa_csv(csv_f, delimiter=';'):
    # HEADER: ,1,2,3
    # CONTROLE ACADEMICO: f1_matr, f2_matr, ..
    pages = []
    with open(csv_f, encoding='utf-8-sig', newline='') as csvfile:
        notas_reader = csv.reader(csvfile, delimiter=delimiter, newline='')
        header = next(notas_reader)
        total_pages = int(int(header[-1]) / 10) + 1
        pages = [{} for _ in range(total_pages)]
        for linha in notas_reader:
            matr = linha[0]
            for f, n in zip(header[1:], linha[1:]):
                current_page = int((int(f) - 1) / 10)
                if n:
                    pages[current_page]['f' + f + "_" + matr] = 'f'
                else:
                    pages[current_page]['f' + f + "_" + matr] = ''
    return pages


def processa_csv(codigo, turma, csv_f, delimiter=';'):
    pages = _processa_csv(csv_f, delimiter)
    for n, p in enumerate(pages):
        data = controle.base(codigo, turma, 'ProfessorTurmaFrequenciaConfirmar')
        data["p"] = n + 1
        print(controle.chamada(data, jsessionid).read())


# ICC: 1411001
# LP2: 1411181
# P2 : 1411168
def main():
    login_ = input("LOGIN: ")
    senha_ = getpass("SENHA: ")
    jsessionid = controle.login(login_, senha_)
    processa_csv("1411168", "02", 'presenca.csv')
    print(jsessionid)


if __name__ == "__main__":
    main()
