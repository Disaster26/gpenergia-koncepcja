# -*- coding: utf-8 -*-
"""All page copy for gpenergia.com.pl (EN main, PL mirror).
Facts come from: client's history docx (od_klienta_2810), sister-company texts and
references (client consent 30.10.2026), KRS. Nothing invented.
Only "-" as a dash. Keep this file the single source of copy for the WordPress port."""

EMAIL = "info@gpenergia.com.pl"

COMPANY = {
    "legal": "GP ENERGIA sp. z o.o.",
    "krs": "0000344186",
    "nip": "966-201-77-48",
    "nip_raw": "9662017748",
    "regon": "200320804",
    "capital_en": "PLN 2,029,000.00",
    "capital_pl": "2 029 000,00 zł",
    "street": "ul. Polna 29",
    "postcode": "55-095",
    "city": "Długołęka",
    "lat": 51.17991,
    "lon": 17.21027,
}

# ---------------------------------------------------------------- categories
CATEGORIES = [
    {
        "id": "cabinets", "img": "cabinet",
        "en": {"t": "Switchboards, cabinets and enclosures",
               "d": "Enclosures and cabinets that organise and protect wiring, circuits and automation components on production lines, in warehouses, server rooms and buildings.",
               "s": ["Control enclosures", "Terminal boxes", "Distribution boards", "Control cabinets", "Server cabinets", "Meter panels for PV", "Cabinet accessories"],
               "alt": "Open control cabinet with modular devices and wiring"},
        "pl": {"t": "Rozdzielnice, szafy i obudowy",
               "d": "Obudowy i szafy, które porządkują i chronią przewody, obwody i elementy automatyki na liniach produkcyjnych, w magazynach, serwerowniach i budynkach.",
               "s": ["Obudowy sterownicze", "Skrzynki zaciskowe", "Rozdzielnice instalacyjne", "Szafy sterownicze", "Szafy serwerowe", "Panele licznikowe do fotowoltaiki", "Wyposażenie szaf"],
               "alt": "Otwarta szafa sterownicza z aparaturą modułową i okablowaniem"},
    },
    {
        "id": "low-voltage", "img": "breakers",
        "en": {"t": "Low-voltage equipment and automation",
               "d": "Control, protection and power for machinery, from modular devices and contactors to PLCs, HMI panels and drives.",
               "s": ["Modular devices", "PLCs", "HMI panels", "Contactors", "Circuit breakers and switch-disconnectors", "Motor starters", "Drives and servo drives", "Frequency inverters", "UPS", "Encoders and measurement", "Capacitors"],
               "alt": "Miniature circuit breakers"},
        "pl": {"t": "Aparatura elektryczna i automatyka",
               "d": "Sterowanie, zabezpieczenia i zasilanie maszyn: od aparatury modułowej i styczników po sterowniki PLC, panele HMI i napędy.",
               "s": ["Aparatura modułowa", "Sterowniki PLC", "Panele HMI", "Styczniki", "Wyłączniki i rozłączniki", "Urządzenia rozruchowe", "Napędy i serwonapędy", "Falowniki", "Zasilanie awaryjne UPS", "Enkodery i pomiar", "Kondensatory"],
               "alt": "Wyłączniki nadprądowe"},
    },
    {
        "id": "installation", "img": "gauges",
        "en": {"t": "Electrical installation equipment",
               "d": "Parts for connecting and protecting cables, plus metering and control in buildings and industrial halls.",
               "s": ["Meters and gauges", "Switches and push buttons", "Sockets", "Telecom equipment", "Bus systems", "Dimmers and sensors"],
               "alt": "Pressure gauges"},
        "pl": {"t": "Osprzęt elektroinstalacyjny",
               "d": "Elementy do łączenia i ochrony przewodów oraz do pomiaru i sterowania w budynkach i halach.",
               "s": ["Liczniki i mierniki", "Łączniki i przyciski", "Gniazda", "Technika telekomunikacyjna", "Systemy magistralne", "Ściemniacze i czujniki"],
               "alt": "Manometry"},
    },
    {
        "id": "fire-protection", "img": "sprinklers",
        "en": {"t": "Fire protection systems",
               "d": "Detection and alarm systems for offices, retail sites, warehouses and plants, where business continuity and people's safety come first.",
               "s": ["Fire alarm control panels", "Flame detectors", "Gas detectors", "Voice alarm systems", "Sounders and beacons", "Fire-rated power supplies", "Monitoring and control modules"],
               "alt": "Sprinkler heads on a red pipe"},
        "pl": {"t": "Systemy przeciwpożarowe i ogniochronne",
               "d": "Wykrywanie i sygnalizacja zagrożeń w biurach, obiektach handlowych, magazynach i zakładach, gdzie liczy się ciągłość pracy i bezpieczeństwo ludzi.",
               "s": ["Centrale sygnalizacji pożaru", "Detektory ognia", "Detektory gazów", "Dźwiękowe systemy ostrzegawcze", "Sygnalizatory", "Zasilacze ppoż.", "Moduły kontrolno-sterujące"],
               "alt": "Tryskacze na czerwonym rurociągu"},
    },
    {
        "id": "lighting", "img": "lamps",
        "en": {"t": "Lighting",
               "d": "Energy-efficient luminaires, light sources and lighting control for indoor, outdoor and industrial use.",
               "s": ["Lighting accessories", "Lighting control", "Indoor lighting", "Outdoor luminaires and poles", "Mounting accessories"],
               "alt": "Red, amber and green signal lamps"},
        "pl": {"t": "Oświetlenie",
               "d": "Energooszczędne oprawy, źródła światła i sterowanie oświetleniem do wnętrz, na zewnątrz i do obiektów przemysłowych.",
               "s": ["Osprzęt oświetleniowy", "Sterowanie oświetleniem", "Oświetlenie wewnętrzne", "Oprawy i słupy zewnętrzne", "Akcesoria montażowe"],
               "alt": "Czerwona, żółta i zielona lampka sygnalizacyjna"},
    },
    {
        "id": "accessories", "img": "marking",
        "en": {"t": "Accessories",
               "d": "What speeds up wiring and commissioning: connection technology, wire marking, ferrules and terminals.",
               "s": ["Wire marking printers and markers", "Cable lugs and ferrules", "DIN rail terminal blocks", "Connection technology", "Installation connectors", "Contact inserts"],
               "alt": "Wire marking printer with marker strips (Phoenix Contact)"},
        "pl": {"t": "Akcesoria",
               "d": "To, co skraca oprzewodowanie i uruchomienie: technika łączenia, oznaczanie przewodów, końcówki i zaciski.",
               "s": ["Drukarki i oznaczniki przewodów", "Końcówki kablowe", "Zaciski na szynę DIN", "Technika łączenia", "Złączki instalacyjne", "Wkładki stykowe"],
               "alt": "Drukarka oznaczników przewodów z paskami oznaczników (Phoenix Contact)"},
    },
]

