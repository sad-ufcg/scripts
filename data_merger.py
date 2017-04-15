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
    for email in acha_email(nome.split()) + acha_email(nome[0:40].split()):
        if email in emails:
            return email


emails = set()

with open('all.csv', 'r') as ficheiro:
    for linha in ficheiro.readlines()[1:]:
        nome = linha[1:].split()[0].split("@")[0].split(".")
        emails.add('.'.join(nome).lower())

# 14102100;112222222;EI BOY TUDO BOM;Em Curso

for arquivo in os.listdir(diretorio):
    print(arquivo)
    data = open(diretorio + os.sep + arquivo, 'r').readlines()
    pessoas_por_turma = {}
    contagem_por_turma = {}
    for dado in data:
        dado = unicodedata.normalize('NFKD', unicode(dado, 'utf-8')).encode("ascii","ignore").lower()
        dado = dado.split(';')
        nome = dado[2]
        matr = dado[1]
        email = procura_email(emails, nome)
        galera = []
        if email:
            galera.append((email, nome))
        else:
            print(">>>MISSING:", nome)
    if galera:
        saida = open('out' + os.sep + arquivo, 'w')
        saida.write('"firstname";"lastname";"email"')
        for pessoa in galera:
            email, nome = pessoa
            nome, sobrenome = nome.split()[0], ' '.join(nome.split()[1:])
            linha = '"' + nome + '";"' + sobrenome + '";"' + email + '@ccc.ufcg.edu.br"'
            saida.write(linha + '\n')
