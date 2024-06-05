from collections import defaultdict
import os
from glob import glob
import numpy as np
import shutil

#-----------------------------------------------------------------------------------------------------------------------------
def get__class_id__group_id(utm_east, utm_north, heading, M, alpha, N, L):
        """Return class_id and group_id for a given point.
            The class_id is a triplet (tuple) of UTM_east, UTM_north and
            heading (e.g. (396520, 4983800,120)).
            The group_id represents the group to which the class belongs
            (e.g. (0, 1, 0)), and it is between (0, 0, 0) and (N, N, L).
        """
        rounded_utm_east = int(utm_east // M * M)  # Rounded to nearest lower multiple of M
        rounded_utm_north = int(utm_north // M * M)
        rounded_heading = int(heading // alpha * alpha)
        
        class_id = (rounded_utm_east, rounded_utm_north, rounded_heading)
        # group_id goes from (0, 0, 0) to (N, N, L)
        group_id = (rounded_utm_east % (M * N) // M,
                    rounded_utm_north % (M * N) // M,
                    rounded_heading % (alpha * L) // alpha)
        return class_id, group_id

#-----------------------------------------------------------------------------------------------------------------------------
def read_images_paths(folder_name):
  """
  Read image paths and save them in a list.
  """
  #check if folder exists
  if not os.path.exists(folder_name):
          raise FileNotFoundError(f"Folder {folder_name} does not exist")
  else:
      # Use glob to return a list of jpg files
      images_paths = sorted(glob(f"{folder_name}/**/*.jpg", recursive=True))
      # Remove folder_name from the path
      images_paths = [p[len(folder_name) + 1:] for p in images_paths]
  return images_paths


#-----------------------------------------------------------------------------------------------------------------------------
def get_metadata_from_images_paths(images_paths):
  """Returns the metadata extracted from the images paths
  """
  images_metadatas = [p.split("@") for p in images_paths]
  utmeast_utmnorth_heading = [(m[1], m[2], m[9]) for m in images_metadatas]
  utmeast_utmnorth_heading = [(float(x) if x else 0, float(y) if y else 0, float(z) if z else 0) for x, y, z in utmeast_utmnorth_heading]
  utmeast_utmnorth_heading = np.array(utmeast_utmnorth_heading)

  return utmeast_utmnorth_heading

#-----------------------------------------------------------------------------------------------------------------------------
def divide_images_into_classes(images_paths):
  """Divides the images into classes and returns a dict of images per class"""

  print("For each image, get class and group to which it belongs")
  class_id__group_id = [get__class_id__group_id(*m, M=10, alpha=30, N=5, L=2) for m in get_metadata_from_images_paths(images_paths)]

  print("Group together images belonging to the same class")
  images_per_class = defaultdict(list)
  for image_path, (class_id,_) in zip(images_paths, class_id__group_id):
      images_per_class[class_id].append(image_path)

  # Images_per_class is a dict where the key is class_id, and the value
  # is a list with the paths of images within that class.
  images_per_class = {k: v for k, v in images_per_class.items() if len(v) >= 10}

  print("Group together classes belonging to the same group")
  # Classes_per_group is a dict where the key is group_id, and the value
  # is a list with the class_ids belonging to that group.
  classes_per_group = defaultdict(set)
  for class_id, group_id in class_id__group_id:
      if class_id not in images_per_class:
          continue  # Skip classes with too few images
      classes_per_group[group_id].add(class_id)

  # Convert classes_per_group to a list of lists.
  # Each sublist represents the classes within a group.
  classes_per_group = [list(c) for c in classes_per_group.values()]

  return images_per_class


#-----------------------------------------------------------------------------------------------------------------------------
def create_classes_folders(images_paths, source_folder):
  """Creates folders for each class and fills them with images"""
  # Get the keys of the dictionary and sort them
  images_per_class = divide_images_into_classes(images_paths)
  keys = sorted(images_per_class.keys())

  # Create a new dictionary to map the incremental ids to the original keys
  id_to_key = {i: k for i, k in enumerate(keys)}

  # Create the folders
  for i in id_to_key.keys():
      print(f"Creating folder {i}...")
      # Get the original key
      key = id_to_key[i]
      # Create the folder name
      folder_name = f"{i}"
      # Create the full path of the folder
      folder_path = os.path.join("data" + os.sep + "train", folder_name)
      # Create the folder
      os.makedirs(folder_path, exist_ok=True)

      # Copy the images to the folder
      print(f"Copying images to folder {i}...")
      for image_path in images_per_class[key]:
          # Create the full path of the image
          image_full_path = os.path.join(source_folder, image_path)
          # Create the new path of the image
          #new_path = os.path.join(folder_path, image_path)
          # Copy the image
          shutil.copy(image_full_path, folder_path)


        

