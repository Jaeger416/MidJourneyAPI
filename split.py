import os
import json
from tqdm import tqdm
from PIL import Image

path = "/media/caesar/Expansion/MDJ"
save_path = "/media/caesar/Expansion/new_mdj"
def split_image(image_name):
    image_path = os.path.join(path, image_name)
    image = Image.open(image_path)

    width, height = image.size


    left_top = (0, 0, width / 2, height / 2)

    right_top = (width / 2, 0, width, height / 2)

    left_bottom = (0, height / 2, width / 2, height)

    right_bottom = (width / 2, height / 2, width, height)

    # 拆分图像并保存
    image.crop(left_top).save(os.path.join(save_path, '0', image_name))
    image.crop(right_top).save(os.path.join(save_path, '1', image_name))
    image.crop(left_bottom).save(os.path.join(save_path, '2', image_name))
    image.crop(right_bottom).save(os.path.join(save_path, '3', image_name))
    
data = json.load(open("/media/caesar/Expansion/new_1.json", 'r'))
for d in tqdm(data):
    assert os.path.exists(os.path.join(path, d['filename']))
    split_image(d['filename'])