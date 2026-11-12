# Site KAÏRA Interior Design — mise en ligne sur votre domaine

Ce dossier est le site complet : `index.html`, `img/` (vos rendus), `fonts/` (polices), `vendor/` (bibliothèques
d'animation), `favicon.png`, `og-image.jpg`. Il est autonome : il ne dépend d'aucun service externe et fonctionne sur
n'importe quel hébergement de site statique (aucun serveur ni base de données nécessaire).

## 1. Compléter vos coordonnées (5 minutes)
Ouvrez `index.html` avec un éditeur de texte, cherchez la ligne :

    const CONFIG = { email: "", phone: "", city: "", formEndpoint: "", founderPortrait: "" };

et remplissez ce que vous voulez afficher, par exemple :

    const CONFIG = { email: "contact@votre-domaine.com", phone: "+…", city: "…", formEndpoint: "", founderPortrait: "" };

Un champ laissé vide n'apparaît pas sur le site.

**Votre portrait (optionnel)** : déposez une photo dans `img/` (par exemple `karen.jpg`, format portrait) et écrivez
`founderPortrait: "karen.jpg"`. Elle apparaîtra dans l'arche de la séquence « Karen Wehbe ». Sans photo, l'arche montre
un de vos rendus.

## 2. Activer le formulaire de contact (optionnel)
Sans service de formulaire, le site affiche « The form is not connected yet » et renvoie vers Instagram.
Pour recevoir les messages par e-mail : créez un formulaire gratuit sur https://formspree.io, copiez son adresse
(`https://formspree.io/f/xxxxxxx`) dans `formEndpoint`. Les messages arrivent alors dans votre boîte e-mail.

## 3. Mettre le site en ligne
**Le plus simple — Netlify** : ouvrez https://app.netlify.com/drop et glissez ce dossier entier. Le site est en ligne
en quelques secondes à une adresse provisoire. Puis *Domain management › Add a domain* : Netlify vous indique les
enregistrements DNS à créer chez le fournisseur de votre nom de domaine.

**Votre propre hébergeur** (OVH, Hostinger, o2switch…) : envoyez le contenu de ce dossier dans le répertoire
public du site (souvent `www` ou `public_html`) par le gestionnaire de fichiers ou en FTP.

Pensez à activer le HTTPS (gratuit chez la plupart des hébergeurs).

## À savoir
- Les pages ont des adresses du type `votre-domaine.com/#projects`, `#project-villa`, `#studio`, `#services`, `#contact`.
- Vos rendus ne sont ni recadrés ni retouchés. Les rendus JPEG sont les fichiers originaux, à l'octet près ; les rendus
  PNG (villa, chambres d'enfants, 2 à 5 Mo chacun) sont enregistrés une fois en JPEG haute qualité (q90, pleine
  résolution des couleurs, mêmes dimensions). Le cadrage plein écran et les mouvements se font uniquement à l'affichage.
- Les visiteurs qui ont réduit les animations dans leur système voient une version calme du site, sans défilement animé.
