def query_all(cls):
    return cls.query.all()

def query_by_id(cls, id):
    return cls.query.get_or_404(id)

def serialize_cupcakes(cupcake):
    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }
