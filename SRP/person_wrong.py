"""
This Person class has two jobs:
    - Manage the person's property.
    - Store the person in the database.
"""

class Person:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Person(name={self.name})'

    @classmethod
    def save(cls, person):
        print(f'Save the {person} to the database')


if __name__ == '__main__':
    p = Person('John Doe')
    Person.save(p)

"""Later, if you want to save the Person into different storage such as a file,
you'll need to change the save() method, which also changes the whole Person class."""
