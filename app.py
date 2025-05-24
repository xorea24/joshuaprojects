from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# Gumagawa ng Flask app
app = Flask(__name__)

# Tamang URI at configuration key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize ang database
db = SQLAlchemy(app)

# Define ng model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

# Gumamit ng application context para gumawa ng tables
with app.app_context():
    db.create_all()

# Route para sa home
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        note_content = request.form.get('note')
        if note_content:
            new_note = Note(content=note_content)
            db.session.add(new_note)
            db.session.commit()
        return redirect('/')

    all_notes = Note.query.all()
    return render_template('index.html', notes=all_notes)

# Route para sa pag-delete
@app.route('/delete/<int:id>', methods=['POST'])
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return redirect('/')

# Route para sa pag-edit
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_note(id):
    note = Note.query.get_or_404(id)
    if request.method == 'POST':
        new_content = request.form.get('content')
        if new_content:
            note.content = new_content
            db.session.commit()
        return redirect('/')
    return render_template('edit.html', note=note)

# Run ang Flask app
if __name__ == '__main__':
    app.run(debug=True)
