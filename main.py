from fastapi import FastAPI, Depends, HTTPException, Request, Form, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from database import get_db, engine
import models, auth
from seed import seed_demo_data

models.Base.metadata.create_all(bind=engine)
seed_demo_data()

app = FastAPI(title="ShopEase E-Commerce")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ─── AUTH ROUTES ───────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    user = auth.get_current_user(request, db)
    products = db.query(models.Product).all()
    categories = db.query(models.Category).all()
    return templates.TemplateResponse("shop/home.html", {
        "request": request, "user": user,
        "products": products, "categories": categories
    })

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})

@app.post("/register")
def register(request: Request, name: str = Form(...), email: str = Form(...),
             password: str = Form(...), db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == email).first()
    if existing:
        return templates.TemplateResponse("auth/register.html", {
            "request": request, "error": "Email already registered!"
        })
    hashed = auth.get_password_hash(password)
    user = models.User(name=name, email=email, hashed_password=hashed)
    db.add(user)
    db.commit()
    return RedirectResponse("/login", status_code=302)

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})

@app.post("/login")
def login(request: Request, response: Response, email: str = Form(...),
          password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not auth.verify_password(password, user.hashed_password):
        return templates.TemplateResponse("auth/login.html", {
            "request": request, "error": "Invalid email or password!"
        })
    token = auth.create_access_token({"sub": user.email})
    resp = RedirectResponse("/", status_code=302)
    resp.set_cookie("access_token", f"Bearer {token}", httponly=True)
    return resp

@app.get("/logout")
def logout():
    resp = RedirectResponse("/login", status_code=302)
    resp.delete_cookie("access_token")
    return resp

# ─── ADMIN DASHBOARD ───────────────────────────────────────

@app.get("/admin/dashboard", response_class=HTMLResponse)
def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    user = auth.get_current_user(request, db)
    if not user or not user.is_admin:
        return RedirectResponse("/login", status_code=302)
    product_count = db.query(models.Product).count()
    order_count = db.query(models.Order).count()
    user_count = db.query(models.User).count()
    all_orders = db.query(models.Order).all()
    revenue = sum(o.total_amount for o in all_orders)
    recent_orders = db.query(models.Order).order_by(models.Order.created_at.desc()).limit(5).all()
    return templates.TemplateResponse("admin/dashboard.html", {
        "request": request, "user": user,
        "product_count": product_count, "order_count": order_count,
        "user_count": user_count, "revenue": revenue,
        "recent_orders": recent_orders
    })

# ─── CATEGORY ROUTES ───────────────────────────────────────

@app.get("/admin/categories", response_class=HTMLResponse)
def categories(request: Request, db: Session = Depends(get_db)):
    user = auth.get_current_user(request, db)
    if not user or not user.is_admin:
        return RedirectResponse("/login", status_code=302)
    cats = db.query(models.Category).all()
    return templates.TemplateResponse("admin/categories.html", {
        "request": request, "user": user, "categories": cats
    })

@app.post("/admin/categories/add")
def add_category(request: Request, name: str = Form(...),
                 description: str = Form(""), db: Session = Depends(get_db)):
    user = auth.get_current_user(request, db)
    if not user or not user.is_admin:
        return RedirectResponse("/login", status_code=302)
    cat = models.Category(name=name, description=description)
    db.add(cat)
    db.commit()
    return RedirectResponse("/admin/categories", status_code=302)

@app.post("/admin/categories/delete/{cat_id}")
def delete_category(cat_id: int, request: Request, db: Session = Depends(get_db)):
    user = auth.get_current_user(request, db)
    if not user or not user.is_admin:
        return RedirectResponse("/login", status_code=302)
    cat = db.query(models.Category).filter(models.Category.id == cat_id).first()
    if cat:
        db.delete(cat)
        db.commit()
    return RedirectResponse("/admin/categories", status_code=302)

# ─── PRODUCT ROUTES ────────────────────────────────────────

@app.get("/admin/products", response_class=HTMLResponse)
def admin_products(request: Request, db: Session = Depends(get_db)):
    user = auth.get_current_user(request, db)
    if not user or not user.is_admin:
        return RedirectResponse("/login", status_code=302)
    products = db.query(models.Product).all()
    categories = db.query(models.Category).all()
    return templates.TemplateResponse("admin/products.html", {
        "request": request, "user": user,
        "products": products, "categories": categories
    })

@app.post("/admin/products/add")
def add_product(request: Request, name: str = Form(...), description: str = Form(""),
                price: float = Form(...), stock: int = Form(...),
                image_url: str = Form(""), category_id: int = Form(...),
                db: Session = Depends(get_db)):
    user = auth.get_current_user(request, db)
    if not user or not user.is_admin:
        return RedirectResponse("/login", status_code=302)
    product = models.Product(name=name, description=description, price=price,
                             stock=stock, image_url=image_url, category_id=category_id)
    db.add(product)
    db.commit()
    return RedirectResponse("/admin/products", status_code=302)

@app.post("/admin/products/delete/{product_id}")
def delete_product(product_id: int, request: Request, db: Session = Depends(get_db)):
    user = auth.get_current_user(request, db)
    if not user or not user.is_admin:
        return RedirectResponse("/login", status_code=302)
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    return RedirectResponse("/admin/products", status_code=302)

@app.get("/admin/products/edit/{product_id}", response_class=HTMLResponse)
def edit_product_page(product_id: int, request: Request, db: Session = Depends(get_db)):
    user = auth.get_current_user(request, db)
    if not user or not user.is_admin:
        return RedirectResponse("/login", status_code=302)
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    categories = db.query(models.Category).all()
    return templates.TemplateResponse("admin/edit_product.html", {
        "request": request, "user": user,
        "product": product, "categories": categories
    })

@app.post("/admin/products/edit/{product_id}")
def edit_product(product_id: int, request: Request, name: str = Form(...),
                 description: str = Form(""), price: float = Form(...),
                 stock: int = Form(...), image_url: str = Form(""),
                 category_id: int = Form(...), db: Session = Depends(get_db)):
    user = auth.get_current_user(request, db)
    if not user or not user.is_admin:
        return RedirectResponse("/login", status_code=302)
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        product.name = name
        product.description = description
        product.price = price
        product.stock = stock
        product.image_url = image_url
        product.category_id = category_id
        db.commit()
    return RedirectResponse("/admin/products", status_code=302)

# ─── USERS ROUTE ───────────────────────────────────────────

@app.get("/admin/users", response_class=HTMLResponse)
def admin_users(request: Request, db: Session = Depends(get_db)):
    user = auth.get_current_user(request, db)
    if not user or not user.is_admin:
        return RedirectResponse("/login", status_code=302)
    users = db.query(models.User).all()
    return templates.TemplateResponse("admin/users.html", {
        "request": request, "user": user, "users": users
    })

# ─── CART ROUTES ───────────────────────────────────────────

@app.get("/cart", response_class=HTMLResponse)
def view_cart(request: Request, db: Session = Depends(get_db)):
    user = auth.get_current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=302)
    cart_items = db.query(models.CartItem).filter(models.CartItem.user_id == user.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return templates.TemplateResponse("shop/cart.html", {
        "request": request, "user": user,
        "cart_items": cart_items, "total": total
    })

@app.post("/cart/add/{product_id}")
def add_to_cart(product_id: int, request: Request, quantity: int = Form(1), db: Session = Depends(get_db)):
    user = auth.get_current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=302)
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product or product.stock <= 0:
        return RedirectResponse("/", status_code=302)
    quantity = max(1, min(quantity, product.stock))
    existing = db.query(models.CartItem).filter(
        models.CartItem.user_id == user.id,
        models.CartItem.product_id == product_id
    ).first()
    if existing:
        existing.quantity = min(existing.quantity + quantity, product.stock)
    else:
        cart_item = models.CartItem(user_id=user.id, product_id=product_id, quantity=quantity)
        db.add(cart_item)
    db.commit()
    return RedirectResponse("/cart", status_code=302)

