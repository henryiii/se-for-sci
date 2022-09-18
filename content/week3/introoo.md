---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python [conda env:se-for-sci] *
  language: python
  name: conda-env-se-for-sci-py
---

# Intro to Object Oriented Programming (OOP)

## Objects as collections of data and functions

An object is simply a collection of data and functions that operate on that
data.

For example, let’s say we wanted to represent our home directory as an object.
It might look something like this:

```{mermaid}
graph TD
    A{home_directory} -->|string_location| B["'/home/me'"]
    A -->|exists| C("def exists(...): ...")
```

This object holds a single data "member" (named `string_location`), and has a
function, called a "method", to see if the directory exists.

We could produce lots of these, each with different `string_location` values,
and we could use them in our code to track directories and see if they exist.
All of these objects are interchangeable, and all of them have identical
functions - only the contents of the data are different. This suggests we could
make a further improvement to the model. (Unless we were in JavaScript, by the
way, where this really is how objects were implemented!)

To ensure we make exactly the same structure of object, we could make a
templating function that "constructs" the same sort of object. Classic
JavaScript (before ES6 in 2015) does exactly this. We will quickly upgrade this
idea to something much nicer and more native to Python! But let's just try it
out to illustrate the point:

```{code-cell} python3
import os
from types import SimpleNamespace

def make_path(string_location):
    self = SimpleNamespace()
    self.string_location = string_location
    self.exists = lambda: os.path.exists(string_location)
    return self

my_dir = make_path("my/dir")
print(f"{my_dir.string_location = }")
print(f"{my_dir.exists() = }")
```

Again, don't do this in Python! There's a better way. But you'll see it's not
_so_ different. The key feature is is we are "templating" new object creation to
ensure they all have the attributes we require. As you'll see, languages
formalize this in something called "constructors".

There's one other issue above. We make a brand new function "exist" every single
object we create. If "exists" simply had access to the object it was being
called from, you could make it completely generic and just share it between all
objects that are "similar". But first, let's formalize "similar"!

## Classes

People like to categorize things; it helps us think. If I asked you what Bluey
was, you would say she's a dog (at least if you are around small children and
have seen the show). We would say Bluey is an object, an instance of a dog, a
class (we capitalize instances and classes backwards from English).

In our example, we want a concept for the type of thing that `make_path`
produced, and `my_dir` was an instance of - we'll call it `Path` - that's the
class.

Here's what making such a class looks like in several languages:

`````{tab-set}
````{tab-item} Python
```python
import os


class Path:
    def __init__(self, string_location):
        self.string_location = string_location

    def exists(self):
        return os.path.exists(self.string_location)
```
````

````{tab-item} Python dataclasses
```python
import os
import dataclasses


@dataclasses.dataclass
class Path:
    string_location: str

    def exists(self):
        return os.path.exists(self.string_location)
```
````


````{tab-item} C++
```cpp
#include <filesystem>
#include <string>

class Path {
  public:
    std::string string_location;

    Path(std::string string_location) : string_location(string_location) {}

    bool exists() const {
        const std::filesystem::path path_location{string_location};
        return std::filesystem::exists(path_location);
    }
};
```
````
````{tab-item} Matlab
```matlab
classdef Path
    properties
        string_location
    end
    methods
        function obj = Path(string_location)
            obj.string_location = string_location;
        end

        function res = exists()
            res = isfile(filename)
        end
    end
end
```
````
````{tab-item} Ruby
```ruby
class Path
    attr_accessor :string_location

    def initialize(string_location)
        @string_location = string_location
    end

    def exists?
        Path.exists? @string_location
    end
end
```
````
````{tab-item} NodeJS
```js
const fs = require("fs");

class Path {
    constructor(string_location) {
        this.string_location = string_location;
    }

    exists() {
        return fs.existsSync(path);
    }
}
```
````
`````

This gives us several benefits: If we get a Path, we know it has
`string_location` and `exists()`. We no longer need an `exists` function on
every instance, we can define it on the class, and Python's syntax will help us
use it. Python provides a handy shortcut for calling `Path.exists(instance)`;
you can just call `instance.exists()` instead, and it passes the instance in as
the first value to the function (traditionally called `self`).

The "template" function in this case was `__init__`. In this function, you get
the new, empty class and you have to add the members manually, just like in our
template example. This will always run when classes are constructed, and it gets
the arguments used to make the class, too.

You can access the class that an object belongs to with `.__class__`.
`self.__class__.__name__` is a common trick for getting the name of the class.

### Subclassing

We can take our analogy one step further. Bluey is a dog, and a dog is an
animal. We like to have sets of broader and broader labels. Only Bluey is an
instance, so dog is a subclass of animal (or animal is a parent class of dog).
You could have as many of these as you wanted - for example, maybe Bluey is
actually an instance of "blue healer", which is a subclass of dog.

When Python looks up something on a class, it goes through the "Method
Resolution Order". The procedure to look up an attribute access looks something
like this:

```{mermaid}
graph TD
    O[object] --> A
    A[Path] --> B(home_directory)
```

First, is in contained in `home_directory`? No, then is it contained in `Path`?
The final look up is in `object`, which is the implicit parent at the top of all
MRO's.

```{code-cell} python3
class Animal:
    def eat(self, food):
        print(f"{self.__class__.__name__} eating {food}")

class Dog(Animal):
    pass

bluey = Dog()
rascal.eat("fruit")
```