# Brands list supplied with client materials (46) - logos where we have files
BRANDS = ["ABB", "Allen-Bradley", "AVE", "BAKS", "Balluff", "Beckhoff", "Bosch", "Cabur", "Degson", "DEHN", "Doepke", "Eaton",
          "Elektromontaż Rzeszów", "Emerson", "Endress+Hauser", "Ensto", "Fanuc", "Finder", "Frako", "Gewiss", "Gira", "Hirschmann",
          "Honeywell", "Jean Müller", "Jumo", "Katko", "Leds C4", "Legrand", "Mersen", "Moxa", "nVent Hoffman", "OBO Bettermann",
          "Omron", "Panasonic", "PCE", "Phoenix Contact", "R. Stahl", "Rittal", "Rosa", "Schneider Electric", "SEW Eurodrive",
          "Siemens", "Spelsberg", "TE Connectivity", "WAGO", "Weidmüller", "Wieland"]
BRANDS_EXTRA = ["Pilz", "IFM", "SICK", "Pepperl+Fuchs", "Murrelektronik", "Danfoss", "SMC", "Hensel", "Harting"]
# logo file slug -> display name, in display order
LOGOS = [("siemens", "Siemens"), ("schneider-electric", "Schneider Electric"), ("abb", "ABB"), ("phoenix-contact", "Phoenix Contact"),
         ("rittal", "Rittal"), ("eaton", "Eaton"), ("allen-bradley", "Allen-Bradley"), ("legrand", "Legrand"), ("omron", "Omron"),
         ("wago", "WAGO"), ("weidmuller", "Weidmüller"), ("finder", "Finder"), ("beckhoff", "Beckhoff"), ("balluff", "Balluff"),
         ("endresshauser", "Endress+Hauser"), ("honeywell", "Honeywell"), ("emerson", "Emerson"), ("bosch", "Bosch"),
         ("sew-eurodrive", "SEW Eurodrive"), ("fanuc", "Fanuc"), ("moxa", "Moxa"), ("hirschmann", "Hirschmann"),
         ("obo-bettermann", "OBO Bettermann"), ("spelsberg", "Spelsberg"), ("gewiss", "Gewiss"),
         ("mersen", "Mersen"), ("panasonic", "Panasonic"), ("te-connectivity", "TE Connectivity"), ("wieland", "Wieland")]
