# Star Web Tools & Scripting Suite Specification (PHP-style Suite)

**Version**: 1.0.0 (GA)  
**Standard**: Open Digital Continuity Standard (ODCS) Web Architecture  
**Author**: Star Language Architectural Team  
**Status**: Canonical Standard & Production Specification

---

## 1. Overview & Vision

Star combines the simplicity, rapid feedback loop, and rich server tooling of **PHP** with the performance, type safety, and modern concurrency of **Star**:
- **Embedded HTML Templating**: Expressive Blade/Jinja-style tags (`{{ ... }}`, `{% whenever %}`, `{% for each %}`) with automatic XSS escaping.
- **Fluent Database ORM & Query Builder**: Eloquent/PDO-style query interface for in-memory and SQLite/SQL databases (`DB.table("users").where(...).get()`).
- **Cryptographic Security Suite**: PBKDF2-HMAC-SHA256 password hashing, declarative input validation, and CSRF token verification.
- **Stateful Web Sessions & Cookies**: Stateful session management with flash storage (`Session.flash()`) and HTTP cookie serialization.
- **Scaffolding Code Generators**: Artisan-style generators (`star make:page`, `star make:api`, `star make:model`).
- **Embedded Development Web Server**: Built-in zero-config dev server with template auto-rendering (`star web:serve`).

---

## 2. API Reference & Code Examples

### 2.1 Embedded HTML Templating (`use Template`)

```star
use Template

variable template = "
<div class='profile'>
    <h1>{{ user.name | uppercase }}</h1>
    <p>{{ user.bio | trim }}</p>
    {% whenever user.is_verified %}
        <span class='verified'>Verified Developer</span>
    {% end %}
    <ul>
        {% for each skill in user.skills %}
            <li>Skill: {{ skill }}</li>
        {% end %}
    </ul>
</div>
"

variable data = {
    "user": {
        "name": "Alice Vance",
        "bio": "  Senior Distributed Systems Engineer  ",
        "is_verified": true,
        "skills": ["Star", "HyperFlow", "OmniEngine"]
    }
}

variable html_content = Template.render(template, data)
```

### 2.2 Fluent Database ORM (`use DB`)

```star
use DB

// 1. Table Query Builder
variable users = DB.table("users")

// 2. Insert records
users.insert({ "name": "Bob", "email": "bob@star.org", "role": "admin" })

// 3. Query with chaining
variable admins = users.where("role", "admin").order_by("name", "asc").limit(10).get()

// 4. Update
users.where("email", "bob@star.org").update({ "role": "superadmin" })

// 5. Delete
users.where("id", 42).delete()

// 6. Direct Raw SQL
variable count = DB.raw("SELECT COUNT(*) as total FROM users")
```

### 2.3 Cryptographic Security, Hashing & Validation (`use Security`)

```star
use Security

// 1. Password Hashing (PBKDF2-HMAC-SHA256 with 100,000 rounds)
variable hashed = Security.hash_make("user_secret_password")
variable is_valid = Security.hash_verify("user_secret_password", hashed)

// 2. Declarative Input Validation
variable payload = {
    "email": "user@domain.com",
    "age": 24,
    "username": "coder"
}

variable rules = {
    "email": "required|email",
    "age": "required|numeric|min:18",
    "username": "required|min:3|max:16"
}

variable val = Security.validate(payload, rules)
whenever not val["is_valid"]
    show val["errors"]
end

// 3. CSRF Protection
variable token = Security.csrf_token("app_secret_key", session_id)
variable verified = Security.csrf_verify(token, "app_secret_key", session_id)
```

### 2.4 Stateful Web Sessions (`use Session`)

```star
use Session

variable session = Session.start()
session.set("user_id", 1001)
session.set("cart", ["item1", "item2"])

// Flash message (disappears on next request)
session.flash("notice", "Your order has been placed successfully!")

variable notice = session.get("notice")
```

---

## 3. CLI Scaffolding & Web Server Commands

```powershell
# 1. Scaffold a new Star HTML template view in views/
star make:page dashboard

# 2. Scaffold a new REST API route in routes/
star make:api orders

# 3. Scaffold a database data model in models/
star make:model Order

# 4. Launch the embedded development web server (default port 8000)
star web:serve --port 8000
```
