from flask import current_app as app, render_template, request, redirect, url_for, session
from app.models.admin import db, Admin, Product, Section
import shutil
from werkzeug.utils import secure_filename

def getAdmin(phone=''):
     admin = Admin.query.filter_by(phone = phone).first()
     return admin 

@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    if request.method =="GET":
        return render_template("login_admin.html")
    if request.method=="POST":
        phone = request.form["mobile_num"]
        password = request.form["password"]
        admin = Admin.query.filter_by(phone=phone, password=password).first()
        
        if not admin:
            return render_template('login_admin.html', error='Wrong Credentials.')

        else:
            session['uid'] = admin.uid
            return redirect(url_for("home"))
            
    #If the request method is not GET or POST, it will reach here. You should handle this case accordingly.
    return redirect(url_for("login_admin"))
@app.route('/logout_admin')
def logout_admin():
    session.pop('uid', None)
    return redirect(url_for('login_admin'))

@app.route('/home')
def home():
    if 'uid' in session:
        admin_id = session['uid']
        sections = Section.query.all()
        return render_template('home.html', uid= admin_id, Section_list=sections)
    else:
        return redirect(url_for('login_admin'))

    
@app.route("/create_prod/<int:sid>", methods=["GET", "POST"])
def create_prod(sid):
    if 'uid' in session:
        uid= session['uid']
        if request.method == "GET":
            return render_template("product_create.html",sid=sid, uid=uid)
        
        if request.method == "POST":
        # Retrieve the sid from the form data
            product = request.form["name"]
            uploaded_file = request.files['file']
            price= request.form["price"]
            Quantity= request.form["Quantity"]
            section_id= sid
            
            existing_product = Product.query.filter(Product.product_name.ilike(product)).first()
            if existing_product: 
                return render_template('product_create.html',sid=sid, error='Product already exists')
            else:
                uploaded_file.save(uploaded_file.filename)
                destination_path = "static/docs/uploads/" + uploaded_file.filename 
                
                # to move file from root folder to designated path
                shutil.move(uploaded_file.filename, destination_path)
                new_product = Product(product_name= product,
                                price= price,
                                quantity= Quantity,
                                filepath = uploaded_file.filename,
                                section_id= section_id)

                db.session.add(new_product)
                db.session.commit()

            return redirect(url_for("edit_sec",sid=sid))
        else:
            return redirect(url_for('login_admin'))

@app.route("/delete_prod/<int:pid>", methods=["GET" , "POST"])
def delete_prod(pid):
    if request.method == "GET":
        selected_product = Product.query.filter(Product.pid== pid).first()
        db.session.delete(selected_product)
        db.session.commit()
        return redirect(url_for("home"))

@app.route("/edit_prod<int:pid>", methods=["GET", "POST"])
def edit_prod(pid):
    if 'uid' in session:
        uid= session['uid']
        selected_product = Product.query.get(pid)
        if request.method == "GET":
            return render_template("product_edit.html", product=selected_product, uid=uid)

        if request.method == "POST":
            # Update product_name if form field is not empty
            selected_id= selected_product.section_id
            new_product_name = request.form["name"].strip()
            if new_product_name:
                selected_product.product_name = new_product_name

            # Update price if form field is not empty
            new_price = request.form["price"].strip()
            if new_price:
                selected_product.price = new_price

            # Update quantity if form field is not empty
            new_quantity = request.form["Quantity"].strip()
            if new_quantity:
                selected_product.quantity = new_quantity

            uploaded_file = request.files['file']
            if uploaded_file:
                filename = secure_filename(uploaded_file.filename)
                destination_path = "static/docs/uploads/" + filename
                uploaded_file.save(destination_path)
                selected_product.filepath = filename

            db.session.commit()

            return redirect(url_for("edit_sec",sid= selected_id))
    else:
        return redirect(url_for('login_admin'))
    

@app.route("/create_sec", methods=["GET", "POST"])
def create_sec():
    if 'uid' in session:
        uid= session['uid']
        if request.method == "GET":
            return render_template("section_create.html",uid=uid)
        
        if request.method == "POST":
            section = request.form["name"]
            existing_section = Section.query.filter(Section.section_name.ilike(section)).first()
            if existing_section:
                return render_template("section_create.html", error="Section already exists!!")
            else:
                new_section = Section(section_name= section)

                db.session.add(new_section)
                db.session.commit()

        return redirect(url_for("home"))
    else:
        return redirect(url_for('login_admin'))

@app.route("/delete_sec<int:sid>", methods=["GET" , "POST"])
def delete_sec(sid):
    if request.method == "GET":
        selected_section = Section.query.filter(Section.sid== sid).first()
        db.session.delete(selected_section)
        db.session.commit()
        return redirect(url_for("home"))

@app.route("/edit_sec<int:sid>", methods=["GET" , "POST"])
def edit_sec(sid):
    if 'uid' in session:
        uid= session['uid']
        selected_section = Section.query.get(sid)
        if request.method == "GET":
            #products = Product.query.all()
            product= selected_section.products
            return render_template("section_edit.html", section= selected_section, Product_list= product, uid=uid)
        
        if request.method == "POST":
            # Query the product from the database using the product ID
            
            new_section_name = request.form["name"].strip()
            if new_section_name:
                selected_section.section_name = new_section_name

            db.session.commit()

            return redirect(url_for("edit_sec",sid=sid, uid=uid))   
    else:
        return redirect(url_for('login_admin'))  
