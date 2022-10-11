from flask import (
    Flask,
    g,
    redirect,
    render_template,
    app,
    request,
    session,
    url_for
)
import sqlite3
import os
from redis import Redis

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

@app.route('/')
def defaultPage():
    return redirect(url_for('produit'))

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='julien', password='password'))

class Produit:
    def __init__(self, id, code, marque, modele, coloris, prix, image):
        self.id = id
        self.code = code
        self.marque = marque
        self.modele = modele
        self.coloris = coloris
        self.prix = prix
        self.image = image

    def __repr__(self):
        return f'<Produit: {self.code}>'

listProduits = []
listProduits.append(
    Produit(id=1, code='SNKRS-001', marque='Nike', modele='Vaporwaffle Sacai', coloris='Black White', prix=570,
            image='Nike-Sacai-Vaporwaffle-black-white.png'))
listProduits.append(
    Produit(id=2, code='SNKRS-002', marque='Nike', modele='Vaporwaffle Sacai', coloris='Sport Fuchsia Game Royal',
            prix=590, image='Nike-Sacai-VaporWaffle-Game-Royal-Fuchsia.png'))
listProduits.append(
    Produit(id=3, code='SNKRS-003', marque='Nike', modele='Vaporwaffle Sacai', coloris='Tour Yellow Stadium Green',
            prix=490, image='Nike-Sacai-VaporWaffle-Tour-Yellow-Stadium-Green.png'))
listProduits.append(
    Produit(id=4, code='SNKRS-004', marque='Nike', modele='Vaporwaffle Sacai', coloris='Villain Red Neptune Green',
            prix=510, image='Nike-Sacai-Vaporwaffle-Villain-Red-Neptune-Green.png'))

listProduits.append(Produit(id=5, code='SNKRS-005', marque='Nike', modele='Air Jordan 1 Retro High Travis Scott',
                            coloris='Cactus Jack', prix=1520, image='Air-Jordan-1-Cactus-Jack-Travis-Scott.webp'))
listProduits.append(
    Produit(id=6, code='SNKRS-006', marque='Nike', modele='Air Jordan 1 Retro High Off-White', coloris='NRG White',
            prix=2370, image='Air-Jordan-1-Retro-High-Off-White-The-Ten-NRJ.webp'))
listProduits.append(
    Produit(id=7, code='SNKRS-007', marque='Nike', modele='Air Jordan 1 Retro High', coloris='UNC Patent', prix=730,
            image='Air-Jordan-1-Retro-High-UNC-Patent.webp'))
listProduits.append(
    Produit(id=8, code='SNKRS-008', marque='Nike', modele='Air Jordan 1 Retro High', coloris='Fearless OG',
            prix=460, image='Air-Jordan-1-Retro-High-OG-Fearless.webp'))
listProduits.append(
    Produit(id=8, code='SNKRS-009', marque='Moi', modele='Cest moi', coloris='moi',
            prix=10000000000, image='moi.png'))

listPanier = []

app.secret_key = 'somesecretkey'

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user


@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        session.pop('user_id', None)
        result = request.form
        username = result['username']
        password = result['password']

        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('produit'))

        return redirect(url_for('connexion'))

    return render_template("view_connexion.html")

@app.route('/deconnexion')
def deconnexion():
    session.clear()
    listPanier.clear()
    return redirect(url_for('connexion'))

@app.route('/produit')
def produit():
    if not g.user:
        return redirect(url_for('connexion'))

    return render_template("view_produit.html", listProduits=listProduits, listPanier=listPanier)

@app.route('/addPanier', methods=['GET', 'POST'])
def addPanier():
    if not g.user:
        return redirect(url_for('connexion'))

    if request.method == 'POST':
        result = request.form
        unProduit = result['produitCode']
        leProduit = [x for x in listProduits if x.code == unProduit][0]
        listPanier.append(leProduit)
        return render_template("view_panier.html", listPanier=listPanier)

    return render_template("view_panier.html", listPanier=listPanier)

@app.route('/delPanier', methods=['GET', 'POST'])
def delPanier():
    if not g.user:
        return redirect(url_for('connexion'))

    if request.method == 'POST':
        result = request.form
        unProduit = result['produitCode']
        leProduit = [x for x in listProduits if x.code == unProduit][0]
        listPanier.remove(leProduit)
        return render_template("view_panier.html", listPanier=listPanier)

    return render_template("view_panier.html", listPanier=listPanier)


@app.route('/panier')
def panier():
    if not g.user:
        return redirect(url_for('connexion'))
    return render_template("view_panier.html", listPanier=listPanier)

@app.route('/contact')
def contact():
    return render_template("contact.html")

if __name__ == "__main__":  
    app.run("0.0.0.0", debug=False)







