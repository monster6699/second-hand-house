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


class StaticAsansy(APIView):
    def get(self,request):
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        mpl.rcParams['axes.unicode_minus'] = False
        analysis_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'analysis.csv')
        house_data = pd.read_csv(analysis_path)
        house_count = house_data.groupby('address_qu').size().sort_values(ascending=False)
        asd, sdf = plt.subplots(1, 1, dpi=150)
        house_count.plot(kind='bar')
        plt.title("各区的房屋数量")
        buffer = BytesIO()
        plt.savefig(buffer)
        plot_data = buffer.getvalue()
        imb = base64.b64encode(plot_data)  # 对plot_data进行编码
        ims = imb.decode()
        imd = "data:image/png;base64," + ims
        context = {
            'imd': imd
        }
        template = loader.get_template('house_count.html')
        html_text = template.render(context)
        file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'house_count.html')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_text)
