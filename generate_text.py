import subprocess

# ==============================
# 1) TEMPLATE LATEX
# ==============================
latex = r"""
\documentclass[12pt,a4paper]{article}

\usepackage{amssymb}
% Cases à cocher personnalisées
\newcommand{\CheckedBox}{\ensuremath{\boxtimes}} % case "cochée"
\newcommand{\EmptyBox}{\ensuremath{\square}} % case "non cochée"
\usepackage{graphicx}
\usepackage[a4paper, top=3cm, bottom=1.8cm, left=1.2cm, right=1.2cm]{geometry}
\usepackage{titlesec}
\usepackage{titleps}

\newpagestyle{pontsstyle}{
    \sethead{}{\textbf{École nationale des Ponts et Chaussées}}{}
    \setfoot{}{}{}
}

\pagestyle{pontsstyle}
\setlength{\headsep}{1.5cm}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[french]{babel}
\usepackage{longtable}

\setlength{\parindent}{0pt}
\renewcommand{\arraystretch}{1.2}

\begin{document}

\begin{center}
    {\Large \textbf{Annuel des PFE - TEST 4}}\\[0.2cm]
    Merci de respecter la casse (minuscules/majuscules).
\end{center}

\vspace{0.7cm}

\begin{longtable}{|p{7cm}|p{9cm}|}
\hline
    \textbf{Département d'enseignement} & __Departement_Enseignement__ \\ \hline
    \textbf{Prénom NOM} & __Prenom_NOM__ \\ \hline
    \textbf{Adresse mail permanente} & __Adresse_mail_permanente__ \\ \hline
    \textbf{Statut étudiant entrepreneur} & __Statut_etudiant_entrepreneur__~ \\ \hline
    \textbf{Profil (voie d'entrée)} & __Profil__ \\ \hline
    \textbf{Si Double diplôme, préciser Établissement, Ville, Pays} & __Double_diplome__ \\ \hline
    \textbf{Titre du parcours ou de toute formation diplômante en 3A (le cas échéant), qu'elle soit effectuée dans l'École ou à l'extérieur} & __Titre_parcours_3A__ \\ \hline
    \textbf{Si vous avez indiqué une formation diplômante à la case précédente, précisez le nom de l'établissement, la ville et le pays.} & __Etablissement_formation_3A__ \\ \hline
    \textbf{Promotion (indiquez l'année)} & __Promotion__ \\ \hline
    \textbf{Votre photo portrait (minimum 295 pixels de large, sous format jpeg ou png)} & \center\includegraphics[width=4cm]{__Photo_portrait__} \\ \hline
    \textbf{Type de PFE} & __Type_de_PFE__ \\ \hline
    \textbf{Organisme du PFE} & __Organisme_du_PFE__ \\ \hline
    \textbf{Type d'organisme d'accueil} & __Type_organisme_accueil__ \\ \hline
    \textbf{Tuteur professionnel} sous la forme Prénom NOM& __Tuteur_professionnel__ \\ \hline
    \textbf{Fonction du tuteur professionnel} & __Fonction_tuteur_professionnel__ \\ \hline
    \textbf{Tuteur académique} sous la forme Prénom NOM & __Tuteur_academique__ \\ \hline
    \textbf{Fonction du tuteur académique} & __Fonction_tuteur_academique__ \\ \hline
    \textbf{Organisme de rattachement du tuteur académique} & __Organisme_rattachement_tuteur_academique__ \\ \hline
    \textbf{Langue de rédaction du PFE} & __Langue_de_redaction__ \\ \hline
    \textbf{Si PFE Non confidentiel} & ~Je suis en accord avec la phrase suivante :~__Si_PFE_Confidentiel__~ \newline\newline« Pour l'Annuel des PFE, je fournis dans ce questionnaire des éléments non confidentiels de mon travail. J'en autorise la diffusion au format numérique et papier. »\\ \hline
    \textbf{Si PFE Confidentiel} &  Je suis d'accord avec la phrase suivante : ~__Si_PFE_Confidentiel__~ \newline\newline « Je suis informé(e) que les éléments textuels et iconographiques demandés dans ce questionnaire sont destinés à une publication numérique et papier (Annuel des PFE). Je m'engage à ne fournir que des éléments diffusables et en autorise la diffusion. » \\ \hline
    \textbf{Durée de confidentialité} & __Duree_de_confidentialite__ \\ \hline
    \textbf{Titre du PFE en français} (Entre 10 et 75 signes espaces compris) & __Titre_PFE_FR__ \\ \hline
    \textbf{Thématique principale \newline\newline 
(Se référer à la liste fournie par le Département)} & __Thematique_principale__ \\ \hline
    \textbf{Mots-clés en français (3 à 5) (séparés par des ; sans majuscule)} & __Mots_cles_FR__ \\ \hline
    \textbf{Présentation du contexte du PFE (version non confidentielle)} Longueur conseillée entre 200 et 450 signes, espaces compris
 & __Presentation_contexte_FR__ \\ \hline
    \textbf{Présentation des missions et objectifs du PFE (version non confidentielle)} Longueur conseillée entre 200 et 450 signes, espaces compris & __Presentation_missions_FR__ \\ \hline
    \textbf{Résumé en français du PFE (version non confidentielle)} Longueur conseillée entre 1150 et 1700 signes, espaces compris & __Resume_FR__ \\ \hline
    \textbf{Titre du PFE en anglais} (Entre 10 et 75 signes espaces compris) & __Titre_PFE_EN__ \\ \hline
    \textbf{Mots-clés en anglais (3 à 5)} & __Mots_cles_EN__ \\ \hline
    \textbf{Présentation du contexte du PFE en anglais (version non confidentielle)} Longueur conseillée : entre 200 et 450 signes, espaces compris & __Presentation_contexte_EN__ \\ \hline
    \textbf{Présentation des missions et objectifs du PFE en anglais (version non confidentielle)} Longueur conseillée : entre 200 et 450 signes, espaces compris & __Presentation_missions_EN__ \\ \hline
    \textbf{Résumé du PFE en anglais (version non confidentielle)}\newline\newline Longueur conseillée entre 1150 et 1700 signes, espaces compris & __Resume_EN__ \\ \hline
    \textbf{Bibliographie}\newline\begin{itemize} \item Référence 1 (optionnel) : \item Référence 2 (optionnel) : \item Référence 3 (optionnel) : \end{itemize} &\begin{itemize} \item __Bibliographie1__  \item __Bibliographie2__  \item __Bibliographie3__ \end{itemize}  \\ \hline
    \textbf{Image associée} \newline\newline
    (Graphique, photographie…)\newline\newline
    \textbf{À noter :} Sans références précises l’image ne sera pas publiée.\newline\newline
    Si vous n’êtes pas l’auteur principal de l’illustration utilisée, vous pouvez demander au 
    propriétaire une autorisation d’utilisation et de reproduction. Si vous l’obtenez, merci de
    la joindre à votre dossier.& Nom du fichier transmis en annexe de ce fichier 
    Word, au format jpeg ou png : \newline\newline  __Nom_Image_associee__ \newline\newline \textbf{Légende :}\newline\newline __Legende__
    \newline\newline Droits : Nom du photographe ou de l’auteur, références bibliographiques d’où est issue l’image…\newline\newline
    __Nom_Du_Photographe__\\ \hline
\end{longtable}
\vspace{0.8cm}
\newpage
% Cases à cocher contrôlées par Python
\noindent __CHECK_1__~Je confirme que les éléments textuels et iconographiques transmis dans ce questionnaire
sont non confidentiels et diffusables au format numérique et papier (Annuel des PFE).\\[0.25cm]

\noindent __CHECK_2__~Je confirme et autorise la diffusion.\\[0.25cm]

\noindent __CHECK_3__~Je certifie sur l'honneur l'exactitude des informations.

\vspace{1cm}

\begin{center}
\rule{4cm}{0.4pt}\\

\end{center}

\vspace{0.8cm}

\textbf{Validation du département}

\vspace{0.2cm}

\begin{tabular}{|p{7cm}|p{9cm}|}
\hline
\textbf{Date de validation} & \\[0.8cm] \hline
\textbf{Nom du valideur} & \\[0.8cm] \hline
\textbf{Mail du valideur} & \\[0.8cm] \hline
\end{tabular}

\end{document}
"""

