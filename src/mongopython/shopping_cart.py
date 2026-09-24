from pymongo import MongoClient

class Product:

    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity


class Cart:

    def __init__(self):

        connection_string ="mongodb+srv://tripathi20t_db_user:YcvNRnPnxRs1w1Jr@attendanceassign.sbapwws.mongodb.net/"


        self.client = MongoClient(connection_string)
        self.db = self.client["shoppingcart"]

        self.products = self.db["products"]
        self.cart = self.db["cart"]

    def add_product(self, product):

        if product.price <= 0 or product.quantity <= 0:
            print("Invalid price or quantity")
            return

        item = {
            "name": product.name,
            "price": product.price,
            "quantity": product.quantity
        }

        self.cart.insert_one(item)

        print(product.name, "added to cart")


    def remove_product(self, product_name):

        result = self.cart.delete_one({
            "name": product_name
        })

        if result.deleted_count > 0:
            print(product_name, "removed from cart")
        else:
            print("Product not found in cart")


    def show_cart(self):

        items = list(self.cart.find())

        if not items:
            print("Cart is empty")
            return

        print("\n----- Shopping Cart -----")

        for item in items:

            total = item["price"] * item["quantity"]

            print(
                f'{item["name"]} | '
                f'Price: ₹{item["price"]} | '
                f'Quantity: {item["quantity"]} | '
                f'Total: ₹{total}'
            )


    def calculate_total(self):

        total = 0

        for item in self.cart.find():

            total += item["price"] * item["quantity"]

        return total


laptop = Product("Laptop", 60000, 1)
mouse = Product("Wireless Mouse", 800, 2)
keyboard = Product("Keyboard", 1500, 1)



my_cart = Cart()

my_cart.add_product(laptop)
my_cart.add_product(mouse)
my_cart.add_product(keyboard)



my_cart.show_cart()



print("\nTotal Cart Value", my_cart.calculate_total())


