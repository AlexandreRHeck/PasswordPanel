from flask import Flask, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO, emit, join_room
from models import db, Password, Clinic, Attendant
from datetime import datetime, timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@db:5432/mydatabase'
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

def get_today_passwords():
    """Retorna as senhas geradas hoje."""
    today = datetime.now(timezone.utc).date()
    return Password.query.filter_by(date=today).order_by(Password.number).all()

def get_last_password_number(clinic_id):
    """Retorna o número da última senha gerada para uma clínica, independente da data."""
    last_password = Password.query.filter_by(clinic_id=clinic_id).order_by(Password.id.desc()).first()
    return last_password.number if last_password else 0


@app.route('/admin/attendants', methods=['GET', 'POST'])
def manage_attendants():
    if request.method == 'POST':
        # Captura os dados do formulário
        attendant_name = request.form.get('name')
        clinic_id = request.form.get('clinic_id')

        # Cria e salva o novo atendente
        new_attendant = Attendant(name=attendant_name, clinic_id=clinic_id)
        db.session.add(new_attendant)
        db.session.commit()

        flash(f"Atendente {attendant_name} foi criado com sucesso!", "success")
        return redirect(url_for('manage_attendants'))

    attendants = Attendant.query.all()  # Pega todos os atendentes para exibir na página
    clinics = Clinic.query.all()  # Pega todas as clínicas para o formulário
    return render_template('admin_attendants.html', attendants=attendants, clinics=clinics)


@app.route('/admin/clinics', methods=['GET', 'POST'])
def manage_clinics():
    if request.method == 'POST':
        # Captura os dados do formulário
        clinic_name = request.form.get('name')
        clinic_location = request.form.get('location')

        # Cria e salva a nova clínica
        new_clinic = Clinic(name=clinic_name, location=clinic_location)
        db.session.add(new_clinic)
        db.session.commit()

        flash(f"Clínica {clinic_name} foi criada com sucesso!", "success")
        return redirect(url_for('manage_clinics'))

    clinics = Clinic.query.all()  # Pega todas as clínicas para exibir na página
    return render_template('admin_clinics.html', clinics=clinics)


@app.route('/clinica/<int:clinic_id>/panel')
def panel(clinic_id):
    """Renderiza o painel da clínica."""
    clinic = Clinic.query.get_or_404(clinic_id)
    return render_template('panel.html', clinic=clinic)

@app.route('/clinica/<int:clinic_id>/attendant')
def attendant(clinic_id):
    """Renderiza o painel do atendente."""
    clinic = Clinic.query.get(clinic_id)
    if not clinic:
        return "Clínica não encontrada", 404
    return render_template('attendant.html', clinic=clinic)

@socketio.on('generate_password')
def generate_password(data):
    """Gera uma nova senha, emite-a para a sala da clínica e redefine se o número da senha atingir 99."""
    clinic_id = data.get('clinic_id')
    guiche = data.get('guiche')

    if not clinic_id or not guiche:
        return

    # Obtém o número da última senha gerada hoje para a clínica específica
    today = datetime.now(timezone.utc).date()
    last_password_number = get_last_password_number(clinic_id)

    # Verifique se o último número de senha é 99 ou mais
    if last_password_number >= 99:
        new_password = 1  # Reinicia para 1
    else:
        new_password = last_password_number + 1

    # Salva a nova senha no banco de dados
    password = Password(number=new_password, guiche=guiche, date=today, clinic_id=clinic_id)
    db.session.add(password)
    db.session.commit()

    # Emitir a nova senha para a sala da clínica
    emit('new_password', {'password': new_password, 'guiche': guiche}, broadcast=True, room=f"clinic_{clinic_id}")
    print(f"Emitted new password {new_password} for clinic {clinic_id}")


@socketio.on('join')
def handle_join(data):
    """Cliente entra na sala da clínica para receber atualizações."""
    clinic_id = data.get('clinic_id')
    if clinic_id:
        room = f"clinic_{clinic_id}"
        join_room(room)
        print(f"Painel conectado à sala {room}")

if __name__ == '__main__':
    with app.app_context():
        print("CRIANDO TABELAS")
        db.create_all()
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
