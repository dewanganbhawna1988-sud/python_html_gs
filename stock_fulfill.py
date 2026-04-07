from flask import Blueprint, render_template, request, redirect, session
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

stock_fulfill_bp = Blueprint('stock_fulfill_bp', __name__, url_prefix="/stock_fulfill")

# -----------------------------
# GOOGLE SHEET CONNECT
# -----------------------------
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "pythonhtmlformgs-230b6b2a1e42.json", scope)

client = gspread.authorize(creds)

# SHEETS
req_sheet = client.open("REQUIREMENT_DEPENDS_LAST_FIELD").worksheet("Sheet1")
fulfill_sheet = client.open("STOCK_FULFILL").worksheet("Sheet1")

# 🔥 NEW: ITEM MASTER SHEET
item_master_sheet = client.open("ITEM_MASTER").worksheet("Sheet1")


# -----------------------------
# ✅ STOCK LIST PAGE
# -----------------------------
'''@stock_fulfill_bp.route("/")
def stock_list():

    if "user" not in session:
        return redirect("/")

    user = session["user"].strip().lower()

    # 🔥 REQUIREMENT DATA
    req_data = req_sheet.get_all_values()
    headers = req_data[0]
    rows = req_data[1:]

    # 🔥 FIND COLUMN INDEXES
    def get_col_index(col_name):
        return headers.index(col_name)

    user_col = get_col_index("USER")
    status_col = get_col_index("FULFILL STATUS")

    filtered_data = []

    for row in rows:

        if len(row) > max(user_col, status_col):

            row_user = str(row[user_col]).strip().lower()
            status = str(row[status_col]).strip().lower()

            # ✅ CONDITION
            if row_user == user and (status == "" or status == "pending"):
                filtered_data.append(row)

    # =====================================================
    # 🔥 NEW CODE: HIDE USER & STATUS COLUMN
    # =====================================================

    new_headers = [h for i, h in enumerate(headers) if i not in (user_col, status_col)]

    new_data = []
    for row in filtered_data:
        new_row = [cell for i, cell in enumerate(row) if i not in (user_col, status_col)]
        new_data.append(new_row)

    return render_template(
        "stock_fulfill.html",
        data=new_data,
        headers=new_headers,
        user=session["user"]
    )'''

@stock_fulfill_bp.route("/")
def stock_list():

    if "user" not in session:
        return redirect("/")

    # ✅ USER FIRST
    user = session["user"].strip().lower()

    # ✅ DATA FIRST
    req_data = req_sheet.get_all_values()
    headers = req_data[0]
    rows = req_data[1:]

     # 🔥 FILTER VALUES (GET)
    uid_filter = request.args.get("uid", "All")
    subid_filter = request.args.get("subid", "All")
    branch_filter = request.args.get("branch", "All")
    item_filter = request.args.get("item", "All")

    # ✅ COLUMN INDEX AFTER HEADERS
    def get_col_index(col_name):
        return headers.index(col_name)

    user_col = get_col_index("USER")
    status_col = get_col_index("FULFILL STATUS")

    filtered_data = []

    # ✅ LOOP
    for row in rows:

        if len(row) > max(user_col, status_col):

            row_user = str(row[user_col]).strip().lower()
            status = str(row[status_col]).strip().lower()

            # ✅ BASE CONDITION
            if row_user == user and (status == "" or status == "pending"):

                # ✅ FILTER LOGIC
                if uid_filter and uid_filter != "All" and uid_filter != str(row[1]):
                    continue

                if subid_filter and subid_filter != "All" and subid_filter != str(row[2]):
                    continue

                if branch_filter and branch_filter != "All" and branch_filter != str(row[3]):
                    continue

                if item_filter and item_filter != "All" and item_filter != str(row[6]):
                    continue

                filtered_data.append(row)

        
    # =====================================================
    # 🔥 DROPDOWN VALUES (ALL DATA se, filter se nahi)
    # =====================================================
    uids = sorted(set(row[1] for row in rows if len(row) > 1))
    subids = sorted(set(row[2] for row in rows if len(row) > 2))
    branches = sorted(set(row[3] for row in rows if len(row) > 3))
    items = sorted(set(row[6] for row in rows if len(row) > 6))


    # =====================================================
    # 🔥 NEW CODE: HIDE USER & STATUS COLUMN
    # =====================================================

    new_headers = [h for i, h in enumerate(headers) if i not in (user_col, status_col)]

    new_data = []
    for row in filtered_data:
        new_row = [cell for i, cell in enumerate(row) if i not in (user_col, status_col)]
        new_data.append(new_row)

    return render_template(
        "stock_fulfill.html",
        data=new_data,
        headers=new_headers,
        user=session["user"],
        uids=uids,
        subids=subids,
        branches=branches,
        items=items
    )          


