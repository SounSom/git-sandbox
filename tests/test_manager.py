import unittest
import os
import tempfile
from src.manager import TaskManager

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        self.tmp.close()
        self.mgr = TaskManager(storage_path=self.tmp.name)

    def tearDown(self):
        if os.path.exists(self.tmp.name):
            os.remove(self.tmp.name)

    def test_add_and_list(self):
        t1 = self.mgr.add_task("First task")
        self.assertEqual(t1.id, 1)
        self.assertEqual(t1.title, "First task")
        self.assertFalse(t1.completed)

        tasks = self.mgr.list_tasks()
        self.assertEqual(len(tasks), 1)

    def test_complete_task(self):
        t1 = self.mgr.add_task("Complete me")
        res = self.mgr.complete_task(t1.id)
        self.assertIsNotNone(res)
        assert res is not None
        self.assertTrue(res.completed)

    def test_delete_task(self):
        t1 = self.mgr.add_task("Delete me")
        self.assertTrue(self.mgr.delete_task(t1.id))
        self.assertFalse(self.mgr.delete_task(999))
        self.assertEqual(len(self.mgr.list_tasks()), 0)

    def test_add_empty_title_raises_error(self):
        with self.assertRaises(ValueError):
            self.mgr.add_task("   ")

if __name__ == "__main__":
    unittest.main()
