"""
Seed script - creates admin user + demo categories & products.
Run once: python seed.py
"""
from database import engine, SessionLocal
import models
from auth import get_password_hash

models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Admin user — delete old one and recreate to ensure fresh password
old_admin = db.query(models.User).filter(models.User.email == "admin@shop.com").first()
if old_admin:
    db.delete(old_admin)
    db.flush()
admin = models.User(
    name="Admin",
    email="admin@shop.com",
    hashed_password=get_password_hash("1234567@"),
    is_admin=True,
)
db.add(admin)
print("✅ Admin created  →  admin@shop.com / 1234567@")

# Demo customer accounts
demo_customers = [
    ("Rahul Sharma", "rahul@demo.com", "1234567@"),
    ("Priya Singh", "priya@demo.com", "1234567@"),
    ("Amit Kumar", "amit@demo.com", "1234567@"),
]
for cname, cemail, cpwd in demo_customers:
    if not db.query(models.User).filter(models.User.email == cemail).first():
        cu = models.User(name=cname, email=cemail, hashed_password=get_password_hash(cpwd))
        db.add(cu)
print("✅ Demo customer accounts created (password: 1234567@)")

# Categories
cats = {}
for cname, cdesc in [
    ("Electronics", "Gadgets and devices"),
    ("Clothing", "Fashion and apparel"),
    ("Books", "Books and e-books"),
    ("Home & Kitchen", "Home essentials"),
]:
    existing = db.query(models.Category).filter(models.Category.name == cname).first()
    if not existing:
        c = models.Category(name=cname, description=cdesc)
        db.add(c)
        db.flush()
        cats[cname] = c.id
    else:
        cats[cname] = existing.id

# Products
sample_products = [
    # Electronics
    ("Wireless Earbuds", "High-quality sound with active noise cancellation, 24hr battery life", 1999.99, 50, "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400", "Electronics"),
    ("Smart Watch", "Fitness tracker with heart rate monitor and smart notifications", 3499.00, 30, "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400", "Electronics"),
    ("Bluetooth Speaker", "360° surround sound, waterproof, 12hr playtime", 1299.00, 40, "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400", "Electronics"),
    ("Laptop Stand", "Adjustable aluminium stand, ergonomic design", 799.00, 60, "https://images.unsplash.com/photo-1547394765-185e1e68f34e?w=400", "Electronics"),
    ("USB-C Hub 7-in-1", "HDMI, USB 3.0, SD card reader, PD charging", 1499.00, 45, "https://images.unsplash.com/photo-1625948515271-2e7b25b41b70?w=400", "Electronics"),
    ("Mechanical Keyboard", "RGB backlit, tactile switches, compact TKL layout", 2799.00, 20, "https://images.unsplash.com/photo-1601445638532-1f2aba7f346a?w=400", "Electronics"),
    ("Wireless Mouse", "Ergonomic design, 2400 DPI, silent clicks", 899.00, 55, "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400", "Electronics"),
    ("Power Bank 20000mAh", "Fast charging, dual USB output, LED display", 1199.00, 70, "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=400", "Electronics"),
    # Clothing
    ("Men's T-Shirt", "100% premium cotton, breathable, available in 5 colours", 399.00, 100, "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400", "Clothing"),
    ("Women's Jacket", "Slim fit, water resistant, fleece lined", 1599.00, 45, "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=400", "Clothing"),
    ("Running Shoes", "Lightweight mesh upper, anti-slip rubber sole", 2199.00, 35, "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400", "Clothing"),
    ("Denim Jeans", "Slim fit, stretch denim, 5-pocket design", 1299.00, 60, "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400", "Clothing"),
    ("Sports Hoodie", "Moisture-wicking fabric, kangaroo pocket, unisex", 849.00, 80, "https://images.unsplash.com/photo-1556821840-3a63f15732ce?w=400", "Clothing"),
    ("Formal Shirt", "Cotton blend, wrinkle-free, full sleeves", 699.00, 90, "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400", "Clothing"),
    # Books
    ("Python Programming", "Complete guide to learn Python from scratch with projects", 499.00, 200, "https://images.unsplash.com/photo-1550399105-c4db5fb85c18?w=400", "Books"),
    ("Clean Code", "Best practices and principles for professional developers", 599.00, 150, "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400", "Books"),
    ("The Alchemist", "Paulo Coelho's international bestseller about following your dreams", 349.00, 180, "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400", "Books"),
    ("Atomic Habits", "Proven framework for building good habits and breaking bad ones", 449.00, 160, "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=400", "Books"),
    # Home & Kitchen
    ("Coffee Maker", "Brews 12 cups, programmable timer, auto shut-off", 2499.00, 25, "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400", "Home & Kitchen"),
    ("Non-Stick Pan", "Durable ceramic coating, induction compatible, 26cm", 899.00, 70, "https://images.unsplash.com/photo-1585515320310-259814833e62?w=400", "Home & Kitchen"),
    ("LED Desk Lamp", "3 brightness levels, USB charging port, touch control", 649.00, 80, "https://images.unsplash.com/photo-1513506003901-1e6a35549612?w=400", "Home & Kitchen"),
    ("Air Fryer 4L", "1500W, digital display, 8 preset cooking modes", 3999.00, 18, "https://images.unsplash.com/photo-1626509653291-18d9a934b9db?w=400", "Home & Kitchen"),
    ("Water Bottle 1L", "Stainless steel, double-wall insulated, leak-proof lid", 599.00, 120, "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400", "Home & Kitchen"),
]

added_products = []
for name, desc, price, stock, img, cat_name in sample_products:
    existing = db.query(models.Product).filter(models.Product.name == name).first()
    if not existing:
        p = models.Product(
            name=name, description=desc, price=price,
            stock=stock, image_url=img, category_id=cats.get(cat_name, 1)
        )
        db.add(p)
        db.flush()
        added_products.append(p)
    else:
        added_products.append(existing)

print(f"✅ {len(added_products)} products ready!")

# Demo orders from customer accounts
db.flush()
rahul = db.query(models.User).filter(models.User.email == "rahul@demo.com").first()
priya = db.query(models.User).filter(models.User.email == "priya@demo.com").first()
amit  = db.query(models.User).filter(models.User.email == "amit@demo.com").first()

all_products = db.query(models.Product).all()
prod = {p.name: p for p in all_products}

demo_orders = [
    (rahul, [("Wireless Earbuds", 1), ("Smart Watch", 1)], "delivered"),
    (rahul, [("Python Programming", 2), ("Clean Code", 1)], "shipped"),
    (priya, [("Women's Jacket", 1), ("Running Shoes", 1)], "delivered"),
    (priya, [("Coffee Maker", 1)], "processing"),
    (amit,  [("Bluetooth Speaker", 1), ("USB-C Hub 7-in-1", 1)], "pending"),
    (amit,  [("Air Fryer 4L", 1), ("Water Bottle 1L", 2)], "delivered"),
]

orders_created = 0
for user_obj, items, status in demo_orders:
    if not user_obj:
        continue
    total = sum(prod[n].price * qty for n, qty in items if n in prod)
    if total == 0:
        continue
    order = models.Order(user_id=user_obj.id, total_amount=total, status=status)
    db.add(order)
    db.flush()
    for n, qty in items:
        if n in prod:
            oi = models.OrderItem(
                order_id=order.id, product_id=prod[n].id,
                quantity=qty, price=prod[n].price
            )
            db.add(oi)
    orders_created += 1

print(f"✅ {orders_created} demo orders created!")

db.commit()
db.close()
print("✅ Seeding complete.")
