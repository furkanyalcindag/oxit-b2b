class UserProductObject(object):

    def __init__(self, id, product_name, price, count, image, subtotal, slug):
        self.slug = slug
        self.id = id
        self.product_name = product_name
        self.price = price
        self.count = count
        self.image = image
        self.subtotal = subtotal
