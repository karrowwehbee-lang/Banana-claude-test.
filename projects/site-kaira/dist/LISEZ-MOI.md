# Site KAÏRA Interior Design — mise en ligne sur votre domaine

Ce dossier est le site complet : `index.html`, `img/`, `favicon.png`, `og-image.jpg`.
Il fonctionne sur n'importe quel hébergement de site statique (aucun serveur ni base de données nécessaire).

## 1. Compléter vos coordonnées (5 minutes)
Ouvrez `index.html` avec un éditeur de texte, cherchez la ligne :

    const CONFIG = { email: "", phone: "", city: "", formEndpoint: "" };

et remplissez ce que vous voulez afficher, par exemple :

    const CONFIG = { email: "contact@votre-domaine.com", phone: "+225 …", city: "Abidjan", formEndpoint: "" };

Un champ laissé vide n'apparaît pas sur le site.

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
- Les images sont des versions web compressées de vos rendus (sans recadrage ni retouche) ; vos fichiers originaux
  ne sont pas modifiés.
- Les bibliothèques (React, GSAP, Lenis) et les polices (Google Fonts) sont chargées depuis leurs CDN officiels.
