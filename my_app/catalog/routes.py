from flask import request, jsonify, Blueprint #blueprint helps to modularize different routes for you
from my_app import db
from my_app.catalog.models import Product, Category

catalog = Blueprint('catalog', __name__)

@catalog.route('/')
@catalog.route('/home')
def home():
    return "Welcome to the Catalog Home."

@catalog.route('/product/<id>')
def product(id):
    product = Product.query.get_or_404(id)
    return 'Product - %s, $%s' % (product.name, product.price)

@catalog.route('/products')
def products():
    products = Product.query.all()
    res = {}
    for product in products:
        res[product.id] = {
            'name': product.name,
            'price': product.price,
            'category': product.category.name
        }
    return jsonify(res)



@catalog.route('/create-products', methods=['POST',])
def create_products():
    import json
    data = json.loads(request.data)

    for items in data:

        key = data[items]

        name = key['name']
        price = key['price']
        categ_name = key['category']
        
        category = Category.query.filter_by(name=categ_name).first()
        if not category:
            category = Category(categ_name)

        product = Product(name, price, category)

        db.session.add(product)
        db.session.commit()
            
    return "Products created."


@catalog.route('/category-create', methods=['POST', ])
def create_category():
    name = request.json.get('name')
    category = Category(name)
    db.session.add(category)
    db.session.commit()
    return 'Category created'

@catalog.route('/categories')
def categories():
    categories = Category.query.all()
    res = {}
    for category in categories:
        res[category.id] = {
            'name': category.name
        }
        for product in category.products:
            res[category.id]['products'] = {
                'id': product.id,
                'name': product.name,
                'price': product.price}
    return jsonify(res)