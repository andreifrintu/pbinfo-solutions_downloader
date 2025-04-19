### Descarcă sursele oficiale PBinfo - Aplicație pentru 💎 Academia CLA

*Tutorial video de descărcare a surselor necesare CLA folosind aplicația*

https://github.com/user-attachments/assets/9dc9aa38-a8af-41f4-8cc9-a06adab38491

Aplicația, scrisă în Python, folosește un `User Agent` custom și valoarea cookie-ului `SSID` din site-ul PBinfo.ro. Pe baza acestor date, trimite request-uri către toate cele 5000 de probleme (număr ce poate fi modificat), și verifica accesul utilizatorului la sursa oficială (disponibilă dacă a fost obținut anterior cel puțin o dată punctajul maxim, pentru acea problemă).

Dacă accesul este permis, parcurgând textul și elementele paginii se va selecta sursa C++ aflată într-un bloc `<code>` și descărca într-un fișier și folder separat, respectând sintaxa `pbinfo-${id_problema}/main.cpp`.

### Coming Updates:

- Număr modificabil de probleme care vor fi descărcate (range, counter) ✅
- Sintaxa diferită a directoarelor și fișierelor create de program
- Commit & Push într-un repository de GitHub
- Generarea de fișier log pentru probleme și soluții ✅
- Verificarea valabilității pe site înainte de descărcare ✅

### Instrucțiuni de utilizare

După ce te-ai conectat în contul tău de PBinfo vei apăsa tasta `F12`, pentru a deschide meniul de dezvoltatori din browser-ul web. Apoi, în tab-ul `Application`, la secțiunea `Cookies`, se va copia valoarea cookie-ului cu numele `SSID`, aparținând de domeniul `www.pbinfo.ro`, la calea root `/`. Formatul acestui token este un string alfanumeric de 26 de caractere.

Această valoare va fi cerută de program la `fiecare executare`, după care, vor începe să se descarce sursele dacă codul este corect, în caz contrar acesta nu va avea activitate. Programul poate fi suspendat dacă trec mai mult de 50 de secunde fără a fi descarcată vreo rezolvare!
