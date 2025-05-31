"""
horas.py

Conté la funció normalizaHoras(ficText, ficNorm), que llegeix un fitxer de text
amb expressions horàries en format oral i escrit en castellà, i les normalitza al format HH:MM.
Les expressions incorrectes es deixen intactes.
"""

import re

def normalizaHoras(ficText, ficNorm):
    with open(ficText, encoding="utf-8") as f:
        texto = f.read()

    def a24h(hora, periodo):
        """Converteix hora de 12h a 24h segons el període"""
        if hora == 12:
            hora = 0
        if periodo == "mañana":
            return hora
        elif periodo == "mediodía":
            return hora + 12 if hora < 12 else 12
        elif periodo == "tarde":
            return hora + 12 if 1 <= hora <= 7 else -1
        elif periodo == "noche":
            return hora + 12 if 8 <= hora <= 11 else 0 if hora == 12 else -1
        elif periodo == "madrugada":
            return hora if 1 <= hora <= 6 else -1
        return -1

    def normalitzar(match):
        if match.group("formato1"):
            h, m = match.group("h1"), match.group("m1")
            if len(m) == 1:
                return match.group(0)  # minut mal format
            return f"{int(h):02}:{int(m):02}"

        if match.group("formato2"):
            h = int(match.group("h2"))
            m = match.group("m2")
            if m:
                m = int(m)
                if m > 59:
                    return match.group(0)
            else:
                m = 0
            if h > 23:
                return match.group(0)
            return f"{h:02}:{m:02}"

        if match.group("formato3"):
            h = int(match.group("h3"))
            if h > 23:
                return match.group(0)
            return f"{h:02}:00"

        if match.group("formato4"):
            h = int(match.group("h4"))
            if "cuarto" in match.group(0):
                m = 15
            elif "media" in match.group(0):
                m = 30
            elif "menos cuarto" in match.group(0):
                h = h - 1 if h > 1 else 12
                m = 45
            else:
                return match.group(0)
            return f"{h % 12:02}:{m:02}"

        if match.group("formato5"):
            h = int(match.group("h5"))
            periodo = match.group("p5").strip()
            pmap = {
                "mañana": "mañana",
                "mediodía": "mediodía",
                "tarde": "tarde",
                "noche": "noche",
                "madrugada": "madrugada"
            }
            p = pmap.get(periodo, "")
            h24 = a24h(h, p)
            if h24 == -1:
                return match.group(0)
            return f"{h24:02}:00"

        return match.group(0)

    patron = re.compile(r"""
        (?P<formato1>(?P<h1>\d{1,2}):(?P<m1>\d{2}))                         | # 18:30
        (?P<formato2>(?P<h2>\d{1,2})h(?P<m2>\d{1,2})?m?)                    | # 8h, 10h30m
        (?P<formato3>(?P<h3>\d{1,2})\s+en\s+punto)                          | # 7 en punto
        (?P<formato4>(?P<h4>\d{1,2})\s+(y\s+(cuarto|media)|menos\s+cuarto))| # 4 y media
        (?P<formato5>(?P<h5>\d{1,2})\s+de\s+la\s+(mañana|tarde|noche|mediodía|madrugada)) # 7 de la mañana
    """, re.VERBOSE | re.IGNORECASE)

    texto_normalizado = patron.sub(normalitzar, texto)

    with open(ficNorm, "w", encoding="utf-8") as f:
        f.write(texto_normalizado)
