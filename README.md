# PDF Booklet

Interface Windows de sélection de PDF, génération de livrets et impression avec SumatraPDF. Lancer `print-medium-pdf.cmd`.

Le programme exclut les fichiers `-book.pdf` et les sources dont le livret existe déjà. Le choix du format adapte le PDF et le papier d'impression : livret A4 sur feuilles A3 (par défaut), ou livret A5 sur feuilles A4. L'impression reste en couleur, recto verso sur le bord court.

## Installation

Python 3 avec Tkinter est nécessaire. `requirements.txt` ne déclare aucun paquet tiers : le code utilise uniquement la bibliothèque standard.

```powershell
# Create the local Python environment.
python -m venv .venv
# Create the private configuration from the example.
Copy-Item print-medium-pdf.properties.sample print-medium-pdf.properties
```

Renseigner `pdf.directory`, `printer.name` et éventuellement `sumatra.path` dans le fichier local. Les antislashs sont conservés tels quels. Les chemins relatifs partent du dossier du projet. La configuration réelle, les PDF et les environnements locaux sont exclus de Git.

Les outils externes ne sont pas inclus dans le dépôt :

- SumatraPDF, au chemin indiqué dans la configuration ;
- Git for Windows, installé dans `C:\Program Files\Git` pour son shell ;
- MiKTeX avec `pdflatex`, `kpsewhich`, `pdfpages` et leurs dépendances, dans `.tools\miktex-private\install\miktex\bin\x64` ;
- le script shell pdfjam, par défaut dans `%APPDATA%\MiKTeX\2.9\scripts\pdfjam\pdfjam`. La variable d'environnement `PDFJAM_SCRIPT` permet de choisir un autre emplacement.

Les quatre relais de `.tools\bin` sont versionnés. L'installation MiKTeX et `.venv` doivent être préparées sur chaque poste. Aucun installateur ni téléchargement automatique n'est fourni.

## Fonctionnement

`print-medium-pdf.cmd` lance `print-medium-pdf.py`, qui appelle `create-booklet.bat`, puis `pdfbook2\pdfbook2` via les relais Windows. SumatraPDF envoie ensuite le livret à l'imprimante configurée.

Le PDF généré est placé à côté de la source. La génération utilise des fichiers temporaires dans le dossier du projet : éviter les exécutions simultanées. Le batch utilise systématiquement `--no-crop` ; les relais de recadrage ne sont pas nécessaires à ce parcours.

## Licence

GPLv3, voir `LICENSE`. Le moteur est adapté de [pdfbook2 v1.4](https://github.com/jenom/pdfbook2), copyright 2015–2020 Johannes Neumann, basé sur pdfbook de David Firth avec l'aide de Marco Pessotto.
