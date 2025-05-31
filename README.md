# Expresiones Regulares

## Nom i cognoms

## Tratamiento de ficheros de notas

Con el final de curso llega la ardua tarea de evaluar las tareas realizadas por los alumnos durante el
mismo. Para facilitar esta tarea, se dispone de la clase `Alumno` que proporciona los datos
fundamentales de cada alumno: su número de identificación (`numIden`), su nombre completo 
(`nombre`) y la lista de notas obtenidas a lo largo del curso (`notas`). La clase también
proporciona métodos para añadir una nota al expediente del alumno (`__add__()`), para obtener
la representación *oficial* del mismo (`__repr__()`) y para obtener la representación
*bonita* (`__str__()`).

La definición de la clase `Alumno`, disponible en `alumno.py`, es:

```python
class Alumno:
    """
    Clase usada para el tratamiento de las notas de los alumnos. Cada uno
    incluye los atributos siguientes:

    numIden:   Número de identificación. Es un número entero que, en caso
               de no indicarse, toma el valor por defecto 'numIden=-1'.
    nombre:    Nombre completo del alumno.
    notas:     Lista de números reales con las distintas notas de cada alumno.
    """

    def __init__(self, nombre, numIden=-1, notas=[]):
        self.numIden = numIden
        self.nombre = nombre
        self.notas = [nota for nota in notas]

    def __add__(self, other):
        """
        Devuelve un nuevo objeto 'Alumno' con una lista de notas ampliada con
        el valor pasado como argumento. De este modo, añadir una nota a un
        Alumno se realiza con la orden 'alumno += nota'.
        """
        return Alumno(self.nombre, self.numIden, self.notas + [other])

    def media(self):
        """
        Devuelve la nota media del alumno.
        """
        return sum(self.notas) / len(self.notas) if self.notas else 0

    def __repr__(self):
        """
        Devuelve la representación 'oficial' del alumno. A partir de copia
        y pega de la cadena obtenida es posible crear un nuevo Alumno idéntico.
        """
        return f'Alumno("{self.nombre}", {self.numIden!r}, {self.notas!r})'

    def __str__(self):
        """
        Devuelve la representación 'bonita' del alumno. Visualiza en tres
        columnas separas por tabulador el número de identificación, el nombre
        completo y la nota media del alumno con un decimal.
        """
        return f'{self.numIden}\t{self.nombre}\t{self.media():.1f}'
```

A menudo, las notas de los alumnos se almacenan en ficheros de texto en los que los datos de cada alumno
ocupan una línea con los distintos valores separados por espacios y/o tabuladores.

El ejemplo siguiente muestra un fichero típico con las notas de tres alumnos:

```text
171 Blanca Agirrebarrenetse 10  	9 	  9.5
23  Carles Balcell de Lara  5 	    5 	  4.5  	5.2
68  David Garcia Fuster 	7.75    5.25  8   
```

Añada al fichero `alumno.py` la función `leeAlumnos(ficAlum)` que lea un fichero de texto con los datos de 
todos los alumnos y devuelva un diccionario en el que la clave sea el nombre de cada alumno y su contenido 
el objeto `Alumno` correspondiente.

La función deberá cumplir los requisitos siguientes:

- Sólo debe realizar lo que se indica; es decir, debe leer el fichero de texto que se le pasa como único
  argumento y devolver un diccionario con los datos de los alumnos.
- El análisis de cada línea de texto se realizará usando expresiones regulares.
- La función `leeAlumnos()` debe incluir, en su cadena de documentación, la prueba unitaria siguiente según
  el formato de la biblioteca `doctest`, donde el fichero `'alumnos.txt'` es el fichero mostrado como ejemplo
  al principio de este enunciado:

  ```python
  >>> alumnos = leeAlumnos('alumnos.txt')
  >>> for alumno in alumnos:
  ...     print(alumnos[alumno])
  ...
  171     Blanca Agirrebarrenetse 9.5
  23      Carles Balcells de Lara 4.9
  68      David Garcia Fuster     7.0
  ```

  - Evidentemente, es responsabilidad del autor comprobar que la prueba unitaria se pasa satisfactoriamente
    antes de la entrega de la tarea.

  - Para evitar que diferencias debidas a espacios en blanco o tabuladores den lugar a error, se recomienda
    efectuar las pruebas unitarias con la opción `doctest.NORMALIZE_WHITESPACE`. Por ejemplo,
    `doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)`.


## Análisis de expresiones horarias

En casi todos los idiomas más habituales, cualquier hora puede reducirse al formato estándar HH:MM, donde HH es 
un número de dos dígitos, que representa la hora y está comprendido entre 00 y 23, y MM es otro número de dos 
dígitos, que representa el minuto y está comprendido entre 00 y 59.

