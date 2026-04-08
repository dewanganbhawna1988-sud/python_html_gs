<<<<<<< HEAD
from flask import Blueprint, render_template, request, redirect, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials

requirement_only_item_depndency_bp = Blueprint('requirement_only_item_depndency_bp', __name__)

# -------------------------
# GOOGLE SHEET CONNECTION
# -------------------------
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "pythonhtmlformgs-230b6b2a1e42.json", scope)

client = gspread.authorize(creds)

# MAIN SHEET
sheet = client.open("REQUIREMENT").sheet1

# MASTER SHEET
master_sheet = client.open("ITEM_MASTER").sheet1


# -------------------------
# GET NEXT ID
# -------------------------
def get_next_id():
    data = sheet.get_all_values()
    return len(data)


# -------------------------
# MAIN ROUTE
# -------------------------
@requirement_only_item_depndency_bp.route('/', methods=['GET', 'POST'])
def requirement_only_item_depndency():

    error = None

    if request.method == 'POST':

        id = get_next_id()

        branch = request.form.get('branch', '').strip()
        cname = request.form.get('cname', '').strip()
        contact = request.form.get('contact', '').strip()

        items = request.form.getlist('item[]')
        brands = request.form.getlist('brand[]')
        designs = request.form.getlist('design[]')
        types = request.form.getlist('type[]')        # keep name same for HTML
        categories = request.form.getlist('category[]')
        patterns = request.form.getlist('pattern[]')
        sizes = request.form.getlist('size[]')
        qtys = request.form.getlist('qty[]')

        # -------------------------
        # VALIDATION
        # -------------------------
        if not branch or not cname or not contact:
            error = "All fields are required"

        elif not contact.isdigit() or len(contact) != 10:
            error = "Contact must be 10 digit number"

        else:
            for qty in qtys:
                if qty and not qty.isdigit():
                    error = "Qty must be numeric"
                    break

        # -------------------------
        # SAVE MULTIPLE ROWS
        # -------------------------
        if not error:

            for i in range(len(items)):

                item = items[i].strip() if i < len(items) else ""
                brand = brands[i].strip() if i < len(brands) else ""
                design = designs[i].strip() if i < len(designs) else ""
                type_ = types[i].strip() if i < len(types) else ""
                category = categories[i].strip() if i < len(categories) else ""
                pattern = patterns[i].strip() if i < len(patterns) else ""
                size = sizes[i].strip() if i < len(sizes) else ""
                qty = qtys[i].strip() if i < len(qtys) else ""

                # skip empty rows
                if not item or not qty:
                    continue

                sheet.append_row([
                    id,
                    branch,
                    cname,
                    contact,
                    item,
                    brand,
                    design,
                    type_,
                    category,
                    pattern,
                    size,
                    qty
                ])

            return redirect('/requirement_only_item_depndency')

    # -------------------------
    # FETCH DATA
    # -------------------------
    data = sheet.get_all_values()
    rows = data[1:]

    return render_template(
        'requirement_only_item_depndency.html',
        id=get_next_id(),
        data=rows,
        error=error
    )


# -------------------------
# 🔥 DEPENDENT DROPDOWN API
# -------------------------
@requirement_only_item_depndency_bp.route('/get-items')
def get_items():

    data = master_sheet.get_all_records()
    result = {}

    for row in data:

        item = str(row.get('Item') or '').strip()
        brand = str(row.get('Brand') or '').strip()
        design = str(row.get('Design') or '').strip()
        type_ = str(row.get('Type') or '').strip()
        category = str(row.get('Category') or '').strip()
        pattern = str(row.get('Pattern') or '').strip()
        size = str(row.get('Size') or '').strip()

        if not item:
            continue

        if item not in result:
            result[item] = {
                "brand": set(),
                "design": set(),
                "type": set(),
                "category": set(),
                "pattern": set(),
                "size": set()
            }

        if brand: result[item]["brand"].add(brand)
        if design: result[item]["design"].add(design)
        if type_: result[item]["type"].add(type_)
        if category: result[item]["category"].add(category)
        if pattern: result[item]["pattern"].add(pattern)
        if size: result[item]["size"].add(size)

    # set → list
    for item in result:
        for key in result[item]:
            result[item][key] = list(result[item][key])

    return jsonify(result)
 
