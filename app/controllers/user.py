from flask import current_app as app, render_template, request, redirect, url_for, session
from ..models.admin import db, User, Section, Product, Cart
from collections import defaultdict

@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form["name"]
        phone = request.form["mobile_num"]
        password = request.form["password"]
        # Check if the user already exists
        existing_user = User.query.filter_by(phone=phone).first()
        if existing_user:
            return render_template('signup.html', error= "User with this phone number already exists.")
        else:
        # Create a new user
            if not name.isalpha() and not ' ' in name:
                return render_template('signup.html', error="Name should contain only letter and spaces.")
            try:
                phone= str(phone)
                if len(phone)<10:
                    return render_template('signup.html',error="Invalid")
                phone = int(phone)
            except ValueError:
                return render_template('signup.html', error="Invalid Mobile number. Mobile number must be a number.")
            if len(password) < 8 or not any(char.isdigit() for char in password) or not any(char in '!@#$%^&*' for char in password):
                return render_template('signup.html', error="Password must contain at least 8 characters with at least 1 special character and 1 numerical digit.")
            
            new_user = User(name = name,
                            phone = phone,
                            password = password)

            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login_user'))
    return render_template('signup.html')


@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    if request.method =="GET":
        return render_template("login_user.html")
    if request.method=="POST":
        
        phone = request.form["mobile_num"]
        password = request.form["password"]

        user = User.query.filter_by(phone=phone, password=password).first()
        
        if not user:
            return render_template('login_user.html', error='Wrong password')

        else:
            session['user_id'] = user.user_id
            return redirect(url_for("dashboard"))
            

    #If the request method is not GET or POST, it will reach here. You should handle this case accordingly.
    return redirect(url_for("login_user"))

@app.route('/logout_user')
def logout_user():
    session.pop('user_id', None)
    return redirect(url_for('login_user'))

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user= User.query.get(user_id)
        sections = Section.query.all()
        products = Product.query.all()
        cart={}
        return render_template('dashboard.html', user_id=user_id,user=user, Section_list=sections, Product_list=products, cart=cart)
    else:
        return redirect(url_for('login_user'))
@app.route('/search/<int:user_id>', methods=["GET", "POST"])
def search(user_id):
    if 'user_id' in session:
        user_id = session['user_id']
        if request.method == "GET":
            return render_template("search.html",user_id= user_id)

        if request.method == "POST":
            search_type= request.form.get("search_type")
            if search_type == "section":
                # Search by Section/Category
                searched_name = "%" + request.form.get("searched","") + "%"
                if not searched_name.strip("%"):
                    return render_template("search.html",user_id= user_id, error="Section name is required")

                sections = Section.query.filter(Section.section_name.ilike(searched_name)).all()
                if not sections:
                    return render_template("search.html",user_id= user_id, error="No section found")
                product_results = []
                section_names = []
                for sec in sections:
                    products = Product.query.filter(Product.section_id == sec.sid).all()
                    product_results.extend(products)
                    section_names.append(sec.section_name)
                if not product_results:
                    return render_template("search.html",user_id= user_id, error='No products found for the matching sections.')

                return render_template('search.html',user_id= user_id, products=product_results,section_names= section_names)

            # Search by Price
            else:
                searched_price = request.form.get('price')
                if searched_price is None:
                    return render_template("search.html",user_id= user_id, error="Price is required")
                products = Product.query.filter(Product.price == searched_price).all()
                if not products:
                    return render_template("search.html",user_id= user_id, error="No product found for the given criteria.")
                return render_template('search.html' ,user_id= user_id, products =products)
    else:
        return redirect((url_for('dashboard')))
@app.route('/add_to_cart/<int:user_id>/<int:pid>', methods=['POST','GET'])
def add_to_cart(user_id,pid):
    user = User.query.get(user_id)
    product = Product.query.get(pid)
    
    if request.method == "POST":
        quantity = int(request.form['quantity'])
        if quantity >0 and quantity<= product.quantity:
            # Check if the item already exists in the cart for the user
            existing_cart_item = Cart.query.filter_by(user_id=user.user_id, product_id=product.pid).first() 
            if existing_cart_item:
                # If the item already exists, update its quantity instead of adding a new entry
                max_quantity = product.quantity - existing_cart_item.Quantity
                if  quantity<=max_quantity:
                    existing_cart_item.Quantity += quantity
                    db.session.commit()
                return redirect(url_for("view_cart",user_id=user_id)) 
            else: 
                max_quantity = product.quantity
                new_cart = Cart(user_id = user.user_id,
                                product_id = product.pid,
                                name= product.product_name,
                                Price= product.price,
                                Quantity= quantity)

                db.session.add(new_cart)
                db.session.commit()
                return redirect(url_for("view_cart",user_id=user_id))  
        else:
            return redirect('/dashboard')

@app.route('/view_cart/<int:user_id>', methods=["POST","GET"])
def view_cart(user_id):
    if 'user_id' in session:
        user_id= session['user_id']
        user = User.query.get(user_id)
        if not user:
            return "User not authenticated."

        cart_items = Cart.query.filter_by(user_id=user_id).all()
        cart_total = sum(cart_item.Price * cart_item.Quantity for cart_item in cart_items)

        return render_template("cart.html", user_id=user_id, cart=cart_items, cart_total=cart_total)
    else:
        return redirect(url_for('login_user'))

@app.route('/delete_cart_item/<int:user_id>/<int:product_id>', methods=["POST"])
def delete_cart_item(user_id, product_id):
    cart_item = Cart.query.filter_by(product_id=product_id).first()

    db.session.delete(cart_item)
    db.session.commit()

    return redirect(url_for('view_cart', user_id=user_id))


@app.route('/clear_cart/<int:user_id>', methods=['POST'])
def clear_cart(user_id):
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    for item in cart_items:
        db.session.delete(item)
    db.session.commit()
    return redirect(url_for("view_cart", user_id=user_id))

@app.route('/buy', methods=['POST','GET'])
def buy_item():
    user_id = session['user_id']
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    product_quantities = defaultdict(int)

    for cart_item in cart_items:
        product_quantities[cart_item.product_id] += cart_item.Quantity

    if request.method == "POST":
        for product_id, quantity in product_quantities.items():
            product = Product.query.get(product_id)
            if product:
                product.quantity -= quantity
                db.session.commit()
            else:
                return "Product with ID {product_id} not found."

        # Remove all items from the cart
            for item in cart_items:
                db.session.delete(item)
            db.session.commit()

            return redirect('/dashboard')
