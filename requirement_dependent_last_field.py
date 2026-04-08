from flask import Blueprint, render_template, request, redirect, jsonify, session, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

requirement_dependent_last_field_bp = Blueprint('requirement_dependent_last_field_bp', __name__)

# GOOGLE SHEET
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "pythonhtmlformgs-230b6b2a1e42.json", scope)

home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/home')
def home():
    if 'user' not in session:
        return redirect('/login')

    return render_template("home.html", user=session['user'])
client = gspread.authorize(creds)

sheet = client.open("REQUIREMENT_DEPENDS_LAST_FIELD").sheet1
master_sheet = client.open("ITEM_MASTER").sheet1


# 🔥 BRANCH PREFIX
BRANCH_PREFIX = {
    "ambikapur": "AMBK",
    "bhilai": "BHL",
    "bilaspur": "BSP",
    "durg": "DR",
    "raipur": "RPR",
    "rajnandgaon": "RJN",
    "rewa": "RW",
    "jabalpur": "JBP",
    "pulgaon1": "PUL1",
    "pulgaon2": "PUL2"
}


# 🔥 HOME
@requirement_dependent_last_field_bp.route('/home')
def home():
    if 'user' not in session:
        return redirect('/')
    return render_template("home.html", user=session['user'])


# 🔥 LOGOUT
@requirement_dependent_last_field_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# 🔥 SUB ID GENERATOR (GLOBAL)
def get_next_sub_id():
    data = sheet.get_all_values()
    if len(data) <= 1:
        return 1
    try:
        return int(data[-1][1]) + 1
    except:
        return 1


# 🔥 BRANCH UID COUNTER
def get_branch_uid(branch):
    data = sheet.get_all_values()

    count = 0
    for row in data[1:]:
        if len(row) > 3 and row[3].strip().lower() == branch.strip().lower():
            count += 1

    return count + 1


# 🔥 UID GENERATE
def generate_uid(branch):
    prefix = BRANCH_PREFIX.get(branch.lower(), branch[:3].upper())
    number = get_branch_uid(branch)
    return f"{prefix}-{str(number).zfill(2)}"


# 🔥 MAIN ROUTE
@requirement_dependent_last_field_bp.route('/', methods=['GET', 'POST'])
def requirement_dependent_last_field():

    if 'user' not in session:
        return redirect('/')

    branch = session['user']
    error = None

    # 🔥 GET के लिए UID + SUB_ID दिखाने के लिए
    uid = generate_uid(branch)
    sub_id = get_next_sub_id()

    if request.method == 'POST':

        timestamp = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        orderpersonname = request.form.get('orderpersonname', '').strip()
        contact = request.form.get('contact', '').strip()

        items = request.form.getlist('item[]')
        brands = request.form.getlist('brand[]')
        designs = request.form.getlist('design[]')
        types = request.form.getlist('type[]')
        categories = request.form.getlist('category[]')
        patterns = request.form.getlist('pattern[]')
        sizes = request.form.getlist('size[]')
        qtys = request.form.getlist('qty[]')

        if not orderpersonname or not contact:
            error = "All fields required"

        elif not contact.isdigit() or len(contact) != 10:
            error = "Invalid contact"

        else:
            for qty in qtys:
                if qty and not qty.isdigit():
                    error = "Qty must be numeric"
                    break

        if not error:

            for i in range(len(items)):

                if not items[i] or not qtys[i]:
                    continue

                # 🔥 हर row के लिए sub_id increment
                sheet.append_row([
    timestamp,
    str(uid),
    str(sub_id),
    str(branch),
    str(orderpersonname),
    str(contact),
    str(items[i]) if items[i] else "",
    str(brands[i]) if brands[i] else "",
    str(designs[i]) if designs[i] else "",
    str(types[i]) if types[i] else "",
    str(categories[i]) if categories[i] else "",
    str(patterns[i]) if patterns[i] else "",
    str(sizes[i]) if sizes[i] else "",
    str(qtys[i]) if qtys[i] else ""
])

                sub_id += 1   # 🔥 IMPORTANT

            return redirect(url_for('requirement_dependent_last_field_bp.requirement_dependent_last_field'))

    # 🔥 FILTER DATA
    data = sheet.get_all_values()

    rows = [
        row for row in data[1:]
        if len(row) > 3 and row[3].strip().lower() == branch.strip().lower()
    ]

    return render_template(
        'requirement_dependent_last_field.html',
        data=rows,
        error=error,
        branch=branch,
        uid=uid,
        sub_id=sub_id
    )


# 🔥 ITEM API
@requirement_dependent_last_field_bp.route('/get-items')
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

        result.setdefault(item, {})
        result[item].setdefault(brand, {})
        result[item][brand].setdefault(design, {})
        result[item][brand][design].setdefault(type_, {})
        result[item][brand][design][type_].setdefault(category, {})
        result[item][brand][design][type_][category].setdefault(pattern, [])

        if size:
            result[item][brand][design][type_][category][pattern].append(size)

    return jsonify(result)