# 🌟 STAR SYNTAX GUIDE
**Language Version: 0.2.0**

This document provides a clean, practical reference to writing idiomatic Star code.

---

## 1. The Anatomy of a Star Program

In Star, code is organized into clean, spacious blocks delimited with `end`.

### Hello World
```text
app HelloStar

    show "Hello, World!"

end
```

Or as a top-level script:
```text
show "Hello, World!"
```

---

## 2. Comments

Comments start with `#` and run to the end of the line.

```text
# This is a full-line comment
variable name = "Star" # This is an inline comment
```

---

## 3. Variables & Constants

### Mutable Variables
Declared using `variable`. Can be reassigned later.
```text
variable score = 100
score = 150
```

### Immutable Constants
Declared using `constant`. Cannot be reassigned.
```text
constant PI = 3.14159
constant APP_NAME = "Star Explorer"
```

### Optional Type Annotations
```text
variable age: Integer = 25
variable price: Decimal = 19.99
variable title: Text = "Welcome"
variable active: Boolean = true
```

---

## 4. Primitive Types & Literals

| Type | Examples | Description |
|:---|:---|:---|
| **Text** | `"Hello"`, `"Line 1\nLine 2"` | UTF-8 strings |
| **Integer** | `0`, `42`, `-15` | Whole numbers |
| **Decimal** | `3.14`, `0.5`, `-10.2` | Floating point numbers |
| **Boolean** | `true`, `false` | Logical values |
| **Null** | `null` | Absence of value |

---

## 5. Collections

### Lists
Ordered sequences of values:
```text
variable fruits = ["apple", "banana", "cherry"]

# Access by 0-based index
show fruits[0] # "apple"

# Reassign element
fruits[1] = "blueberry"
```

### Maps
Key-value mappings:
```text
variable user = {
    "name": "Alex",
    "age": 28,
    "admin": true
}

# Access property
show user["name"] # "Alex"
```

---

## 6. Operators

### Arithmetic
```text
variable sum = 10 + 5       # 15
variable diff = 10 - 5      # 5
variable prod = 10 * 5      # 50
variable quot = 10 / 4      # 2.5
variable rem = 10 % 3       # 1
```

### Text Concatenation
```text
variable greeting = "Hello, " + "Star"
variable message = "Count: " + 42 # Automatic conversion to text
```

### Comparison
```text
5 > 3       # true
10 <= 10    # true
"a" == "a"  # true
"a" != "b"  # true
```

### Logical
```text
true and true     # true
true or false     # true
not false         # true
```

---

## 7. Conditionals

### If / Else If / Else
```text
if score >= 90

    show "Grade: A"

else if score >= 80

    show "Grade: B"

else

    show "Keep practicing!"

end
```

---

## 8. Loops

### Repeat Loop
Executes a block a specified number of times:
```text
repeat 3

    show "Star is bright!"

end
```

### While Loop
Executes as long as condition remains true:
```text
variable count = 0

while count < 5

    show "Count: " + count
    count = count + 1

end
```

### For-In Loop
Iterates through collections:
```text
variable numbers = [10, 20, 30]

for n in numbers

    show n * 2

end
```

### Break and Continue
```text
for i in [1, 2, 3, 4, 5]

    if i == 2
        continue
    end

    if i == 4
        break
    end

    show i

end
```

---

## 9. Functions

Functions are defined with `function` and end with `end`.

### Simple Function
```text
function greet(name)

    return "Hello, " + name + "!"

end

show greet("Star")
```

### Closures
```text
function makeCounter(start)

    variable current = start

    function increment()
        current = current + 1
        return current
    end

    return increment

end

variable counter = makeCounter(10)
show counter() # 11
show counter() # 12
```

---

## 10. Classes & Object-Oriented Programming

Classes define properties and methods. Methods access properties explicitly via `self`.

```text
class User

    property name
    property email
    property active = true

    function introduce()
        return "User: " + self.name + " (" + self.email + ")"
    end

    function deactivate()
        self.active = false
    end

end

# Instantiation with named arguments
variable user = User(
    name = "Alex",
    email = "alex@star.org"
)

show user.introduce()
```

---

## 11. Module System & Standard Library

Import standard library or local `.star` modules with `use`:

```text
use Math
use Time
use String
use IO
use "helpers.star"

show "Square root of 16 is " + Math.sqrt(16)
show "Current timestamp: " + Time.now()
show "Trimmed: " + String.trim("   hello   ")
```

---

## 12. Error Handling

Catch runtime exceptions cleanly with `try ... catch ... end`.

```text
try

    variable result = 100 / 0
    show result

catch err

    show "Caught error: " + err

end
```

---

## 13. Formatter and Linter Tools

```bash
# Check code semantics and lint warnings
star check app.star
star check app.star --strict

# Format code according to canonical 4-space standard
star format app.star --write
star format app.star --check
```
