## Git Branches to 3d Tree

With this project you can generate a 3d tree from your commit history of a repository.

Just enter your downloaded repository link as a absolute path in the `link.txt` file

```bash
blender -b model_creation.blend -P render_git.py -o render/ -F PNG -f 1
```

## ✴️ Video Tutorial and Demonstration ✴️

[Watch the demo video](https://youtu.be/waMOTfSbYbM)


## Quickstart 

Prerequisites:
 - This software was only tested on linux
 - Blender >= 4 (because of geometry nodes)
 - python 3 with the packages
   - git
   - bpy
   - tqdm
   - numpy

Step-by-step:

1. Download the Git Repository that you want to render (not needed if it you have a local repository)
2. copy the absolute path of the repository
3. save the path into the link.txt file
4. execute from the root of the repository  

`blender -b model_creation.blend -P render_git.py -o render/ -F PNG -f 1`

5. The rendered image should appear after ~30 seconds of waiting in the render directory with the name 0001.png

## Examples of Open Source Projects

### Logseq
https://github.com/logseq/logseq

![Logseq](render/logseq.png)


### Transformer
https://github.com/huggingface/transformers
![transformer](render/huggingface_transformer.png)


### Numpy
https://github.com/numpy/numpy
![Numpy](render/numpy.png)


### Pytorch
https://github.com/pytorch/pytorch
![Pytorch](render/pytorch.png)


### Gimp
https://github.com/GNOME/gimp
![Gimp](render/gimp.png)