@app.post("/cart/update/{item_id}")
def update_cart_item(item_id: int, request: Request, quantity: int = Form(...), db: Session = Depends(get_db)):
    user = auth.get_current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=302)
    item = db.query(models.CartItem).filter(models.CartItem.id == item_id, models.CartItem.user_id == user.id).first()
    if item:
        product = item.product
        if product:
            quantity = max(1, min(quantity, product.stock))
            item.quantity = quantity
            db.commit()
    return RedirectResponse("/cart", status_code=302)

@app.post("/cart/remove/{item_id}")
def remove_from_cart(item_id: int, request: Request, db: Session = Depends(get_db)):
    user = auth.get_current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=302)
    item = db.query(models.CartItem).filter(models.CartItem.id == item_id).first()
    if item and item.user_id == user.id:
        db.delete(item)
        db.commit()
    return RedirectResponse("/cart", status_code=302)

# ─── ORDER ROUTES ──────────────────────────────────────────

@app.post("/orders/place")
def place_order(request: Request, db: Session = Depends(get_db)):
    user = auth.get_current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=302)
    cart_items = db.query(models.CartItem).filter(models.CartItem.user_id == user.id).all()
    if not cart_items:
        return RedirectResponse("/cart", status_code=302)
    total = sum(item.product.price * item.quantity for item in cart_items)
    order = models.Order(user_id=user.id, total_amount=total)
    db.add(order)
    db.flush()
    for item in cart_items:
        order_item = models.OrderItem(
            order_id=order.id, product_id=item.product_id,
            quantity=item.quantity, price=item.product.price
        )
        db.add(order_item)
        db.delete(item)
    db.commit()
    return RedirectResponse("/orders", status_code=302)

@app.get("/orders", response_class=HTMLResponse)
def my_orders(request: Request, db: Session = Depends(get_db)):
    user = auth.get_current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=302)
    orders = db.query(models.Order).filter(
        models.Order.user_id == user.id
    ).order_by(models.Order.created_at.desc()).all()
    return templates.TemplateResponse("shop/orders.html", {
        "request": request, "user": user, "orders": orders
    })

@app.get("/admin/orders", response_class=HTMLResponse)
def admin_orders(request: Request, db: Session = Depends(get_db)):
    user = auth.get_current_user(request, db)
    if not user or not user.is_admin:
        return RedirectResponse("/login", status_code=302)
    orders = db.query(models.Order).order_by(models.Order.created_at.desc()).all()
    return templates.TemplateResponse("admin/orders.html", {
        "request": request, "user": user, "orders": orders
    })

@app.post("/admin/orders/status/{order_id}")
def update_order_status(order_id: int, request: Request,
                        status: str = Form(...), db: Session = Depends(get_db)):
    user = auth.get_current_user(request, db)
    if not user or not user.is_admin:
        return RedirectResponse("/login", status_code=302)
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order:
        order.status = status
        db.commit()
    return RedirectResponse("/admin/orders", status_code=302)
