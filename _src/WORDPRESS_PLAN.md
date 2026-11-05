# GP ENERGIA - plan wdrożenia na WordPress (dhosting, gpenergia.com.pl)

Podgląd do odbioru: https://disaster26.github.io/gpenergia-koncepcja/ (statyczny, noindex). Umowa wymaga WordPressa z blogiem, który klient sam prowadzi. Plan zakłada przeniesienie 1:1 wyglądu i treści z podglądu.

## 1. Hosting i domena
- dpanel.pl (dhosting): nowa instalacja WordPress (PHP 8.2+, MySQL/MariaDB), SSL Let's Encrypt.
- Domena gpenergia.com.pl: zmieniamy tylko rekordy A/AAAA (i www CNAME) na serwer dhosting. Rekordy MX (mx-1/mx-2.dpoczta.pl), SPF i DKIM zostają bez zmian, żeby poczta info@ działała dalej. Przed zmianą zrzut całej strefy DNS.
- Najpierw instalacja na subdomenie testowej (np. nowa.gpenergia.com.pl, noindex), po akceptacji przepięcie domeny.

## 2. Motyw
- Lekki własny motyw potomny (np. na bazie GeneratePress albo motyw blokowy bez page buildera), bez Elementora.
- `assets/site.css`, `assets/site.js`, fonty z `assets/fonts/` (self-hosted, woff2) i obrazy z `img/` kopiujemy do motywu bez zmian. Klasy CSS są te same co w podglądzie, więc szablony PHP generują identyczny HTML.
- Nagłówek, stopka (z dolną linią "wykonanie: Wylinka"), pasek dolny na telefonie i okruszki jako części szablonu (`header.php`, `footer.php`, `template-parts/`).

## 3. Strony statyczne
- Strony WP z własnymi szablonami (`page-home.php`, `page-services.php`, `page-service.php`, `page-products.php`, `page-brands.php`, `page-references.php`, `page-about.php`, `page-contact.php`, `page-privacy.php`).
- Treść każdej strony pochodzi z `_src/content.py` i `_src/build.py` (jedno źródło tekstów EN/PL). Długie teksty wklejamy do edytora bloków, dane tabelaryczne (kategorie, marki, przykładowy BOM, realizacje, historia) jako pola ACF albo stałe tablice w motywie - klient rzadko je zmienia.
- Adresy jak w podglądzie: `/`, `/services/`, `/services/bom-sourcing/`, ... oraz `/pl/`, `/pl/uslugi/`, ... (lista w `content.py` -> `PATHS`).

## 4. Wersje językowe
- Polylang (darmowy): EN jako język domyślny bez prefiksu, PL z prefiksem `/pl/`. Każda strona i wpis ma powiązane tłumaczenie, Polylang wstawia hreflang en/pl, a x-default ustawiamy na EN.
- Slugi PL ręcznie jak w podglądzie (`o-firmie`, `uslugi`, `realizacje`, `kontakt`, `polityka-prywatnosci`, `marki`, `produkty`).
- Alternatywa bez wtyczki: drzewo stron `/pl/...` + własny filtr hreflang. Polylang wybieramy, bo klient sam doda tłumaczenie wpisu jednym kliknięciem.

## 5. Blog
- Wpisy WP (post), szablon `single.php` = szablon artykułu z podglądu: okruszki, H1, data i czas czytania, lead, spis treści generowany z H2, ramka "Masz listę BOM do wyceny?", sekcja FAQ, źródła, powiązane wpisy.
- FAQ: blok "Pytania i odpowiedzi" (ACF repeater albo blok szczegółów) - motyw buduje z niego sekcję i dane FAQPage.
- Każdy wpis: własny tytuł SEO i opis (The SEO Framework albo Yoast), jeden H1, H2/H3 z edytora.
- 3 artykuły startowe EN+PL z `_src/seo_0511/BLOG/` importujemy jako wpisy (Markdown -> bloki), z powiązaniem tłumaczeń w Polylang.
- Instrukcja PDF dla klienta: jak dodać wpis, tłumaczenie, obrazek, FAQ i opis dla Google.

## 6. SEO i dane strukturalne
- Tytuły, opisy, H1 i slugi z `_src/seo_0511/META.json` (już użyte w podglądzie).
- JSON-LD: Organization + WebSite w `header.php` (jak w podglądzie, logo `https://gpenergia.com.pl/img/logo-gpenergia.svg`), BreadcrumbList, Service, FAQPage i BlogPosting generowane przez motyw. Wtyczkę SEO ustawiamy tak, żeby nie dublowała Organization.
- Mapa strony z hreflang (wtyczka SEO + Polylang), `robots.txt` z `_src/production/robots.txt` (zezwala też botom AI), `llms.txt` w katalogu głównym.
- Zgłoszenie do Google Search Console (domena, weryfikacja DNS TXT) i wysłanie mapy strony.

## 7. Formularz zapytania (RFQ)
- Własny endpoint w motywie (`admin-post.php` albo REST `/wp-json/gpe/v1/rfq`), bez zewnętrznych usług. Formularz w HTML zostaje jak w podglądzie, w `site.js` wystarczy ustawić `data-endpoint` (stała `FORM_ENDPOINT` w build.py).
- Wysyłka przez `wp_mail` na info@gpenergia.com.pl przez SMTP skrzynki dpoczta (wtyczka WP Mail SMTP, hasło tylko w konfiguracji serwera, nigdy w repozytorium), Reply-To = adres klienta.
- Załącznik BOM: tylko xlsx, xls, csv, pdf, max 10 MB, sprawdzanie rozszerzenia i typu MIME, zapis poza katalogiem publicznym albo tylko jako załącznik maila (bez publicznego URL).
- Ochrona przed spamem: honeypot (`website`), znacznik czasu (odrzucenie wysyłki szybszej niż 3 s), limit 5 zapytań na godzinę z jednego IP (transient), nonce WP, walidacja po stronie serwera.
- Test: wysyłka testowa z załącznikiem i potwierdzenie odbioru na info@ (wymóg umowy § 2 ust. 3).

## 8. Wydajność i bezpieczeństwo
- Obrazy AVIF/WebP z srcset (gotowe w `img/p/`), lazy loading poniżej pierwszego ekranu, fonty preload, bez jQuery na froncie.
- Cache stron (LiteSpeed Cache albo WP Super Cache na dhostingu), nagłówki cache dla `assets/` i `img/`.
- Aktualizacje automatyczne rdzenia, minimum wtyczek (Polylang, SEO, WP Mail SMTP, ewentualnie ACF), wyłączony XML-RPC, ograniczenie prób logowania, konto administratora klienta + osobne konto wykonawcy.
- Kopia zapasowa dhosting + eksport przed każdą większą zmianą.

## 9. Kolejność
1. Instalacja WP na subdomenie testowej, motyw, Polylang.
2. Strony EN + PL, blog z 3 artykułami, formularz z testem wysyłki.
3. Sprawdzenie na telefonie/tablecie/komputerze (360-2560 px), Lighthouse, hreflang, dane strukturalne.
4. Przepięcie domeny (tylko A/www), SSL, Search Console, mapa strony.
5. Instrukcja PDF dla klienta.
