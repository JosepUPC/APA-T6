import re
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

    def leeAlumnos(ficAlum):
        """
        Lee un fichero de texto con los datos de los alumnos y devuelve un 
        diccionario donde la clave es el nombre completo y el valor es un 
        objeto Alumno con sus datos.

        El fichero debe contener líneas en las que:
        - El primer valor es el número de identificación (entero)
        - Luego viene el nombre (uno o varios nombres)
        - Finalmente, una lista de notas (reales)

        El análisis se realiza con expresiones regulares.

        >>> alumnos = leeAlumnos('alumnos.txt')
        >>> for alumno in alumnos:
        ...     print(alumnos[alumno])
        ...
        171     Blanca Agirrebarrenetse 9.5
        23      Carles Balcells de Lara 4.9
        68      David Garcia Fuster     7.0
        """
        alumnos = {}
        patron = re.compile(r"""
            ^\s*
            (?P<id>\d+)\s+                    # número de identificación
            (?P<nombre>(?:[^\d\.]+\s+)+?)     # nombre completo (no empieza con número o punto)
            (?P<notas>(?:\d+(?:\.\d+)?\s*)+)  # lista de notas (números decimales)
            \s*$
        """, re.VERBOSE)

        with open(ficAlum, 'r', encoding='utf-8') as f:
            for linea in f:
                match = patron.match(linea)
                if match:
                    numIden = int(match.group('id'))
                    nombre = match.group('nombre').strip()
                    notas = list(map(float, match.group('notas').split()))
                    alumnos[nombre] = Alumno(nombre, numIden, notas)
        return alumnos
    
    if __name__ == "__main__":
        import doctest
        doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
