from openai import OpenAI

def traduire_fr_en_dummy(texte_fr: str, max_chars: int = None, max_words: int = None):
    return "english dummy text"

client = OpenAI(api_key="")

def traduire_fr_en(texte_fr: str, max_chars: int = None, max_words: int = None):
    contraintes = ""

    if max_chars:
        contraintes += f"La traduction doit faire au maximum {max_chars} caractères et au minimum {max_chars//2} caractères. "
    if max_words:
        contraintes += f"La traduction doit contenir au maximum {max_words} mots. "

    prompt = f"""
    Traduis en anglais le texte suivant dans un style formel et académique digne d'un étudiant en école d'ingénieur :
    "{texte_fr}"

    {contraintes}

    Ne rajoute aucune explication. Ne change pas le sens.
    Retourne uniquement la traduction.
    """

    réponse = client.chat.completions.create(
        model="gpt-4o-mini",  # très rapide + très bon
        messages=[{"role": "user", "content": prompt}]
    )

    return réponse.choices[0].message.content.strip()

if __name__ == "__main__":
    max_characters = 1500
    texte_fr = "La méthode aux coefficients de réaction repose sur l’hypothèse fondamentale de la modélisation d’un massif de sol semi-infini par un ensemble de ressorts horizontaux et indépendants, dont la partie élastique est caractérisée par le coefficient de réaction. On s’interrogera dans un premier temps sur le choix de ce coefficient de réaction et ses limites d’application. Ensuite, on questionnera l’hypothèse des ressorts indépendants et on présentera le phénomène d’effet de voûte dans le sol. On étudiera son influence sur les résultats et les paramètres favorisant son apparition. On s’interrogera également sur l’hypothèse du massif de sol semi-infini dans le cas d’une fouille étroite et on étudiera le calcul de la butée dans cette situation. Après les problématiques concernant la modélisation du sol, on s’intéressera aux structures en béton des gares souterraines, modélisées sans prise en compte des phénomènes de fluage et de retrait. Dans la dernière partie, on s’attachera à étudier l’influence de ces deux phénomènes sur les résultats. "
    traduction = traduire_fr_en(texte_fr, max_chars=max_characters)


    traduction = traduire_fr_en(texte_fr)
    print(f"Traduction (max {max_characters} caractères) : {traduction}")
    print(f"Longueur de la traduction : {len(traduction)} caractères")