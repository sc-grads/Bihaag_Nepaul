users = [
    (0, "Bob", "password"),
    (1, "Rolf", "bob123"),
    (2, "Jose", "longp4assword"),
    (3, "username", "1234"),
]

# The code `{user[1]: user for user in users}` is a dictionary comprehension in Python.
# It creates a new dictionary where the keys are the second element of each tuple in the `users` list, and the values are the tuples themselves. This is done through a process called "mapping".
#
# In simpler terms, it takes a list of tuples where each tuple contains an ID,
# a username, and a password, and it creates a dictionary where the usernames are the keys and the entire tuples are the values.
# 
# This is a concise way to create a dictionary where the keys are unique from a list of elements. It's a useful feature when you want to quickly create a dictionary from a list or a set of elements.
user_mapping = {user[1]: user for user in users} 
# eg. user_mapping['Bob'] = (0, 'Bob', 'password') for above example
print(user_mapping)

