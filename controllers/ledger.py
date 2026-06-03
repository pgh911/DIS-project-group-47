from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from models.ledger import insert_ledger, list_ledgers
from database import db_connection

bp = Blueprint('ledger', __name__, url_prefix='/ledgers')

@bp.route('', methods=['GET', 'POST'])
@login_required
def ledgers():
    if request.method == 'POST':
        ledger_name = request.form['ledger_name']
        insert_ledger(
            user_id= current_user.id, 
            ledger_name=ledger_name)
        return redirect(url_for('ledger.ledgers'))

    ledgers = list_ledgers(user_id= current_user.id)
    return render_template('ledgers.html', ledgers=ledgers)

@bp.route('/<int:LedgerId>')
@login_required
def ledger(LedgerId):
    conn = db_connection()

    ledger = conn.execute(
        "SELECT * FROM ledgers WHERE lid = " + str(LedgerId) + " ORDER BY lid"
    ).fetchone()
    return render_template('pages/ledger.html', ledger=ledger)