# ==============================
# 2) VARIABLES À INSÉRER
# ==============================
variables = {
    "__Departement_Enseignement__": "Génie Civil",
    "__Prenom_NOM__": "Vincent Canizaro",
    "__Adresse_mail_permanente__": "Vincent.Canizaro@example.com",
    "__Statut_etudiant_entrepreneur__": "$\\Box$",
    "__Profil__": "Voie classique",
    "__Double_diplome__": "Université X, Ville Y, Pays Z",
    "__Titre_parcours_3A__": "Master en Transport",
    "__Etablissement_formation_3A__": "Université X, Ville Y, Pays Z",
    "__Promotion__": "2025",
    "__Photo_portrait__": "photo.jpg",  # fichier qui doit exister !
    "__Type_de_PFE__": "Recherche",
    "__Organisme_du_PFE__": "Entreprise ABC",
    "__Type_organisme_accueil__": "Industrie",
    "__Tuteur_professionnel__": "Alice Martin",
    "__Fonction_tuteur_professionnel__": "Ingénieure R\\&D",
    "__Tuteur_academique__": "Prof. Pierre Durand",
    "__Fonction_tuteur_academique__": "Maître de conférences",
    "__Organisme_rattachement_tuteur_academique__": "ENPC",
    "__Langue_de_redaction__": "Français",
    "__Si_PFE_Non_confidentiel__": "Oui – autorisation de diffusion donnée.",
    "__Si_PFE_Confidentiel__": "$\\Box$",
    "__Duree_de_confidentialite__": "0 mois",
    "__Titre_PFE_FR__": "Optimisation des flux de trafic urbain",
    "__Thematique_principale__": "Transport",
    "__Mots_cles_FR__": "trafic;optimisation;transport",
    "__Presentation_contexte_FR__": "Contexte...",
    "__Presentation_missions_FR__": "Missions...",
    "__Resume_FR__": "Résumé...",
    "__Titre_PFE_EN__": "Optimization of Urban Traffic Flows",
    "__Mots_cles_EN__": "traffic;optimization;transport",
    "__Presentation_contexte_EN__": "Context...",
    "__Presentation_missions_EN__": "Objectives...",
    "__Resume_EN__": "Abstract...",
    "__Bibliographie1__": "Réf.1",
    "__Bibliographie2__":"Réf.2",
    "__Bibliographie3__":"Réf.3",
    "__Nom_Image_associee__": "image.jpg",
    "__Legende__": "Legende de l'image",
    "__Nom_Du_Photographe__": "Meow",
    "__CHECK_1__": "$\\CheckedBox$",
    "__CHECK_2__": "$\\Box$",
    "__CHECK_3__": "$\\Box$"
}

