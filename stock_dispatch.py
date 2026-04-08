from flask import Blueprint, render_template, request, redirect, session
import gspread
from oauth2client.service_account import ServiceAccountCredentials

stock_dispatch_bp = Blueprint('stock_dispatch_bp', __name__)

# -----------------------------
# GOOGLE SHEET
# -----------------------------
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "pythonhtmlformgs-230b6b2a1e42.json", scope)

client = gspread.authorize(creds)

# SHEETS
fulfill_sheet = client.open("STOCK_FULFILL").worksheet("Sheet1")
dispatch_sheet = client.open("STOCK_DISPATCH").worksheet("Sheet1")


# -----------------------------
# ✅ DISPATCH LIST PAGE (ONLY STATUS BLANK)
# -----------------------------
@stock_dispatch_bp.route("/")
def dispatch_list():

    if "user" not in session:
        return redirect("/")

    # 🔥 FULFILL DATA
    fulfill_data = fulfill_sheet.get_all_values()
    headers = fulfill_data[0]
    rows = fulfill_data[1:]

    # 🔥 FIND STATUS COLUMN INDEX
    if "STATUS" not in headers:
        return "STATUS column not found in sheet"

    status_index = headers.index("STATUS")

    # 🔥 FILTER ONLY BLANK STATUS
    filtered_data = []

    for row in rows:
        status_value = ""

        # Safe check (agar row choti ho)
        if len(row) > status_index:
            status_value = str(row[status_index]).strip()

        if status_value == "":
            filtered_data.append(row)

    return render_template(
        "stock_dispatch.html",
        data=filtered_data,
        headers=headers
    )


# -----------------------------
# ✅ BULK DISPATCH FORM OPEN
# -----------------------------
@stock_dispatch_bp.route("/bulk_dispatch", methods=["POST"])
def bulk_dispatch():

    if "user" not in session:
        return redirect("/")

    selected_ids = request.form.getlist("selected_rows")

    if not selected_ids:
        return "No rows selected"

    return render_template(
        "stock_dispatch_form.html",
        selected_ids=selected_ids
    )


# -----------------------------
# ✅ SAVE DISPATCH (MULTIPLE)
# -----------------------------
@stock_dispatch_bp.route("/save_dispatch", methods=["POST"])
def save_dispatch():

    if not request.form.get("dispatch_date"):
        return "Dispatch date required"

    if not request.form.get("lr_num"):
        return "LR number required"

    if not request.form.get("transporter"):
        return "Transporter required"

    if not request.form.get("parcel_qty"):
        return "Parcel qty required"

    if 'photo' not in request.files or request.files['photo'].filename == "":
        return "Photo required"

   
    if "user" not in session:
        return redirect("/")

    selected_ids = request.form.getlist("selected_ids")

    dispatch_date = request.form.get("dispatch_date")
    lr_num = request.form.get("lr_num")
    transporter = request.form.get("transporter")
    parcel_qty = request.form.get("parcel_qty")
    remarks = request.form.get("remarks")

    photo = request.files.get("photo")
    photo_name = photo.filename if photo else ""

    # 🔥 HEADERS
    headers = fulfill_sheet.row_values(1)

    def col(name):
        return headers.index(name) + 1

    all_data = fulfill_sheet.get_all_values()

    # 🔥 LOOP ALL SELECTED
    for data in selected_ids:

        uid, subid = data.split("|")

        uid = str(uid).strip()
        subid = str(subid).strip()

        # -----------------------------
        # ✅ SAVE IN DISPATCH SHEET
        # -----------------------------
        dispatch_sheet.append_row([
            uid,
            subid,
            session["user"],
            dispatch_date,
            lr_num,
            transporter,
            parcel_qty,
            photo_name,
            remarks
        ])

        # -----------------------------
        # 🔥 UPDATE STATUS = Dispatched
        # -----------------------------
        for i, r in enumerate(all_data):

            if str(r[0]).strip() == uid and str(r[1]).strip() == subid:

                status_col = col("STATUS")
                lr_col = col("LR_NUMBER")

                fulfill_sheet.update_cell(i+1, status_col, "Dispatched")
                fulfill_sheet.update_cell(i+1, lr_col, lr_num)

                break

