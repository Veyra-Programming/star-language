// ==============================================================================
// 🐘 Star Web Tools & Platform Independence Showcase (PHP-style Suite)
// Demonstrates Embedded Templates, Database ORM, Security, and PAL Primitives.
// ==============================================================================

use Platform
use Template
use DB
use Security
use Session

show "========================================================================"
show "🌐 STAR PLATFORM INDEPENDENCE (PAL) RUNTIME"
show "========================================================================"
show "Host OS:           " + Platform.os
show "CPU Architecture:  " + Platform.arch
show "Is 64-bit:         " + str(Platform.is_64bit)
show "CPU Cores:         " + str(Platform.cpu_count)
show "Normalized Path:   " + Platform.to_posix_path("src\\controllers\\user.star")
show ""

show "========================================================================"
show "🐘 1. EMBEDDED HTML TEMPLATE ENGINE (Blade / PHP Style)"
show "========================================================================"

variable page_template = "
<div class='card'>
    <h2>{{ title | uppercase }}</h2>
    <p>{{ greeting }}</p>
    {% whenever is_admin %}
        <span class='badge'>Administrator Panel Active</span>
    {% otherwise %}
        <span>Standard User</span>
    {% end %}
    <ul>
        {% for each feature in features %}
            <li>Feature: {{ feature }}</li>
        {% end %}
    </ul>
</div>
"

variable view_data = {
    "title": "Welcome to Star Web",
    "greeting": "Platform independent, elegant, and secure web scripting.",
    "is_admin": true,
    "features": ["Zero-Crash Resilience", "Fluent Database ORM", "Microsecond JIT & Fibers"]
}

variable html_output = Template.render(page_template, view_data)
show "Rendered HTML View:"
show html_output

show "========================================================================"
show "🐘 2. FLUENT DATABASE QUERY BUILDER (Eloquent / PDO Style)"
show "========================================================================"

variable products = DB.table("products")

// Insert records
products.insert({ "name": "Cloud Compute Node", "category": "server", "price": 499 })
products.insert({ "name": "AI Accelerator Board", "category": "hardware", "price": 1299 })
products.insert({ "name": "Star Developer License", "category": "software", "price": 99 })

show "Total products count: " + str(products.count())

// Fluent query with ordering & limit
variable hardware = products.where("category", "hardware").first()
show "Hardware product found: " + hardware["name"] + " ($" + str(hardware["price"]) + ")"
show ""

show "========================================================================"
show "🐘 3. CRYPTOGRAPHIC SECURITY & INPUT VALIDATION"
show "========================================================================"

// Password Hashing
variable raw_secret = "UltraSecurePassword2026!"
variable hashed = Security.hash_make(raw_secret)
show "Hashed secret: " + hashed

variable check_pass = Security.hash_verify(raw_secret, hashed)
show "Password verification: " + str(check_pass)

// Declarative Input Validator
variable user_input = {
    "email": "architect@starlang.org",
    "username": "star_pro",
    "age": 28
}

variable validation_rules = {
    "email": "required|email",
    "username": "required|min:4|max:16",
    "age": "required|numeric|min:18"
}

variable val_result = Security.validate(user_input, validation_rules)
show "Validation status: is_valid=" + str(val_result["is_valid"])
show ""

show "========================================================================"
show "🐘 4. WEB SESSIONS & CSRF PROTECTION"
show "========================================================================"

variable session = Session.start()
session.set("user_role", "Principal Architect")
session.flash("flash_notice", "Profile synchronized across all edge nodes.")

show "Active Session ID: " + session.id
show "Stored User Role:  " + session.get("user_role")
show "Flash Notice:      " + session.get("flash_notice")

variable csrf = Security.csrf_token("app_secret_key", session.id)
show "Generated CSRF Token: " + csrf
variable is_csrf_valid = Security.csrf_verify(csrf, "app_secret_key", session.id)
show "CSRF Token Verified:  " + str(is_csrf_valid)
show ""

show "========================================================================"
show "✓ PHP-Style Web Tools & Platform Independence Showcase Completed!"
show "========================================================================"