STRIP = ["siemens", "schneider-electric", "abb", "phoenix-contact", "rittal", "eaton", "omron", "wago"]

# ---------------------------------------------------------------- sample BOM
BOM = [
    ("PLC", "CPU 1212C, 8DI/6DO, Ethernet", "Sterownik PLC", "CPU 1212C, 8DI/6DO, Ethernet", "Siemens", "6ES7212-1BE40-0XB0", 1),
    ("HMI panel", "PanelView 800, 7 in, touch, Ethernet", "Panel HMI", "PanelView 800, 7 cali, dotykowy, Ethernet", "Allen-Bradley", "2711R-T7T", 1),
    ("Pressure sensor", "0-10 bar, 4-20 mA output", "Czujnik ciśnienia", "0-10 bar, wyjście 4-20 mA", "IFM", "PN7004", 2),
    ("Temperature sensor", "Pt100, 2-wire, up to 200 °C", "Czujnik temperatury", "Pt100, 2-przewodowy, do 200 °C", "Phoenix Contact", "1003290", 2),
    ("Contactor", "3P, 9 A, 230 V AC coil", "Stycznik", "3P, 9 A, cewka 230 V AC", "Schneider Electric", "LC1D09P7", 3),
    ("Power supply", "QUINT 24 V / 10 A, UPS-ready", "Zasilacz", "QUINT 24 V / 10 A, UPS-ready", "Phoenix Contact", "2904617", 1),
]

