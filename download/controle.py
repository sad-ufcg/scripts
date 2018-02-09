import urllib.request
import urllib.parse


HEADERS=[("Host", "pre.ufcg.edu.br:8443"),
		 ("User-Agent", "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0"),
		 ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
		 ("Accept-Language", "en-US,en;q=0.5"),
		 ("Upgrade-Insecure-Requests", "1")]


def base(codigo, turma, comando):
    data = {"command": comando,
        "codigo": codigo,
        "turma": turma
        }
    return data

# processar: <br><span class='text-danger'>O campo <strong>Assunto</strong> deve possuir pelo menos 20 caracteres.</span></td>
def chamada(data, jsessionid=None):
    headers = [("Cookie", "JSESSIONID=" + jsessionid)] + HEADERS if jsessionid else HEADERS
    site="https://pre.ufcg.edu.br:8443/ControleAcademicoOnline/Controlador"
    params = urllib.parse.urlencode(data)
    params = params.encode('ascii')
    opener = urllib.request.build_opener()
    opener.addheaders = headers
    return opener.open(site, params)


def login(siape, senha, tipo="Professor"):
    f = chamada(_data_login(siape, senha, tipo))
    print(f.read())
    for x in f.info()['Set-Cookie'].split(';'):
        if x.startswith("JSESSIONID"):
            return x.split('=')[1]


def _data_login(siape, senha, tipo):
    return {"command": tipo + "Login",
	    "login": siape,
	    "senha": senha}


if __name__ == "__main__":
    login_ = input("LOGIN: ")
    senha_ = input("SENHA: ")
    jsessionid = login(login_, senha_)
    print(jsessionid)
    print(chamada({"command": "ProfessorTurmasListar"}, jsessionid).read())
    exit(0)
