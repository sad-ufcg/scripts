from getpass import getpass

from bs4 import BeautifulSoup

import controle


def main():
    login_ = input("LOGIN: ")
    senha_ = getpass()
    jsessionid = controle.login(login_, senha_)
    return controle.chamada({"command": "ProfessorTurmasListar"}, jsessionid).read()


def processa(html):
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup.prettify())
    for tb in soup.find_all('tbody'):
        for row in tb.find_all('tr'):
            content = [c.getText().strip() for c in row.find_all('td')]
            print(content)
    
if __name__ == "__main__":
    #processa(open('turmas.htm').read())
    processa(main())
