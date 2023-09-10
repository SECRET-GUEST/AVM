![Windows](https://img.shields.io/badge/OS-Windows-blue)
![Disk Space](https://img.shields.io/badge/Disk%20Space-40GB-brightgreen)

```
 █████╗ ██╗   ██╗███╗   ███╗
██╔══██╗██║   ██║████╗ ████║
███████║██║   ██║██╔████╔██║
██╔══██║╚██╗ ██╔╝██║╚██╔╝██║
██║  ██║ ╚████╔╝ ██║ ╚═╝ ██║
╚═╝  ╚═╝  ╚═══╝  ╚═╝     ╚═╝
```
![Conda](https://img.shields.io/badge/conda-python%203.10.12-green)


# AVM - Auto Video Maker

AVM (Auto Video Maker) est un logiciel innovant, en cours de developpement, fonctionnant sous Windows , exploitant la technologie de l'IA ( Voice Cloning ) et une base de données d'images Google pour générer automatiquement du contenu multimédia, automatisant ainsi le processus de génération de vidéos.

Le projet, en cours de développement et actuellement en phase pré-alpha, est sous licence GPL-3.0. Il utilise l'invite de commande comme interface utilisateur. Le logiciel AVM (Auto Video Maker) a pour principal objectif de faciliter la création de contenu multimédia. 

AVM génère des voix à partir des textes contenus dans le fichier `scene.json`, et assemble les vidéos de manière autonome, nécessitant une intervention minimale de l'utilisateur. Cette innovation vise à révolutionner la manière dont les "vidéos" sont créées, en rendant le processus plus rapide et plus efficace.

## 🔧 Installation et Configuration

**Installation du Projet** : Cliquez sur `LANCEUR.bat` pour installer le projet. Cela configurera également l'environnement virtuel et installera les dépendances nécessaires via `lib.py`.

**Mise à jour des Dépendances** : Pour mettre à jour les dépendances après l'installation, cliquez simplement à nouveau sur `LANCEUR.bat`.

## 📂 Structure du Projet

- **assets** : Contient toutes les images nécessaires pour le projet.
- **src** : Contient les scripts, y compris un traducteur automatique pour les mots générés dans l'invite de commande.
- **utils** : Contient des utilitaires, comme un exemple de scène et des requirements alternatifs pour des versions plus stables de certains modules.
- **storyboard** : Le dossier principal où le script s'exécute, contenant un sous-dossier "0ld" pour les anciens projets et un dossier utilisateur pour les scènes.json.

## 💼 Utilisation

Pour utiliser l'AVM, suivez les étapes ci-dessous :

1. **Préparation des Assets** : Préparez manuellement les animations de personnages et les templates de scène. (en cours de developpement)
2. **Génération de Scène** : Utilisez le script pour générer une scène à partir des assets préparés.
3. **Lancement du Logiciel** : Pour lancer le logiciel, cliquez soit sur le raccourci créé sur le bureau après l'installation, soit sur `shortcut.bat` ( vous pouvez faire un raccourcis au besoin, mais ne déplacez pas le fichier ).


<!--
## 🤝 Contribution

Le projet est actuellement en phase de développement pré-alpha. Nous accueillons volontiers les contributions pour améliorer le projet. N'hésitez pas à ouvrir des issues ou à soumettre des pull requests.
-->

## 📚 Ressources Externes

| Ressource                       | Lien                                                         |
|---------------------------------|--------------------------------------------------------------|
| Tortoise (Voice Cloning)        | [GitHub](https://github.com/neonbjb/tortoise-tts)            |
| RVC (Voice Cloning)             | [GitHub](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI) |
| tts generation webui (Voice Cloning) | [GitHub](https://github.com/rsxdalv/tts-generation-webui)   |
| Base de données d'images Google | [Site Web](https://storage.googleapis.com/openimages/web/download_v7.html) |

<!--
## 🙏 Remerciements

Merci de soutenir et de contribuer à ce projet en développement.
-->

## 📜 Licence

Ce projet est distribué sous la licence GPL-3.0. Voir le fichier [**LICENSE**](https://github.com/SECRET-GUEST/AVM/blob/main/LICENSE) pour plus de détails.