# ---------------------------------------------------------------- references
CASES = [
    {
        "id": "prefabricator-czech-republic", "img": "cabinet",
        "en": {"t": "Switchboard prefabricator, Czech Republic",
               "client": "Switchboard prefabricator", "where": "Czech Republic", "scope": "PLC and power supply for a prefabrication order",
               "brands": "Siemens, Phoenix Contact",
               "parts": "6ES7212-1BE40-0XB0, 2904617",
               "sit": "The list included a Siemens S7-1200 controller (6ES7212-1BE40-0XB0) and a Phoenix Contact QUINT 24 V / 10 A power supply (2904617). The manufacturers quoted 6 and 8 weeks.",
               "did": "We delivered both items from stock in the EU within 48-72 hours, and prefabrication started on schedule.",
               "res": "48-72 hours instead of 6-8 weeks"},
        "pl": {"t": "Prefabrykator rozdzielnic, Czechy",
               "client": "Prefabrykator rozdzielnic", "where": "Czechy", "scope": "Sterownik PLC i zasilacz do zlecenia prefabrykacji",
               "brands": "Siemens, Phoenix Contact",
               "parts": "6ES7212-1BE40-0XB0, 2904617",
               "sit": "Lista zawierała sterownik Siemens S7-1200 (6ES7212-1BE40-0XB0) i zasilacz Phoenix Contact QUINT 24 V / 10 A (2904617). Producenci podali terminy 6 i 8 tygodni.",
               "did": "Dostarczyliśmy oba komponenty z magazynów w UE w 48-72 godziny. Prefabrykacja ruszyła zgodnie z planem.",
               "res": "48-72 godziny zamiast 6-8 tygodni"},
    },
    {
        "id": "integrator-plant-modernisation", "img": "breakers",
        "en": {"t": "Automation system integrator, plant modernisation",
               "client": "Automation system integrator", "where": "Industrial plant modernisation", "scope": "Complete component set for the modernisation",
               "brands": "Schneider Electric, Allen-Bradley, IFM, Phoenix Contact, Siemens",
               "parts": "LC1D09P7 and others",
               "sit": "Schneider Electric LC1D09P7 contactors in large quantities, an Allen-Bradley HMI panel, IFM sensors, Phoenix Contact QUINT power supplies and Siemens resistors. The total was above the investor's budget.",
               "did": "We cut the cost of the list by 9.5% on average and by up to 30% on some items, and delivered the complete set in 4 weeks. The integrator kept both the margin and the deadline.",
               "res": "9.5% lower cost of the list, complete set in 4 weeks"},
        "pl": {"t": "Integrator systemów automatyki, modernizacja zakładu",
               "client": "Integrator systemów automatyki", "where": "Modernizacja zakładu przemysłowego", "scope": "Komplet komponentów do modernizacji",
               "brands": "Schneider Electric, Allen-Bradley, IFM, Phoenix Contact, Siemens",
               "parts": "LC1D09P7 i inne",
               "sit": "Styczniki Schneider Electric LC1D09P7 w dużej ilości, panel HMI Allen-Bradley, czujniki IFM, zasilacze Phoenix Contact QUINT i rezystory Siemens. Łączny koszt przekraczał budżet inwestora.",
               "did": "Obniżyliśmy koszt listy średnio o 9,5%, w części pozycji do 30%, i dostarczyliśmy komplet w 4 tygodnie. Integrator utrzymał marżę i termin.",
               "res": "Koszt listy niższy o 9,5%, komplet w 4 tygodnie"},
    },
    {
        "id": "general-contractor-bms-fire", "img": "sprinklers",
        "en": {"t": "General contractor, BMS and fire system upgrade",
               "client": "General contractor", "where": "BMS and fire system modernisation", "scope": "Replacement of discontinued system components",
               "brands": "Alarm, BMS and fire systems from 2005-2010",
               "parts": "Discontinued relays, detectors and control panels",
               "sit": "The design relied on relays, detectors and control panels that are no longer made: alarm, BMS and fire systems from 2005-2010.",
               "did": "Working with an integrator in a project consortium, we proposed a new system concept that was technically compliant, ready to install and cheaper than originally planned.",
               "res": "A new system concept instead of obsolete parts"},
        "pl": {"t": "Generalny wykonawca, modernizacja BMS i ppoż.",
               "client": "Generalny wykonawca", "where": "Modernizacja systemów BMS i ppoż.", "scope": "Zastąpienie wycofanych komponentów systemu",
               "brands": "Systemy alarmowe, BMS i ppoż. z lat 2005-2010",
               "parts": "Wycofane przekaźniki, czujniki i centrale",
               "sit": "Projekt opierał się na wycofanych z produkcji przekaźnikach, czujnikach i centralach: systemach alarmowych, BMS i ppoż. z lat 2005-2010.",
               "did": "Wspólnie z integratorem w konsorcjum projektowym zaproponowaliśmy nową koncepcję systemu: zgodną technicznie, gotową do wdrożenia i tańszą od pierwotnych założeń.",
               "res": "Nowa koncepcja systemu zamiast wycofanych części"},
    },
]

