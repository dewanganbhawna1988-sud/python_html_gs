from flask import Blueprint, render_template, request, redirect, session
import gspread
from oauth2client.service_account import ServiceAccountCredentials

rolebasefootfall_bp = Blueprint('rolebasefootfall_bp', __name__)

# Google Sheet connection
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "pythonhtmlformgs-230b6b2a1e42.json", scope)

client = gspread.authorize(creds)
sheet = client.open("FOOTFALL").sheet1


def get_next_id():
    data = sheet.get_all_values()
    return len(data)


@rolebasefootfall_bp.route('/', methods=['GET', 'POST'])
def rolebasefootfall():

    if 'user' not in session:
        return redirect('/')

    user = session['user']

    # 🔥 ROLE FIX
    if user == "admin":
        role = "admin"
    else:
        role = "user"

    error = None

    # =========================
    # ✅ FORM SUBMIT
    # =========================
    if request.method == 'POST':
        id = get_next_id()

        # 🔥 BRANCH FIX (IMPORTANT)
        if role == "admin":
            branch = request.form.get('branch', '').strip().lower()
        else:
            branch = user.lower()

        name = request.form.get('name', '').strip()
        contact = request.form.get('contact', '').strip()
        address = request.form.get('address', '').strip()
        members = request.form.get('members', '').strip()

        # =========================
        # 🔥 VALIDATION
        # =========================
        if not name or not contact or not address or not members:
            error = "All fields are required"

        elif not contact.isdigit():
            error = "Contact must be numeric"

        elif len(contact) != 10:
            error = "Contact must be 10 digits"

        elif not members.isdigit():
            error = "Members must be numeric"

        # =========================
        # ✅ SAVE DATA
        # =========================
        if not error:
            sheet.append_row([id, branch, name, contact, address, members])
            return redirect('/rolebasefootfall')

    # =========================
    # ✅ DATA FETCH
    # =========================
    data = sheet.get_all_values()

    header = data[0]
    rows = data[1:]

    # 🔥 FILTER + BRANCH FIX
    if role == "admin":
        filtered_data = rows
        branch_fixed = ""   # 🔥 IMPORTANT FIX
    else:
        filtered_data = [
            row for row in rows
            if row[1].strip().lower() == user.lower()
        ]
        branch_fixed = user.lower()

    # =========================
    # ✅ FINAL RENDER
    # =========================
    return render_template(
        'rolebasefootfall.html',
        id=get_next_id(),
        data=filtered_data,
        user=user,
        role=role,                 # 🔥 MUST
        branch_fixed=branch_fixed,
        error=error
    )