from flask import Blueprint, render_template, request, redirect, session
import gspread
from oauth2client.service_account import ServiceAccountCredentials

stock_dispatch_bp = Blueprint('stock_dispatch_bp', __name__)

# -----------------------------
# GOOGLE SHEET
# -----------------------------
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "pythonhtmlformgs-230b6b2a1e42.json", scope)

client = gspread.authorize(creds)

# SHEETS
fulfill_sheet = client.open("STOCK_FULFILL").worksheet("Sheet1")
dispatch_sheet = client.open("STOCK_DISPATCH").worksheet("Sheet1")


# -----------------------------
# ✅ DISPATCH LIST PAGE (ONLY STATUS BLANK)
# -----------------------------
@stock_dispatch_bp.route("/")
def dispatch_list():

    if "user" not in session:
        return redirect("/")

    # 🔥 FULFILL DATA
    fulfill_data = fulfill_sheet.get_all_values()
    headers = fulfill_data[0]
    rows = fulfill_data[1:]

    # 🔥 FIND STATUS COLUMN INDEX
    if "STATUS" not in headers:
        return "STATUS column not found in sheet"

    status_index = headers.index("STATUS")

    # 🔥 FILTER ONLY BLANK STATUS
    filtered_data = []

    for row in rows:
        status_value = ""

        # Safe check (agar row choti ho)
        if len(row) > status_index:
            status_value = str(row[status_index]).strip()

        if status_value == "":
            filtered_data.append(row)

    return render_template(
        "stock_dispatch.html",
        data=filtered_data,
        headers=headers
    )


# -----------------------------
# ✅ BULK DISPATCH FORM OPEN
# -----------------------------
@stock_dispatch_bp.route("/bulk_dispatch", methods=["POST"])
def bulk_dispatch():

    if "user" not in session:
        return redirect("/")

    selected_ids = request.form.getlist("selected_rows")

    if not selected_ids:
        return "No rows selected"

    return render_template(
        "stock_dispatch_form.html",
        selected_ids=selected_ids
    )


# -----------------------------
# ✅ SAVE DISPATCH (MULTIPLE)
# -----------------------------
@stock_dispatch_bp.route("/save_dispatch", methods=["POST"])
def save_dispatch():

    if not request.form.get("dispatch_date"):
        return "Dispatch date required"

    if not request.form.get("lr_num"):
        return "LR number required"

    if not request.form.get("transporter"):
        return "Transporter required"

    if not request.form.get("parcel_qty"):
        return "Parcel qty required"

    if 'photo' not in request.files or request.files['photo'].filename == "":
        return "Photo required"

   
    if "user" not in session:
        return redirect("/")

    selected_ids = request.form.getlist("selected_ids")

    dispatch_date = request.form.get("dispatch_date")
    lr_num = request.form.get("lr_num")
    transporter = request.form.get("transporter")
    parcel_qty = request.form.get("parcel_qty")
    remarks = request.form.get("remarks")

    photo = request.files.get("photo")
    photo_name = photo.filename if photo else ""

    # 🔥 HEADERS
    headers = fulfill_sheet.row_values(1)

    def col(name):
        return headers.index(name) + 1

    all_data = fulfill_sheet.get_all_values()

    # 🔥 LOOP ALL SELECTED
    for data in selected_ids:

        uid, subid = data.split("|")

        uid = str(uid).strip()
        subid = str(subid).strip()

        # -----------------------------
        # ✅ SAVE IN DISPATCH SHEET
        # -----------------------------
        dispatch_sheet.append_row([
            uid,
            subid,
            session["user"],
            dispatch_date,
            lr_num,
            transporter,
            parcel_qty,
            photo_name,
            remarks
        ])

        # -----------------------------
        # 🔥 UPDATE STATUS = Dispatched
        # -----------------------------
        for i, r in enumerate(all_data):

            if str(r[0]).strip() == uid and str(r[1]).strip() == subid:

                status_col = col("STATUS")
                lr_col = col("LR_NUMBER")

                fulfill_sheet.update_cell(i+1, status_col, "Dispatched")
                fulfill_sheet.update_cell(i+1, lr_col, lr_num)

                break

    return redirect("/stock_dispatch")