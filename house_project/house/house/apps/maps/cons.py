import os

from django.conf import settings


from info.models import SelecttData
import csv


import base64

import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from io import BytesIO
import os

from django.conf import settings
from django.template import loader
from pylab import mpl
from rest_framework.views import APIView






def scv_file():
    try:
        datas = SelecttData.objects.all()
    except:
        return False
    file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'house_csv.csv')
    analysis_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'analysis.csv')
    out = open(file_path, 'w', newline='')
    any = open(analysis_path, 'w', newline='')
    csv_write = csv.writer(out, dialect='excel')
    csv_any = csv.writer(any, dialect='excel')
    for data in datas:
        data_list=[]
        data_list.append((data.address_wu+data.address_qu+data.address_detail))
        data_list.append(data.price*10000)
        data_list.append('http://127.0.0.1:8080/detail.html?id=%s'%data.id)
        csv_write.writerow(data_list)


    out.close()

    csv_any.writerow(['address_wu','address_qu','vides','price','area','houseType','buildYear','buildType','tagList','decorate','tradeOwership'])
    for data in datas:
        data_list = [data.address_wu,data.address_qu,data.vides,data.price,data.area,data.houseType,data.buildYear,data.buildType,data.tagList,data.decorate,data.tradeOwnership]
        csv_any.writerow(data_list)

    any.close()






