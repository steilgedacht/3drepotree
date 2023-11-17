import git
from git import Git
from git.objects import commit
import bpy
from git import Repo
from tqdm import tqdm

import numpy as np

print()

def prepare_scene():
    bpy.ops.object.select_all(action='DESELECT')

    # Select and delete all objects in the scene
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Optionally, you can remove any remaining objects like lights or cameras
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.select_by_type(type='CAMERA')
    bpy.ops.object.delete()
    bpy.ops.mesh.primitive_cube_add(size=2, location=(-10, 0, 0))

prepare_scene()

repo_path = '/home/benjamin/Schreibtisch/JKU/Semester 4/Pattern Classification/repository/bird_boy/'
# repo_path = "/home/benjamin/Schreibtisch/JKU/Semester 5/Missing Semester/first_project/"
repo_path = '/home/benjamin/Dokumente/tmp/logseq_rep/logseq/'

class CommitNode:
    def __init__(self, commit_hash, parent_hashes, message, author, date, idx):
        self.commit_hash = commit_hash
        self.parent_hashes = parent_hashes  # List of parent commit hashes
        self.parents = []
        self.message = message
        self.author = author
        self.date = date
        self.children = []
        self.id = idx

    def add_child(self, child_commit):
        if child_commit not in self.children:
            self.children.append(child_commit)

    def add_parent(self, parent_commit):
        if parent_commit not in self.parents:
            self.parents.append(parent_commit)

class GitCommitTree:
    def __init__(self, Repo):
        self.commits = {}
        self.REPO = Repo

        print(len(list(Repo.iter_commits())))
        for commit in tqdm(Repo.iter_commits()):
            self.add_gitpython_commit(commit, False)
        self.update_parents()

        self.root_hash = repo.head.commit.hexsha

    def add_commit(self, commit, update=True):
        if commit.commit_hash in self.commits.keys():
            return

        self.commits[commit.commit_hash] = commit
        if update:
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

    def print_tree_graphical(self, commit_hash=None, prefix="", is_tail=True):
        if commit_hash is None:
            commit_hash = self.root_hash
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

    def add_gitpython_commit(self, git_commit, update=True):
        commit_hash = git_commit.hexsha
        parent_hashes = [parent.hexsha for parent in git_commit.parents]
        author = git_commit.author.name
        message = git_commit.message.strip().split('\n')[0]  # Get the first line of the commit message
        date = git_commit.authored_datetime

        commit_node = CommitNode(commit_hash, parent_hashes, message, author, date, len(self.commits))
        self.add_commit(commit_node, update)

    def create_mesh_for_tree(self):

        radius = 0.5
        # Create a new mesh
        mesh = bpy.data.meshes.new("SingleVertexMesh")
        obj = bpy.data.objects.new("SingleVertexObject", mesh)

        # Link the object to the scene
        bpy.context.collection.objects.link(obj)

        # Set the object's location (optional)
        obj.location = (0, 0, 0)  # Set the location to the desired position

        # Create a single vertex and add it to the mesh
        height = 0
        horizontal = 0
        direction = True
        for i, node in enumerate(self.commits.values()): 
            mesh.vertices.add(1)

            if len(node.parents) > 1:
                horizontal = 0
                height += 0.2
                direction = not direction
            else:
                horizontal += 0.1
            mesh.vertices[-1].co = (
                horizontal * (1 -  2 *int(direction)), 
                0, 
                height)

        # Update the mesh and the scene
        mesh.update()

        # Make the object active (optional)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_add(type='SKIN')
        bpy.ops.object.modifier_add(type='SUBSURF')

        obj.modifiers.new("part", type='PARTICLE_SYSTEM')
        part = obj.particle_systems[0]

        settings = part.settings
        settings.type = 'HAIR'
        settings.emit_from = 'VERT'
        settings.use_modifier_stack = True
        settings.render_type = "OBJECT"
        settings.instance_object = bpy.data.objects['Cube']
        settings.particle_size = 0.02
        settings.count = 100

        # ps = bpy.ops.object.particle_system_add()
        # bpy.data.particles["ParticleSettings"].type = 'HAIR'
        # bpy.data.particles["ParticleSettings"].emit_from = 'VERT'
        # bpy.data.particles["ParticleSettings"].use_modifier_stack = True

repo = Repo(repo_path)
git_tree = GitCommitTree(repo)
git_tree.create_mesh_for_tree()
