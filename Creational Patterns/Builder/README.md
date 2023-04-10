# Builder Pattern

**_The Builder patter is an abstraction on how to create complex objects separating in different parts, so those parts are put together trough the process of construction and may vary to give a concrete object with certain elements._**

## Description
Sometimes the creation of objects turns in to something complex, which might lead in to a multiple constructors or several patches in the object itself, that can go from unused parameters, hardcoded implementation.
For ths reason the Builder pattern give us some techniques to decouple this problem in to smaller peaces that can be added at runtime in different order or deciding if it goes in te object or not.
This functionality consists of 4 main parts.

## Factory
As previously mentioned this factory is a little bit more complex because is going to have at least two factory methods that each of them will create an instance of his own product. Like products in a restaurant combo (factory for burger and factory for fries) and so on, so the goal here is that each factory is going to be responsible for the creation of his particular product due to the concrete logic inside.
This Factories are known as **Concrete Factories**. Every factory will have the conditions to create the needed objects.


### Product
Is the complex object created built by all the parts putted together.  

### Builder Interface
It's where the elements to build a concrete product are provided as an Interface, It's methods are used to create the complex object.

### Concrete builder
The methods settled in the interface are implemented and give the way on what every peace of the object will provide to the final result. Also known as Builder.

### Director
Also found as Creator, is responsible for administrate all the steps in the creation of an object


### Creator
The **creator** is in charge of implement the needed factory, basically is a class that may contain certain logic for the creation of the product or even if the logic is outside of this class can be passed to decide which product to create also known as Client or even can be a function since in python often is a good idea think more in functions than in classes.

![Builder Pattern UML](builder_concept.jpg "Builder Pattern Diagram")

## Summarizing
The builder allows the creation of object down to smaller construction process to be more flexible and adaptable to different situations, this may work for different type of clients or users or usually times where the construction of an object may vary due to certain conditions.