contexte = "13 caractères" * 16  # 208 caractères
objectifs = "13 caractères" * 20  # 260 caractères
resume =  "13 caractères" * 100  # 1300 caractères

contexte_en = "13 caractères" * 16  # 208 caractères
objectifs_en = "13 caractères" * 20  # 260 caractères
resume_en =  "13 caractères" * 100  # 1300 caractères

def render_pdf(variables: dict, out_basename="rapport"):
    tex = latex
    for placeholder, value in variables.items():
        tex = tex.replace(placeholder, value)

    tex_path = f"{out_basename}.tex"
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(tex)

    subprocess.run(["pdflatex", "-interaction=nonstopmode", tex_path], check=False)
    subprocess.run(["pdflatex", "-interaction=nonstopmode", tex_path], check=False)
    return f"{out_basename}.pdf"

if __name__=='__main__':
    variables = {
        "__Departement_Enseignement__": "Génie Civil",
        "__Prenom_NOM__": "Vincent CANNIBALO",
        "__Adresse_mail_permanente__": "Vincent.Cannizzaro@example.com",
        "__Statut_etudiant_entrepreneur__": "$\\Box$",
        "__Profil__": "Voie classique",
        "__Double_diplome__": "Université X, Ville Y, Pays Z",
        "__Titre_parcours_3A__": "Master en Transport",
        "__Etablissement_formation_3A__": "Université X, Ville Y, Pays Z",
        '__Promotion__' : '2023',
        "__Photo_portrait__": "photo.jpg",  # fichier qui doit exister !
        "__Type_de_PFE__": "Recherche",
        "__Organisme_du_PFE__": "Entreprise ABC",
        "__Type_organisme_accueil__": "Industrie",
        '__Tuteur_professionnel__' : 'Marie DURAND',
        "__Fonction_tuteur_professionnel__": "Ingénieure R\\&D",
        '__Tuteur_academique__' : 'Luc MARTIN',
        "__Fonction_tuteur_academique__": "Maître de conférences",
        "__Organisme_rattachement_tuteur_academique__": "ENPC",
        "__Langue_de_redaction__": "Français",
        "__Si_PFE_Non_confidentiel__": "Oui – autorisation de diffusion donnée.",
        "__Si_PFE_Confidentiel__": "$\\Box$",
        "__Duree_de_confidentialite__": "0 mois",
        '__Titre_PFE_FR__' : 'Mon PFE génial',
        "__Thematique_principale__": "Transport",
        '__Mots_cles_FR__' : 'super; pfe; intéressant',
        '__Presentation_contexte_FR__' : contexte,
        '__Presentation_missions_FR__' : objectifs,
        "__Resume_FR__" : resume,
        '__Titre_PFE_EN__' : 'Mon PFE cool',
        '__Mots_cles_EN__' : 'super; pfe; intéressant;génial',
        '__Presentation_contexte_EN__' : contexte_en,
        '__Presentation_missions_EN__' : objectifs_en,
        "__Resume_EN__" : resume_en,
        "__Bibliographie1__": "Réf.1",
        "__Bibliographie2__":"Réf.2",
        "__Bibliographie3__":"Réf.3",
        "__Nom_Image_associee__": "image.jpg",
        "__Legende__": "Legende de l'image",
        "__Nom_Du_Photographe__": "Meow",
        "__CHECK_1__": "$\\CheckedBox$",
        "__CHECK_2__": "$\\CheckedBox$",
        "__CHECK_3__": "$\\CheckedBox$"
    }
    render_pdf(variables)
## ==============================
## 3) INSERTION DES VALEURS
## ==============================
#tex = latex
#for placeholder, value in variables.items():
#    tex = tex.replace(placeholder, value)
#
## ==============================
## 4) ÉCRITURE
## ==============================
#with open("rapport.tex", "w", encoding="utf-8") as f:
#    f.write(tex)
#
#print("✔ Fichier rapport.tex généré")
#
## ==============================
## 5) COMPILATION PDF
## ==============================
#subprocess.run(["pdflatex", "-interaction=nonstopmode", "rapport.tex"])
#subprocess.run(["pdflatex", "-interaction=nonstopmode", "rapport.tex"])
print("✔ PDF généré : rapport.pdf")
