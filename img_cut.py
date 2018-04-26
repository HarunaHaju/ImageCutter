# _*_ coding:utf-8 _*_
from PIL import Image
import sys
import os


class ImgCutter:
    filePath = None
    savePath = 'result'
    img = None
    size = 3

    def argv_parser(self, argv):
        for i in range(1, len(argv), 2):
            if argv[i] == '-fromfile':
                self.filePath = argv[i + 1]
            if argv[i] == '-save2':
                self.savePath = argv[i + 1]
            if argv[i] == '-size':
                self.size = int(argv[i + 1])

    def __init__(self, argv=[]):
        self.argv_parser(argv)

    @staticmethod
    def cut_img(image, size):
        width, height = image.size
        item_width = int(width / size)
        box_list = []
        for i in range(0, size):
            for j in range(0, size):
                box = (j * item_width, i * item_width, (j + 1) * item_width, (i + 1) * item_width)
                box_list.append(box)
        image_list = [image.crop(box) for box in box_list]
        return image_list

    @staticmethod
    def fill_image(image):
        width, height = image.size
        new_image_length = width if width > height else height
        new_image = Image.new(image.mode, (new_image_length, new_image_length), color='white')
        if width > height:
            new_image.paste(image, (0, int((new_image_length - height) / 2)))
        else:
            new_image.paste(image, (int((new_image_length - width) / 2), 0))
        return new_image

    @staticmethod
    def save_images(image_list, save_path):
        index = 1
        for image in image_list:
            image.save('./' + save_path + '/' + str(index) + '.png', 'PNG')
            index += 1

    def cut(self):
        if self.filePath is None:
            print("please input file path")
            return
        if os.path.exists(self.filePath) is False:
            print("file does not exist")
            return
        if os.path.exists(self.savePath) is False:
            os.mkdir(self.savePath)
        self.img = Image.open(self.filePath)
        self.img = self.fill_image(self.img)
        img_list = self.cut_img(self.img, self.size)
        self.save_images(img_list, save_path=self.savePath)


if __name__ == '__main__':
    cutter = ImgCutter(sys.argv)
    cutter.cut()
