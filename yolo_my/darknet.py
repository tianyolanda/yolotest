# 存放yolo的网络结构

from __future__ import division
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np

def parse_cfg(cfgfile):
    #这部分是在解析cfg文件,理解里面的text并按模块存储到blocks这个list里面,list里有很多个字典{},每个字典存储了一个block,也就是一个小conv或者cut模块
    file = open(cfgfile,'r')
    lines = file.read().split('\n') # 将文件中的所有行,存在一个list里面
    lines = [x for x in lines if len(x) > 0 ]  # 将非空行存在x里面
    lines = [x for x in lines if x[0] !='#'] # 去掉其中的注释行
    lines = [x.rstrip().lstrip() for x in lines] # # 去掉每行的头尾符
    block = {}
    blocks = []

    for line in lines:
        if line[0] == "[": # 如果开始了一个新的block
            if len(block) != 0 : # 但是老的block还没有被存储和删去
                blocks.append(block) # 首先存储老的block
                block = {} # 再把旧的内容删去
            block["type"] = line[1:-1].rstrip() #将[]内的字,记录到block"type"中
        else:
            key,value = line.split("=") # 将键值对拆分,比如 stride = 1
            block[key.rstrip()] = value.lstrip() # key去头,作为标签; value去尾, 作为值

    blocks.append(block) # 最后要把最后一个block给加入到blocks里面去

    return blocks
#
# m = parse_cfg('cfg/yolov3.cfg')
# print(m[0])

#接下来需要依次解析这些block,并把他们生成pytorch module, 除了convlution和upsample已经被pytorch定义好了,其他的都需要自己实现
def create_modules(blocks):
    net_info = blocks[0] #输出的是第一个block--net的全部内容
    module_list = nn.ModuleList()
    prev_filters = 3
    output_filters = []



