import re

class Alumno:
    """
    Representa un alumne amb número d'expedient, nom complet i notes.
    """

    def __init__(self, numExp, nom, notes):
        self.numExp = numExp  # Número d'expedient
        self.nom = nom        # Nom complet
        self.notes = notes    # Llista de notes (floats)

    def mitjana(self):
        # Retorna la mitjana aritmètica de les notes (arrodonida a 1 decimal)
        return round(sum(self.notes) / len(self.notes), 1) if self.notes else 0.0

    def __str__(self):
        # numExp: 12 chars left aligned
        # nom: 30 chars left aligned (reduce from 35 to 30)
        # mitjana: 1 decimal float
        return f"{self.numExp:<11}{self.nom:<34}{self.mitjana():.1f}"


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