# ---------------------------------------------------------------- history
HISTORY = {
    "en": [
        ("2009", "The beginning", "GP ENERGIA started out in electrical installation work, building hands-on experience in the electrical trade."),
        ("2012-2015", "Gas sector projects", "Together with business partners we took part in projects for the gas sector and worked with industrial and energy companies."),
        ("2015-2020", "Switchboard and cabinet prefabrication", "We prefabricated control cabinets and electrical switchboards and installed electrical equipment. This is where our knowledge of components, protection devices and automation systems comes from."),
        ("2022", "Wholesale and sourcing", "We moved into wholesale, industrial procurement and sourcing of electrical and automation components for distributors, trading companies, resellers and procurement teams in Poland, with access to Siemens, Schneider Electric, ABB, Eaton, Rittal, Phoenix Contact, Legrand and other leading manufacturers."),
        ("2025", "International markets", "We are growing export sales and partnerships abroad, delivering industrial components across Europe, to the United States, Asia and the Middle East."),
        ("Today", "Industrial automation and electrical supply", "We focus on distribution and sourcing of industrial automation components, electrical equipment and technical supplies, and on long-term relationships built on competitive terms, clear communication and reliable delivery."),
    ],
    "pl": [
        ("2009", "Początki", "GP ENERGIA zaczynała od usług elektroinstalacyjnych. Wykonując instalacje elektryczne, zdobyliśmy praktyczne doświadczenie w branży."),
        ("2012-2015", "Projekty w sektorze gazowym", "Razem z partnerami biznesowymi uczestniczyliśmy w projektach dla sektora gazowego i współpracowaliśmy z firmami przemysłowymi i energetycznymi."),
        ("2015-2020", "Prefabrykacja rozdzielnic i szaf", "Prefabrykowaliśmy szafy sterownicze i rozdzielnice elektryczne oraz montowaliśmy urządzenia elektrotechniczne. Stąd nasza wiedza o komponentach, aparaturze zabezpieczeniowej i systemach automatyki."),
        ("2022", "Handel hurtowy i sourcing", "Rozwijamy handel hurtowy, zaopatrzenie przemysłowe i sourcing komponentów elektrycznych i automatyki dla dystrybutorów, firm handlowych, resellerów i działów zaopatrzenia w Polsce. Dostarczamy produkty m.in. Siemens, Schneider Electric, ABB, Eaton, Rittal, Phoenix Contact i Legrand."),
        ("2025", "Rynki międzynarodowe", "Rozwijamy sprzedaż eksportową i współpracę z partnerami zagranicznymi. Dostarczamy komponenty przemysłowe w Europie, do Stanów Zjednoczonych, krajów Azji i na Bliski Wschód."),
        ("Dziś", "Zaopatrzenie w automatykę i elektrotechnikę", "Koncentrujemy się na dystrybucji i sourcingu komponentów automatyki przemysłowej, aparatury elektrycznej i wyposażenia technicznego. Stawiamy na długoterminowe relacje: konkurencyjne warunki, sprawną komunikację i niezawodne dostawy."),
    ],
}

# ---------------------------------------------------------------- UI strings
T = {
    "en": {
        "skip": "Skip to content",
        "util_addr": "Warehouse and dispatch: ul. Polna 29, 55-095 Długołęka near Wrocław, Poland",
        "nav": [("products", "Products"), ("services", "Services"), ("references", "References"), ("about", "About"), ("blog", "Blog"), ("contact", "Contact")],
        "cta": "Request a quote", "cta_short": "Get a quote",
        "menu_open": "Open menu", "menu_close": "Close menu",
        "lang_label": "Language",
        "home": "Home",
        "mob_mail": "E-mail", "mob_cta": "Request a quote",
        "foot_desc": "Industrial automation and electrical components sourced to your BOM. Genuine products, one quote for the whole list, deliveries in Poland and worldwide.",
        "foot_cols": ("Offer", "Company", "Contact"),
        "foot_privacy": "Privacy policy",
        "foot_note": "Product photos: Adobe Stock (licensed) and Phoenix Contact. Brand names and logos belong to their owners and are shown only to indicate the products we supply.",
        "foot_switch": "Wersja polska",
        "read": "Read article", "min": "min read", "published": "Published", "updated": "Updated",
        "related": "More from the blog", "faq": "Frequently asked questions",
        "toc": "In this article",
        "case_more": "All references", "see_brands": "See all brands",
        "breadcrumb": "Breadcrumb",
    },
    "pl": {
        "skip": "Przejdź do treści",
        "util_addr": "Magazyn i wysyłka: ul. Polna 29, 55-095 Długołęka k. Wrocławia",
        "nav": [("products", "Produkty"), ("services", "Usługi"), ("references", "Realizacje"), ("about", "O firmie"), ("blog", "Blog"), ("contact", "Kontakt")],
        "cta": "Zapytaj o wycenę", "cta_short": "Wycena",
        "menu_open": "Otwórz menu", "menu_close": "Zamknij menu",
        "lang_label": "Język",
        "home": "Strona główna",
        "mob_mail": "E-mail", "mob_cta": "Zapytaj o wycenę",
        "foot_desc": "Komponenty automatyki przemysłowej i elektrotechniki według Twojej listy BOM. Oryginalne produkty, jedna oferta na całą listę, dostawy w Polsce i na eksport.",
        "foot_cols": ("Oferta", "Firma", "Kontakt"),
        "foot_privacy": "Polityka prywatności",
        "foot_note": "Zdjęcia produktów: Adobe Stock (licencja) i Phoenix Contact. Nazwy i logotypy marek należą do ich właścicieli i wskazują wyłącznie produkty, które dostarczamy.",
        "foot_switch": "English version",
        "read": "Czytaj artykuł", "min": "min czytania", "published": "Opublikowano", "updated": "Aktualizacja",
        "related": "Więcej na blogu", "faq": "Najczęstsze pytania",
        "toc": "W tym artykule",
        "case_more": "Wszystkie realizacje", "see_brands": "Zobacz wszystkie marki",
        "breadcrumb": "Ścieżka",
    },
}

