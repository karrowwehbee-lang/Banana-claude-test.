# KAÏRA Interior Design website — publishing on your own domain

This folder is the complete, self-contained website (no outside service needed): `index.html` (all pages), `img/`
(your renders), `fonts/` and `vendor/` (fonts and animation libraries), icons, `og-image.jpg` (link preview),
`robots.txt`, `404.html`, `.htaccess` and `_headers` (search engines, unknown addresses, caching and compression).
Keep the files that start with a dot or an underscore: they make the site faster.

## 1. Your details (5 minutes)
Open `index.html` in a plain-text editor. At the very top, find the **KAÏRA — SETTINGS** block and this line:

    const CONFIG = { email: "", phone: "", city: "", formEndpoint: "", founderPortrait: "" };

Fill in what you want to show between the quotes. An empty field is not shown.
- Portrait (optional): put a photo in `img/` (e.g. `karen.jpg`) and write `founderPortrait: "karen.jpg"`.
- Contact form (optional): create a free form at https://formspree.io and paste its address in `formEndpoint`;
  messages then arrive in your inbox.
You can also send me these details and I will return the folder ready to upload.

## 2. Put it online — choose ONE option
**A. Netlify (simplest, free for a site like this)**
1. Create an account at https://app.netlify.com.
2. Open https://app.netlify.com/drop and drag this whole folder onto the page. The site goes live at a temporary
   `…netlify.app` address: check it.
3. *Domain management › Add a domain*: type your domain. Netlify lists the DNS records to create.
4. At your domain registrar (OVH, GoDaddy, Namecheap…), create those DNS records exactly as shown.
   It takes from a few minutes to 24 hours. Netlify turns on HTTPS automatically.

**B. Your own web host (OVH, Hostinger, o2switch…)**
Upload the *contents* of this folder to the public directory (`www` or `public_html`) with the host's file manager
or an FTP app such as FileZilla (show hidden files so `.htaccess` is uploaded), then turn on the free SSL certificate.

## 3. After launch
Open the site on a computer and a phone. Send me the final address: I will add it to the site (link previews on
WhatsApp, Facebook and LinkedIn, and a sitemap for Google) and send you the final version to upload the same way.
Then add the link to your Instagram bio (see the Instagram launch kit).
