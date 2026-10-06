import os
import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup


# ============================================================
# ASETUKSET
# ============================================================

# ntfy-topic haetaan GitHub Secretistä.
NTFY_TOPIC = os.environ.get("NTFY_TOPIC")

# Tiedosto, johon tallennetaan tuotteiden edellinen tila.
STATE_FILE = "stock_state.json"


PRODUCTS = [
    {
        "name": "30th Celebration Mini Tin",
        "store": "Muovitukku",
        "url": "https://www.muovitukku.fi/tuote/pokemon-30th-celebration-mini-tin/",
    },
    {
        "name": "30th Celebration Booster Bundle",
        "store": "Muovitukku",
        "url": "https://www.muovitukku.fi/tuote/pokemon-tcg-30th-celebration-booster-bundle/",
    },
    {
        "name": "30th Celebration Elite Trainer Box",
        "store": "Muovitukku",
        "url": "https://www.muovitukku.fi/tuote/pokemon-elite-trainer-box-30th/",
    },
    {
        "name": "30th Celebration Booster Bundle",
        "store": "TCG-kauppa",
        "url": "https://www.tcgkauppa.fi/tuote/pokemon-30th-celebration-booster-bundle/",
    },
    {
        "name": "30th Celebration Elite Trainer Box",
        "store": "TCG-kauppa",
        "url": "https://www.tcgkauppa.fi/tuote/pokemon-30th-celebration-elite-trainer-box/",
    },
    {
        "name": "30th Celebration Elite Trainer Box",
        "store": "Verkkokauppa.com",
        "url": "https://www.verkkokauppa.com/fi/product/1069670/Pokemon-TCG-30th-Elite-Trainer-Box-kerailykortit",
    },
    {
        "name": "30th Celebration Booster Bundle",
        "store": "Verkkokauppa.com",
        "url": "https://www.verkkokauppa.com/fi/product/1069691/Pokemon-TCG-30th-Booster-Bundle-kerailykortit-6-pack",
    },
    {
        "name": "Prismatic Evolutions Booster Bundle",
        "store": "Verkkokauppa.com",
        "url": "https://www.verkkokauppa.com/fi/product/972680/Pokemon-TCG-Scarlet-Violet-8-5-Prismatic-Evolutions-Booster",
    },
    {
        "name": "Prismatic Evolutions Elite Trainer Box",
        "store": "Verkkokauppa.com",
        "url": "https://www.verkkokauppa.com/fi/product/972662/Pokemon-TCG-Scarlet-Violet-8-5-Prismatic-Evolutions-Elite-Tr",
    },
    {
        "name": "Ascended Heroes Booster Bundle",
        "store": "Verkkokauppa.com",
        "url": "https://www.verkkokauppa.com/fi/product/1037309/Pokemon-ME02-5-Ascended-Heroes-Booster-Bundle-kerailykorttip",
    },
    {
        "name": "Ascended Heroes Elite Trainer Box",
        "store": "Verkkokauppa.com",
        "url": "https://www.verkkokauppa.com/fi/product/1031984/Pokemon-TCG-ME02-5-Ascended-Heroes-Elite-Trainer-Box-keraily",
    },
    {
        "name": "30th Celebration Elite Trainer Box",
        "store": "PokéPulls",
        "url": "https://pokepulls.fi/tuote/pokemon-tcg-30th-celebration-elite-trainer-box",
    },
    {
        "name": "30th Celebration Booster Bundle",
        "store": "PokéPulls",
        "url": "https://pokepulls.fi/product/pokemon-tcg-30th-celebration-booster-bundle-julkaisu-2-10-2026-max-2-asiakas",
    },
    {
        "name": "30th Celebration 2-Pack Blister",
        "store": "MaxGaming",
        "url": "https://www.maxgaming.fi/fi/pokemon/pokemon-30th-celebration-2-pack-blister",
    },
    {
        "name": "30th Celebration Elite Trainer Box",
        "store": "MaxGaming",
        "url": "https://www.maxgaming.fi/fi/pokemon/pokemon-30th-celebration-elite-trainer-box",
    },
    {
        "name": "30th Celebration Booster Bundle",
        "store": "Korttistoppi",
        "url": "https://www.korttistoppi.fi/tuote/pokemon-tcg-30th-celebration-booster-bundle-julkaisupaiva-2102026",
    },
    {
        "name": "Ascended Heroes Elite Trainer Box",
        "store": "Korttistoppi",
        "url": "https://www.korttistoppi.fi/tuote/pokemon-tcg-mega-evolution-25-ascended-heroes-elite-trainer-box-julkaisupaiva-2022026",
    },
    {
        "name": "30th Celebration Elite Trainer Box",
        "store": "Prisma",
        "url": "https://www.prisma.fi/tuotteet/111388829/pokemon-elite-trainer-box-30th-111388829",
    },
    {
        "name": "30th Celebration 2-Pack Blister",
        "store": "Prisma",
        "url": "https://www.prisma.fi/tuotteet/111388834/pokemon-2-pack-blister-30th-111388834",
    },
    {
        "name": "30th Celebration Booster Bundle",
        "store": "Prisma",
        "url": "https://www.prisma.fi/tuotteet/111388842/pokemon-bst-bundle-30th-111388842",
    },
    {
        "name": "Ascended Heroes Booster Bundle",
        "store": "Prisma",
        "url": "https://www.prisma.fi/tuotteet/111268553/pokemon-tcg-kerailykortit-me025-ascended-heroes-booster-bundle-111268553",
    },
    {
        "name": "Ascended Heroes Elite Trainer Box",
        "store": "Prisma",
        "url": "https://www.prisma.fi/tuotteet/111239007/pokemon-tcg-me025-elite-trainer-box-111239007",
    },
    {
        "name": "30th Celebration Elite Trainer Box",
        "store": "Peliparatiisi",
        "url": "https://peliparatiisi.net/en/products/pokemon-tcg-30th-celebration-elite-trainer-box",
    },
    {
        "name": "30th Celebration Booster Bundle",
        "store": "Peliparatiisi",
        "url": "https://peliparatiisi.net/en/products/pokemon-tcg-30th-celebration-booster-bundle",
    },
    {
        "name": "30th Celebration Sylveon ex Box",
        "store": "Peliparatiisi",
        "url": "https://peliparatiisi.net/en/products/pokemon-tcg-30th-celebration-sylveon-ex-box",
    },
    {
        "name": "30th Celebration 2-Pack Blister",
        "store": "Peliparatiisi",
        "url": "https://peliparatiisi.net/en/products/pokemon-tcg-30th-celebration-2-pack-blister",
    },
    {
        "name": "Prismatic Evolutions Elite Trainer Box",
        "store": "TCG-kauppa",
        "url": "https://www.tcgkauppa.fi/tuote/pokemon-sv8-5-prismatic-evolutions-elite-trainer-box/",
    },
    {
        "name": "Prismatic Evolutions Elite Trainer Box",
        "store": "Kärkkäinen",
        "url": "https://www.karkkainen.com/verkkokauppa/pokemon-tcg-scarlet-violet-8-5-prismatic-evolutions-elite-trainer-box-kerailykortit",
    },
    {
        "name": "Prismatic Evolutions Booster Bundle",
        "store": "Kärkkäinen",
        "url": "https://www.karkkainen.com/verkkokauppa/pokemon-booster-bundle-scarlet-violet-prismatic-evolutions",
    },
]


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/154.0.0.0 Safari/537.36"
    )
}


