import requests
import uuid

BASE_URL = "http://127.0.0.1:8000"  # URL de l'API

# --------------------------
# Fonctions d'aide
# --------------------------
def get_first_compagnie():
    resp = requests.get(f"{BASE_URL}/compagnies")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) > 0
    return data[0]["id"]

def get_first_aeroport():
    resp = requests.get(f"{BASE_URL}/aeroports")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) > 0
    return data[0]["id"]

def get_first_passager():
    resp = requests.get(f"{BASE_URL}/passager/FR123456")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) > 0
    return data[0]["id"]

def creer_vol_test(compagnie_id, dep_id, arr_id):
    numero_vol = f"TEST-{uuid.uuid4().hex[:6]}"
    data = {
        "numero_vol": numero_vol,
        "compagnie_id": compagnie_id,
        "aeroport_depart_id": dep_id,
        "aeroport_arrivee_id": arr_id,
        "heure_depart": "2025-10-01 10:00:00",
        "heure_arrivee": "2025-10-01 12:00:00",
        "prix": 200.0,
        "places_disponibles": 2
    }
    resp = requests.post(f"{BASE_URL}/vols", json=data)
    print(resp.status_code, resp.text)
    assert resp.status_code == 200
    # Retourner le numero_vol car GET /vols/<ref> recherche par numero_vol
    return numero_vol

def creer_reservation_test(passager_id, vol_id):
    data = {
        "passager_id": passager_id,
        "vol_id": vol_id,  # vol_id doit être numérique
        "status": "confirmee",
        "date_reservation": "2025-10-01 09:00:00"
    }
    resp = requests.post(f"{BASE_URL}/reservations", json=data)
    print(resp.status_code, resp.text)
    assert resp.status_code == 200
    return resp.json().get("id"), data["status"]

# --------------------------
# Tests Compagnies
# --------------------------
def test_lister_compagnies():
    resp = requests.get(f"{BASE_URL}/compagnies")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_get_compagnie():
    compagnie_id = get_first_compagnie()
    resp = requests.get(f"{BASE_URL}/compagnies/{compagnie_id}")
    assert resp.status_code == 200

# --------------------------
# Tests Aéroports
# --------------------------
def test_lister_aeroports():
    resp = requests.get(f"{BASE_URL}/aeroports")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

# --------------------------
# Tests Vols
# --------------------------
def test_creer_et_lister_vol():
    compagnie_id = get_first_compagnie()
    dep_id = get_first_aeroport()
    aeroports = requests.get(f"{BASE_URL}/aeroports").json()
    arr_id = next(a["id"] for a in aeroports if a["id"] != dep_id)

    numero_vol = creer_vol_test(compagnie_id, dep_id, arr_id)
    resp = requests.get(f"{BASE_URL}/vols/{numero_vol}")  # recherche par numero_vol
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert data[0]["numero_vol"].lower() == numero_vol.lower()

# --------------------------
# Tests Passagers
# --------------------------
def test_get_passager():
    resp = requests.get(f"{BASE_URL}/passager/FR123456")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)

# --------------------------
# Tests Réservations
# --------------------------
def test_creer_lister_et_annuler_reservation():
    compagnie_id = get_first_compagnie()
    dep_id = get_first_aeroport()
    aeroports = requests.get(f"{BASE_URL}/aeroports").json()
    arr_id = next(a["id"] for a in aeroports if a["id"] != dep_id)

    numero_vol = creer_vol_test(compagnie_id, dep_id, arr_id)

    # Récupérer l'ID numérique du vol créé
    vols = requests.get(f"{BASE_URL}/vols").json()
    vol_id = next(v["id"] for v in vols if v["numero_vol"].lower() == numero_vol.lower())

    passager_id = get_first_passager()

    reservation_id, status = creer_reservation_test(passager_id, vol_id)
    assert status == "confirmee"

    resp = requests.get(f"{BASE_URL}/reservations")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

    # DELETE par passager_id comme dans reservations.py
    resp_delete = requests.delete(f"{BASE_URL}/reservations/{passager_id}")
    assert resp_delete.status_code in [200, 204]