# ---------------------------------------------------------------- page meta (overridden by SEO agent META.json when present)
META = {
    "home": {
        "en": {"title": "GP ENERGIA - automation and electrical components sourced to your BOM",
               "desc": "B2B supplier of genuine industrial automation and electrical components: PLCs, HMIs, sensors, contactors, power supplies, switchgear. One quote for your whole BOM, export worldwide.",
               "h1": "Automation and electrical components, sourced to your BOM"},
        "pl": {"title": "GP ENERGIA - komponenty automatyki i elektrotechniki według listy BOM",
               "desc": "Hurtowe dostawy oryginalnych komponentów automatyki przemysłowej i elektrotechniki: PLC, HMI, czujniki, styczniki, zasilacze. Jedna oferta na całą listę BOM, eksport.",
               "h1": "Komponenty automatyki i elektrotechniki według Twojej listy BOM"},
    },
    "services": {
        "en": {"title": "BOM sourcing, obsolete parts and export supply | GP ENERGIA",
               "desc": "BOM sourcing for automation and electrical components, discontinued and hard-to-find parts, project supply for prefabricators and integrators, logistics and export.",
               "h1": "Sourcing and supply services for automation and electrical components"},
        "pl": {"title": "Wycena BOM, części wycofane i dostawy eksportowe | GP ENERGIA",
               "desc": "Wycena list BOM komponentów automatyki i elektrotechniki, wyszukiwanie części wycofanych z produkcji, dostawy projektowe dla prefabrykatorów i integratorów, eksport.",
               "h1": "Sourcing i dostawy komponentów automatyki i elektrotechniki"},
    },
    "products": {
        "en": {"title": "Products and brands: automation and electrical components | GP ENERGIA",
               "desc": "Cabinets and enclosures, low-voltage equipment, PLCs and HMIs, installation equipment, fire protection, lighting and accessories from Siemens, Schneider Electric, ABB and 40+ brands.",
               "h1": "Products and brands we supply"},
        "pl": {"title": "Produkty i marki: komponenty automatyki i elektrotechniki | GP ENERGIA",
               "desc": "Szafy i obudowy, aparatura elektryczna, PLC i HMI, osprzęt elektroinstalacyjny, ppoż., oświetlenie i akcesoria marek Siemens, Schneider Electric, ABB i ponad 40 innych.",
               "h1": "Produkty i marki, które dostarczamy"},
    },
    "references": {
        "en": {"title": "References: component supply projects | GP ENERGIA",
               "desc": "Examples of our work: PLC and power supplies in 48-72 hours instead of 6-8 weeks, a BOM 9.5% cheaper for an integrator, a new concept for a BMS and fire system built on obsolete parts.",
               "h1": "References"},
        "pl": {"title": "Realizacje: dostawy komponentów dla projektów | GP ENERGIA",
               "desc": "Przykłady realizacji: sterownik i zasilacz w 48-72 godziny zamiast 6-8 tygodni, lista BOM tańsza o 9,5% dla integratora, nowa koncepcja systemu BMS i ppoż. na wycofanych częściach.",
               "h1": "Realizacje"},
    },
    "about": {
        "en": {"title": "About GP ENERGIA - in the electrical trade since 2009",
               "desc": "GP ENERGIA sp. z o.o.: from electrical installation work in 2009 through switchboard prefabrication to wholesale, sourcing and export of automation components.",
               "h1": "About GP ENERGIA"},
        "pl": {"title": "O firmie GP ENERGIA - w branży elektrotechnicznej od 2009 roku",
               "desc": "GP ENERGIA sp. z o.o.: od usług elektroinstalacyjnych w 2009 roku, przez prefabrykację rozdzielnic, po handel hurtowy, sourcing i eksport komponentów automatyki.",
               "h1": "O firmie GP ENERGIA"},
    },
    "blog": {
        "en": {"title": "Blog: BOM sourcing, automation components and export | GP ENERGIA",
               "desc": "Practical guides for buyers and engineers: how to prepare a BOM, how to replace discontinued automation parts and how to ship components abroad.",
               "h1": "Blog"},
        "pl": {"title": "Blog: wycena BOM, komponenty automatyki i eksport | GP ENERGIA",
               "desc": "Praktyczne poradniki dla zaopatrzeniowców i inżynierów: jak przygotować listę BOM, czym zastąpić wycofane komponenty i jak wysyłać części za granicę.",
               "h1": "Blog"},
    },
    "contact": {
        "en": {"title": "Contact and request for quote | GP ENERGIA",
               "desc": "Send part numbers or your BOM file (xlsx, csv, pdf) for price and availability. E-mail info@gpenergia.com.pl, warehouse ul. Polna 29, 55-095 Długołęka near Wrocław.",
               "h1": "Request a quote"},
        "pl": {"title": "Kontakt i zapytanie ofertowe | GP ENERGIA",
               "desc": "Wyślij kody produktów albo plik BOM (xlsx, csv, pdf) z prośbą o cenę i dostępność. E-mail info@gpenergia.com.pl, magazyn ul. Polna 29, 55-095 Długołęka k. Wrocławia.",
               "h1": "Zapytaj o wycenę"},
    },
    "privacy": {
        "en": {"title": "Privacy policy | GP ENERGIA",
               "desc": "How GP ENERGIA sp. z o.o. processes personal data sent through the enquiry form and by e-mail.",
               "h1": "Privacy policy"},
        "pl": {"title": "Polityka prywatności | GP ENERGIA",
               "desc": "Jak GP ENERGIA sp. z o.o. przetwarza dane osobowe przesłane przez formularz zapytania i pocztą elektroniczną.",
               "h1": "Polityka prywatności"},
    },
}

