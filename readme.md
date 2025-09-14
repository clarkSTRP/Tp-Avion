## Instruction d'installation
<details>
        <summary>Docker en local</summary>
        
#### Prérequis:
- Docker installé & allumé
- Git

#### Téléchargement de la branche principale (stable)
```
git clone https://github.com/clarkSTRP/Tp-Avion
```

#### Lancement du conteneur
```
docker compose up --build
```

#### Après arrêt du docker, vous pouvez effacer les informations laissées en mémoire avec
```
docker compose down -v
```
</details>

<details>
        <summary>Docker orchestré avec K8s (1 master 2 workers)</summary>
        
#### Prérequis:
- 3 machines virtuelles (VM) Ubuntu server minimal

#### Téléchargement des paquets (sur chaque VM)
##### Docker
```
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
sudo systemctl enable docker
sudo systemctl start docker
```
##### Kubernetes (K8s)
```
sudo swapoff -a
sudo sed -i '/ swap / s/ˆ\(.*\)$/#\1/g' /etc/fstab
echo "vm.swappiness=0" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
sudo apt install -y apt-transport-https gpg

curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.34/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.34/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
sudo systemctl enable --now kubelet
```

#### Initialisation du cluster sur la VM master
```

```

#### Après arrêt du docker, vous pouvez effacer les informations laissées en mémoire avec
```
docker compose down -v
```
</details>

## Liste des routes disponibles
<details>
<summary>Routes de compagnie</summary>

- `GET /compagnies` Liste les compagnies
- `GET /compagnies/<nom>` Affiche les détails d'une compagnie
- `POST /compagnie` Crée une compagnie (préciser les informations en JSON)

</details>

<details>
<summary>Routes de aéroports</summary>

- `GET /aeroports` Liste les aéroports
- `POST /aeroports` Crée un aéroport

</details>

<details>
<summary>Routes de vols</summary>

- `GET /vols` Afficher la liste des vols
- `GET /vols/<numero_vol>` Afficher les détails d'un vol en particulier
- `POST /vols` Créer un vol
- `PUT /vols/<idVol>` Modifier un vol

</details>

<details>
<summary>Routes de passagers</summary>

- `GET /passager/<passport_numero>` Afficher les détails sur un passager
- `POST /passager` Créer un passager

</details>

<details>
<summary>Routes de réservations</summary>

- `GET /reservations` Afficher les réservations
- `POST /reservations` Créer une réservation
- `DELETE /reservations` Annuler une réservation

</details>


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
```bash
curl -X PUT http://localhost:8000/vols/1 \
  -H "Content-Type: application/json" \
  -d '{"prix": 199.99, "places_disponibles": 30
  }'
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
