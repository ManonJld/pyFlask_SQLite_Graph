from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import database
import os
import datetime

app = Flask (__name__)
bootstrap = Bootstrap(app)
app.secret_key = os.environ['SECRET_KEY'] = 'testkey'
database.init_db()
import models

@app.route ('/', methods=['GET','POST'])
def page_index():
    if request.method == 'POST':
        data = request.form.to_dict()
        if 'value' in data and 'unite' in data and 'date' in data and 'capteur' in data:
            captor = None
            # cherche si un capteur avec ce nom existe déjà
            query_captor = models.Capteur.query.filter(models.Capteur.name == data['capteur']).first()
            # si pas de capteur avec ce nom, il en crée un nouveau dans la table Capteur
            if query_captor is None:
                captor = models.Capteur(data['capteur'])
                database.db_session.add(captor)
                database.db_session.commit()
            # sinon, s'il a trouvé un capteur correspondant, il prend ces données
            else:
                captor = query_captor
            t = models.Donnee(data['value'], data['unite'], datetime.datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S.%f'), captor.id)
            print(t)
            database.db_session.add(t)
            database.db_session.commit()
        else:
            return 'Bad value'
    capteurs = models.Capteur.query.all()
    return render_template('index.html', capteurs=capteurs)

@app.route ('/capteur')
def page_capteur_none():

    return render_template('capteurNone.html')

@app.route ('/capteur/<idcapteur>', methods=['GET', 'POST'])
def page_capteur(idcapteur):
    capteurs = models.Capteur.query.filter(models.Capteur.id == idcapteur).all()
    donneestable = models.Donnee.query.filter(models.Donnee.capteurid == idcapteur)
    return render_template('capteur.html', idcapteur=idcapteur, capteurs=capteurs, donneestable=donneestable)


@app.route ('/graphique')
def page_graphique_none():
    return render_template('graphiqueNone.html')

@app.route ('/graphique/<idcapteur>', methods=['GET', 'POST'])
def page_graphique(idcapteur):
    capteurs = models.Capteur.query.filter(models.Capteur.id == idcapteur).all()
    donneesgraph = models.Donnee.query.filter(models.Donnee.capteurid == idcapteur).order_by(models.Donnee.id.desc()).limit(10)
    listdata = []
    for donnee in donneesgraph:
        listdata.append(donnee.value)
    return render_template('graphique.html', idcapteur=idcapteur, capteurs=capteurs, donnees=donneesgraph, listdata=listdata)