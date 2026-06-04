from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from models.ledger import insert_ledger, list_ledgers, get_ledger, delete_ledger
from models.posting import Posting, list_postings
from models.categories import Category, CategoryType, list_categories
from models.budget import BudgetEntry, list_budget_entries
# from database import db_connection

bp = Blueprint('ledger', __name__, url_prefix='/ledgers')

@bp.route('', methods=['GET', 'POST'])
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

    ledgers = ledgers = list_ledgers(user_id=1)
    return render_template('pages/ledgers.html', ledgers=ledgers)

@bp.route('/<int:LedgerId>')
def ledger(LedgerId):

    ledger = get_ledger(LedgerId)
    postings = list_postings(LedgerId)
    categories = list_categories(LedgerId)
    
    if ledger is None:
        return "Ledger not found", 404
    return render_template('pages/ledger.html', ledger=ledger, postings=postings, categories=categories)

@bp.route('/<int:LedgerId>/postings')
def postings(LedgerId):
    ledger = get_ledger(LedgerId)
    
    if ledger is None:
        return "Ledger not found", 404

    postings = list_postings(LedgerId)
    return render_template('pages/postings.html', ledger=ledger, postings=postings)


@bp.route('/<int:LedgerId>/budget', methods=['GET', 'POST'])
def budget(LedgerId):
    ledger = get_ledger(LedgerId)

    if ledger is None:
        return "Ledger not found", 404

    categories = list_categories(LedgerId)

    months = [
        {"number": 1, "name": "January"},
        {"number": 2, "name": "February"},
        {"number": 3, "name": "March"},
        {"number": 4, "name": "April"},
        {"number": 5, "name": "May"},
        {"number": 6, "name": "June"},
        {"number": 7, "name": "July"},
        {"number": 8, "name": "August"},
        {"number": 9, "name": "September"},
        {"number": 10, "name": "October"},
        {"number": 11, "name": "November"},
        {"number": 12, "name": "December"},
    ]

    if request.method == "POST":
        action = request.form.get("action")
        year = request.form.get("year", 2026)

        if action == "add_year":
            #For DATABASE
            return redirect(url_for("ledger.budget", LedgerId=LedgerId, year=year))

    year = request.args.get("year", 2026)

    return render_template(
        "pages/budget.html",
        ledger=ledger,
        categories=categories,
        months=months,
        year=year
    )