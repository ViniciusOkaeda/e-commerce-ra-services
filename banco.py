from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:kaiserstan#1@localhost:3306/e_commerce_db' # coloca o nome do banco, e eu coloquei assim por padrão, nn sei oq vcs vao usar
db = SQLAlchemy(app)

# Modelos do banco de dados
class Category(db.Model):
    __tablename__ = 'products_category'  # Alinhando com o nome da tabela no banco
    id = db.Column(db.Integer, primary_key=True, name='products_category_id')
    name = db.Column(db.String(255), unique=True, nullable=False, name='category_name')
    description = db.Column(db.String(255), nullable=False, name='category_description')
    image = db.Column(db.String(255), nullable=False, name='category_image')

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True, name='products_id')
    name = db.Column(db.String(255), nullable=False, name='products_name')
    description = db.Column(db.String(255), nullable=False, name='products_description')
    price = db.Column(db.Float, nullable=False, name='products_price')
    image = db.Column(db.String(255), nullable=False, name='products_image')
    category_id = db.Column(db.Integer, db.ForeignKey('products_category.products_category_id'), nullable=False, name='products_category_id')
    is_highlight = db.Column(db.Boolean, default=False, nullable=False)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, name='user_id')
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)

class FavoriteProduct(db.Model):
    __tablename__ = 'favorite_product'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.products_id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)

    # Relacionamentos para acessar os dados dos produtos e usuários favoritos
    product = db.relationship('Product', backref='favorites')
    user = db.relationship('User', backref='favorites')


# Mostra categorias
@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([{"id": c.id, "name": c.name, "description": c.description, "image": c.image} for c in categories])

# Mostra produtos por categoria
@app.route('/categories/<int:products_category_id>/products_category', methods=['GET'])
def get_products(products_category_id):
    products = Product.query.filter_by(products_category_id=products_category_id).all()
    return jsonify([{"id": p.id, "name": p.name, "price": p.price} for p in products])

# Mostra produtos por ID
@app.route('/products/<int:products_id>', methods=['GET'])
def get_product_by_id(products_id):
    product = Product.query.get_or_404(products_id)
    return jsonify({"id": product.id, "name": product.name, "price": product.price})

# Mostra produtos favoritos
@app.route('/favorites', methods=['GET'])
def get_favorite_products():
    favorites = FavoriteProduct.query.all()
    products = [Product.query.get(f.product_id) for f in favorites]
    return jsonify([{"id": p.id, "name": p.name, "price": p.price} for p in products])

# Adiciona favoritos
@app.route('/favorites', methods=['POST'])
def add_favorite_product():
    data = request.get_json()
    product_id = data.get('product_id')
    user_id = data.get('user_id')

    # Verificar se o produto existe
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Produto não encontrado."}), 404

    # Verificar se o favorito já existe
    existing_favorite = FavoriteProduct.query.filter_by(user_id=user_id, product_id=product_id).first()
    if existing_favorite:
        return jsonify({"error": "O produto já está nos favoritos."}), 400

    favorite = FavoriteProduct(user_id=user_id, product_id=product_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({"message": "Produto adicionado aos favoritos!"}), 201


# Deleta produto dos favoritos
@app.route('/favorites/<int:user_id>/<int:product_id>', methods=['DELETE'])
def delete_favorite_product(user_id, product_id):
    favorite = FavoriteProduct.query.filter_by(user_id=user_id, product_id=product_id).first()

    if not favorite:
        return jsonify({"error": "Produto não encontrado nos favoritos."}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Produto removido dos favoritos!"}), 200


# Mostra HomePage (Destaques)
@app.route('/homepage', methods=['GET'])
def get_homepage():
    highlights = Product.query.filter_by(is_highlight=True).all()
    return jsonify([{"id": p.id, "name": p.name, "price": p.price, "image": p.image} for p in highlights])


# Adicionar uma nova categoria
@app.route('/categories', methods=['POST'])
def add_category():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    image = data.get('image')

    # Verificar se todos os campos obrigatórios foram fornecidos
    if not all([name, description, image]):
        return jsonify({"error": "Todos os campos são obrigatórios."}), 400

    # Criar um novo objeto de categoria
    new_category = Category(
        name=name,
        description=description,
        image=image
    )

    # Adicionar e salvar no banco de dados
    db.session.add(new_category)
    db.session.commit()

    return jsonify({"message": "Categoria adicionada com sucesso!"}), 201

#Adiciona produto
@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    image = data.get('image')
    category_id = data.get('category_id')

    # Verificar se todos os campos obrigatórios foram fornecidos
    if not all([name, description, price, image, category_id]):
        return jsonify({"error": "Todos os campos são obrigatórios."}), 400

    # Verificar se a categoria existe
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Categoria não encontrada."}), 404

    # Criar um novo objeto de produto
    new_product = Product(
        name=name,
        description=description,
        price=price,
        image=image,
        category_id=category_id
    )

    # Adicionar e salvar no banco de dados
    db.session.add(new_product)
    db.session.commit()

    # Retornar a resposta com o ID do produto criado
    return jsonify({"message": "Produto adicionado com sucesso!", "product_id": new_product.id}), 201



# Endpoint para listar todos os produtos
@app.route('/products', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    return jsonify([{"id": p.id, "name": p.name, "description": p.description, "price": p.price, "image": p.image, "category_id": p.category_id} for p in products])


if __name__ == '__main__':
    app.run(debug=True)

with app.app_context():
    db.create_all()
