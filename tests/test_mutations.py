import os
import json
from git2gpt.core import apply_gpt_mutations
from pyfakefs.fake_filesystem_unittest import TestCase


class TestGPTMutations(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_add_file(self):
        repo_path = "/repo"
        os.makedirs(repo_path)
        mutations = [
            {
                "action": "add",
                "file_path": "new_file.txt",
                "content": "This is a new file.",
            }
        ]
        apply_gpt_mutations(repo_path, mutations)

        new_file_path = os.path.join(repo_path, "new_file.txt")
        self.assertTrue(os.path.exists(new_file_path))
        with open(new_file_path, "r") as f:
            content = f.read()
        self.assertEqual(content, "This is a new file.")

    def test_modify_file(self):
        repo_path = "/repo"
        os.makedirs(repo_path)
        file_path = os.path.join(repo_path, "existing_file.txt")
        with open(file_path, "w") as f:
            f.write("This is the original content.")

        mutations = [
            {
                "action": "modify",
                "file_path": "existing_file.txt",
                "content": "This is the modified content.",
            }
        ]
        apply_gpt_mutations(repo_path, mutations)

        with open(file_path, "r") as f:
            content = f.read()
        self.assertEqual(content, "This is the modified content.")

    def test_delete_file(self):
        repo_path = "/repo"
        os.makedirs(repo_path)
        file_path = os.path.join(repo_path, "file_to_delete.txt")
        with open(file_path, "w") as f:
            f.write("This file will be deleted.")

        mutations = [{"action": "delete", "file_path": "file_to_delete.txt"}]
        apply_gpt_mutations(repo_path, mutations)

        self.assertFalse(os.path.exists(file_path))

    def test_delete_empty_directory(self):
        repo_path = "/repo"
        os.makedirs(repo_path)
        dir_path = os.path.join(repo_path, "empty_dir")
        os.makedirs(dir_path)

        mutations = [{"action": "delete", "file_path": "empty_dir"}]
        apply_gpt_mutations(repo_path, mutations)

        self.assertFalse(os.path.exists(dir_path))


if __name__ == "__main__":
    from unittest import main

    main()