No obstante, en el lenguaje hablado, es raro usar este formato estándar. En el caso del castellano, existe una
gran variedad de formatos. La lista siguiente alguna de las posibilidades más frecuentes, aunque existen bastantes
más:

- **08:27**

  Es el formato estándar. Cuando la hora es menor que 10, es posible representarla con
  dos dígitos (08:27), o sólo uno (8:27). Los minutos se representan siempre con dos (8:05).

- **8h27m**

  Las horas o minutos menores que 10 pueden representarse usando uno o dos dígitos. Las horas
  *en punto* pueden indicarse sin minutos (8h).

- **8 en punto**

  Las horas exactas suelen indicarse con la partícula *'en punto'*. En ese caso, es
  habitual omitir la letra *h* después de la cifra.

  Otras alternativas semejantes son las *'8 y cuarto'*, las *'8 y media'* o las *'8 menos cuarto'*.

  En todos estos casos, el reloj empleado será de 12 horas y empezando en 1 (de 1 a 12). El
  resultado será ambiguo, ya que no sabremos si una cierta hora es AM o PM, pero así es cómo
  se suele hablar (la gente queda a *'las 11 en punto'* para ir a una fiesta, no a las
  *'las 23 en punto'*). El resultado se devolverá siempre en el rango de 00:00 a 11:59.

- **... de la mañana**

  Las expresiones horarias entre las 4 y las 12 pueden ir seguidas de la partícula *'de la mañana'*.

  Análogamente, las horas entre las 12 y las 3 pueden ir seguidas de *'del mediodía'*, las horas entre
  las 3 y las 8 pueden serlo de *'de la tarde'*, entre 8 y 4 de *'de la noche'* y entre 1 y
  6 de *'de la madrugada'*.

  En estos casos, el reloj empleado es siempre de 12 horas (nunca se dice *'las 18 de la tarde'*, sino
  *'las 6 de la tarde'*). Además la hora no puede ser cero, sino que, en ese caso, se usaría 12.

### Tarea: normalización de las expresiones horarias de un texto

Escriba el fichero `horas.py` con la función `normalizaHoras(ficText, ficNorm)`, que lee el fichero de
texto `ficText`, lo analiza en busca de expresiones horarias y escribe el fichero `ficNorm` en el que
éstas se expresan según el formato normalizado, con las horas y los minutos indicados por dos dígitos
y separados por dos puntos (08:27).

Cada línea del fichero puede contener, o no, una o más expresiones horarias, pero éstas nunca aparecerán
partidas en más de una línea.

Las horas con expresión incorrecta, por ejemplo, *'17:5'* (en la expresión normalizada deben usarse dos
dígitos para expresar los minutos) u *'11 de la tarde'* (la tarde nunca llega hasta esa hora), deben
dejarse tal cual.

Para la evaluación de la tarea se usará un texto con unas cien expresiones horarias, que incluirán tanto
expresiones correctas como incorrectas. Una parte de la nota dependerá de la precisión en su normalización.

Se recomienda empezar normalizando textos que sólo contengan expresiones correctas del tipo más sencillo;
es decir, con la forma *'18h45m'*. La consecución de este objetivo garantiza una nota mínima de notable
bajo (7). La extensión al resto de formatos indicados y la detección de expresiones incorrectas serán
necesarias para alcanzar la nota máxima (10).

La tabla siguiente muestra un ejemplo de texto antes y después de su normalización, incluyendo tanto
expresiones horarias **correctas** como <span style="color:red">**incorrectas**</span>.

### Ejemplo de normalización de las expresiones horarias de un texto

Las líneas siguientes muestran ejemplos de expresiones horarias, tanto correctas como incorrectas. Las
mismas expresiones se encuentran en el fichero `horas.txt`, que puede usar para comprobar el correcto
funcionamiento de su función.

#### Expresiones válidas

> - La llegada del tren está prevista a las **18:30**
> - La llegada del tren está prevista a las **18:30**

> - Tenía su clase entre las **8h** y las **10h30m**
> - Tenía su clase entre las **08:00** y las **10:30**

> - Se acaba a las **4 y media de la tarde**
> - Se acaba a las **16:30**

> - Empieza a trabajar a las **7h de la mañana**
> - Empieza a trabajar a las **07:00**

> - Es lo mismo **5 menos cuarto** que **4:45**
> - Es lo mismo **04:45** que **04:45**

> - Tenemos descanso hasta las **17h5m**
> - Tenemos descanso hasta las **17:05**

> - Las campanadas son a las **12 de la noche**
> - Las campanadas son a las **00:00**

#### Expresiones incorrectas

> - Son exactamente las $\textbf{\color{red}17:5}$
> - Son exactamente las $\textbf{\color{red}17:5}$

