use db;

CREATE TABLE utilisateur (
  idUtilisateur int AUTO_INCREMENT,
  username varchar(100) UNIQUE NOT NULL,
  password varchar(100) NOT NULL,
  role varchar(100) NOT NULL,
  PRIMARY KEY(idUtilisateur)
);

CREATE TABLE produit (
  idProduit int AUTO_INCREMENT,
  code varchar(100) NOT NULL,
  marque varchar(100) NOT NULL,
  modele varchar(100) NOT NULL,
  coloris varchar(100) NOT NULL,
  prix int NOT NULL,
  image varchar(100),
  PRIMARY KEY(idProduit)
);

CREATE TABLE panier (
  idPanier int AUTO_INCREMENT,
  idUtilisateur int NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(idPanier),
  FOREIGN KEY (idUtilisateur) REFERENCES utilisateur(idUtilisateur)
);

CREATE TABLE produit_panier (
  idProduitPanier int AUTO_INCREMENT,
  idProduit int NOT NULL,
  idPanier int NOT NULL,
  quantite int,
  PRIMARY KEY(idProduitPanier),
  FOREIGN KEY (idProduit) REFERENCES produit(idProduit),
  FOREIGN KEY (idPanier) REFERENCES panier(idPanier)
);

CREATE TABLE commande (
  idCommande int AUTO_INCREMENT,
  idUtilisateur int NOT NULL,
  idPanier int NOT NULL,
  dateCommande TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  prixTotal int NOT NULL,
  PRIMARY KEY(idCommande),
  FOREIGN KEY (idUtilisateur) REFERENCES utilisateur(idUtilisateur),
  FOREIGN KEY (idPanier) REFERENCES panier(idPanier)
);

INSERT INTO utilisateur(username, password, role)
VALUES("julien", "password", "admin");

INSERT INTO produit(code, marque, modele, coloris, prix, image)
VALUES('SNKRS-001', 'Nike', 'Vaporwaffle Sacai', 'Black White', 570, 'Nike-Sacai-Vaporwaffle-black-white.png'), 
      ('SNKRS-002', 'Nike', 'Vaporwaffle Sacai', 'Sport Fuchsia Game Royal', 590, 'Nike-Sacai-VaporWaffle-Game-Royal-Fuchsia.png'),
      ('SNKRS-003', 'Nike', 'Vaporwaffle Sacai', 'Tour Yellow Stadium Green', 490, 'Nike-Sacai-VaporWaffle-Tour-Yellow-Stadium-Green.png'),
      ('SNKRS-004', 'Nike', 'Vaporwaffle Sacai', 'Villain Red Neptune Green', 510, 'Nike-Sacai-Vaporwaffle-Villain-Red-Neptune-Green.png'),
      ('SNKRS-005', 'Nike', 'Air Jordan 1 Retro High Travis Scott', 'Cactus Jack', 1520, 'Air-Jordan-1-Cactus-Jack-Travis-Scott.webp'),
      ('SNKRS-006', 'Nike', 'Air Jordan 1 Retro High Off-White', 'NRG White', 2370, 'Air-Jordan-1-Retro-High-Off-White-The-Ten-NRJ.webp'),
      ('SNKRS-007', 'Nike', 'Air Jordan 1 Retro High', 'UNC Patent', 730, 'Air-Jordan-1-Retro-High-UNC-Patent.webp'),
      ('SNKRS-008', 'Nike', 'Air Jordan 1 Retro High', 'Fearless OG', 460, 'Air-Jordan-1-Retro-High-OG-Fearless.webp');

