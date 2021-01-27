import requests
import time
import pandas, re

# 在用户请求 roleUrl 时 会给这个验证。如果失效了需要重新输入
real_xoyokey = "%5CigJpJeM%26WUS%3DtetHt6m6g6t%26%26Mk%2F%2Fr8j%3Dt6ttgtJpJe%2678etH66%26%26%21k%2F_%3DJTT.p.%26WHTpetUt%21%26t6gWg%3D9r%26rpT%3Dk8%21tt%21M.t%3DtarrWjp%26jmM6tp;"
# 该属性是当前时间的毫秒数
__ts__ = float(time.time())
# 保存数据的字典
all_data_reverse_dic = {
    'consignment_id': [],
    'name': [],
    '哪个区': [],
    '价格': [],
    '门派': [],
    '等级': [],
    '装备分': [],
    "江湖资历": [],

    '体型': [],
    '剩余可购买时间':[],

}
consignment_id = "671267077236867072"
equipmentUrl = "https://api-wanbaolou.xoyo.com/api/buyer/goods/additional_data?" \
               "req_id=xQz8SBGmvW4uZJ1OfJkTGarNIhhviaMX&" \
               "consignment_id={}&" \
               "goods_type=2&" \
               "additional_key=role_equipment_info&" \
               "__ts__={}".format(consignment_id, __ts__)

"""
检查全部列表中的数据的方法
参数表示要查询多少数据
"""


def check_totallist_method(need_datas=20):
    page = '1'
    role_list = []
    for t in range(1, need_datas//10 + 1):
        print('第{}batch'.format(str(t)))
        page = str(t)
        originalurl = 'https://api-wanbaolou.xoyo.com/api/buyer/goods/list?' \
                      'req_id=M3K4uJ8pw0jIze2DyfdtjQZ46dlolcRp&' \
                      'zone_id=&server_id=&' \
                      'filter%5Bprice%5D=0&filter%5Bstate%5D=0&filter%5Btags%5D=0&filter%5Brole_sect%5D=0&filter%5Brole_shape%5D=0&filter%5Brole_camp%5D=0&filter%5Brole_equipment_point%5D=0&filter%5Brole_experience_point%5D=0&filter%5Brole_level%5D=0&game=jx3' \
                      '&page=' + page +\
                      '&size=10' \
                      '&goods_type=2' \
                      '&__ts__={}'.format(__ts__)
        rp = requests.get(originalurl, headers={
            'Referer': 'https://jx3.seasunwbl.com/buyer?t=role',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
                                            })
        role_list.append(rp.json()['data']['list'])
    # 添加到all_data_reverse_dic 字典中，用来保存成excel时候用
    for i in role_list:
        for r in i:
            print("^^^^^^^^^^^^^^^^^^")
            all_data_reverse_dic['name'].append(r['seller_role_name'])
            print(r['seller_role_name']) # 用户名字
            all_data_reverse_dic['哪个区'].append(r['info'])
            print(r['info'])# 哪个区
            all_data_reverse_dic['价格'].append(r['single_unit_price'])
            print(r['single_unit_price']) # 价格
            all_data_reverse_dic['门派'].append(r['attrs']['role_sect'])
            print(r['attrs']['role_sect']) # 门派
            all_data_reverse_dic['等级'].append(r['attrs']['role_level'])
            print(r['attrs']['role_level']) # 等级
            all_data_reverse_dic['装备分'].append(r['attrs']['role_equipment_point'])
            print(r['attrs']['role_equipment_point'])# 装备分
            all_data_reverse_dic['江湖资历'].append(r['attrs']['role_experience_point'])
            print(r['attrs']['role_experience_point']) # 江湖资历
            all_data_reverse_dic['consignment_id'].append(r['consignment_id'])
            print(r['consignment_id']) # consignment_id
            print("^^^^^^^^^^^^^^^^^^")


"""
获得角色的基本属性信息
"""


def invoke_role_other_info():

    for id in all_data_reverse_dic['consignment_id']:
        roleUrl = "https://api-wanbaolou.xoyo.com/api/buyer/goods/detail?" \
                  "req_id=xQz8SBGmvW4uZJ1OfJkTGarNIhhviaMX&" \
                  "consignment_id={}&goods_type=2&__ts__={}".format(id, __ts__)
        rp_role = requests.get(roleUrl, headers={
            'Cookie': 'ts_session_id_=lBiaDKRYWyp7ybiMAMmb1znjhTDUZFW9DL1Q5jak; xoyokey=' + real_xoyokey +'ts_session_id_=lBiaDKRYWyp7ybiMAMmb1znjhTDUZFW9DL1Q5jak;_wsi1=514512eb61567fae01a474c6cdda2d2f2260a50e; UM_distinctid=1773d28a6f6189-076b0aa9d8e802-67e1b3f-e1000-1773d28a6f9354; OZ_1U_751=vid=v00fa81b7907d0.0&ctime=1611638849&ltime=1611638810;_wsi2=3abf118016a329b3a1c0e87c18be7b3c9f0667ef;_wsi3=0cb96347add5d18a52bb2b88bbd51f7dff2f28ad;',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
        })
        # 获取奇迹属性的URL和方法
        # miracleUrl = "https://api-wanbaolou.xoyo.com/api/buyer/goods/additional_data?" \
        #              "consignment_id={}&" \
        #              "goods_type=2&" \
        #              "additional_key=role_adventure_info&" \
        #              "__ts__={}".format(consignment_id, __ts__)
        #rp_role_miracle = requests.get(miracleUrl, headers=contain_cookies_header)
        roleBaselist = rp_role.json()['data']
        #roleMiraclelist = rp_role_miracle.json()['data']['additional_data']
        # 将新数据添加到 all_data_reverse_dic
        print(roleBaselist)
        all_data_reverse_dic['体型'].append(roleBaselist['attrs']['role_shape'])
        all_data_reverse_dic['剩余可购买时间'].append(round(roleBaselist['remaining_time'] / 3600, 2))


if __name__ == '__main__':
    check_totallist_method()
    invoke_role_other_info()
    print(all_data_reverse_dic)
    pandas.DataFrame(all_data_reverse_dic).to_excel('数据.xlsx')

