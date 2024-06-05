from utils import read_images_paths, create_classes_folders


train_folder = "data/small/train"

images_paths = read_images_paths(train_folder)
create_classes_folders(images_paths, train_folder)