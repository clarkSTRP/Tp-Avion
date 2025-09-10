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
INSERT INTO aeroport (nom, code, ville) VALUES ("Paris Charles de Gaulle", "CDG", "Paris"), ("London Heathrow", "LHR", "Londres"), ("Frankfurt Airport", "FRA", "Francfort"), ("Dubai International", "DXB", "Dubaï"), ("Doha Hamad", "DOH", "Doha"), ("Singapore Changi", "SIN", "Singapour"), ("Hong Kong International", "HKG", "Hong Kong"), ("Tokyo Haneda", "HND", "Tokyo"), ("Tokyo Narita", "NRT", "Tokyo"), ("Amsterdam Schiphol", "AMS", "Amsterdam");
INSERT INTO vol (numero_vol, compagnie_id, aeroport_depart_id, aeroport_arrivee_id, heure_depart, heure_arrivee, prix, places_disponibles) VALUES ("AF123", 1, 1, 2, '2025-09-12 08:30:00', '2025-09-12 09:30:00', 150.00, 50), ("BA456", 2, 2, 1, '2025-09-13 14:00:00', '2025-09-13 16:20:00', 160.00, 60), ("LH789", 3, 3, 1, '2025-09-14 10:15:00', '2025-09-14 12:00:00', 180.00, 45), ("EK202", 4, 4, 1, '2025-09-15 23:50:00', '2025-09-16 06:30:00', 450.00, 100), ("QR333", 5, 5, 2, '2025-09-16 18:40:00', '2025-09-16 22:15:00', 400.00, 80), ("SQ101", 6, 6, 1, '2025-09-17 09:00:00', '2025-09-17 16:00:00', 600.00, 70), ("CX888", 7, 7, 1, '2025-09-18 21:30:00', '2025-09-19 05:30:00', 500.00, 65), ("NH212", 8, 8, 1, '2025-09-19 13:10:00', '2025-09-19 19:30:00', 550.00, 55), ("JL401", 9, 9, 1, '2025-09-20 07:45:00', '2025-09-20 14:00:00', 540.00, 40), ("KL789", 10, 10, 1, '2025-09-21 11:20:00', '2025-09-21 12:50:00', 140.00, 75);
INSERT INTO passager (nom, email, tel, passport_numero) VALUES ("Jean Dupont", "jean.dupont@example.com", "+33611223344", "FR123456"), ("Sophie Martin", "sophie.martin@example.com", "+33655667788", "FR654321"), ("John Smith", "john.smith@example.com", "+447911223344", "UK998877"), ("Maria Rossi", "maria.rossi@example.com", "+390612345678", "IT112233"), ("Ahmed Khan", "ahmed.khan@example.com", "+971501234567", "AE778899"), ("Chen Wei", "chen.wei@example.com", "+8613812345678", "CN445566"), ("Akira Tanaka", "akira.tanaka@example.com", "+819012345678", "JP556677"), ("Laura Johnson", "laura.johnson@example.com", "+14155552671", "US889900"), ("Peter Muller", "peter.muller@example.com", "+4915112345678", "DE334455"), ("Fatima Al Thani", "fatima.althani@example.com", "+97455512345", "QA223344");
INSERT INTO reservation (passager_id, vol_id, status, date_reservation) VALUES (1, 1, 'confirmee', '2025-09-10 09:00:00'), (2, 1, 'confirmee', '2025-09-10 10:00:00'), (3, 2, 'annulee', '2025-09-11 11:30:00'), (4, 3, 'confirmee', '2025-09-12 14:15:00'), (5, 4, 'confirmee', '2025-09-13 20:00:00'), (6, 5, 'confirmee', '2025-09-14 07:45:00'), (7, 6, 'annulee', '2025-09-15 16:20:00'), (8, 7, 'confirmee', '2025-09-16 19:10:00'), (9, 8, 'confirmee', '2025-09-17 12:00:00'), (10, 9, 'confirmee', '2025-09-18 09:30:00');
