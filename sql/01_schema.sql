CREATE TABLE IF NOT EXISTS compagnie (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nom VARCHAR(255),
  code VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS aeroport (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nom VARCHAR(255),
  code VARCHAR(10),
  ville VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS vol (
  id INT AUTO_INCREMENT PRIMARY KEY,
  numero_vol VARCHAR(20),
  compagnie_id INT,
  aeroport_depart_id INT,
  aeroport_arrivee_id INT,
  heure_depart DATETIME,
  heure_arrivee DATETIME,
  prix DECIMAL(10,2),
  places_disponibles INT,
  FOREIGN KEY (compagnie_id) REFERENCES compagnie(id),
  FOREIGN KEY (aeroport_depart_id) REFERENCES aeroport(id),
  FOREIGN KEY (aeroport_arrivee_id) REFERENCES aeroport(id)
);

CREATE TABLE IF NOT EXISTS passager (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nom VARCHAR(255),
  email VARCHAR(255),
  tel VARCHAR(20),
  passport_numero VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS reservation (
  id INT AUTO_INCREMENT PRIMARY KEY,
  passager_id INT,
  vol_id INT,
  status ENUM('confirmee', 'annulee'),
  date_reservation DATETIME,
  FOREIGN KEY (passager_id) REFERENCES passager(id),
  FOREIGN KEY (vol_id) REFERENCES vol(id)
);

INSERT INTO compagnie (nom, code) VALUES ("Air France", "AF"), ("British Airways", "BA"), ("Lufthansa", "LH"), ("Emirates", "EK"), ("Qatar Airways", "QR"), ("Singapore Airlines", "SQ"), ("Cathay Pacific", "CX"), ("ANA", "NH"), ("Japan Airlines", "JL"), ("KLM", "KL");

