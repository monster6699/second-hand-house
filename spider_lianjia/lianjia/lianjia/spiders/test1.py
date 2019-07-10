import json
import pymysql
from redis import StrictRedis


# with open('house.json','w') as fp:
print("aa")
    # for line in fp.readlines():
    #     print(line)

    #
    # sql1_data = itmes['base_info'][0]
    # sql1 = "insert into tb_baseattr values({},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
    #     self.i + 1, sql1_data['house_type'], sql1_data['floor'], sql1_data['area'], sql1_data['structure'],
    #     sql1_data['in_area'], sql1_data['build_type'], sql1_data['build_head'], sql1_data['build_struct'],
    #     sql1_data['decorate'], sql1_data['ladder_hou_pro'], sql1_data['heat_method'], sql1_data['lift'],
    #     sql1_data['period_int'], sql1_data['ladder_hou_pro'])
    # row_count = cursor.execute(sql1)
    # conn.commit()
    # print(sql1)
    #
    # sql2_data = itmes['base_info'][1]
    # sql2 = "insert into tb_tradeattr values({},'{}','{}','{}','{}','{}','{}','{}','{}')".format(self.i + 1, sql2_data[
    #     'listed_time'], sql2_data['trade_ownership'], sql2_data['last_transation_time'], sql2_data['house_use'],
    #                                                                                             sql2_data[
    #                                                                                                 'house_year'],
    #                                                                                             sql2_data[
    #                                                                                                 'belong_to'],
    #                                                                                             sql2_data[
    #                                                                                                 'mortgage_info'],
    #                                                                                             sql2_data[
    #                                                                                                 'room_bak'])
    # row_count = cursor.execute(sql2)
    # print(sql2)
    #
    # sql6 = 'insert into tb_tag values (%d,"%s")' % (self.i + 1, itmes['tag'])
    # row_count = cursor.execute(sql6)
    # conn.commit()
    # print(sql6)
    #
    # sql4 = "insert into tb_house values(%d,'%s','%s','%s','%s','%s','%s','%s',%d,%d)" % (
    #     self.i + 1, itmes['title'], itmes['price'], itmes['unit_price'], itmes['url'], itmes['vide'],
    #     itmes['focus'], itmes['source'], self.i + 1, self.i + 1)
    # row_count = cursor.execute(sql4)
    # conn.commit()
    # print(sql4)
    #
    # for key, value in itmes['house_charact'].items():
    #     self.index = self.index + 1
    #     sql5 = "insert into tb_housecharact values (%d,'%s','%s',%d,%d)" % (
    #     self.index, key, value, self.i + 1, self.i + 1)
    #     row_count = cursor.execute(sql5)
    #     conn.commit()
    #     print(sql5)
    #
    # for key, value in itmes['images'].items():
    #     self.num = self.num + 1
    #     sql5 = "insert into tb_image values (%d,'%s','%s',%d)" % (self.num, key, value, self.i + 1)
    #     row_count = cursor.execute(sql5)
    #     conn.commit()
    #     print(sql5)
    #
    # # # 关闭游标和连接
    # cursor.close()
    # conn.close()
    # self.con.set('num', self.num)
    # self.con.set('index', self.index)
    # self.con.set('i', self.i + 1)