Title: Python with pizzas or, why I use @staticmethod
Date: 2015-01-15 18:30
Tags: python, 
Category: coding
Slug: python-with-pizzas-why-use-staticmethod
Author: Kasper Jacobsen
Summary: -

I feel python's ``@staticmethod`` decorator has a bad rep.
But I use it! It makes it easier to read code and distinguish where some utility functionality are being used when reading the source, especially if the person using your functionality is looking at the source or ``dir`` because maybe the documentation wasn't sufficient.

A good reason to use ``@staticmethod`` is that if someone wants to sub-class your work, they can override or add to the functionality of your ``@staticmethod``, which is very handy.

Let's say you've written a class that will help you calculate how many slices that are in a pizza:

```python
class MyPizza(object):
    def __init__(self, size, toppings):
        self.size = size
        self.toppings = toppings
        self.pizza = {}

    def _calculate_slices(self):
        area = math.pi * (self.size / 2.0) * (self.size / 2.0)
        return area / self.size

    def bake(self):
        self.pizza['slices'] = self._calculate_slices()
        self.pizza['toppings'] = self.toppings
        return self.pizza
```

It's all good! It'll calculate how many slices your pie should have, and bake you a pizza. Great!
A friend of yours wants one of your pizzas so you send him your glorious pizza machine, but he wants 8 slices in all his pizzas instead of a perfectly calculated amount of slices in each pie!
You could change ``calculate_slices`` to always ``return 8``, not very handy though.

``@staticmethod`` to the rescue! You can use ``@staticmethod`` in this case. Here's what your revised class will look like.

```python
class MyPizza(object):
    def __init__(self, size, toppings):
        self.size = size
        self.toppings = toppings
        self.pizza = {}

    @staticmethod
    def _calculate_slices(size):
        area = math.pi * (size / 2.0) * (size / 2.0)
        return area / size

    def bake(self):
        self.pizza['slices'] = self._calculate_slices(self.size)
        self.pizza['toppings'] = self.toppings
        return self.pizza
```

Now your buddy can sub-class ``MyPizza`` and make his own pizza machine with little effort, like so:

```python
class GeoffsPizza(MyPizza):
    @staticmethod
    def _calculate_slices(size):
        return 8
```

If you changed the method ``calculate_slices`` in your original class to be a function (e.g. putting it outside of your class on the module-level) you'd have had to override the whole ``bake`` method instead (well, you could've gotten around it another way, but I won't get into that solution in this post).

Here's what that would've looked like:

```python
def _calculate_slices(size):
    area = math.pi * (size / 2.0) * (size / 2.0)
    return area / size


class MyPizza(object):
    def __init__(self, size, toppings):
        self.size = size
        self.toppings = toppings
        self.pizza = {}

    def bake(self):
        self.pizza['slices'] = _calculate_slices(self.size)
        self.pizza['toppings'] = self.toppings
        return self.pizza
```

And the sub-class:

```python
class GeoffsPizza(MyPizza):
    def bake(self):
        self.pizza['slices'] = 8
        self.pizza['toppings'] = self.toppings
        return self.pizza
```

Not a great way to do it in my eyes.
Imagine if you had a much more complex ``bake`` method! You'd have to copy all the logic into your sub-class and just change a few lines so the class would do what you wanted it to.

That's why I use ``@staticmethod``.
