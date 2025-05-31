import re

def normalizaHoras(ficText, ficNorm):
    with open(ficText, encoding='utf-8') as f:
        lineas = f.readlines()

    patrones = [
        # 1. hh:mm
        (re.compile(r'\b(?P<h>\d{1,2}):(?P<m>\d{2})\b'), lambda h, m, _: validar_hora(h, m)),

        # 2. hhHmMm, hhH
        (re.compile(r'\b(?P<h>\d{1,2})h(?P<m>\d{1,2})m\b'), lambda h, m, _: validar_hora(h, m)),
        (re.compile(r'\b(?P<h>\d{1,2})h\b'), lambda h, _, __: validar_hora(h, 0)),

        # 3. 8 en punto
        (re.compile(r'\b(?P<h>\d{1,2})\s+en punto\b'), lambda h, _, __: validar_hora(h, 0)),

        # 4. 8 y cuarto/media/menos cuarto
        (re.compile(r'\b(?P<h>\d{1,2})\s+y\s+cuarto\b'), lambda h, _, __: validar_hora(h, 15)),
        (re.compile(r'\b(?P<h>\d{1,2})\s+y\s+media\b'), lambda h, _, __: validar_hora(h, 30)),
        (re.compile(r'\b(?P<h>\d{1,2})\s+menos\s+cuarto\b'), lambda h, _, __: validar_hora(int(h) - 1, 45)),

        # 5. hh amb franja (matí, tarda...)
        (re.compile(r'\b(?P<h>\d{1,2})(?::(?P<m>\d{2}))?\s+de la (?P<franja>mañana|tarde|noche|madrugada)\b'), lambda h, m, franja: convertir_con_franja(h, m, franja)),
    
        # 6. del mediodía
        (re.compile(r'\b(?P<h>\d{1,2})(?::(?P<m>\d{2}))?\s+(de la|del)\s+(?P<franja>mañana|tarde|noche|madrugada|mediodía)\b')),

        (re.compile(r'\b(?P<h>\d{1,2})\s+(y\s+(?P<tipo>cuarto|media)|menos\s+(?P<menos>cuarto))\s+(de la|del)\s+(?P<franja>mañana|tarde|noche|madrugada|mediodía)\b')),

    ]

    nuevas_lineas = []
    lambda h, m, franja, tipo=None, menos=None: convertir_franja_con_palabras(h, tipo, menos, franja)


    for linea in lineas:
        original = linea
        for patron, funcion in patrones:
            def reemplazo(m):
                h = m.group('h')
                mnt = m.group('m') if 'm' in m.groupdict() else 0
                franja = m.group('franja') if 'franja' in m.groupdict() else None
                try:
                    hhmm = funcion(h, mnt, franja)
                    if hhmm:
                        return hhmm
                except:
                    pass
                return m.group(0)
            linea = patron.sub(reemplazo, linea)
        nuevas_lineas.append(linea)

    with open(ficNorm, 'w', encoding='utf-8') as f:
        f.writelines(nuevas_lineas)

def validar_hora(h, m):
    h, m = int(h), int(m)
    if 0 <= h <= 23 and 0 <= m <= 59:
        return f"{h:02d}:{m:02d}"
    return None

def convertir_con_franja(h, m, franja):
    h = int(h)
    m = int(m) if m else 0

    if h == 0 or h > 12 or m > 59:
        return None

    if franja == 'mañana':  # 4-12 -> 04-12
        if 4 <= h <= 11:
            return f"{h:02d}:{m:02d}"
        elif h == 12:
            return f"00:{m:02d}"
    elif franja == 'mediodía':  # 12-15 -> 12-15
        if 12 <= h <= 15:
            return f"{h:02d}:{m:02d}"
    elif franja == 'tarde':  # 16-20
        if 1 <= h <= 7:
            return f"{h+12:02d}:{m:02d}"
    elif franja == 'noche':  # 21-03
        if 8 <= h <= 11:
            return f"{h+12:02d}:{m:02d}"
        elif h == 12:
            return f"00:{m:02d}"
    elif franja == 'madrugada':
        if 1 <= h <= 6:
            return f"{h:02d}:{m:02d}"
    return None

def convertir_franja_con_palabras(h, tipo, menos, franja):
    h = int(h)
    if menos:
        h -= 1
        m = 45
    elif tipo == 'cuarto':
        m = 15
    elif tipo == 'media':
        m = 30
    else:
        m = 0
    return convertir_con_franja(h, m, franja)

def _test():
    """
    >>> validar_hora("17", "05")
    '17:05'
    >>> validar_hora("17", "5") is None
    True
    >>> convertir_con_franja("6", "15", "de la tarde")
    '18:15'
    >>> convertir_con_franja("7", None, "noche")
    '19:00'
    >>> convertir_franja_con_palabras("5", "media", None, "mañana")
    '05:30'
    """

if __name__ == '__main__':
    import doctest
    doctest.testmod()
