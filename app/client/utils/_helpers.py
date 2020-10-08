import os, uuid, base64
from random import randint
from flask import current_app, session, flash
from PIL import Image

def save_new_photo(file):
    try:
        filename = str(uuid.uuid4())

        _, f_ext = os.path.splitext(file.filename)

        picture_fn = filename + f_ext

        picture_path = os.path.join(app.root_path,"static/images", picture_fn)

        output_size = (500, 500)

        i = Image.open(file)

        i.thumbnail(output_size)

        i.save(picture_path)

    except:
        return 500

