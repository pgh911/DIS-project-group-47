from flask import Blueprint, render_template, request, redirect, url_for, Response
from flask_login import login_required, current_user
from werkzeug.wrappers import Response as WerkzeugResponse

from models.ledger import insert_ledger, list_ledgers, get_ledger, delete_ledger, get_summed_totals,get_summed_totals_fullyear, SummedTotal, Ledger
from models.posting import Posting, list_postings, insert_posting, delete_posting, update_posting
from models.categories import Category, CategoryType, list_categories, insert_category, update_category, delete_category, list_category_types
from models.budget import BudgetEntry, list_budget_entries, list_budget_years, get_budget_entry, update_budget_entry, add_ledger_year, LedgerYear, list_budget_entries_detailed, list_budget_entries_detailed_fullyear

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

@bp.route('/<int:LedgerId>', methods=["GET", "POST"])
@login_required
def ledger(LedgerId: int) -> str | tuple[str, int]:

    ledger:list[Ledger] = get_ledger(LedgerId)
    ledger_years:list[LedgerYear] = list_budget_years(LedgerId)
    idList = [0,0,0,0,0,0]

    if not ledger_years:
        if ledger is None:
            return "Ledger not found", 404
        return render_template('pages/ledger.html', ledger=ledger, budget_entries=[], summed_totals=[], ledger_years=[],idList = idList)

    budget_entries:list[BudgetEntry] = list_budget_entries_detailed_fullyear(LedgerId, ledger_years[0].ledger_year)
    summed_totals:list[SummedTotal] = get_summed_totals_fullyear(LedgerId, ledger_years[0].ledger_year)

    if request.form.get("action") and request.form.get("action") == "update-timeframe":
        if request.form["month"] == "all":
            summed_totals = get_summed_totals_fullyear(LedgerId, request.form["year"])
            budget_entries:list[BudgetEntry] = list_budget_entries_detailed_fullyear(LedgerId, request.form["year"])

        elif request.form["month"]:
            summed_totals = get_summed_totals(LedgerId, request.form["year"], request.form["month"])
            budget_entries:list[BudgetEntry] = list_budget_entries_detailed(LedgerId, request.form["year"], request.form["month"])

    percentList = []
    idOne= 0
    idTwo = 0
    idThree = 0
    idBOne = 0
    idBTwo = 0
    idBThree = 0
    for budget in budget_entries:
        percentage = 0
        sumTotal = 0
        if(budget.type_id == 1):
            idBOne = idBOne + budget.amount
        elif (budget.type_id == 2):
            idBTwo = idBTwo + budget.amount
        elif (budget.type_id == 3) :
            idBThree = idBThree + budget.amount
        for total in summed_totals:
            if (
                budget.category_name == total.category_name
                and budget.type_name == total.type_name
            ):
                if(budget.type_id == 1):
                    idOne = idOne + total.total_amount
                elif (budget.type_id == 2):
                    idTwo = idTwo + total.total_amount
                elif (budget.type_id == 3) :
                    idThree = idThree + total.total_amount

                if budget.amount > 0:
                    percentage = round(
                        (abs(total.total_amount / budget.amount)) * 100,
                        2)
                sumTotal = total.total_amount
                break
        percentList.append({
            "category_name": budget.category_name,
            "budget": budget.amount,
            "totalSum": sumTotal,
            "percentage": percentage,
            "budgetID" : budget.type_id
        })
    idTotalList = [idOne,idTwo,idThree,idBOne,idBTwo,idBThree]
    return render_template('pages/ledger.html', 
                           ledger=ledger, 
                           summed_totals=summed_totals,
                           ledger_years=ledger_years,
                           budget_entries=budget_entries,
                           percentages = percentList,
                           idList = idTotalList)

@bp.route('/<int:LedgerId>/postings', methods=['GET', 'POST'])
@login_required
def postings(LedgerId: int) -> str | tuple[str, int] | WerkzeugResponse:
    ledger = get_ledger(LedgerId)
    if request.method == "POST":
        action: str = request.form["action"]

        if action == "create_posting":
            try:
                insert_posting(
                    lid=request.form["lid"],
                    cid=request.form["cid"],
                    amount=request.form["amount"],
                    description=request.form["description"],
                    posting_date=request.form["posting_date"]
                )
            except ValueError as e:
                categories: list[Category] = list_categories(LedgerId)
                postings: list[Posting] = list_postings(LedgerId)
                return render_template('pages/postings.html', ledger=ledger, postings=postings, categories=categories, error=str(e))
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
    type_id = request.args.get("type_name", "all")

    categories = list_categories(LedgerId)
    postings = list_postings(LedgerId)

    if type_id != "all":
        filtered_postings = []
        for i in postings:
            if i.type_name == type_id:
                filtered_postings.append(i)

        postings = filtered_postings
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
    
    if request.method == "POST" and request.form["action"] == "create-category":
        insert_category(request.form["category_name"], request.form["type_id"], LedgerId)

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
