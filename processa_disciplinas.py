import re
import sys

# Processa o PDF de disciplinas quando convertido para TXT
def processa(arquivo):
    disciplina = ''
    lendo_disciplina = False
    turma = None
    lendo_prof = False
    prof_re = re.compile('([0-9]+) - ([\W\w ]+)', re.UNICODE)
    disciplinas = []
    for l in open(arquivo, 'r').readlines():
        l = l.strip()
        if lendo_disciplina:
            if lendo_prof:
                if not l.strip():
                    disciplinas.append((disciplina, turma, profs))
                    lendo_disciplina = False
                    turma = None
                    lendo_prof = False
                else:
                    prof_m = prof_re.match(l)
                    if prof_m:
                        profs.append((prof_m.group(1), prof_m.group(2)))
            elif l.startswith('Ofer.'):
                lendo_prof = True
                profs = []
            elif not turma:
                if l.strip().isdigit():
                    turma = l
        else:
            if l.startswith('Ofertada'):
                lendo_disciplina = True
            else:
                disciplina = l
    return disciplinas

if __name__ == "__main__":
    import pprint
    pprint.pprint(processa(sys.argv[1]))
