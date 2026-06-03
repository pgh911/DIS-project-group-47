from flask import Blueprint, render_template, request, redirect, url_for
from models.ledger import insert_ledger, list_ledgers

bp = Blueprint('ledger', __name__, url_prefix='/ledgers')

@bp.route('', methods=['GET', 'POST'])
def categories():
    if request.method == 'POST':
        ledger_name = request.form['ledger_name']
        insert_ledger(ledger_name)
        return redirect(url_for('ledger.categories'))

    ledgers = list_ledgers()
    return render_template('ledger.html', ledgers=ledgers)