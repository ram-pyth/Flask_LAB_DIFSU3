from flask import Flask, render_template, request, redirect, url_for
from config import Config
from models import db, Projektas, AtliktasDarbas

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    """
    Visų eilučių rodinys(list view)
    :return:
    """
    search_text = request.args.get('paieskoslaukelis')
    if search_text:
        projects = Projektas.query.filter(Projektas.pavadinimas.ilike(search_text + '%'))
    else:
        projects = Projektas.query
    return render_template('index.html', projects=projects)


@app.route('/projektai/<int:projektas_id>', methods=['GET', 'POST'])
def one_project(projektas_id):
    """
    Vienos eilutės rodinys(detail view)
    projekto detalizacija, kombinuota su
    atliktų darbų eilutėmis, bei atlikto
    darbo įvedimo forma
    :param projektas_id:
    :return:
    """
    project = Projektas.query.get(projektas_id)
    if not project:
        return "bloga nuoroda, projektas neegzistuoja"

    if request.method == 'POST':
        darbas = request.form.get('darbaslaukelis')
        samata = request.form.get('samatalaukelis')
        imone = request.form.get('imonelaukelis')
        if darbas and samata and imone:
            atliktas_darbas = AtliktasDarbas(darbas, samata, imone)
            atliktas_darbas.projektas = project
            db.session.add(atliktas_darbas)
            db.session.commit()
            return redirect(url_for('one_project', projektas_id=project.id))
    return render_template('vienas_projektas.html', project=project)

# C - create

@app.route('/projektai/naujas', methods=['GET', 'POST'])
def new_project():
    """
    Vienos eilutės kūrimo rodinys(create view)
    :return:
    """
    if request.method == 'GET':
        return render_template('naujo_projekto_ivedimas.html')
    elif request.method == 'POST':
        pavadinimas = request.form.get('pavadinimolaukelis')
        kaina = request.form.get('kainoslaukelis')
        if pavadinimas and kaina:
            project = Projektas(pavadinimas, kaina)
            db.session.add(project)
            db.session.commit()
    return redirect(url_for('home'))  # home - funkcijos pavadinimas(maršrutas "/")


# D - delete

@app.route('/projektai/trinti/<int:projektas_id>', methods=['POST'])
def delete_project(projektas_id):
    """
    Vienos eilutės trynimo rodinys(delete view)
    :param projektas_id:
    :return:
    """
    project = Projektas.query.get(projektas_id)
    if project:
        db.session.delete(project)
        db.session.commit()
    return redirect(url_for('home'))


# U - update

@app.route('/projektai/redaguoti/<int:projektas_id>', methods=['GET', 'POST'])
def edit_project(projektas_id):
    """
    Vienos eilutės redagavimo rodinys(update view)
    :param projektas_id:
    :return:
    """
    project = Projektas.query.get(projektas_id)
    if not project:
        return "projektas neegzistuoja"

    if request.method == 'GET':
        return render_template('projekto_update.html', project=project)

    elif request.method == 'POST':
        pavadinimas = request.form.get('pavadinimolaukelis')
        kaina = request.form.get('kainoslaukelis')
        if pavadinimas and kaina:
            project.pavadinimas = pavadinimas
            project.kaina = kaina
            db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
    # app.run(host="0.0.0.0", port=80, debug=True) # cloude
