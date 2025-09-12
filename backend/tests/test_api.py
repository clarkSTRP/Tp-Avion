import requests
import uuid

BASE_URL = "http://127.0.0.1:8000"  # URL de l'API
API_KEY = "cle1"  # <- ta clé API

HEADERS = {
    "X-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

# --------------------------
# Fonctions d'aide
# --------------------------
def get_first_compagnie():
    resp = requests.get(f"{BASE_URL}/compagnies", headers=HEADERS)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert len(data) > 0
    return data[0]["nom"]  # endpoint /compagnies/<ref> attend "nom"

def get_first_aeroport():
    resp = requests.get(f"{BASE_URL}/aeroports", headers=HEADERS)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert len(data) > 0
    return data[0]["id"]

def get_first_passager():
    resp = requests.get(f"{BASE_URL}/passager/FR123456", headers=HEADERS)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert len(data) > 0
    return data[0]["passport_numero"]  # endpoint /passager/<ref> attend le numéro

def creer_vol_test(compagnie_nom, dep_id, arr_id):
    numero_vol = f"TEST-{uuid.uuid4().hex[:6]}"
    data = {
        "numero_vol": numero_vol,
        "compagnie_id": 1,  # <-- à adapter à ton jeu de données
        "aeroport_depart_id": dep_id,
        "aeroport_arrivee_id": arr_id,
        "heure_depart": "2025-10-01 10:00:00",
        "heure_arrivee": "2025-10-01 12:00:00",
        "prix": 200.0,
        "places_disponibles": 2
    }
    resp = requests.post(f"{BASE_URL}/vols", json=data, headers=HEADERS)
    print("Création vol:", resp.status_code, resp.text)
    assert resp.status_code == 201, resp.text
    return numero_vol

def creer_reservation_test(passager_id, vol_id):
    data = {
        "passager_id": passager_id,
        "vol_id": vol_id,
        "status": "confirmee",
        "date_reservation": "2025-10-01 09:00:00"
    }
    resp = requests.post(f"{BASE_URL}/reservations", json=data, headers=HEADERS)
    print("Création réservation:", resp.status_code, resp.text)
    assert resp.status_code == 201, resp.text
    return data["status"]

# --------------------------
# Tests Compagnies
# --------------------------
def test_lister_compagnies():
    resp = requests.get(f"{BASE_URL}/compagnies", headers=HEADERS)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_get_compagnie():
    nom_compagnie = get_first_compagnie()
    resp = requests.get(f"{BASE_URL}/compagnies/{nom_compagnie}", headers=HEADERS)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)

# --------------------------
# Tests Aéroports
# --------------------------
def test_lister_aeroports():
    resp = requests.get(f"{BASE_URL}/aeroports", headers=HEADERS)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

# --------------------------
# Tests Vols
# --------------------------
def test_creer_et_lister_vol():
    nom_compagnie = get_first_compagnie()
    dep_id = get_first_aeroport()
    aeroports = requests.get(f"{BASE_URL}/aeroports", headers=HEADERS).json()
    arr_id = next(a["id"] for a in aeroports if a["id"] != dep_id)

    numero_vol = creer_vol_test(nom_compagnie, dep_id, arr_id)
    resp = requests.get(f"{BASE_URL}/vols/{numero_vol}", headers=HEADERS)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert data[0]["numero_vol"].lower() == numero_vol.lower()

# --------------------------
# Tests Passagers
# --------------------------
def test_get_passager():
    passport_numero = get_first_passager()
    resp = requests.get(f"{BASE_URL}/passager/{passport_numero}", headers=HEADERS)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)

# --------------------------
# Tests Réservations
# --------------------------
def test_creer_lister_et_annuler_reservation():
    nom_compagnie = get_first_compagnie()
    dep_id = get_first_aeroport()
    aeroports = requests.get(f"{BASE_URL}/aeroports", headers=HEADERS).json()
    arr_id = next(a["id"] for a in aeroports if a["id"] != dep_id)

    numero_vol = creer_vol_test(nom_compagnie, dep_id, arr_id)
    vols = requests.get(f"{BASE_URL}/vols", headers=HEADERS).json()
    vol_id = next(v["id"] for v in vols if v["numero_vol"].lower() == numero_vol.lower())

    passager_numero = get_first_passager()
    # ⚠️ Ici tu dois avoir l'ID numérique du passager, pas juste son numéro de passeport
    passager_id = 1  # adapte selon ta DB
    status = creer_reservation_test(passager_id, vol_id)
    assert status == "confirmee"

    resp = requests.get(f"{BASE_URL}/reservations", headers=HEADERS)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

    resp_delete = requests.delete(f"{BASE_URL}/reservations/{passager_id}", headers=HEADERS)
    assert resp_delete.status_code in [200, 202, 204]
