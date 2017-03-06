import math

import controle


def data_notas(codigo, turma, pesos):
    data = {"command": "ProfessorTurmaNotasConfirmar",
	    "codigo": codigo,
	    "turma": turma
		}
    data["notas"] = str(len(pesos))
    data["numNotas"] = str(len(pesos))
    for n, peso in enumerate(pesos):
        data["peso" + str(n + 1)] = str(peso)
    return data


def notas_csv(csv):
    # HEADER: matr,n1,n2,n3,f
    # CONTROLE ACADEMICO: n1_matr, n2_matr, .. final = f
    data = {}
    lines = open(csv).readlines()
    header = lines[0].strip().split(',')
    # 1 casa decimal, virgulas no lugar de ponto:
    conv = lambda y: ("%.1f" % (math.ceil(10 * float(y)) / 10)).replace('.', ',')
    for line in lines[1:]:
        line = line.strip()
        cols = line.split(',')
        matr = cols[0]
        for field, nota in zip(header[1:], cols[1:]):
            if nota:
                data[field + "_" + matr] = conv(nota)
    return data


login_ = input("LOGIN: ")
senha_ = input("SENHA: ")
data = data_notas("1411168", "02", [27, 27, 26, 20])
data.update(notas_csv("p2.csv"))
jsessionid = controle.login(login_, senha_)
print(jsessionid)
print(controle.chamada(data, jsessionid).read())