# -----------------------------
# ✅ FULFILL FORM PAGE
# -----------------------------
@stock_fulfill_bp.route("/<uid>/<subid>", methods=["GET", "POST"])
def fulfil(uid, subid):

    if "user" not in session:
        return redirect("/")

    data = req_sheet.get_all_values()
    headers = data[0]
    rows = data[1:]

    selected_row = None
    row_index = None

    for i, row in enumerate(rows):
        if str(row[1]).strip() == str(uid).strip() and str(row[2]).strip() == str(subid).strip():
            selected_row = row
            row_index = i + 2
            break

    if not selected_row:
        return "Data not found"

    # 🔥 ITEM MASTER
    item_data = item_master_sheet.get_all_records()

    items = sorted(set(str(i.get("Item", "")).strip() for i in item_data if i.get("Item")))
    brands = sorted(set(str(i.get("Brand", "")).strip() for i in item_data if i.get("Brand")))
    designs = sorted(set(str(i.get("Design", "")).strip() for i in item_data if i.get("Design")))
    types = sorted(set(str(i.get("Type", "")).strip() for i in item_data if i.get("Type")))
    categories = sorted(set(str(i.get("Category", "")).strip() for i in item_data if i.get("Category")))
    patterns = sorted(set(str(i.get("Pattern", "")).strip() for i in item_data if i.get("Pattern")))
    sizes = sorted(set(str(i.get("Size", "")).strip() for i in item_data if i.get("Size")))

    if request.method == "POST":

        item = request.form.get("item")
        brand = request.form.get("brand")
        design = request.form.get("design")
        type_ = request.form.get("type")
        category = request.form.get("category")
        pattern = request.form.get("pattern")
        size = request.form.get("size")

        final_item = item if item else selected_row[6]
        final_brand = brand if brand else selected_row[7]
        final_design = design if design else selected_row[8]
        final_type = type_ if type_ else selected_row[9]
        final_category = category if category else selected_row[10]
        final_pattern = pattern if pattern else selected_row[11]
        final_size = size if size else selected_row[12]

        qty = request.form.get("qty")

        if not qty:
            return "Qty is required"

        # ✅ SAVE
        # 🔥 TIMESTAMP
        timestamp = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")

        # 🔥 CLEAN DATA
        uid_val = selected_row[1]
        subid_val = selected_row[2]

        # Branch first letter capital
        branch = str(selected_row[3]).strip().title()

        # Other person + contact
        other_person = selected_row[4]
        contact = selected_row[5]   # ⚠️ check index if needed

        # Procurement user
        proc_user = session["user"]

        fulfill_sheet.append_row([
            timestamp,        # ✅ Timestamp added
            uid_val,
            subid_val,
            proc_user,
            branch,
            other_person,
            contact,
            final_item,
            final_brand,
            final_design,
            final_type,
            final_category,
            final_pattern,
            final_size,
            qty
        ])

        # 🔥 STATUS UPDATE
        status_col = headers.index("FULFILL STATUS") + 1
        req_sheet.update_cell(row_index, status_col, "Fulfilled")

        return redirect("/stock_fulfill")   
    

    return render_template(
        "stock_fulfill_form.html",
        uid=uid,
        subid=subid,
        row=selected_row,
        items=items,
        brands=brands,
        designs=designs,
        types=types,
        categories=categories,
        patterns=patterns,
        sizes=sizes
    )


# -----------------------------
# LOGOUT
# -----------------------------
@stock_fulfill_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")