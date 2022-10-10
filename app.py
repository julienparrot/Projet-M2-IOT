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
import os
from redis import Redis

from mysql.connector import (connection)

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

cnx = connection.MySQLConnection(
    user='root', password='root', host='mysql', port='3306', database='db')
print("DB connect")

cursor = cnx.cursor()
cursor.execute('SELECT * FROM produit')
produit = cursor.fetchall()
cursor.execute('SELECT * FROM utilisateur')
user = cursor.fetchall()
cnx.close()

@app.route('/')
def defaultPage():
    return redirect(url_for('produit'))

class User:
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
for i in range(len(user)):
    users.append(User(id=user[i][0], username=user[i][1], password=user[i][2], role=user[i][3]))

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
for i in range(len(produit)):
    listProduits.append(
        Produit(id=produit[i][0], code=produit[i][1], marque=produit[i][2], modele=produit[i][3], coloris=produit[i][4], prix=produit[i][5],
                image=produit[i][6]))

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







