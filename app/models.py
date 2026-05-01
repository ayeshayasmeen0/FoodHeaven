from datetime import datetime
from bson import ObjectId

# Helper function - MongoDB ke _id ko string mein convert karta hai
def serialize_doc(doc):
    if doc:
        doc['_id'] = str(doc['_id'])
    return doc

# Category Model
class Category:
    @staticmethod
    def create(name, icon_emoji, description, image_url):
        from app import mongo
        return mongo.categories.insert_one({
            'name': name,
            'icon_emoji': icon_emoji,
            'description': description,
            'image_url': image_url,
            'is_active': True,
            'created_at': datetime.now()
        })
    
    @staticmethod
    def get_all():
        from app import mongo
        categories = mongo.categories.find({'is_active': True})
        return [serialize_doc(cat) for cat in categories]

# Dish Model
class Dish:
    @staticmethod
    def create(name, category_id, price, description, image_url, is_veg, ingredients):
        from app import mongo
        return mongo.dishes.insert_one({
            'name': name,
            'category_id': category_id,
            'price': price,
            'description': description,
            'image_url': image_url,
            'is_veg': is_veg,
            'ingredients': ingredients,
            'is_available': True,
            'rating': 0,
            'reviews_count': 0,
            'created_at': datetime.now()
        })
    
    @staticmethod
    def get_all():
        from app import mongo
        dishes = mongo.dishes.find({'is_available': True})
        return [serialize_doc(dish) for dish in dishes]
    
    @staticmethod
    def get_by_category(category_id):
        from app import mongo
        dishes = mongo.dishes.find({'category_id': category_id, 'is_available': True})
        return [serialize_doc(dish) for dish in dishes]
    
    @staticmethod
    def get_by_id(dish_id):
        from app import mongo
        return serialize_doc(mongo.dishes.find_one({'_id': ObjectId(dish_id)}))

# User Model
class User:
    @staticmethod
    def create(data):
        from app import mongo
        return mongo.users.insert_one(data)
    
    @staticmethod
    def find_by_email(email):
        from app import mongo
        return mongo.users.find_one({'email': email})
    
    @staticmethod
    def find_by_id(user_id):
        from app import mongo
        return mongo.users.find_one({'_id': ObjectId(user_id)})

# Order Model
class Order:
    @staticmethod
    def create(user_id, items, total_price, delivery_address, phone):
        from app import mongo
        return mongo.orders.insert_one({
            'user_id': user_id,
            'items': items,
            'total_price': total_price,
            'delivery_address': delivery_address,
            'phone': phone,
            'status': 'pending',
            'order_date': datetime.now(),
            'estimated_delivery': None
        })
    
    @staticmethod
    def get_user_orders(user_id):
        from app import mongo
        orders = mongo.orders.find({'user_id': user_id}).sort('order_date', -1)
        return [serialize_doc(order) for order in orders]
    
    @staticmethod
    def get_all_orders():
        from app import mongo
        orders = mongo.orders.find().sort('order_date', -1)
        return [serialize_doc(order) for order in orders]
    
    @staticmethod
    def update_status(order_id, status):
        from app import mongo
        return mongo.orders.update_one(
            {'_id': ObjectId(order_id)},
            {'$set': {'status': status}}
        )