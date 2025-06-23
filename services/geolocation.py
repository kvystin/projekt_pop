import re, requests
from bs4 import BeautifulSoup

FALLBACK = [52.2297, 21.0122]

def _dms_to_decimal(txt: str) -> float:
    #Konwersja formatu DMS na liczbę dziesiętną
    m = re.match(r"(\d+)°(\d+)′(\d+)″\s*([NSEW])", txt)
    if not m:
        raise ValueError("Nieznany format DMS")
    d, mnt, s, hemi = m.groups()
    dec = int(d) + int(mnt) / 60 + int(s) / 3600
    return -dec if hemi in ("S", "W") else dec


def _as_float(txt: str) -> float:
    #Próba rzutowania na float, ewentualnie konwersja z DMS
    try:
        return float(txt.replace(",", "."))
    except ValueError:
        return _dms_to_decimal(txt)


def get_coordinates(place: str) -> list[float]:
    #Zwraca [lat, lon] lub fallback w razie błędu
    url = f"https://pl.wikipedia.org/wiki/{place}"
    try:
        soup = BeautifulSoup(requests.get(url, timeout=4).text, "html.parser")
        lat_txt = soup.select(".latitude")[-1].text.strip()
        lon_txt = soup.select(".longitude")[-1].text.strip()
        return [_as_float(lat_txt), _as_float(lon_txt)]
    except Exception as exc:
        print("[Geo]", exc)
        return FALLBACK
