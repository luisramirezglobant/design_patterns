# Design Patterns

Design Patterns are standard, reusable solutions to common challenges in software design. When you are architecting how a codebase will be implemented, critical questions often arise:

- Scalability: How do we plan to grow the codebase, add morfunctionality and support multiple complex scenarios?

- Testability: How can we achieve high test coverage easily?

- Maintainability: Is the logic and functionality separated enough to be easily managed?

- Flexibility: Can modifications be applied without causing a "domino effect" of bugs?

If your planning is based on the **Object-Oriented paradigm (OOP)**, or if you are looking for a reliable way to refactor existing code, design patterns serve as a blueprint. They provide a proven toolkit for architecting how each piece of code is built and how those pieces interact with one another.

Think of it like repairing a wall: you need a specific set of tools and materials. Those materials must be prepared in a precise way and applied using proven techniques. These steps weren't just guessed; they were refined by countless experts over time to ensure the wall stays standing.

Design Patterns work in a very similar way. They aren't just good ideas, they are actually proven blueprints for organizing your code. When you use them, you're making sure your project is robust enough to handle all sorts of different situations while keeping order and integrity across the entire codebase.

This patterns can be clasified in three main categories, this approach of categories was originally proposed in the book the *gang of four*

[Creational Patterns](/Creational%20Patterns/)

Creational patterns are all about the way we bring objects to life in our code. Instead of just creating objects randomly whenever we need them, these patterns give us a smarter, more controlled way to handle that process. This is really helpful when the setup logic is a bit complicated or when we need to manage how many instances of a class actually exist, like making sure we only have one single point of truth for a specific task.

[Structural Patterns](/Structural%20Patterns/)

Structural patterns focus on how we plug different classes and objects together to build something bigger. Think of it like making sure all the different parts of a building fit together perfectly so the whole thing stays strong. These patterns help us organize our code so that even when we have many different pieces, they can still work together as one cohesive system without it turning into a "spaghetti" mess.

[Behavioral Patterns](/Behavioral%20Patterns/)

Behavioral patterns are really about the "conversation" between your objects. They help define how different parts of your code talk to each other and how they share the workload. By using these, you can make sure that information flows smoothly and that each part of your system knows exactly what it is supposed to do, which keeps the logic organized and easy to follow.

## SOLID