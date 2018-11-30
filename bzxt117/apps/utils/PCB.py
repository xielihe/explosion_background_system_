import os
from bzxt117.settings import MEDIA_ROOT,BASE_DIR

path2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def getPCB(id,type):
    # print(os.path.abspath('.'))
    # os.popen("./getPCB.exe", 'w').write(str(1.2) + r' ' + "Sample")
    # os.popen("./getPCB.exe", 'r')

    path = os.path.join(path2, 'utils/getPCB.exe')
    # type是"Sample"
    os.popen(path + r' '+str(id) + r' ' + type).read()

    # os.system(path + str(1.2) + r' ' + "Sample")

def segComp(id,type):
    path = os.path.join(path2, 'utils/segComp.exe')
    os.popen(path+r' '+str(id)+r' '+type).read()



def CompMatching(id):
    path = os.path.join(path2, 'utils/CompMatching.exe')
    os.popen(path + r' ' + str(id)).read()

def FeatureMatching(id):
    path = os.path.join(path2, 'utils/FeatureMatching.exe')
    os.popen(path + r' ' + str(id)).read()




