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
    
    # Select and delete all objects in the scene
    bpy.ops.object.select_by_type(type='META')
    bpy.ops.object.delete()

    # Select and delete all objects in the scene
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.delete()
    
    # Optionally, you can remove any remaining objects like lights or cameras
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.select_by_type(type='CAMERA')
    bpy.ops.object.delete()

    # add a camera
    camera_data = bpy.data.cameras.new("CustomCamera")
    camera_obj = bpy.data.objects.new("CustomCamera", camera_data)
    bpy.context.collection.objects.link(camera_obj)

    # add a light source
    bpy.ops.object.light_add(type='SUN', radius=1, align='WORLD', location=(33.4475, 0.308792, 39.9238), scale=(1, 1, 1))
    new_light = bpy.context.active_object
    new_light.rotation_euler = (0, 0.97, -0.73)

file_path = 'link.txt' 
base_path = bpy.path.abspath('//')
with open(base_path + file_path, 'r') as file:
    file_contents = file.read()
    repo_path = file_contents.replace('\n', '')


prepare_scene()


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

    def add_branch(self, horizontal, height, direction, max_height):

        if max_height < 10:
            # Get the source scene and object
            source_scene = bpy.data.scenes["Tree Branch"]
            source_object = source_scene.objects["branch"]

            # Create a new object in the current scene by copying the source object
            branch = source_object.copy()
            branch.data = source_object.data.copy()

            # Link the new object to the current scene
            bpy.context.collection.objects.link(branch)

            # Make the new object the active object in the current scene
            bpy.context.view_layer.objects.active = branch

            # Select the new object
            branch.select_set(True)
            branch.modifiers["GeometryNodes"]["Socket_2"] = horizontal
            branch.modifiers["GeometryNodes"]["Socket_5"] = 3 / (height + 1) + 0.2
            bpy.context.object.modifiers["GeometryNodes"]["Socket_5"] = 1.4
            bpy.context.object.modifiers["GeometryNodes"]["Socket_9"] = max_height * 0.1


            branch.scale = (2,2,2)
            branch.location = (0, 0, height)
            branch.rotation_euler = (4.7, -13, np.pi / 2 * (- direction*2 + 1))
        elif horizontal > 4:
            # Get the source scene and object
            source_scene = bpy.data.scenes["Tree Branch"]
            source_object = source_scene.objects["branch"]

            # Create a new object in the current scene by copying the source object
            branch = source_object.copy()
            branch.data = source_object.data.copy()

            # Link the new object to the current scene
            bpy.context.collection.objects.link(branch)

            # Make the new object the active object in the current scene
            bpy.context.view_layer.objects.active = branch

            # Select the new object
            branch.select_set(True)
            branch.modifiers["GeometryNodes"]["Socket_2"] = horizontal
            branch.modifiers["GeometryNodes"]["Socket_5"] = 3 / (height + 1) + 0.2
            bpy.context.object.modifiers["GeometryNodes"]["Socket_5"] = 0.4
            bpy.context.object.modifiers["GeometryNodes"]["Socket_9"] = 0.4 + height / 100

            branch.scale = (2,2,2)
            branch.location = (0, 0, height)
            branch.rotation_euler = (4.7, -13, np.pi / 2 * (- direction*2 + 1)) 
        else:
            metaball = bpy.data.metaballs.new("Metaball")
            metaball_obj = bpy.data.objects.new("MetaballObject", metaball)

            # Link the metaball object to the current scene
            bpy.context.collection.objects.link(metaball_obj)

            # Make the metaball object the active object
            bpy.context.view_layer.objects.active = metaball_obj

            # Select the metaball object
            metaball_obj.select_set(True)

            # Add a new ball element to the metaball
            ball = metaball.elements.new(type='BALL')

            # Set the ball's parameters (e.g., radius)
            ball.radius = 2 - horizontal * horizontal + 3 / (height + 1)  # Adjust the radius as needed
            ball.co = (horizontal * (- direction*2 + 1), 0, height)


    def create_mesh_for_tree(self):

        height_threshold = 200
        # Create a new mesh
        mesh = bpy.data.meshes.new("SingleVertexMesh")
        obj = bpy.data.objects.new("SingleVertexObject", mesh)

        # Link the object to the scene
        bpy.context.collection.objects.link(obj)


        # calculate max_height
        max_height = 0
        for node in self.commits.values(): 
            if len(node.parents) > 1:
                max_height += 0.2

        max_height = min(max_height, height_threshold)

        # Set the object's location (optional)
        obj.location = (0, 0, 0)  # Set the location to the desired position

        # Create a single vertex and add it to the mesh
        height = 0
        horizontal = 0
        direction = True
        for i, node in enumerate(self.commits.values()): 
            if height > height_threshold: break # this is because otherwise the tree gets too big
            if len(node.parents) > 1:

                self.add_branch(horizontal, height, direction, max_height)

                horizontal = 0
                height += 0.2
                direction = not direction
                
            else:
                horizontal += 0.1

        if max_height > 10:
            bpy.ops.object.select_all(action='DESELECT')
            metaball_obj = bpy.data.objects.get('MetaballObject')
            bpy.context.view_layer.objects.active = metaball_obj
            metaball_obj.select_set(True)
            bpy.ops.object.convert(target='MESH')
            mesh_obj = bpy.context.active_object
        
            material = bpy.data.materials.get("Branch")
            mesh_obj.data.materials.append(material)
            bpy.context.view_layer.update()

        # Update the mesh and the scene
        mesh.update()

        # Make the object active (optional)
        bpy.context.view_layer.objects.active = obj

        camera_obj = bpy.data.objects.get("CustomCamera")
        camera_obj.location = (0, -2 * max_height - 10, 1)
        camera_obj.rotation_euler = (1.74, 0, 0)
        camera_obj.data.lens = 50

        # Set the camera object as the active camera
        bpy.context.scene.camera = camera_obj


        # Specify the source scene and collection name
        source_scene_name = "Tree Branch"  # Replace with the name of the source scene
        collection_name_to_copy = "env"    # Replace with the name of the collection you want to copy

        # Get the source scene and collection
        source_scene = bpy.data.scenes.get(source_scene_name)
        collection_to_copy = bpy.data.collections.get(collection_name_to_copy)

        # Check if the source scene and collection exist
        if source_scene and collection_to_copy:
            # Create a new collection in the current scene
            current_scene = bpy.context.scene
            new_collection = bpy.data.collections.new(collection_name_to_copy)

            # Link the new collection to the current scene
            current_scene.collection.children.link(new_collection)

            # Copy the objects from the source collection to the new collection
            for obj in collection_to_copy.objects:
                new_obj = obj.copy()
                new_obj.data = obj.data.copy()
                new_collection.objects.link(new_obj)


repo = Repo(repo_path)
git_tree = GitCommitTree(repo)
git_tree.create_mesh_for_tree()
