class Store:
    def __init__(self, name):
        self.name = name
        self.items = []
        
    def add_item(self, name, price):

        item = {'name': name, 'price': price}
        self.items.append(item)
        
    def stock_price(self):
        
        return sum([item['price'] for item in self.items])
        
    def print_items(self):
        for item in self.items:
            print(item)

# Create an instance of the Store
store = Store("My Store")

# Add two items
store.add_item("Laptop", 1200)
store.add_item("Phone", 800)
store.add_item("Tablet", 600)

# Get the total stock price
total_price = store.stock_price()

print(f"Total stock price: ${total_price}")

store.print_items()