Notice that `self.__class__` inside `eat` was `Dog`, even though we defined the
method on `Animal`. That's because `self` was `bluey`, which is an instance of
`Dog`.

We can override an method if we want:

```{code-cell} python3
class Racoon(Animal):
    def eat(self, food):
        print("Washing first")
        super().eat(food)

rascal = Racoon()
rascal.eat("berries")
```

In this case, all `Animal`s can eat - if you know you take an `Animal`, you know
it can eat. However, `Racoon` has have a custom eat function. It has the same
signature (important!), but it does a bit more. This is also how Python calls a
method from the "class above", by using `super()`. You could have also said
`Animal.eat(self, food)` here, but `super()` is better.

An important feature of subclassing is instance checks. `rascal`, above, is both
an instance of Racoon and of Animal.

```{code-cell} python3
print(f"{isinstance(rascal, Racoon)}")
print(f"{isinstance(rascal, Animal)}")
```

You can look up the exact method resolution order by looking at `__mro__`:

```{code-cell} python3
print(f"{Racoon.__mro__ = }")
```

This is how error catching works in Python. If you see custom errors, they often
have no members or methods at all; they are just utilizing this inheritance
concept!

```{code-cell} python3
print(f"{KeyError.__mro__ = }")
```

This means you'll catch a `KeyError` if you ask for a `KeyError`, `LookupError`,
or an `Exception`! (Or a `BaseException`, but don't ask for that, too general,
catches things like `MemoryError` too!)

### Special methods

We've already seen a special method in Python: `__init__`. You can customize
almost every aspect of the behavior with special methods; it's easier to go over
what you can't do than what you can. You can't change assignment, `and`/`or`
behavior (due to short-circuiting logic and some limitations that might be
removed in the future). That's about it, almost every other behavior can be
changed.

One point to note about special behavior: Python shortcuts the object lookup
check for special operations, meaning the operation must be defined in the class
or above.

Here are a few to give you a taste of what is available

- `__add__`/`__sub__`/`__mul__`/`__truediv__`: The standard math operators.
- `__iadd__`/`__isub__`/`__imul__`/`__itruediv__`: Inplace versions of math
  operators.
- `__radd__`/`__rsub__`/`__rmul__`/`__rtruediv__`: Reversed versions of math
  operators. These are called if the other direction is not supported.
- `__eq__`/`__neq__`/`__lt__`/...: The comparison operators. You can just
  specify two and then let `@functools.totalordering` generate the rest for you.
- `__repr__`/`__str__`: Controls hows the object is printed. Unlike some other
  languages, Python allows customizing the repr ("programmer view") and the str
  ("user view").

Want more? There are many, many more, handling other operators, conversion to
various things, indexing, attribute access, you name it. The
[Python Data Model](https://docs.python.org/3/reference/datamodel.html)
describes all of them.

Other languages have equivalents. C++ uses `operator +` as the function name,
for example. Matlab uses normal names like `plus` (AFAICK, it's the only one not
to call this `add`) Ruby allows almost anything as a function name, so it uses
the operator by itself as the function name. JavaScript is the only one with no
operator overloading at all (and ironically, the defaults are horrible, with "1"

- 2 producing 3). It still has some special named methods, though.

## Dataclasses

If you look at other languages, you'll notice that some other languages
(especially compiled ones) have a nice way of declaring exactly what members the
classes are allowed to have. While there is a trick to force the attributes to
be limited to a pre-defined collection in Python (look up `__slots__` and
`__dict__`, but it's a bit involved), what we'd like is that nice syntax -
**init** is very repetitive to write, especially for the common use case of
classes as "data + functions". Python has a trick to write this very nicely
these days:

`````{tab-set}
````{tab-item} Dataclass
```python
from dataclasses import dataclass


@dataclasses.dataclass
class Vector:
    x: float
    y: float
```
````
````{tab-item} Classic class
```python
from typing import Any


class Vector:
    __match_args__ = ("x", "y")

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.__class__.__name__}(x={self.x!r}, y={self.y!r})"

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return (self.x, self.y) == (other.x, other.y)
        return NotImplemented

    __hash__ = None
```
````
`````

You can use the toggle to see what dataclasses automatically generates for you.
I've included type annotations, because dataclasses include them for free -
we'll cover those later. You get a free `__init__`, `__repr__`, and `__eq__`. If
you add options to the decorator, you can generate even more useful things.
`order=True` will generate all the ordering methods. `frozen=True` will make the
members unsettable by wrapping every member with a property (a non-trivial
amount of code!) and will generate a `__hash__` as well. Python 3.10 added two
more fantastic options, `slots=True` and `kw_only=True`, too.

The `dataclasses` module has other useful tools in it, as well. You have tools
to control each field when you define them. You also have a way to iterate over
all the fields. There's a tool to convert to a `dict` or a `tuple`; dicts can be
then combined with other libraries like the `json` library. And there's a
`replace` function that will make a new dataclass but with a subset of fields
replaced, which can help you "modify" a frozen instance by making a new one.

Dataclasses are a really great way to use OOP as data + actions (which is a
really important usage) without having to write a learn/write a lot of
boilerplate. But you also get one more feature: dataclasses are a standard.
Other third-party tools can detect them `using dataclasses.is_dataclass(...)`,
and work with them. The `rich` library can pretty-print their reprs. The
`cattrs` library has tools to convert - you can get modularity and separation of
concerns by building a `cattrs` converter separate from your dataclass.