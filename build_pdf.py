import subprocess
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# --- (optionnel) filtre pour échapper LaTeX ---
LATEX_SUBS = {
    '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_',
    '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}',
    '^': r'\^{}', '\\': r'\textbackslash{}',
}
def texescape(s):
    if s is None:
        return ''
    return ''.join(LATEX_SUBS.get(ch, ch) for ch in str(s))

# --- config Jinja2 avec délimiteurs compatibles LaTeX ---
env = Environment(
    loader=FileSystemLoader("."),
    block_start_string=r'\BLOCK{',
    block_end_string='}',
    variable_start_string=r'\VAR{',
    variable_end_string='}',
    comment_start_string=r'\#',
    comment_end_string='}',
    autoescape=False,
)
env.filters['tex'] = texescape

# --- données à injecter ---
context = {
    "titre": "Rapport automatisé",
    "auteur": "Votre Nom",
    "date": "10 novembre 2025",
    "resume": "Ce rapport a été généré automatiquement depuis Python et LaTeX.",
    "points": [
        "Pipeline reproductible (Jinja2 + latexmk)",
        "Gestion des caractères spéciaux",
        "Tables et images dynamiques",
    ],
    "tableau": [
        {"nom": "Alpha", "cat": "A", "valeur": 12},
        {"nom": "Beta",  "cat": "B", "valeur": 7},
        {"nom": "Gamma", "cat": "A", "valeur": 19},
    ],
    "image_path": "figures/exemple.png",
}

# --- rendu vers un .tex ---
template = env.get_template("template.tex")
build_dir = Path("build")
build_dir.mkdir(exist_ok=True)
tex_path = build_dir / "rapport.tex"
tex_path.write_text(template.render(**context), encoding="utf-8")

# --- compilation PDF avec latexmk ---
# Vous pouvez passer à -xelatex en remplaçant -pdf par -xelatex
cmd = [
    "latexmk", "-pdf",
    "-interaction=nonstopmode", "-halt-on-error",
    f"-outdir={build_dir}",
    str(tex_path)
]
proc = subprocess.run(cmd, capture_output=True, text=True)

if proc.returncode != 0:
    print("LaTeX a échoué. Log (stderr):")
    print(proc.stderr)
    # Afficher le log principal
    log_path = build_dir / "rapport.log"
    if log_path.exists():
        print("\n--- Extrait du log ---")
        print(log_path.read_text(encoding="utf-8")[-3000:])
    raise SystemExit(1)
print("sdkljsadlk", build_dir)
print(f"PDF généré : {build_dir / 'rapport.pdf'}")
