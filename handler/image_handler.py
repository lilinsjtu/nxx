# -*- coding:utf-8 -*-
__author__ = 'lilin'

from PIL import Image
import os
import time

# 打开图片目录
srcImgFolder = r"uploads"
# 保存图片目录
saveImgFolder = srcImgFolder + os.sep + r"dst"
# 缩放图片比例(100,200,400,600)
targetWidthArray = (480,)
targetHeightArray = (480,)


# resize all file in src folder to save folder
def resizeFold(dir_proc):
    for file in os.listdir(dir_proc):
        if dir_proc == saveImgFolder:
            return
        fullFile = os.path.join(dir_proc, file)
        if os.path.isdir(fullFile):
            resizeFold(fullFile)
            continue

        # 带有下划线的目标图片不需要处理
        # if fullFile.find("_") != -1:
        #    continue

        # 正常图片
        srcImgFullFileName = fullFile
        print "INFO:process file %s" % (os.path.join(dir_proc, file))
        # 处理文件
        if os.path.isfile(srcImgFullFileName):
            folderPath = srcImgFullFileName[:srcImgFullFileName.rfind(os.sep)]
            fileName = srcImgFullFileName[srcImgFullFileName.rfind(os.sep) + 1:]

            img = Image.open(srcImgFullFileName)
            #           img.show()
            width, height = img.size
            if width > height:
                for targetWidth in targetWidthArray:
                    targetImg = img.resize(
                        (targetWidth, targetWidth * height / width),
                        Image.ANTIALIAS
                    )
                    # newFileName = fileName.split(".")[0] + "_" + str(targetWidth) + "." + fileName.split(".")[1]
                newFileName = str(time.time()) + "_w" + str(targetWidth) + "." + fileName.split(".")[1]
            else:
                for targetHeight in targetHeightArray:
                    targetImg = img.resize(
                        (targetHeight * width / height, targetHeight),
                        Image.ANTIALIAS
                    )
                newFileName = str(time.time()) + "_h" + str(targetHeight) + "." + fileName.split(".")[1]
            targetImg.save(saveImgFolder + os.sep + newFileName, 'jpeg')


if __name__ == "__main__":
    if os.path.exists(srcImgFolder):
        if not os.path.exists(saveImgFolder):
            os.mkdir(saveImgFolder)
        resizeFold(srcImgFolder)
    else:
        print "文件目录不存在"

'''
    python图片处理
    @author:fc_lamp
    @blog:http://fc-lamp.blog.163.com/
'''


# 等比例压缩图片
def resizeImg(**args):
    args_key = {'ori_img': '', 'dst_img': '', 'dst_w': '', 'dst_h': '', 'save_q': 75}
    arg = {}
    for key in args_key:
        if key in args:
            arg[key] = args[key]

    im = Image.open(arg['ori_img'])
    ori_w, ori_h = im.size
    widthRatio = heightRatio = None
    ratio = 1
    if (ori_w and ori_w > arg['dst_w']) or (ori_h and ori_h > arg['dst_h']):
        if arg['dst_w'] and ori_w > arg['dst_w']:
            widthRatio = float(arg['dst_w']) / ori_w  # 正确获取小数的方式
        if arg['dst_h'] and ori_h > arg['dst_h']:
            heightRatio = float(arg['dst_h']) / ori_h

        if widthRatio and heightRatio:
            if widthRatio < heightRatio:
                ratio = widthRatio
            else:
                ratio = heightRatio

        if widthRatio and not heightRatio:
            ratio = widthRatio
        if heightRatio and not widthRatio:
            ratio = heightRatio

        newWidth = int(ori_w * ratio)
        newHeight = int(ori_h * ratio)
    else:
        newWidth = ori_w
        newHeight = ori_h

    im.resize((newWidth, newHeight), Image.ANTIALIAS).save(arg['dst_img'], quality=arg['save_q'])

    '''
    image.ANTIALIAS还有如下值：
    NEAREST: use nearest neighbour
    BILINEAR: linear interpolation in a 2x2 environment
    BICUBIC:cubic spline interpolation in a 4x4 environment
    ANTIALIAS:best down-sizing filter
    '''


# 裁剪压缩图片
def clipResizeImg(**args):
    args_key = {'ori_img': '', 'dst_img': '', 'dst_w': '', 'dst_h': '', 'save_q': 75}
    arg = {}
    for key in args_key:
        if key in args:
            arg[key] = args[key]

    im = Image.open(arg['ori_img'])
    ori_w, ori_h = im.size

    dst_scale = float(arg['dst_h']) / arg['dst_w']  # 目标高宽比
    ori_scale = float(ori_h) / ori_w  # 原高宽比

    if ori_scale >= dst_scale:
        # 过高
        width = ori_w
        height = int(width * dst_scale)

        x = 0
        y = (ori_h - height) / 3

    else:
        # 过宽
        height = ori_h
        width = int(height * dst_scale)

        x = (ori_w - width) / 2
        y = 0

    # 裁剪
    box = (x, y, width + x, height + y)
    # 这里的参数可以这么认为：从某图的(x,y)坐标开始截，截到(width+x,height+y)坐标
    # 所包围的图像，crop方法与php中的imagecopy方法大为不一样
    newIm = im.crop(box)
    im = None

    # 压缩
    ratio = float(arg['dst_w']) / width
    newWidth = int(width * ratio)
    newHeight = int(height * ratio)
    newIm.resize((newWidth, newHeight), Image.ANTIALIAS).save(arg['dst_img'], quality=arg['save_q'])


# 水印(这里仅为图片水印)
def waterMark(**args):
    args_key = {'ori_img': '', 'dst_img': '', 'mark_img': '', 'water_opt': ''}
    arg = {}
    for key in args_key:
        if key in args:
            arg[key] = args[key]

    im = Image.open(arg['ori_img'])
    ori_w, ori_h = im.size

    mark_im = Image.open(arg['mark_img'])
    mark_w, mark_h = mark_im.size
    option = {'leftup': (0, 0), 'rightup': (ori_w - mark_w, 0), 'leftlow': (0, ori_h - mark_h),
              'rightlow': (ori_w - mark_w, ori_h - mark_h)
              }

    im.paste(mark_im, option[arg['water_opt']], mark_im.convert('RGBA'))
    im.save(arg['dst_img'])

# 裁剪压缩
# clipResizeImg(ori_img=ori_img, dst_img=dst_img, dst_w=dst_w, dst_h=dst_h, save_q=save_q)
# 等比例压缩
# resizeImg(ori_img=ori_img,dst_img=dst_img,dst_w=dst_w,dst_h=dst_h,save_q=save_q)
# 水印
# waterMark(ori_img=ori_img,dst_img=dst_img,mark_img=mark_img,water_opt=water_opt)
