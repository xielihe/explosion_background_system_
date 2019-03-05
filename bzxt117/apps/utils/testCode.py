import os
import shutil

from bzxt117.settings import MEDIA_ROOT




matchUrl = os.path.join(MEDIA_ROOT, "image/devShapeEvi/match/" + str(1) + "/")
shutil.rmtree(matchUrl)