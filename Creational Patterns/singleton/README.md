# Singleton Pattern

**_Singleton is a creational design pattern that ensures that a class has only one instance, and provides a global point of access to that instance. It is important to have a single object that is shared by all parts of the application._**

## Description
It's often when we need to have a single instance of certain object to perform operations. Like a db instance, event loop, or some other objects that might be reused or wanted to be shared (at certain state) across our application. Singlenton pattern help us in this cases, it's a class that checks if an attributes has a value (in this case the instance) and if it's set then you cant create another.

### Pros
* It ensures that there is only one instance of a class, which can be useful in a number of situations.
* It simplifies the code by providing a global point of access to an object.
* It can improve performance by avoiding the overhead of creating multiple objects of the same class.

### Cons
* It can be difficult to test code that uses the singleton pattern.
* It can be difficult to extend the code that uses the singleton pattern.
* It can be abused, leading to bad design decisions.

