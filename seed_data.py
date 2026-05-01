import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import Category, Dish

# Create app
app = create_app()

# Get mongo inside app context
with app.app_context():
    from app import mongo
    
    if mongo is None:
        print("❌ MongoDB is not connected! Check your .env file and MongoDB service.")
        sys.exit(1)
    
    print("\n🌶️ Adding Pakistani Categories and Dishes...")
    
    # Clear old data
    mongo.categories.delete_many({})
    mongo.dishes.delete_many({})
    print("🗑️ Old data cleared")
    
    # Categories
    categories_data = {
        'BBQ & Tandoori': '🍖',
        'Biryani & Pulao': '🍚',
        'Karhai & Handi': '🍲',
        'Street Food': '🌯',
        'Fast Food': '🍔',
        'Desi Mithai': '🍰',
        'Desi Nasta': '🍳',
        'Seafood': '🦐',
        'Chaat & Dahi Bhalla': '🥗',
        'Desi Drinks': '🥤'
    }
    
    category_ids = {}
    for name, emoji in categories_data.items():
        result = Category.create(
            name=name,
            icon_emoji=emoji,
            description=f"Befiqri se {name} ka maza lo",
            image_url=f"/static/images/{name.lower().replace(' ', '_')}.jpg"
        )
        category_ids[name] = result.inserted_id
        print(f"✅ Category added: {emoji} {name}")
    
    # Dishes (20 sample dishes - full list aap baad mein add kar sakte ho)
    dishes = [
        ('Chicken Tikka Boti', 'BBQ & Tandoori', 450, 'Juicy boneless chicken', 'non-veg'),
        ('Malai Boti', 'BBQ & Tandoori', 480, 'Creamy tender chicken', 'non-veg'),
        ('Seekh Kabab', 'BBQ & Tandoori', 420, 'Minced meat kababs', 'non-veg'),
        ('Chicken Biryani', 'Biryani & Pulao', 350, 'Hyderabadi style biryani', 'non-veg'),
        ('Mutton Biryani', 'Biryani & Pulao', 450, 'Slow cooked mutton biryani', 'non-veg'),
        ('Chicken Karhai', 'Karhai & Handi', 550, 'Lahori style karhai', 'non-veg'),
        ('Mutton Karhai', 'Karhai & Handi', 750, 'Tender mutton karhai', 'non-veg'),
        ('Gol Gappay', 'Street Food', 120, '6 pieces with spicy water', 'veg'),
        ('Dahi Bhalay', 'Street Food', 150, 'Soft lentil fritters', 'veg'),
        ('Zinger Burger', 'Fast Food', 350, 'Crispy chicken fillet burger', 'non-veg'),
        ('Chicken Cheese Burger', 'Fast Food', 320, 'Grilled chicken with cheese', 'non-veg'),
        ('Gulab Jamun', 'Desi Mithai', 200, '4 pieces soft milk dumplings', 'veg'),
        ('Jalebi', 'Desi Mithai', 150, 'Crispy sweet spirals', 'veg'),
        ('Halwa Puri', 'Desi Nasta', 250, '2 puris with halwa', 'veg'),
        ('Nihari with Naan', 'Desi Nasta', 450, 'Traditional nihari with naan', 'non-veg'),
        ('Fried Fish', 'Seafood', 550, 'Crispy battered fish', 'non-veg'),
        ('Prawn Karhai', 'Seafood', 750, 'Prawns in karhai masala', 'non-veg'),
        ('Dahi Bhalla', 'Chaat & Dahi Bhalla', 150, 'Yogurt lentil fritters', 'veg'),
        ('Mango Lassi', 'Desi Drinks', 180, 'Sweet mango yogurt drink', 'veg'),
        ('Salt Lassi', 'Desi Drinks', 120, 'Traditional salted lassi', 'veg')
    ]
    
    # Insert dishes
    count = 0
    for dish_name, category_name, price, desc, veg_type in dishes:
        category_id = str(category_ids[category_name])
        is_veg = True if veg_type == 'veg' else False
        
        Dish.create(
            name=dish_name,
            category_id=category_id,
            price=price,
            description=desc,
            image_url=f"/static/images/{dish_name.lower().replace(' ', '_')}.jpg",
            is_veg=is_veg,
            ingredients="Traditional Pakistani spices and ingredients"
        )
        veg_emoji = '🥬' if is_veg else '🍗'
        count += 1
        print(f"  {veg_emoji} Added: {dish_name} - ₹{price}")
    
    print("\n" + "="*50)
    print(f"🎉 DATABASE SEED COMPLETE!")
    print(f"📊 Categories: {len(categories_data)}")
    print(f"🍽️ Dishes: {count}")
    print("="*50)
    
    # Verify
    print("\n📋 Category-wise dish count:")
    for cat_name in categories_data:
        cat_id = str(category_ids[cat_name])
        dish_count = mongo.dishes.count_documents({'category_id': cat_id})
        print(f"  {categories_data[cat_name]} {cat_name}: {dish_count} dishes")