# ============================================================
# TILAN TALLENNUS
# ============================================================

def load_state():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as file:
        json.dump(state, file, indent=2, ensure_ascii=False)


# ============================================================
# SAATAVUUDEN TARKISTUS
# ============================================================

def check_availability(product):

    response = requests.get(
        product["url"],
        headers=HEADERS,
        timeout=20
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    page_text = soup.get_text(" ", strip=True).lower()

    out_of_stock_phrases = [
        "varasto loppu",
        "tämä tuote on tällä hetkellä loppu",
        "ei varastossa",
        "ei saatavilla",
        "loppuunmyyty",
        "loppunut",
        "sold out",
    ]

    for phrase in out_of_stock_phrases:
        if phrase in page_text:
            return False

    return True


# ============================================================
# PUHELINILMOITUS
# ============================================================

def send_phone_notification(product):

    if not NTFY_TOPIC:
        print("⚠️ NTFY_TOPIC puuttuu GitHub Secretsistä.")
        return

    try:
        response = requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data=(
                f"🔥 {product['name']} on nyt saatavilla "
                f"kaupasta {product['store']}!"
            ).encode("utf-8"),
            headers={
                "Title": "Pokemon SAATAVILLA!",
                "Click": product["url"],
                "Priority": "high",
                "Tags": "fire",
            },
            timeout=10,
        )

        response.raise_for_status()

    except requests.RequestException as error:
        print(f"Puhelinilmoituksen lähetys epäonnistui: {error}")


# ============================================================
# TUOTTEIDEN TARKISTUS
# ============================================================

def check_products():

    previous_state = load_state()
    new_state = {}

    print("=" * 75)
    print("Tarkistus:", datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
    print("=" * 75)

    for product in PRODUCTS:

        product_id = product["url"]

        try:
            available = check_availability(product)

            new_state[product_id] = available

            if available:

                print(
                    f"{product['store']:<16} | "
                    f"{product['name']:<42} | "
                    f"🟢 SAATAVILLA"
                )

                # Ilmoitus vain, jos tuote oli aikaisemmin loppu.
                if previous_state.get(product_id) is False:

                    print(
                        f"🔥 UUSI SAATAVUUS: "
                        f"{product['store']} - {product['name']}"
                    )

                    send_phone_notification(product)

                # Ensimmäisellä ajolla ei lähetetä ilmoitusta.
                elif product_id not in previous_state:

                    print("   Ensimmäinen tarkistus – tila tallennetaan.")

            else:

                print(
                    f"{product['store']:<16} | "
                    f"{product['name']:<42} | "
                    f"🔴 LOPPU"
                )

        except requests.RequestException as error:

            print(
                f"{product['store']:<16} | "
                f"{product['name']:<42} | "
                f"⚠️ YHTEYSVIRHE"
            )

            print("   ", error)

            # Säilytetään edellinen tila yhteysvirheen aikana.
            if product_id in previous_state:
                new_state[product_id] = previous_state[product_id]

        except Exception as error:

            print(
                f"{product['store']:<16} | "
                f"{product['name']:<42} | "
                f"⚠️ VIRHE: {error}"
            )

            if product_id in previous_state:
                new_state[product_id] = previous_state[product_id]

    save_state(new_state)


# ============================================================
# PÄÄOHJELMA
# ============================================================

if __name__ == "__main__":

    print()
    print("================================================")
    print("       POKEMON CLOUD STOCK WATCHER")
    print("================================================")
    print()
    print(f"Seurattavia tuotteita: {len(PRODUCTS)}")
    print()

    check_products()
