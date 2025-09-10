CREATE TABLE IF NOT EXISTS compagnie (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nom VARCHAR(255),
  code VARCHAR(10)
);

INSERT INTO compagnie (nom, code) VALUES ("Air France", "AF"), ("British Airways", "BA"), ("Lufthansa", "LH"), ("Emirates", "EK"), ("Qatar Airways", "QR"), ("Singapore Airlines", "SQ"), ("Cathay Pacific", "CX"), ("ANA", "NH"), ("Japan Airlines", "JL"), ("KLM", "KL");

