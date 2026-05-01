# 🍖 FoodHeaven - Online Food Ordering System

Online food ordering system with Flask and MongoDB.

---

## What is this?

A complete website where users can:
- Browse Pakistani food menu
- Add items to cart
- Place orders
- Admin can manage orders

---

## What I Used?

| Technology | Purpose |
|------------|---------|
| Python | Backend logic |
| Flask | Web framework |
| MongoDB | Database |
| HTML/CSS/JS | Frontend |
| Font Awesome | Icons |
| AOS | Animations |

---

## Features?

### Users Can:
- ✅ Register / Login
- ✅ Browse menu by categories
- ✅ Add to cart
- ✅ Place orders
- ✅ View order confirmation

### Admin Can:
- ✅ Login to admin panel
- ✅ View all orders
- ✅ Update order status
- ✅ See total revenue
- ✅ View all users

### Design:
- ✅ Black & Yellow theme
- ✅ Mobile responsive
- ✅ Smooth animations
- ✅ Emojis everywhere

---

## Database Collections?

| Collection | Stores |
|------------|--------|
| users | User and admin data |
| categories | Food types (10) |
| dishes | Food items (50+) |
| orders | Customer orders |

---

## How to Install?

```bash
# 1. Clone
git clone https://github.com/yourusername/FoodHeaven.git
cd FoodHeaven

# 2. Create virtual env
python -m venv venv
venv\Scripts\activate

# 3. Install packages
pip install -r requirements.txt

# 4. Create .env file
MONGO_URI=mongodb://localhost:27017/foodheaven
SECRET_KEY=your-secret-key

# 5. Start MongoDB
net start MongoDB

# 6. Seed database
python seed_data.py

# 7. Create admin
python check_users.py

# 8. Run
python run.py

Default Logins?
Role	Email	Password
Admin	admin@foodheaven.com	admin123
User	Create your own	-


Project Structure?

FoodHeaven/
├── app/
│   ├── templates/   # All HTML files
│   ├── routes.py    # All URLs and logic
│   ├── models.py    # Database models
│   └── __init__.py  # App setup
├── run.py           # Start here
├── seed_data.py     # Add food data
├── check_users.py   # Create admin
├── requirements.txt # Packages needed
└── .env            # Secret keys

Made With?
❤️ + Python + Flask + MongoDB

Author?
Ayesha Yasmin 
