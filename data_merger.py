"""
Script para converter nomes/turmas em emails por turma.
"""
import csv
import os
import unicodedata

diretorio='disciplinas'

def acha_email(nome):
    res = []
    primeiro = nome[0]
    for i in range(len(nome) - 1, 0, -1):
        for j in range(i - 1, 0, -1):
            res.append(primeiro + '.' + nome[j] + '.' + nome[i])
    res.append(nome[0] + '.' + nome[-1])
    for i in range(len(nome) - 2, 0, -1):
        res.append(primeiro + '.' + nome[i])
    return res

def procura_email(emails, nome):
    for email in acha_email(nome):
        if email in emails:
            return email


emails = set()

with open('all.csv', 'rb') as ficheiro:
    for linha in ficheiro.readlines()[1:]:
        nome = linha[1:].split()[0].split("@")[0].split(".")
        emails.add('.'.join(nome).lower())


for arquivo in os.listdir(diretorio):
    print arquivo
    data = open(diretorio + os.sep + arquivo, 'rb').readlines()[21:]
    pessoas_por_turma = {}
    contagem_por_turma = {}
    for dado in data:
        if not dado.strip():
            continue
	dado = unicodedata.normalize('NFKD', unicode(dado,"ISO-8859-1")).encode("ascii","ignore")
        dado = dado.split()
        nome = ' '.join(dado[:-2]).lower()
        curso = dado[-2]
        matr = dado[-1]
        email = procura_email(emails, nome.split())
        if email:
            galera = pessoas_por_turma.get(curso, [])
            galera.append((email, nome))
            pessoas_por_turma[curso] = galera

            galera = contagem_por_turma.get(curso, 0)
            galera += 1
            contagem_por_turma[curso] = galera
        else:
            galera = contagem_por_turma.get(curso, 0)
            galera -= 1
            contagem_por_turma[curso] = galera
    magia = [(x[0], x[1]) for x in contagem_por_turma.items()]
    magia.sort(key=lambda x: -x[1])
    primeiro = magia[0]
    if (primeiro[1] > 0):
        saida = open('out' + os.sep + arquivo, 'w')
        saida.write('"firstname";"lastname";"email"')
        for pessoa in pessoas_por_turma[primeiro[0]]:
            email, nome = pessoa
            nome, sobrenome = nome.split()[0], ' '.join(nome.split()[1:])
            linha = '"' + nome + '";"' + sobrenome + '";"' + email + '@ccc.ufcg.edu.br"'
            saida.write(linha + '\n')
