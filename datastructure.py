from git import Repo

class CommitNode:
    def __init__(self, commit_hash, parent_hashes, message, author, date):
        self.commit_hash = commit_hash
        self.parent_hashes = parent_hashes  # List of parent commit hashes
        self.parents = []
        self.message = message
        self.author = author
        self.date = date
        self.children = []

    def add_child(self, child_commit):
        if child_commit not in self.children:
            self.children.append(child_commit)

    def add_parent(self, parent_commit):
        if parent_commit not in self.parents:
            self.parents.append(parent_commit)

class GitCommitTree:
    def __init__(self, Repo):
        self.commits = {}  # Dictionary to store commits with their hashes as keys
        self.REPO = Repo
        self.root_hash = None

    def add_commit(self, commit):
        if commit.commit_hash in self.commits.keys():
            return

        self.commits[commit.commit_hash] = commit
        self.update_parents()
    
    def update_parents(self):
        for commit in self.commits.values():
            for parent_hash in commit.parent_hashes:
                if parent_hash not in self.commits.keys():
                    continue
                self.commits[parent_hash].add_child(commit)
                self.commits[commit.commit_hash].add_parent(self.commits[parent_hash])


    def get_commit(self, commit_hash):
        return self.commits.get(commit_hash, None)

    def print_tree_graphical(self, commit_hash, prefix="", is_tail=True):
        commit = self.get_commit(commit_hash)
        if not commit:
            return

        connector = "└── " if is_tail else "├── "
        print(prefix + connector + f"Commit: {commit.commit_hash}, Author: {commit.author}, Date: {commit.date}, Message: {commit.message}")

        if commit.parents:
            extension = "    " if is_tail else "|   "
            new_prefix = prefix + extension
            for i, parent in enumerate(commit.parents):
                is_last_parent = (i == len(commit.parents) - 1)
                self.print_tree_graphical(parent.commit_hash, new_prefix, is_last_parent)

    def add_gitpython_commit(self, git_commit):
        commit_hash = git_commit.hexsha
        parent_hashes = [parent.hexsha for parent in git_commit.parents]
        author = git_commit.author.name
        message = git_commit.message.strip().split('\n')[0]  # Get the first line of the commit message
        date = git_commit.authored_datetime

        commit_node = CommitNode(commit_hash, parent_hashes, message, author, date)
        self.add_commit(commit_node)

repo_path = '/home/benjamin/Schreibtisch/JKU/Semester 5/Missing Semester/first_project/' 
repo = Repo(repo_path)
git_tree = GitCommitTree(repo)

for commit in repo.iter_commits():
    git_tree.add_gitpython_commit(commit)

root_hash = repo.head.commit.hexsha
git_tree.root_hash = repo.head.commit.hexsha
git_tree.print_tree_graphical(root_hash)
