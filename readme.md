## Instruction d'installation

## Liste des routes disponibles

## Exemples de requêtes
#### Création d'une compagnie
```bash
curl -X POST http://localhost:8000/compagnies   -H "Content-Type: application/json"   -d '{
        "nom": "La compagnie test",
        "code": "TT"
      }'
```

#### Création d'un aéroport:
```bash
curl -X POST http://localhost:8000/aeroports   -H "Content-Type: application/json"   -d '{
        "nom": "Aeroport TEST",
        "code": "TST",
        "ville": "MaVille"
      }'
```

#### Creation d'un vol
```bash
curl -X POST http://localhost:8000/vols   -H "Content-Type: application/json"   -d '{
        "numero_vol": "FR555",
        "compagnie_id": 4,
        "aeroport_depart_id": 5,
        "aeroport_arrivee_id": 4,
        "heure_depart": "2026-09-12 08:30:00",
        "heure_arrivee": "2029-12-12 08:30:00",
        "prix": 847.37,
        "places_disponibles": 60
      }'
```
#### Modification d'un vol
```
curl -X PUT http://localhost:8000/vols/1 \
  -H "Content-Type: application/json" \
  -d '{"prix": 199.99, "places_disponibles": 30}'

```

#### Création d'un passager:
```bash
curl -X POST http://localhost:8000/passager   -H "Content-Type: application/json"   -d '{
        "nom": "Prenom NOM",
        "email": "email@domain.fr",
        "tel": "+33700000000",
        "passport_numero": "FR888888"
      }'
```

#### Création d'une réservation:
```bash
curl -X POST http://localhost:8000/reservations   -H "Content-Type: application/json"   -d '{
        "passager_id": 1,
        "vol_id": 2,
        "status": "confirmee"
      }'
```
## Docker
#### Dockerfile
```Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/


CMD ["python", "-m", "app.main"]
```
#### docker-compose.yml
```yml
version: "3.9"

services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: tp_avion
      MYSQL_USER: tp_user
      MYSQL_PASSWORD: tp_pass
    ports:
      - "3306:3306"
    volumes:
      - db_data:/var/lib/mysql
      - ./sql:/docker-entrypoint-initdb.d:ro

  api:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DB_HOST: db
      DB_PORT: 3306
      DB_NAME: tp_avion
      DB_USER: tp_user
      DB_PASS: tp_pass
    depends_on:
      - db

volumes:
  db_data:
```

## Tests unitaires ou d'intégration
