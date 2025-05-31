"""
horas.py

Normalitza expressions d'hores en castellà al format HH:MM.
Les que no es poden reconèixer bé es deixen igual.
"""

import re

def normalizaHoras(ficText, ficNorm):
    # Llegeix tot el contingut del fitxer original
    with open(ficText, encoding="utf-8") as f:
        texto = f.read()

    def a24h(hora, periodo):
        """Converteix de 12h a 24h segons si és matí, tarda, etc."""
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
        return -1  # si no encaixa amb cap període

    def normalitzar(match):
        # Cas format HH:MM → ja està bé, només comprovem que el minut tingui 2 xifres
        if match.group("formato1"):
            h, m = match.group("h1"), match.group("m1")
            if len(m) == 1:
                return match.group(0)  # si minut és raro, ho deixem com està
            return f"{int(h):02}:{int(m):02}"

        # Cas tipus 8h, 10h30m → convertim al format correcte si té sentit
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

        # Cas "7 en punto" → el minut sempre és 00
        if match.group("formato3"):
            h = int(match.group("h3"))
            if h > 23:
                return match.group(0)
            return f"{h:02}:00"

        # Cas com "4 y media", "5 menos cuarto" → fem càlculs segons si és media, cuarto, etc.
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

        # Cas com "7 de la mañana", "9 de la noche" → convertim al format de 24h
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

        # Si no és cap dels casos → deixem la frase igual
        return match.group(0)

    # Compilem una expressió regular que detecta diferents formats d'hores
    patron = re.compile(r"""
        (?P<formato1>(?P<h1>\d{1,2}):(?P<m1>\d{2}))                         | # 18:30
        (?P<formato2>(?P<h2>\d{1,2})h(?P<m2>\d{1,2})?m?)                    | # 8h, 10h30m
        (?P<formato3>(?P<h3>\d{1,2})\s+en\s+punto)                          | # 7 en punto
        (?P<formato4>(?P<h4>\d{1,2})\s+(y\s+(cuarto|media)|menos\s+cuarto))| # 4 y media
        (?P<formato5>(?P<h5>\d{1,2})\s+de\s+la\s+(mañana|tarde|noche|mediodía|madrugada)) # 7 de la mañana
    """, re.VERBOSE | re.IGNORECASE)

    # Substituïm les hores trobades pel format normalitzat
    texto_normalizado = patron.sub(normalitzar, texto)

    # Guardem el text modificat al nou fitxer
    with open(ficNorm, "w", encoding="utf-8") as f:
        f.write(texto_normalizado)