PATHS = {
    "home": ("", "pl/"),
    "services": ("services/", "pl/uslugi/"),
    "products": ("products/", "pl/produkty/"),
    "references": ("references/", "pl/realizacje/"),
    "about": ("about/", "pl/o-firmie/"),
    "blog": ("blog/", "pl/blog/"),
    "contact": ("contact/", "pl/kontakt/"),
    "privacy": ("privacy-policy/", "pl/polityka-prywatnosci/"),
}

# ---------------------------------------------------------------- service subpages + brands (copy from seo_0511/TEXTS.md, sales@ -> info@)
PATHS.update({
    "service_bom": ("services/bom-sourcing/", "pl/uslugi/zaopatrzenie-wg-bom/"),
    "service_obsolete": ("services/obsolete-parts/", "pl/uslugi/czesci-wycofane-z-produkcji/"),
    "service_project": ("services/project-supply/", "pl/uslugi/dostawy-projektowe/"),
    "service_export": ("services/logistics-export/", "pl/uslugi/logistyka-i-eksport/"),
    "brands": ("brands/", "pl/marki/"),
})
for _k, _en, _pl in [
    ("service_bom", ("BOM sourcing: one quote for your whole list | GP ENERGIA", "Send your bill of materials as it is and get one quote for every line, with price, lead time and alternatives.", "BOM sourcing: one quote for your whole bill of materials"),
                    ("Wycena listy BOM: jedna oferta na całą listę | GP ENERGIA", "Wyślij listę BOM w takiej postaci, w jakiej ją masz, i dostań jedną ofertę z ceną, terminem i zamiennikami.", "Zaopatrzenie wg listy BOM: jedna oferta na całą listę")),
    ("service_obsolete", ("Obsolete and discontinued automation parts | GP ENERGIA", "Discontinued PLC modules, relays, detectors and control panels: we search European stock or propose a compatible replacement.", "Obsolete and discontinued automation parts"),
                         ("Części automatyki wycofane z produkcji | GP ENERGIA", "Wycofane moduły PLC, przekaźniki, czujki i centrale: szukamy w magazynach w Europie albo proponujemy zgodny zamiennik.", "Części automatyki wycofane z produkcji")),
    ("service_project", ("Project supply for panel builders and integrators | GP ENERGIA", "Complete component packages for switchboard prefabrication, plant retrofits and building system upgrades.", "Project supply for panel builders, integrators and contractors"),
                        ("Dostawy projektowe dla prefabrykatorów | GP ENERGIA", "Kompletne dostawy komponentów do prefabrykacji rozdzielnic, modernizacji zakładów i systemów w budynkach.", "Dostawy projektowe dla prefabrykatorów, integratorów i wykonawców")),
    ("service_export", ("Logistics and export of automation components | GP ENERGIA", "Consolidation near Wrocław, courier or pallet freight, EXW, FCA or DAP, deliveries to Europe, the US, Asia, the Middle East and Africa.", "Logistics and export of automation components"),
                       ("Logistyka i eksport komponentów automatyki | GP ENERGIA", "Konsolidacja pod Wrocławiem, kurier lub spedycja paletowa, EXW, FCA albo DAP, dostawy do Europy, USA, Azji i na Bliski Wschód.", "Logistyka i eksport komponentów automatyki")),
    ("brands", ("Brands we supply: Siemens, Schneider Electric, ABB | GP ENERGIA", "Genuine products of more than 40 manufacturers, combined in one order, with alternatives for discontinued models.", "Brands we supply"),
               ("Marki, które dostarczamy: Siemens, Schneider, ABB | GP ENERGIA", "Oryginalne produkty ponad 40 producentów w jednym zamówieniu, z zamiennikami dla wycofanych modeli.", "Marki, które dostarczamy")),
]:
    META[_k] = {"en": dict(zip(("title", "desc", "h1"), _en)), "pl": dict(zip(("title", "desc", "h1"), _pl))}

