import git
from git import Git
from git.objects import commit
import bpy
import numpy as np

print()

repo_path = '/home/benjamin/Schreibtisch/JKU/Semester 5/Missing Semester/first_project/'

# Datastructure for the tree
class Node:
    def __init__(self, hash_value, idx):
        self.hash = hash_value
        self.parent = []
        self.child = []
        self.id = idx
    
    def __repr__(self):
        return f"Commit {self.hash}"

# Datastructure for the Tree
class CommitTree:
    def __init__(self, repo_path):

        self.start_node = None
        self.nodes = {}

        repo = git.Repo(repo_path)
        all_commits = list(repo.iter_commits())
        for commit_obj in all_commits:
            commit_info = self.build_commit_tree(commit_obj) 
            self.nodes[commit_info.hash] = commit_info
            
        self.recalculate_start_node()
        self.update_children()
        pass
            
    def recalculate_start_node(self):
        for node in self.nodes.keys():
            if self.nodes[node].parent == []:
                self.start_node = node

    def update_children(self):
        for node in list(self.nodes.values()):
            for parent in node.parent:
                self.nodes[parent.hash].child.append(node)

    def build_commit_tree(self, commit_obj):
        commit_node = Node(commit_obj.hexsha, len(self.nodes.keys()))

        for parent_commit in commit_obj.parents:
            parent_node = self.build_commit_tree(parent_commit)
            commit_node.parent.append(parent_node)

        return commit_node
    
    def create_mesh_for_tree(self):
        # Create a new mesh
        mesh = bpy.data.meshes.new("SingleVertexMesh")
        obj = bpy.data.objects.new("SingleVertexObject", mesh)

        # Link the object to the scene
        bpy.context.collection.objects.link(obj)

        # Set the object's location (optional)
        obj.location = (0, 0, 0)  # Set the location to the desired position

        # Create a single vertex and add it to the mesh
        for i, node in enumerate(self.nodes.values()): 
            mesh.vertices.add(1)
            mesh.vertices[-1].co = (np.cos(np.random.rand() * 2 * np.pi), np.sin(np.random.rand() * 2 * np.pi), node.id)  # Set the vertex's position

            for child in node.child:
                mesh.edges.add(1)
                mesh.edges[-1].vertices = [child.id, node.id]


        # Update the mesh and the scene
        mesh.update()

        # Make the object active (optional)
        bpy.context.view_layer.objects.active = obj


c = CommitTree(repo_path)
c.create_mesh_for_tree()

