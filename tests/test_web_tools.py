"""
Unit Tests for Star Web Tools (PHP-style Scripting Suite)
Authoritative Reference: STAR_WEB_TOOLS_SPEC.md
"""

import unittest
from star_engine.web_tools.template import TemplateEngine
from star_engine.web_tools.database import Database
from star_engine.web_tools.security import Hash, Sanitizer, Validator, CSRF
from star_engine.web_tools.session import SessionManager, Cookie
from star_engine.lexer import Lexer
from star_engine.parser import Parser
from star_engine.interpreter import Interpreter


class TestWebTools(unittest.TestCase):
    # 1. Template Engine
    def test_template_rendering_and_escaping(self):
        engine = TemplateEngine()
        template = "<h1>{{ title }}</h1><p>{{ desc | uppercase }}</p>"
        res = engine.render(template, {"title": "<Alert>", "desc": "welcome"})
        self.assertEqual(res, "<h1>&lt;Alert&gt;</h1><p>WELCOME</p>")

    def test_template_loops_and_conditionals(self):
        engine = TemplateEngine()
        template = """
        {% whenever show_users %}
            <ul>{% for each user in users %}<li>{{ user }}</li>{% end %}</ul>
        {% otherwise %}
            <p>No users</p>
        {% end %}
        """
        res_true = engine.render(template, {"show_users": True, "users": ["Alice", "Bob"]})
        self.assertIn("<li>Alice</li>", res_true)
        self.assertIn("<li>Bob</li>", res_true)

        res_false = engine.render(template, {"show_users": False, "users": []})
        self.assertIn("<p>No users</p>", res_false)

    # 2. Database & Fluent Query Builder
    def test_fluent_database_query_builder(self):
        db = Database(":memory:")
        users = db.table("users")

        id1 = users.insert({"name": "Alice", "role": "admin", "age": 28})
        id2 = users.insert({"name": "Bob", "role": "editor", "age": 34})
        id3 = users.insert({"name": "Charlie", "role": "admin", "age": 42})

        self.assertEqual(users.count(), 3)

        # Where and limit
        admins = users.where("role", "admin").order_by("age", "desc").get()
        self.assertEqual(len(admins), 2)
        self.assertEqual(admins[0]["name"], "Charlie")
        self.assertEqual(admins[1]["name"], "Alice")

        # Update
        users.where("name", "Bob").update({"role": "senior_editor"})
        bob = users.where("name", "Bob").first()
        self.assertEqual(bob["role"], "senior_editor")

        # Delete
        users.where("name", "Charlie").delete()
        self.assertEqual(users.count(), 2)

    # 3. Security, Hashing & Validation
    def test_password_hashing(self):
        pwd = "SecretPass123!"
        hashed = Hash.make(pwd)
        self.assertTrue(Hash.verify(pwd, hashed))
        self.assertFalse(Hash.verify("WrongPass", hashed))

    def test_sanitization_and_slugify(self):
        html_input = "<script>alert('xss')</script>Hello <b>World</b>"
        self.assertEqual(Sanitizer.escape("<b>Bold</b>"), "&lt;b&gt;Bold&lt;/b&gt;")
        self.assertEqual(Sanitizer.strip_tags(html_input), "alert('xss')Hello World")
        self.assertEqual(Sanitizer.slugify("Star Web Tools 2.0!"), "star-web-tools-20")

    def test_input_validator(self):
        rules = {
            "email": "required|email",
            "age": "required|numeric|min:18",
            "username": "required|min:3|max:12",
        }
        valid_data = {"email": "dev@starlang.org", "age": 25, "username": "stardev"}
        res1 = Validator.validate(valid_data, rules)
        self.assertTrue(res1["is_valid"])

        invalid_data = {"email": "not-an-email", "age": 15, "username": "a"}
        res2 = Validator.validate(invalid_data, rules)
        self.assertFalse(res2["is_valid"])
        self.assertIn("email", res2["errors"])
        self.assertIn("age", res2["errors"])
        self.assertIn("username", res2["errors"])

    def test_csrf_tokens(self):
        secret = "super-secret-star-key"
        sess_id = "session-abc-123"
        token = CSRF.generate_token(secret, sess_id)
        self.assertTrue(CSRF.verify_token(token, secret, sess_id))
        self.assertFalse(CSRF.verify_token("invalid.token", secret, sess_id))

    # 4. Session & Cookie
    def test_session_state(self):
        mgr = SessionManager()
        sess = mgr.start()
        sess.set("user_id", 42)
        sess.set("theme", "dark")
        self.assertEqual(sess.get("user_id"), 42)
        self.assertEqual(sess.get("theme"), "dark")

        # Flash session
        sess.flash("message", "Item created")
        self.assertEqual(sess.get("message"), "Item created")
        self.assertIsNone(sess.get("message"))  # Flashed data removed after read

    def test_cookie_serialization(self):
        serialized = Cookie.serialize("token", "xyz123", max_age=3600, http_only=True)
        self.assertIn("token=xyz123", serialized)
        self.assertIn("Max-Age=3600", serialized)
        self.assertIn("HttpOnly", serialized)

        parsed = Cookie.parse("user=alice; theme=dark; token=xyz123")
        self.assertEqual(parsed["user"], "alice")
        self.assertEqual(parsed["theme"], "dark")
        self.assertEqual(parsed["token"], "xyz123")

    # 5. Star Language SDK (use Web / use DB / use Template)
    def test_star_sdk_web_scripting(self):
        code = """
        use Web
        use DB
        use Template
        use Security

        // 1. Template Rendering
        variable tmpl = "Hello, {{ name | uppercase }}!"
        variable rendered = Template.render(tmpl, { "name": "Star Developer" })
        show rendered

        // 2. Database ORM
        variable users = DB.table("members")
        users.insert({ "name": "Alice", "role": "lead" })
        variable all_members = users.get()
        show all_members[0]["name"]

        // 3. Security
        variable hashed = Security.hash_make("my_password")
        variable is_ok = Security.hash_verify("my_password", hashed)
        show is_ok
        """
        out = []
        interp = Interpreter(output_handler=lambda s: out.append(s), source_code=code)
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens, source_code=code).parse()
        interp.interpret(ast)

        self.assertEqual(out, ["Hello, STAR DEVELOPER!", "Alice", "true"])


if __name__ == "__main__":
    unittest.main()