BRAND_GROUPS = {
    "en": [("Automation and control", ["Siemens", "Schneider Electric", "ABB", "Allen-Bradley", "Omron", "Beckhoff", "Fanuc", "Emerson", "Honeywell", "Bosch", "SEW Eurodrive", "Danfoss", "SMC", "Panasonic", "Pilz", "Moxa", "Hirschmann"]),
           ("Sensors and measurement", ["Balluff", "Endress+Hauser", "Jumo", "IFM", "SICK", "Pepperl+Fuchs"]),
           ("Connection technology and power supplies", ["Phoenix Contact", "WAGO", "Weidmüller", "Wieland", "Cabur", "Degson", "TE Connectivity", "Harting", "Murrelektronik", "Finder"]),
           ("Protection and power distribution", ["Eaton", "Legrand", "DEHN", "Doepke", "Jean Müller", "Mersen", "Katko", "Frako", "Ensto", "OBO Bettermann", "Hensel"]),
           ("Enclosures and cabinets", ["Rittal", "nVent Hoffman", "Spelsberg", "R. Stahl"]),
           ("Installation equipment and lighting", ["Gewiss", "Gira", "AVE", "PCE", "BAKS", "Leds C4", "Rosa", "Elektromontaż Rzeszów"])],
}
BRAND_GROUPS["pl"] = list(zip(["Automatyka i sterowanie", "Czujniki i pomiary", "Technika połączeń i zasilacze", "Zabezpieczenia i rozdział energii", "Obudowy i szafy", "Osprzęt instalacyjny i oświetlenie"],
                              [g[1] for g in BRAND_GROUPS["en"]]))
