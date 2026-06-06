from flask import Blueprint, render_template, request, redirect, url_for, Response
from flask_login import login_required, current_user
from werkzeug.wrappers import Response as WerkzeugResponse

from models.ledger import insert_ledger, list_ledgers, get_ledger, delete_ledger, get_category_total
from models.posting import Posting, list_postings, insert_posting, delete_posting, update_posting
from models.categories import Category, CategoryType, list_categories, insert_category, update_category, delete_category, list_category_types
from models.budget import BudgetEntry, list_budget_entries, list_budget_years, get_budget_entry, update_budget_entry, add_ledger_year

bp = Blueprint('ledger', __name__, url_prefix='/ledgers')

@bp.route('', methods=['GET', 'POST'])
@login_required
def ledgers() -> str | WerkzeugResponse:
    if request.method == 'POST':

        if request.form["action"] and request.form["action"] == "delete":
            delete_ledger(request.form["lid"])
            
        elif request.form["action"] and request.form["action"] == "create":
            ledger_name: str = request.form['ledger_name']
            lid: int | None = insert_ledger(
                user_id= current_user.id, 
                ledger_name=ledger_name)
        return redirect(url_for('ledger.ledgers'))

    ledgers = list_ledgers(user_id=current_user.id)
    return render_template('pages/ledgers.html', ledgers=ledgers)

@bp.route('/<int:LedgerId>')
@login_required
def ledger(LedgerId: int) -> str | tuple[str, int]:

    ledger = get_ledger(LedgerId)
    postings = list_postings(LedgerId)
    categories = list_categories(LedgerId)
    category_total = get_category_total(LedgerId)
    
    if ledger is None:
        return "Ledger not found", 404
    return render_template('pages/ledger.html', ledger=ledger, postings=postings, categories=categories, categoryTotals = category_total)

@bp.route('/<int:LedgerId>/postings', methods=['GET', 'POST'])
@login_required
def postings(LedgerId: int) -> str | tuple[str, int] | WerkzeugResponse:
    ledger = get_ledger(LedgerId)
    if request.method == "POST":
        action: str = request.form["action"]

        if action == "create_posting":
            insert_posting(
                lid=request.form["lid"],
                cid=request.form["cid"],
                amount=request.form["amount"],
                description=request.form["description"],
                posting_date=request.form["posting_date"]
            )
        elif action == "delete_posting":
            delete_posting(pid=int(request.form["pid"]))

        elif action == "update_posting":
            update_posting(
                pid=int(request.form["pid"]),
                cid=int(request.form["cid"]),
                amount=float(request.form["amount"]),
                description=request.form["description"]
            )

    if ledger is None:
        return "Ledger not found", 404
    
    categories: list[Category] = list_categories(LedgerId)
    postings: list[Posting] = list_postings(LedgerId)
    return render_template('pages/postings.html', ledger=ledger, postings=postings, categories=categories)

@bp.route('/<int:LedgerId>/budget', methods=['GET', 'POST'])
@login_required
def budget(LedgerId: int) -> str | tuple[str, int]:
    ledger = get_ledger(LedgerId)

    if ledger is None:
        return "Ledger not found", 404
    
    categories: list[Category] = list_categories(LedgerId)
    if categories is None:
        return "Categories not found", 404
    budget: list[BudgetEntry] | None = list_budget_entries(LedgerId)

    if budget is None:
        return "budget not found", 404
    budget_years = list_budget_years(LedgerId)
    if budget_years is None:
        return "budget_years not found", 404

    if request.method == "POST" and request.form["action"] == "add-year":
        year: str | None = request.form.get("year")
        if not year:
            return "Year not found", 404

        add_ledger_year(LedgerId, year)

    return render_template('pages/budget.html', ledger=ledger, budget=budget, budget_years=budget_years, categories=categories)

@bp.route('/<int:LedgerId>/budget/save', methods=['POST'])
@login_required
def save_budget(LedgerId: int) -> tuple[dict, int]:
    ledger = get_ledger(LedgerId)

    if ledger is None:
        return {"error": "Ledger not found"}, 404

    entries: list[dict] | None = request.get_json()

    if not entries:
        return {"error": "No entries supplied"}, 400
    
    updated_count: int = 0

    for entry in entries:
        amount: float = entry["amount"]
        bid: int = entry["bid"]

        budget_entry: BudgetEntry | None = get_budget_entry(bid)

        print(budget_entry.amount)
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

@bp.route('/<int:LedgerId>/budget/add_year', methods=['POST'])
@login_required
def add_year(LedgerId: int) -> str | tuple[str, int] | tuple[dict, int]:
    ledger = get_ledger(LedgerId)
    if ledger is None:
        return {"error": "Ledger not found"}, 404
    
    categories: list[Category] = list_categories(LedgerId)
    if categories is None:
        return "Categories not found", 404

    budget: list[BudgetEntry] | None = list_budget_entries(LedgerId)
    if budget is None:
        return "budget not found", 404
    
    budget_years = list_budget_years(LedgerId)
    if budget_years is None:
        return "budget_years not found", 404
    # print(budget_years)

    return render_template('pages/budget.html', ledger=ledger, budget=budget, budget_years=budget_years, categories=categories)

@bp.route('/<int:LedgerId>/categories', methods=['GET', 'POST'])
@login_required
def categories(LedgerId: int) -> str | tuple[str, int] | WerkzeugResponse:
    ledger = get_ledger(LedgerId)

    if ledger is None:
        return "Ledger not found", 404

    if request.method == "POST":
        action: str = request.form["action"]

        if action == "create_category":
            insert_category(
                category_name=request.form["category_name"],
                type_id=int(request.form["type_id"]),
                lid=LedgerId
            )
        elif action == "update_category":
            update_category(
                cid=int(request.form["cid"]),
                category_name=request.form["category_name"],
                type_id=int(request.form["type_id"])
            )
        elif action == "delete_category":
            delete_category(cid=int(request.form["cid"]))

        return redirect(url_for('ledger.categories', LedgerId=LedgerId))

    category_list: list[Category] = list_categories(LedgerId)
    category_types: list[CategoryType] = list_category_types()
    return render_template('pages/categories.html', ledger=ledger, categories=category_list, category_types=category_types)
