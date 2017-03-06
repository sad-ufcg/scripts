from getpass import getpass

from bs4 import BeautifulSoup

import controle


class Disciplina:

    def __init__(self, cod, nome, turma):
        self.cod = cod.strip()
        self.nome = nome.strip()
        self.turma = turma.strip()

    def __str__(self):
        return self.cod + " - " + self.turma + " - " + self.nome

    def __repr__(self):
        return self.__str__()


class Aluno:

    def __init__(self, matr, curso, nome, estado):
        self.matr = matr.strip()
        self.curso = curso.strip()
        self.nome = nome.strip()
        self.estado = estado.strip()

    def __str__(self):
        return self.curso + ";" + self.matr + ";" + self.nome + ";" + self.estado

    def __repr__(self):
        return self.__str__()


def data_resumo(codigo, turma):
    data = {"command": "CoordenacaoTurmaResumo",
            "codigo": codigo,
            "turma": turma
            }
    return data


def main():
    login_ = input("LOGIN: ")
    senha_ = getpass()
    jsessionid = controle.login(login_, senha_, "Coordenacao")
    resultado_listagem = controle.chamada({"command": "CoordenacaoDisciplinasOfertadasListar"}, jsessionid).read()
    disciplinas = processa(listagem)
    for disciplina in disciplinas:
        alunos = resumo(disciplina, jsessionid)
        arquivo = open(disciplina.nome + " - " + disciplina.turma + ".csv", 'wb')
        arquivo.write('\n'.join([str(x) for x in processa_resumo(open('coord-alunos.htm', 'rb').read())]))
        arquivo.close()


def processa(html):
    soup = BeautifulSoup(html, 'html.parser')
    disciplinas = []
    for tb in soup.find_all('tbody'):
        for row in tb.find_all('tr'):
            content = [c.getText().strip().replace('\n','').replace('\r','') for c in row.find_all('td')]
            disciplina = Disciplina(*content[0:3])
            disciplinas.append(disciplina)
    return disciplinas


def processa_resumo(html):
    soup = BeautifulSoup(html, 'html.parser')
    alunos = []
    for tb in soup.find_all('tbody'):
        for row in tb.find_all('tr'):
            content = [c.getText().strip().replace('\n','').replace('\r','') for c in row.find_all('td')]
            _, matr, curso, nome, estado = content[0:5]
            aluno = Aluno(matr, curso, nome, estado)
            alunos.append(aluno)
    return alunos


def resumo(disciplina, jsessionid):
    resultado_resumo = controle.chamada(data_resumo(disciplina.cod, disciplina.turma), jsessionid).read()
    
    pass


if __name__ == "__main__":
    main()
    #disciplinas = processa(open('coord-turmas.htm', 'rb').read())
    #disciplinas = processa(main())
    #print('\n'.join([str(x) for x in disciplinas]))
    #'\n'.join([str(x) for x in processa_resumo(open('coord-alunos.htm', 'rb').read())]))
