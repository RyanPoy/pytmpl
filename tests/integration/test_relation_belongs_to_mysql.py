#coding: utf8
from sweet.tests import TestCase, User, Mobile


class TestRelationBelongsToMysql(TestCase):
    
    def setUp(self):
        self.remove_record()

    def tearDown(self):
        self.remove_record()

    def remove_record(self):
        Mobile.delete_all()
        User.delete_all()

    def test_query(self):
        user_id = User.create(name="Jon", age=31).id
        Mobile.create(name="Nokia", user_id=user_id)
        Mobile.create(name="IPhone", user_id=user_id)

        m = Mobile.where(name='Nokia').first()
        u = m.user
        self.assertEqual(User, type(u))
        self.assertEqual('Jon', u.name)
        self.assertEqual(31, u.age)

        m = Mobile.where(name='IPhone', user_id=user_id).first()
        self.assertEqual(u.id, m.user.id)

    def test_create(self):
        u = User.create(name="Jon", age=31)
        mobile_id = Mobile.create(name="Nokia", user=u).id
        m = Mobile.find(mobile_id)
        self.assertEqual(u.id, m.user_id)

        u = m.user
        self.assertEqual("Jon", u.name)
        self.assertEqual(31, u.age)

    def test_save(self):
        u = User.create(name="Jon", age=31)
        mobile_id = Mobile(name="Nokia", user=u).save().id

        m = Mobile.find(mobile_id)
        self.assertEqual(u.id, m.user_id)

        u = m.user
        self.assertEqual("Jon", u.name)
        self.assertEqual(31, u.age)

    def test_update(self):
        u1 = User.create(name="Jon", age=31)
        u2 = User.create(name="Lily", age=21)
        u3 = User.create(name="Lucy", age=11)

        m = Mobile(name="Nokia", user=u1).save()
        self.assertEqual(u1.id, m.user_id)

        m.update(user=u2)
        self.assertEqual(u2.id, m.user_id)
        
        m = Mobile.where(name='Nokia').first()
        self.assertEqual(u2.id, m.user_id)

        m.user = u3
        m.save()
        self.assertEqual(u3.id, m.user_id)

        m = Mobile.where(name='Nokia').first()
        self.assertEqual(u3.id, m.user_id)


if __name__ == '__main__':
    import unittest
    unittest.main()
