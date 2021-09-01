from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake
from helper import query_all, query_by_id, serialize_cupcakes

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcake'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'oh-so-secret'

connect_db(app)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/api/cupcakes')
def list_cupcakes():
    cupcakes = query_all(Cupcake)
    serialize = [serialize_cupcakes(c) for c in cupcakes]

    return jsonify(cupcakes=serialize)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    data = request.json

    cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None)

    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=serialize_cupcakes(cupcake)), 201)

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    cupcake = query_by_id(Cupcakes, cupcake_id)
    serialize = serialize_cupcakes(cupcake)
    return jsonify(cupcake=serialize)
    
@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    data = request.json

    cupcake = query_by_id(Cupcake, cupcake_id)

    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=serialize_cupcakes(cupcake))

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def remove_cupcake(cupcake_id):
    cupcake = query_by_id(Cupcake, cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message = 'Deleted')