from flask import Flask, render_template, request, redirect, session
from rolebasefootfall import rolebasefootfall_bp
from requirement_only_item_depndency import requirement_only_item_depndency_bp
from requirement_dependent_last_field import requirement_dependent_last_field_bp
from stock_fulfill import stock_fulfill_bp
from stock_dispatch import stock_dispatch_bp


app = Flask(__name__)
app.secret_key = "secret123"   # required for session

app.register_blueprint(rolebasefootfall_bp, url_prefix='/rolebasefootfall')

app.register_blueprint(requirement_only_item_depndency_bp, url_prefix='/requirement_only_item_depndency')   # 🔥 register
app.register_blueprint(requirement_dependent_last_field_bp, url_prefix='/requirement_dependent_last_field')   # 🔥 register
app.register_blueprint(stock_fulfill_bp, url_prefix='/stock_fulfill')   # 🔥 register
app.register_blueprint(stock_dispatch_bp, url_prefix='/stock_dispatch')   # 🔥 register


# Dummy users
users = {
    "admin": "123",
    "ambikapur": "123",
    "bhilai": "123",
    "bilaspur": "123",
    "durg": "123",
    "jabalpur": "123",
    "pulgaon1": "123",
    "pulgaon2": "123",
    "raipur": "123",
    "rajnandgaon": "123",    
    "rewa": "123", 
    "nikita": "123",
    "vishal": "123",
    "minesh": "123",
    "mahaveer": "123",
    "manish": "123",   
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']

        if user in users and users[user] == password:
            session['user'] = user
            return redirect('/home')
        else:
            return "Invalid Login"

    return render_template('login.html')


@app.route('/home')
def home():
    if 'user' not in session:
        return redirect('/login')

    user = session['user']

    # Procurement Users
    procurement_users = ["nikita", "vishal", "minesh", "mahaveer"]

    return render_template("home.html",
                           user=user,
                           is_procurement=user in procurement_users)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
