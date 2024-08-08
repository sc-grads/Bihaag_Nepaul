class Store:
    def __init__(self, name):
        self.name = name
        self.items = []

    def add_item(self, name, price):
        self.items.append({
            'name': name,
            'price': price
        })

    def stock_price(self):
        total = 0
        for item in self.items:
            total += item['price']
        return total

    @classmethod
    def franchise(cls, store):
        return cls(store.name + " - franchise")
    @staticmethod
    def store_details(store):
        return '{}, total stock price: {}'.format(store.name,int(store.stock_price()))


'''-----------------------------------------------------------------------------------------'''

# Create a store
store1 = Store("Tech Store")

# Add items to the store
store1.add_item("Laptop", 1000)
store1.add_item("Smartphone", 500)
store1.add_item("Tablet", 300)

# Calculate the stock price
print("Total stock price of the store:", store1.stock_price())  # Output: 1800

# Create a franchise of the store
franchise_store = Store.franchise(store1)

# Check the franchise store's name
print("Franchise store name:", franchise_store.name)  # Output: "Tech Store - franchise"

# Display store details using static method
print(Store.store_details(store1))  # Output: "Tech Store, total stock price: 1800"
print(Store.store_details(franchise_store))  # Output: "Tech Store - franchise, total stock price: 0"
