from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from models.ledger import insert_ledger, list_ledgers, get_ledger, delete_ledger
from models.posting import Posting, list_postings, insert_posting
from models.categories import Category, CategoryType, list_categories
from models.budget import BudgetEntry, list_budget_entries, list_budget_years
# from database import db_connection

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

    ledger = get_ledger(LedgerId)
    postings = list_postings(LedgerId)
    categories = list_categories(LedgerId)
    
    if ledger is None:
        return "Ledger not found", 404
    return render_template('pages/ledger.html', ledger=ledger, postings=postings, categories=categories)

@bp.route('/<int:LedgerId>/postings', methods=['GET', 'POST'])
@login_required
def postings(LedgerId):
    ledger = get_ledger(LedgerId)

    if request.method == "POST":
        if request.form["action"] and request.form["action"] == "create_posting":
            insert_posting(
                lid=request.form["lid"],
                cid=request.form["cid"],
                amount=request.form["amount"],
                description=request.form["description"],
                posting_date=request.form["posting_date"]
            )
    
    if ledger is None:
        return "Ledger not found", 404

    postings = list_postings(LedgerId)
    categories = list_categories(LedgerId)
    return render_template('pages/postings.html', ledger=ledger, postings=postings, categories=categories)


@bp.route('/<int:LedgerId>/budget')
@login_required
def budget(LedgerId):
    ledger = get_ledger(LedgerId)
    
    if ledger is None:
        return "Ledger not found", 404

    budget = list_budget_entries(LedgerId)
    budget_years = list_budget_years(LedgerId)
    categories = list_categories(LedgerId)
    return render_template('pages/budget.html', ledger=ledger, budget=budget, budget_years=budget_years, categories=categories)