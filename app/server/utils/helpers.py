import os, uuid
from PIL import Image

def save_new_photo(file):
    filename = str(uuid.uuid4())

    _, f_ext = os.path.splitext(file.filename)

    picture_fn = filename + f_ext

    picture_path = os.path.join(app.root_path,"static/images", picture_fn)

    output_size = (500, 500)

    i = Image.open(file)

    i.thumbnail(output_size)

    i.save(picture_path)