def named(**kwargs):
    print(kwargs)


named(name="Bob", age=25, height=5.6)

def print_nicely(**kwargs):
    named(**kwargs)
    for arg, value in kwargs.items():
        print(f"{arg}: {value}")

print(print_nicely(name="Bob", age=25, height=5.6))