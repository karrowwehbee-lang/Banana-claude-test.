# Site KAÏRA Interior Design — mise en ligne sur votre domaine

Ce dossier est le site complet et autonome (aucun service externe nécessaire) :

| Élément | Rôle |
|---|---|
| `index.html` | le site (toutes les pages) |
| `img/` | vos rendus |
| `fonts/`, `vendor/` | polices et bibliothèques d'animation |
| `favicon.png`, `apple-touch-icon.png`, `og-image.jpg` | icônes et image d'aperçu des liens partagés |
| `robots.txt`, `404.html`, `.htaccess`, `_headers` | référencement, adresses inconnues, cache et compression |

Il fonctionne sur n'importe quel hébergement de site statique : aucun serveur ni base de données nécessaire.
Les fichiers `.htaccess` et `_headers` commencent par un point ou un tiret bas : gardez-les, ils accélèrent le site.

## 1. Vos coordonnées (5 minutes)
Ouvrez `index.html` avec un éditeur de texte (Bloc-notes, TextEdit en mode texte brut). Tout en haut du fichier,
cherchez le bloc **KAÏRA — SETTINGS** et la ligne :

    const CONFIG = { email: "", phone: "", city: "", formEndpoint: "", founderPortrait: "" };

Remplissez ce que vous voulez afficher, entre les guillemets, par exemple :

    const CONFIG = { email: "contact@votre-domaine.com", phone: "+…", city: "…", formEndpoint: "", founderPortrait: "" };

Un champ laissé vide n'apparaît pas sur le site.

- **Votre portrait (optionnel)** : déposez une photo dans `img/` (par exemple `karen.jpg`, format portrait) et écrivez
  `founderPortrait: "karen.jpg"`. Elle apparaît dans l'arche de la séquence « Karen Wehbe ».
- **Formulaire de contact (optionnel)** : créez un formulaire gratuit sur https://formspree.io, copiez son adresse
  (`https://formspree.io/f/xxxxxxx`) dans `formEndpoint`. Les messages arrivent alors dans votre boîte e-mail.
  Sans formulaire, le site indique que le formulaire n'est pas encore relié et renvoie vers Instagram.

Vous pouvez aussi simplement m'envoyer ces informations : je les intègre et je vous renvoie le dossier prêt.

## 2. Mettre le site en ligne — choisissez UNE option

### Option A — Netlify (le plus simple, gratuit pour un site comme celui-ci)
1. Créez un compte sur https://app.netlify.com (avec votre e-mail).
2. Ouvrez https://app.netlify.com/drop et **glissez ce dossier entier** dans la page.
   Le site est en ligne en quelques secondes à une adresse provisoire (`…netlify.app`) : vérifiez-le.
3. *Domain management › Add a domain* : tapez votre nom de domaine. Netlify affiche les enregistrements DNS à créer.
4. Chez le fournisseur de votre nom de domaine (OVH, GoDaddy, Namecheap…), dans la zone DNS, créez ces
   enregistrements exactement comme indiqué par Netlify. La propagation prend de quelques minutes à 24 h.
5. Netlify active le HTTPS (cadenas) automatiquement.
Pour une mise à jour plus tard : *Deploys › glisser le nouveau dossier*.

### Option B — votre propre hébergeur (OVH, Hostinger, o2switch…)
1. Ouvrez le gestionnaire de fichiers de votre hébergement (ou un logiciel FTP comme FileZilla).
2. Envoyez **le contenu** de ce dossier (pas le dossier lui-même) dans le répertoire public du site,
   souvent `www` ou `public_html`. Vérifiez que `.htaccess` est bien envoyé (affichez les fichiers cachés).
3. Activez le certificat SSL gratuit (Let's Encrypt) dans le panneau de l'hébergeur.

## 3. Après la mise en ligne
- Ouvrez votre domaine sur ordinateur et sur téléphone, et parcourez les pages.
- **Envoyez-moi l'adresse définitive** : j'ajoute l'adresse officielle dans le site (aperçu des liens sur WhatsApp,
  Facebook et LinkedIn, plan du site pour Google) et je vous renvoie la version finale à déposer de la même façon.
- Ajoutez le lien dans votre bio Instagram (voir le kit de lancement Instagram).
- Optionnel : déclarez le site dans Google Search Console (https://search.google.com/search-console) pour qu'il
  apparaisse plus vite dans Google.

## À savoir
- Adresses des pages : `votre-domaine.com/#projects`, `#project-villa`, `#project-residential`, `#project-workspaces`,
  `#project-rooftop`, `#project-retail`, `#project-kids`, `#studio`, `#services`, `#contact`.
- Vos rendus ne sont ni recadrés ni retouchés. Les rendus JPEG sont vos fichiers originaux, à l'octet près ; les rendus
  PNG (villa, chambres d'enfants, 2 à 5 Mo chacun) sont enregistrés une fois en JPEG haute qualité (q90, pleine
  résolution des couleurs, mêmes dimensions). Le cadrage plein écran et les mouvements se font uniquement à l'affichage ;
  la visionneuse des pages projets montre chaque rendu en entier.
- Les visiteurs qui ont réduit les animations dans les réglages de leur appareil voient une version calme du site.
