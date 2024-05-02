from unittest import TestCase

from app import app
from models import db, User, Post, Tag, PostTag

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_test"
app.config["SQLALCHEMY_ECHO"] = False

app.config["TESTING"] = True

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for User."""

    def setUp(self):
        """Add sample user."""

        PostTag.query.delete()
        Tag.query.delete()
        Post.query.delete()
        User.query.delete()

        user = User(first_name="First", last_name="Last")
        db.session.add(user)
        db.session.commit()

        post = Post(title="test_title", content="test_content", user_id=user.id)
        db.session.add(post)
        db.session.commit()

        tag = Tag(name="test_tag")
        db.session.add(tag)
        db.session.commit()

        post_tag = PostTag(post_id=post.id, tag_id=tag.id)
        db.session.add(post_tag)
        db.session.commit()

        self.user_id = user.id
        self.post_id = post.id
        self.tag_id = tag.id

    def tearDown(self):
        """Clean up."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("First Last", html)

    def test_user_details(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>First Last</h1>", html)
            self.assertIn("test_title", html)

    def test_post_details(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>test_title</h1>", html)
            self.assertIn("<p>test_content</p>", html)
            self.assertIn("test_tag", html)

    def test_tag_details(self):
        with app.test_client() as client:
            resp = client.get(f"/tags/{self.tag_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>test_tag</h1>", html)
            self.assertIn(f'<a href="/posts/{self.post_id}">test_title</li>', html)

    def test_edit_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<input type="text" name="title" value="test_title">', html)
            self.assertIn("test_content", html)
            self.assertIn(
                f'<li><input type="checkbox" name="tags" value="{self.tag_id}" checked>test_tag</li>',
                html,
            )
