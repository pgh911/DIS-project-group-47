from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from models.ledger import insert_ledger, list_ledgers, get_ledger, delete_ledger
from models.posting import Posting, list_postings
from database import db_connection

bp = Blueprint('ledger', __name__, url_prefix='/ledgers')

@bp.route('', methods=['GET', 'POST'])
@login_required
def ledgers():
    if request.method == 'POST':

        if request.form["action"] and request.form["action"] == "delete":
            delete_ledger(request.form["lid"])
            
        elif request.form["action"] and request.form["action"] == "create":
            ledger_name = request.form['ledger_name']
            lid = insert_ledger(
                user_id= current_user.id, 
                ledger_name=ledger_name)
        return redirect(url_for('ledger.ledgers'))

    ledgers = list_ledgers(user_id= current_user.id)
    return render_template('pages/ledgers.html', ledgers=ledgers)

@bp.route('/<int:LedgerId>')
@login_required
def ledger(LedgerId):
    conn = db_connection()

    ledger = get_ledger(LedgerId)
    postings = list_postings(LedgerId)
    
    if ledger is None:
        return "Ledger not found", 404
    conn.close()

    return render_template('pages/ledger.html', ledger=ledger, postings=postings)

@bp.route('/<int:LedgerId>/postings')
@login_required
def postings(LedgerId):
    conn = db_connection()

    ledger = get_ledger(LedgerId)
    postings = list_postings(LedgerId)
    
    if ledger is None:
        return "Ledger not found", 404
    conn.close()

    return render_template('pages/postings.html', ledger=ledger, postings=postings)