student = {
    'name': 'Jose',
    'school': 'Computing',
    'grades': (66, 77, 88)
}

# Function to calculate the average grade from the 'grades' key in the dictionary
def average_grade(data):
    grades = data['grades']  
    return sum(grades) / len(grades)  

print(average_grade(student))  # Output the average grade
