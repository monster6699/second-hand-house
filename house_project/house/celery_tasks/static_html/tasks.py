import os
from celery_tasks.main import app
import base64

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from io import BytesIO
import os

from django.conf import settings
from django.template import loader
from pylab import mpl
from rest_framework.views import APIView
# def globaldel():
#     mpl.rcParams['font.sans-serif'] = ['SimHei']
#     mpl.rcParams['axes.unicode_minus'] = False
#     analysis_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'analysis.csv')
#     house_data = pd.read_csv(analysis_path)
#
#     return house_data
#
# @app.task(name='house_count_html')
# def house_count_html():
#     house_data = globaldel()
#     house_count = house_data.groupby('address_qu').size().sort_values(ascending=False)
#     plt.subplots(1, 1, dpi=150)
#     house_count.plot(kind='bar')
#     plt.title("各区的房屋数量")
#     buffer = BytesIO()
#     plt.savefig(buffer)
#     plot_data = buffer.getvalue()
#     imb = base64.b64encode(plot_data)  # 对plot_data进行编码
#     ims = imb.decode()
#     imd = "data:image/png;base64," + ims
#     context = {
#         'imd': imd
#     }
#     plt.close()
#     template = loader.get_template('house_count.html')
#     html_text = template.render(context)
#     file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'house_count.html')
#     with open(file_path, 'w', encoding='utf-8') as f:
#         f.write(html_text)
#
# @app.task(name='houseType_count_html')
# def houseType_count_html():
#     # 户型数量
#     house_data = globaldel()
#     temp_list = house_data['houseType'].values
#     houseType_list = pd.unique(temp_list)
#     houseType_count = pd.DataFrame(np.zeros([house_data.shape[0], houseType_list.shape[0]]), columns=houseType_list)
#     for i in range(houseType_count.shape[0]):
#         houseType_count.ix[i, temp_list[i]] = 1
#     plt.subplots(1, 1, dpi=150)
#     houseType_count.sum().plot(kind='bar', title="户型数量", )
#
#     buffer = BytesIO()
#     plt.savefig(buffer)
#     plot_data = buffer.getvalue()
#     imb = base64.b64encode(plot_data)  # 对plot_data进行编码
#     ims = imb.decode()
#     imd = "data:image/png;base64," + ims
#     context = {
#         'imd': imd
#     }
#     template = loader.get_template('house_count.html')
#     html_text = template.render(context)
#     file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'houseType_count.html')
#     with open(file_path, 'w', encoding='utf-8') as f:
#         f.write(html_text)
#     plt.close()
#
#
# @app.task(name='area_price_html')
# def area_price_html():
#     # 探究房屋面积和房屋价格的关系
#     house_data = globaldel()
#     y = list(house_data['price'].values)
#     x = list(house_data['area'].values)
#     # 1.创建画布
#     plt.figure(figsize=(20, 8), dpi=200)
#     # plt.subplots(1,1,dpi=150)
#     # 2.绘制散点图
#     plt.scatter(x, y)
#     plt.suptitle('房屋面积与价格的关系', fontsize=18)
#     # 3.显示图像
#     buffer = BytesIO()
#     plt.savefig(buffer)
#     plot_data = buffer.getvalue()
#     imb = base64.b64encode(plot_data)  # 对plot_data进行编码
#     ims = imb.decode()
#     imd = "data:image/png;base64," + ims
#     context = {
#         'imd': imd
#     }
#     template = loader.get_template('house_count.html')
#     html_text = template.render(context)
#     file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'area_price.html')
#     with open(file_path, 'w', encoding='utf-8') as f:
#         f.write(html_text)
#
# @app.task(name='houseType_vide_html')
# def houseType_vide_html():
#     # 户型与关注人数的分布
#     house_data = globaldel()
#     type_interest_group = house_data['vides'].groupby(house_data['houseType']).agg(
#         [('户型', 'count'), ('带看人数', 'sum')])
#     type_interest_group = type_interest_group[type_interest_group['户型'] > 20]
#     asd, sdf = plt.subplots(1, 1, dpi=150)
#     type_interest_group.plot(kind='barh', alpha=0.7, grid=True, ax=sdf)
#     plt.title('二手房户型和带看人数分布')
#     plt.ylabel('户型')
#
#     buffer = BytesIO()
#     plt.savefig(buffer)
#     plot_data = buffer.getvalue()
#     imb = base64.b64encode(plot_data)  # 对plot_data进行编码
#     ims = imb.decode()
#     imd = "data:image/png;base64," + ims
#     context = {
#         'imd': imd
#     }
#     template = loader.get_template('house_count.html')
#     html_text = template.render(context)
#     file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'houseType_vide.html')
#     with open(file_path, 'w', encoding='utf-8') as f:
#         f.write(html_text)
#     plt.close()
#
#
# @app.task(name='address_qu_avg_html')
# def address_qu_avg_html():
#     # 各区的房屋均价
#     house_data = globaldel()
#     count = house_data.groupby(['address_qu'])['price'].mean().sort_values(ascending=False)
#     plt.subplots(1, 1, dpi=150)
#     count.plot(kind='bar')
#     plt.title("各区的房屋均价")
#     buffer = BytesIO()
#     plt.savefig(buffer)
#     plot_data = buffer.getvalue()
#     imb = base64.b64encode(plot_data)  # 对plot_data进行编码
#     ims = imb.decode()
#     imd = "data:image/png;base64," + ims
#     context = {
#         'imd': imd
#     }
#     template = loader.get_template('house_count.html')
#     html_text = template.render(context)
#     file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'address_qu_avg.html')
#     with open(file_path, 'w', encoding='utf-8') as f:
#         f.write(html_text)
#
#     plt.close()
#
# @app.task(name='address_qu_num_html')
# def address_qu_num_html():
#     # 各区的房屋数量
#     house_data = globaldel()
#     house_count = house_data.groupby('address_qu').size().sort_values(ascending=False)
#     plt.subplots(1, 1, dpi=150)
#     house_count.plot(kind='bar')
#     plt.title("各区的房屋数量")
#
#     buffer = BytesIO()
#     plt.savefig(buffer)
#     plot_data = buffer.getvalue()
#     imb = base64.b64encode(plot_data)  # 对plot_data进行编码
#     ims = imb.decode()
#     imd = "data:image/png;base64," + ims
#     context = {
#         'imd': imd
#     }
#     template = loader.get_template('house_count.html')
#     html_text = template.render(context)
#     file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'address_qu_num.html')
#     with open(file_path, 'w', encoding='utf-8') as f:
#         f.write(html_text)
#     plt.close()
#
# @app.task(name='address_wu_vide_html')
# def address_wu_vide_html():
#     # 前20个小区的看房人数
#     house_data = globaldel()
#     house_vide = house_data.groupby(['address_wu'])['vides'].sum().sort_values(ascending=False).head(20)
#     plt.subplots(1, 1, dpi=150)
#     house_vide.plot(kind='bar')
#     plt.title("小区的前20个看房人数")
#
#     buffer = BytesIO()
#     plt.savefig(buffer)
#     plot_data = buffer.getvalue()
#     imb = base64.b64encode(plot_data)  # 对plot_data进行编码
#     ims = imb.decode()
#     imd = "data:image/png;base64," + ims
#     context = {
#         'imd': imd
#     }
#     template = loader.get_template('house_count.html')
#     html_text = template.render(context)
#     file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'address_wu_vide.html')
#     with open(file_path, 'w', encoding='utf-8') as f:
#         f.write(html_text)
#     plt.close()
#
# @app.task(name='house_area_html')
# def house_area_html():
#     # 二手房面积分布
#     house_data = globaldel()
#     area_level = [0, 50, 100, 150, 200, 250, 300, 500]
#     label_level = ['小于50', '50-100', '100-150', '150-200', '200-250', '250-300', '300-350']
#
#     cut_label = pd.cut(house_data['area'], area_level, label_level)
#     house_area = cut_label.value_counts().sort_values(ascending=False)
#     plt.subplots(1, 1, dpi=150)
#     house_area.plot(kind='bar')
#     plt.title("二手房面积分布")
#
#     buffer = BytesIO()
#     plt.savefig(buffer)
#     plot_data = buffer.getvalue()
#     imb = base64.b64encode(plot_data)  # 对plot_data进行编码
#     ims = imb.decode()
#     imd = "data:image/png;base64," + ims
#     context = {
#         'imd': imd
#     }
#     template = loader.get_template('house_count.html')
#     html_text = template.render(context)
#     file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'house_area.html')
#     with open(file_path, 'w', encoding='utf-8') as f:
#         f.write(html_text)
#     plt.close()

