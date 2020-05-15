#coding: utf8
from sweet.tests import TestCase, User, Mobile
from sweet.orm import Model
from sweet.database import MySQL
from contextlib import contextmanager


class FakeDB(MySQL):

    SQLS = []

    @classmethod
    def clear_sqls(cls):
        cls.SQLS = []

    def fetchall(self, sql, *params):
        relt = super().fetchall(sql, *params)
        self.__class__.SQLS.append(sql)
        return relt

def chg_new_db():
    mgr = Model.db_manager
    return FakeDB(
        mgr.database, user=mgr.user, password=mgr.password, 
        host=mgr.host, port=mgr.port, charset='utf8', 
        show_sql=mgr.show_sql
    )


class TestRelationIncludeQueryMysql(TestCase):
    
    def setUp(self):
        self.remove_record()

    def tearDown(self):
        self.remove_record()

    def remove_record(self):
        Mobile.delete_all()
        User.delete_all()

    @contextmanager
    def mock_db(self):
        src_new_db = Model.db_manager.new_db
        Model.db_manager.new_db = chg_new_db
        try:
            yield self
        except Exception:
            raise
        finally:
            Model.db_manager.new_db = src_new_db
            FakeDB.clear_sqls()


    def test_include_belongs_to(self):
        user1 = User.create(name="Jon", age=31)
        user2 = User.create(name="Lily", age=20)
        Mobile.create(name="Nokia", user=user1)
        Mobile.create(name="IPhone", user=user1)
        Mobile.create(name="Vivo", user=user2)
        Mobile.create(name="Xiaomi", user=user2)

        with self.mock_db():
            ms = Mobile.include("user").all()
            for m in ms:
                m.user.name
            self.assertEqual(2, len(FakeDB.SQLS))
            self.assertEqual('SELECT * FROM `mobiles`', FakeDB.SQLS[0])
            self.assertEqual('SELECT * FROM `users` WHERE `id` IN (%s, %s)', FakeDB.SQLS[1])

        with self.mock_db():
            ms = Mobile.all()
            for m in ms:
                m.user.name
            self.assertEqual(5, len(FakeDB.SQLS))
            self.assertEqual('SELECT * FROM `mobiles`', FakeDB.SQLS[0])
            self.assertEqual('SELECT * FROM `users` WHERE `id` IN (%s)', FakeDB.SQLS[1])
            self.assertEqual('SELECT * FROM `users` WHERE `id` IN (%s)', FakeDB.SQLS[2])
            self.assertEqual('SELECT * FROM `users` WHERE `id` IN (%s)', FakeDB.SQLS[3])
            self.assertEqual('SELECT * FROM `users` WHERE `id` IN (%s)', FakeDB.SQLS[4])

    def test_include_has_many(self):
        user1 = User.create(name="Jon", age=31)
        user2 = User.create(name="Lily", age=20)
        Mobile.create(name="Nokia", user=user1)
        Mobile.create(name="IPhone", user=user1)
        Mobile.create(name="Vivo", user=user2)
        Mobile.create(name="Xiaomi", user=user2)

        with self.mock_db():
            us = User.include("mobiles").all()
            for u in us:
                u.mobiles.all()
            self.assertEqual(2, len(FakeDB.SQLS))
            self.assertEqual('SELECT * FROM `users`', FakeDB.SQLS[0])
            self.assertEqual('SELECT * FROM `mobiles` WHERE `user_id` IN (%s, %s)', FakeDB.SQLS[1])

        with self.mock_db():
            us = User.all()
            for u in us:
                u.mobiles.all()
            print ("FakeDB.SQLS = ", FakeDB.SQLS)
            self.assertEqual(3, len(FakeDB.SQLS))
            self.assertEqual('SELECT * FROM `users`', FakeDB.SQLS[0])
            self.assertEqual('SELECT * FROM `mobiles` WHERE `user_id` = %s', FakeDB.SQLS[1])
            self.assertEqual('SELECT * FROM `mobiles` WHERE `user_id` = %s', FakeDB.SQLS[2])


if __name__ == '__main__':
    import unittest
    unittest.main()
