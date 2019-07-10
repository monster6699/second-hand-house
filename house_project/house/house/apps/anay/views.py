

import base64
import threading
import time

import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
plt.switch_backend('agg')
from io import BytesIO
import os

from django.conf import settings
from django.template import loader
from pylab import mpl
from rest_framework.response import Response
from rest_framework.views import APIView

from celery_tasks.static_html import tasks



    # def globaldel(self):
    #     mpl.rcParams['font.sans-serif'] = ['SimHei']
    #     mpl.rcParams['axes.unicode_minus'] = False
    #     analysis_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'analysis.csv')
    #     house_data = pd.read_csv(analysis_path)
    #
    #     return house_data



class addressQuCount(APIView):
    def get(self, request):
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        mpl.rcParams['axes.unicode_minus'] = False
        analysis_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'analysis.csv')
        house_data = pd.read_csv(analysis_path)

        house_count = house_data.groupby('address_qu').size().sort_values(ascending=False)
        plt.subplots(1, 1, dpi=150)
        house_count.plot(kind='bar')
        plt.title("市区的房屋数量")
        buffer = BytesIO()
        plt.savefig(buffer)
        plot_data = buffer.getvalue()
        imb = base64.b64encode(plot_data)  # 对plot_data进行编码
        ims = imb.decode()
        imd = "data:image/png;base64," + ims
        context = {
            'imd': imd
        }
        plt.close()
        template = loader.get_template('house_count.html')
        html_text = template.render(context)
        file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'address_qu_count.html')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_text)
        return Response('./address_qu_count')

        # 户型数量
class houseTypeCount(APIView):
    def get(self,request):
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        mpl.rcParams['axes.unicode_minus'] = False
        analysis_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'analysis.csv')
        house_data = pd.read_csv(analysis_path)
        temp_list = house_data['houseType'].values
        houseType_list = pd.unique(temp_list)
        houseType_count = pd.DataFrame(np.zeros([house_data.shape[0], houseType_list.shape[0]]), columns=houseType_list)
        for i in range(houseType_count.shape[0]):
            houseType_count.ix[i, temp_list[i]] = 1
        plt.subplots(1, 1, dpi=150)
        houseType_count.sum().plot(kind='bar', title="户型数量", )

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
        file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'houseType_count.html')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_text)
        plt.close()

        return Response('houseType_count')

class areaPrice(APIView):
    def get(self, request):
        # 探究房屋面积和房屋价格的关系
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        mpl.rcParams['axes.unicode_minus'] = False
        analysis_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'analysis.csv')
        house_data = pd.read_csv(analysis_path)
        y = list(house_data['price'].values)
        x = list(house_data['area'].values)
        # 1.创建画布
        plt.figure(figsize=(20, 8), dpi=200)
        # plt.subplots(1,1,dpi=150)
        # 2.绘制散点图
        plt.scatter(x, y)
        plt.suptitle('房屋面积与价格的关系', fontsize=18)
        # 3.显示图像
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
        file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'area_price.html')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_text)

        return Response('ok-anay')

class houseTypeVide(APIView):
    def get(self, request):
        # 户型与关注人数的分布
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        mpl.rcParams['axes.unicode_minus'] = False
        analysis_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'analysis.csv')
        house_data = pd.read_csv(analysis_path)
        type_interest_group = house_data['vides'].groupby(house_data['houseType']).agg(
            [('户型', 'count'), ('带看人数', 'sum')])
        type_interest_group = type_interest_group[type_interest_group['户型'] > 20]
        asd, sdf = plt.subplots(1, 1, dpi=150)
        type_interest_group.plot(kind='barh', alpha=0.7, grid=True, ax=sdf)
        plt.title('二手房户型和带看人数分布')
        plt.ylabel('户型')

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
        file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'houseType_vide.html')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_text)
        plt.close()

        return Response('ok-anay')

class addressQuAvg(APIView):
    def get(self, request):
        # 各区的房屋均价
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        mpl.rcParams['axes.unicode_minus'] = False
        analysis_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'analysis.csv')
        house_data = pd.read_csv(analysis_path)
        count = house_data.groupby(['address_qu'])['price'].mean().sort_values(ascending=False)
        plt.subplots(1, 1, dpi=150)
        count.plot(kind='bar')
        plt.title("小区的房屋均价")
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
        file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'address_qu_avg.html')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_text)

        plt.close()

        return Response('ok-anay')


        # 各小区的房屋数量
class addressWuNum(APIView):
    def get(self, request):
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        mpl.rcParams['axes.unicode_minus'] = False
        analysis_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'analysis.csv')
        house_data = pd.read_csv(analysis_path)
        house_wu = house_data.groupby('address_wu').size().sort_values(ascending=False).head(20)
        plt.subplots(1, 1, dpi=150)
        house_wu.plot(kind='bar')
        plt.title("小区的房屋数量")

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
        file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'address_qu_num.html')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_text)
        plt.close()



class addressWuVide(APIView):
    def get(self, request):
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        mpl.rcParams['axes.unicode_minus'] = False
        analysis_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'analysis.csv')
        house_data = pd.read_csv(analysis_path)
        # 前20个小区的看房人数
        house_vide = house_data.groupby(['address_wu'])['vides'].sum().sort_values(ascending=False).head(20)
        plt.subplots(1, 1, dpi=150)
        house_vide.plot(kind='bar')
        plt.title("小区的前20个看房人数")

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
        file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'address_wu_vide.html')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_text)
        plt.close()

        return Response('ok-anay')

class houseArea(APIView):
    def get(self, request):
        # 二手房面积分布
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        mpl.rcParams['axes.unicode_minus'] = False
        analysis_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'analysis.csv')
        house_data = pd.read_csv(analysis_path)
        area_level = [0, 50, 100, 150, 200, 250, 300, 500]
        label_level = ['小于50', '50-100', '100-150', '150-200', '200-250', '250-300', '300-350']

        cut_label = pd.cut(house_data['area'], area_level, label_level)
        house_area = cut_label.value_counts().sort_values(ascending=False)
        plt.subplots(1, 1, dpi=150)
        house_area.plot(kind='bar')
        plt.title("二手房面积分布")

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
        file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'house_area.html')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_text)
        plt.close()

        return Response('ok-anay')







        # self.address_qu_avg_html()
        #
        # self.address_qu_num_html()
        # self.address_wu_vide_html()
        # time.sleep(3)
        # self.area_price_html()
        # self.house_area_html()
        # time.sleep(3)
        # self.house_count_html()
        # self.houseType_vide_html()
        # thread_list=[]
        # t1 = threading.Thread(target=self.address_qu_avg_html)
        # thread_list.append(t1)
        #
        # t2 = threading.Thread(target=self.address_qu_num_html)
        # thread_list.append(t2)
        #
        # t4 = threading.Thread(target=self.address_wu_vide_html)
        # thread_list.append(t4)
        #
        # t5 = threading.Thread(target=self.area_price_html)
        # thread_list.append(t5)
        #
        # t6 = threading.Thread(target=self.house_area_html)
        # thread_list.append(t6)
        #
        # t7 = threading.Thread(target=self.house_count_html)
        # thread_list.append(t7)
        #
        # t8 = threading.Thread(target=self.houseType_vide_html)
        # thread_list.append(t8)
        #
        #
        # for t in thread_list:
        #     t.daemon = False
        #     t.start()


        return Response('ok-anay')