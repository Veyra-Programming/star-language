# Lists and Maps in Star

# List operations
variable fruits = ["Apple", "Banana", "Cherry"]
show "Original list: " + fruits
show "First fruit: " + fruits[0]
show "List length: " + len(fruits)

fruits[1] = "Blueberry"
show "Modified list: " + fruits

# Map operations
variable profile = {
    "username": "stargazer",
    "level": 42,
    "active": true
}

show "User: " + profile["username"]
show "Level: " + profile["level"]

profile["role"] = "Architect"
show "Updated Profile: " + profile
