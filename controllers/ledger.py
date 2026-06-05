from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from models.ledger import insert_ledger, list_ledgers, get_ledger, delete_ledger, get_category_total
from models.posting import Posting, list_postings, insert_posting
from models.categories import Category, CategoryType, list_categories
from models.budget import BudgetEntry, list_budget_entries, list_budget_years, get_budget_entry, update_budget_entry

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

    ledgers = ledgers = list_ledgers(user_id=current_user.id)
    return render_template('pages/ledgers.html', ledgers=ledgers)

@bp.route('/<int:LedgerId>')
@login_required
def ledger(LedgerId):

    ledger = get_ledger(LedgerId)
    postings = list_postings(LedgerId)
    categories = list_categories(LedgerId)
    category_total = get_category_total()
    
    if ledger is None:
        return "Ledger not found", 404
    return render_template('pages/ledger.html', ledger=ledger, postings=postings, categories=categories, categoryTotals = category_total)

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
    
    categories = list_categories(LedgerId)
    postings = list_postings(LedgerId)
    return render_template('pages/postings.html', ledger=ledger, postings=postings, categories=categories)


@bp.route('/<int:LedgerId>/budget', methods=['GET', 'POST'])
@login_required
def budget(LedgerId):
    ledger = get_ledger(LedgerId)

    if ledger is None:
        return "Ledger not found", 404

    if request.method == "POST":
        action = request.form.get("action")
        year = request.form.get("year", 2026)

        if action == "add_year":
            return redirect(url_for("ledger.budget", LedgerId=LedgerId, year=year))

    categories:list[Category] = list_categories(LedgerId)
    if categories is None:
        return "Categories not found", 404
    budget = list_budget_entries(LedgerId)

    if budget is None:
        return "budget not found", 404
    budget_years = list_budget_years(LedgerId)
    if budget_years is None:
        return "budget_years not found", 404

    return render_template('pages/budget.html', ledger=ledger, budget=budget, budget_years=budget_years, categories=categories)

@bp.route('/<int:LedgerId>/budget/save', methods=['POST'])
@login_required
def save_budget(LedgerId):
    ledger = get_ledger(LedgerId)

    if ledger is None:
        return {"error": "Ledger not found"}, 404

    entries = request.get_json()

    if not entries:
        return {"error": "No entries supplied"}, 400
    
    updated_count = 0

    for entry in entries:
        amount = entry["amount"]
        bid = entry["bid"]

        budget_entry = get_budget_entry(bid)

        if budget_entry.amount != amount:
            updated_count += 1
            print(f"attempting to insert budget entry {bid}")
            update_budget_entry(
                bid=bid,
                amount=amount,
            )

    return {
        "success": True,
        "updated": updated_count
    }, 200