> - Cuando llegó, ya eran las $\textbf{\color{red}11 de la tarde}$
> - Cuando llegó, ya eran las $\textbf{\color{red}11 de la tarde}$

> - El examen es a las $\textbf{\color{red}17 de la tarde}$
> - El examen es a las $\textbf{\color{red}17 de la tarde}$

> - Cenamos en las $\textbf{\color{red}7}$ puertas
> - Cenamos en las $\textbf{\color{red}7}$ puertas

> - No llegará antes de las $\textbf{\color{red}1h78m}$
> - No llegará antes de las $\textbf{\color{red}1h78m}$

> - *Corrió* la maratón en $\textbf{\color{red}32h31m}$, pero no ganó
> - *Corrió* la maratón en $\textbf{\color{red}32h31m}$, pero no ganó

> - Quedamos a las $\textbf{\color{red}23 en punto}$
> - Quedamos a las $\textbf{\color{red}23 en punto}$


#### Entrega

##### Ficheros `alumno.py` y `horas.py`

- Ambos ficheros deben incluir una cadena de documentación con el nombre del alumno o alumnos
  y una descripción de su contenido.

- Se valorará lo pythónico de la solución; en concreto, su claridad y sencillez, y el
  uso de los estándares marcados por PEP-ocho.

##### Ejecución de los tests unitarios de `alumno.py`

Inserte a continuación una captura de pantalla que muestre el resultado de ejecutar el
fichero `alumno.py` con la opción *verbosa*, de manera que se muestre el
resultado de la ejecución de los tests unitarios.

![](Test.jpg)

##### Código desarrollado

Inserte a continuación los códigos fuente desarrollados en esta tarea, usando los
comandos necesarios para que se realice el realce sintáctico en Python del mismo (no
vale insertar una imagen o una captura de pantalla, debe hacerse en formato *markdown*).

###### Alumnos

```python
def leeAlumnos(ficAlum):
    """
    Llegeix un fitxer amb dades d'alumnes i retorna un diccionari amb objectes Alumno.

    També escriu al fitxer 'visto.txt' un resum dels alumnes i la seva mitjana.

    >>> alumnes = leeAlumnos("alumnos.txt")
    >>> for a in sorted(alumnes.values(), key=lambda x: x.numExp):
    ...     print(a)
    23         Carles Balcell de Lara            4.9
    68         David Garcia Fuster               7.0
    171        Blanca Agirrebarrenetse           9.5
    """

    alumnes = {}  # Diccionari per guardar els objectes Alumno

    # Obrim el fitxer d'entrada
    with open(ficAlum, encoding="utf-8") as f:
        for linia in f:
            # Extraiem totes les xifres (notes i número d'expedient)
            trobat = re.findall(r"\d+(?:\.\d+)?", linia)
            if not trobat:
                continue  # Ignorem línies sense dades

            numExp = int(trobat[0])            # Primer número = número d'expedient
            notes = list(map(float, trobat[1:]))  # La resta són notes

            # Eliminem les xifres de la línia per extreure el nom
            nom = re.sub(r"\d+(?:\.\d+)?", "", linia).strip()
            nom = re.sub(r"\s+", " ", nom)  # Netegem espais múltiples

            # Guardem l'objecte Alumno al diccionari
            alumnes[numExp] = Alumno(numExp, nom, notes)

    # Obrim el fitxer de sortida per escriure els resultats
    with open("visto.txt", "w", encoding="utf-8") as fout:
        for a in sorted(alumnes.values(), key=lambda x: x.numExp):
            fout.write(str(a) + "\n")  # Escrivim cada alumne amb mitjana

    return alumnes


# Només executem els tests si s'executa com a programa principal
if __name__ == "__main__":
    import doctest
    # Executem els tests incrustats al docstring
    doctest.testmod(verbose=True)
```

###### Horas

```python
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
```

##### Subida del resultado al repositorio GitHub y *pull-request*

La entrega se formalizará mediante *pull request* al repositorio de la tarea.

El fichero `README.md` deberá respetar las reglas de los ficheros Markdown y
visualizarse correctamente en el repositorio, incluyendo la imagen con la ejecución de
los tests unitarios y el realce sintáctico del código fuente insertado.

##### Y NADA MÁS

Sólo se corregirá el contenido de este fichero `README.md` y los códigos fuente `alumno.py`
y `horas.py`. No incluya otros ficheros con código fuente, notebooks de Jupyter o explicaciones
adicionales; simplemente, no se tendrán en cuenta para la evaluación de la tarea. Evidentemente,
sí puede añadir ficheros con las imágenes solicitadas en el enunciado, pero éstas deberán ser
visualizadas correctamente desde este mismo fichero al acceder al repositorio de la tarea.