=======
from flask import Blueprint, render_template, request, redirect, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials

requirement_only_item_depndency_bp = Blueprint('requirement_only_item_depndency_bp', __name__)

# -------------------------
# GOOGLE SHEET CONNECTION
# -------------------------
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "pythonhtmlformgs-230b6b2a1e42.json", scope)

client = gspread.authorize(creds)

# MAIN SHEET
sheet = client.open("REQUIREMENT").sheet1

# MASTER SHEET
master_sheet = client.open("ITEM_MASTER").sheet1


# -------------------------
# GET NEXT ID
# -------------------------
def get_next_id():
    data = sheet.get_all_values()
    return len(data)


# -------------------------
# MAIN ROUTE
# -------------------------
@requirement_only_item_depndency_bp.route('/', methods=['GET', 'POST'])
def requirement_only_item_depndency():

    error = None

    if request.method == 'POST':

        id = get_next_id()

        branch = request.form.get('branch', '').strip()
        cname = request.form.get('cname', '').strip()
        contact = request.form.get('contact', '').strip()

        items = request.form.getlist('item[]')
        brands = request.form.getlist('brand[]')
        designs = request.form.getlist('design[]')
        types = request.form.getlist('type[]')        # keep name same for HTML
        categories = request.form.getlist('category[]')
        patterns = request.form.getlist('pattern[]')
        sizes = request.form.getlist('size[]')
        qtys = request.form.getlist('qty[]')

        # -------------------------
        # VALIDATION
        # -------------------------
        if not branch or not cname or not contact:
            error = "All fields are required"

        elif not contact.isdigit() or len(contact) != 10:
            error = "Contact must be 10 digit number"

        else:
            for qty in qtys:
                if qty and not qty.isdigit():
                    error = "Qty must be numeric"
                    break

        # -------------------------
        # SAVE MULTIPLE ROWS
        # -------------------------
        if not error:

            for i in range(len(items)):

                item = items[i].strip() if i < len(items) else ""
                brand = brands[i].strip() if i < len(brands) else ""
                design = designs[i].strip() if i < len(designs) else ""
                type_ = types[i].strip() if i < len(types) else ""
                category = categories[i].strip() if i < len(categories) else ""
                pattern = patterns[i].strip() if i < len(patterns) else ""
                size = sizes[i].strip() if i < len(sizes) else ""
                qty = qtys[i].strip() if i < len(qtys) else ""

                # skip empty rows
                if not item or not qty:
                    continue

                sheet.append_row([
                    id,
                    branch,
                    cname,
                    contact,
                    item,
                    brand,
                    design,
                    type_,
                    category,
                    pattern,
                    size,
                    qty
                ])

            return redirect('/requirement_only_item_depndency')

    # -------------------------
    # FETCH DATA
    # -------------------------
    data = sheet.get_all_values()
    rows = data[1:]

    return render_template(
        'requirement_only_item_depndency.html',
        id=get_next_id(),
        data=rows,
        error=error
    )


# -------------------------
# 🔥 DEPENDENT DROPDOWN API
# -------------------------
@requirement_only_item_depndency_bp.route('/get-items')
def get_items():

    data = master_sheet.get_all_records()
    result = {}

    for row in data:

        item = str(row.get('Item') or '').strip()
        brand = str(row.get('Brand') or '').strip()
        design = str(row.get('Design') or '').strip()
        type_ = str(row.get('Type') or '').strip()
        category = str(row.get('Category') or '').strip()
        pattern = str(row.get('Pattern') or '').strip()
        size = str(row.get('Size') or '').strip()

        if not item:
            continue

        if item not in result:
            result[item] = {
                "brand": set(),
                "design": set(),
                "type": set(),
                "category": set(),
                "pattern": set(),
                "size": set()
            }

        if brand: result[item]["brand"].add(brand)
        if design: result[item]["design"].add(design)
        if type_: result[item]["type"].add(type_)
        if category: result[item]["category"].add(category)
        if pattern: result[item]["pattern"].add(pattern)
        if size: result[item]["size"].add(size)

    # set → list
    for item in result:
        for key in result[item]:
            result[item][key] = list(result[item][key])

    return jsonify(result)
 
>>>>>>> 4947770b7ba4b0344e6954f92e5b89d402830ddf
