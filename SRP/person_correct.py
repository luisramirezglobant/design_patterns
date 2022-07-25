"""
To make the Person class conforms to the single responsibility principle,
you'll need to create another class that is in charge of storing the Person to a database
"""
class Person:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Person(name={self.name})'


class PersonDB:
    def save(self, person):
        print(f'Save the {person} to the database')


if __name__ == '__main__':
    p = Person('John Doe')

    db = PersonDB()
    db.save(p)