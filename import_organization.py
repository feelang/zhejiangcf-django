import os
import pymysql
from datetime import datetime

# 要导入的数据
data = [
    (1, "浙江大学医学院肿瘤妇科医院", "WCH", None),
    (2, "浙江省肿瘤医院", "ZJCH", None),
    (3, "浙江大学医学院附属第一医院", "ZJU1H", None),
    (4, "浙江大学医学院附属第二医院", "ZJU2H", "含山海工程塘社区院；龙泉市人民医院；松阳县人民医院；开化县人民医院；仙居县第一人民医院；含院区：庆春院区、解放路院区、滨江院区"),
    (5, "浙江大学医学院附属邵逸夫医院", "SYFH", "含山海工程塘社区院；武义县第一人民医院；含院区：庆春院区、钱塘院区、大运河院区、和睦院区"),
    (6, "浙江市人民医院", "ZJPH", "含山海工程塘社区院；萧山第一人民医院；萧山市定海医疗中心医院；义乌市第二人民医院；含院区：朝晖院区、留下院区、城西院区"),
    (7, "浙江省立同德医院", "ZJTDH", None),
    (8, "浙江省中医院", "ZJZH", "朗院院区、滨康院区、下沙分院、九山分院"),
    (9, "浙江医院", "ZJH", "含山海工程塘社区院；岭脚县人民医院"),
    (10, "中国人民解放军联勤保障部队第九〇三医院", "903H", None),
    (11, "树兰（杭州）医院", "SLH", None),
    (12, "杭州市第一人民医院", "HZ1H", "朗院院区、城北院区、笕山院区"),
    (13, "杭州师范大学附属医院", "HZNUH", None),
    (14, "杭州市妇产科医院", "HZWMCH", None),
    (15, "浙江省中西医结合医院（杭州市红十字会医院）", "HZRCH", None),
    (16, "杭州市中医院（丁桥院区）", "HZTH", "医院联动：金华市中医院"),
    (17, "杭州市萧山区第一人民医院", "LAH", None),
    (18, "杭州市富阳区妇幼保健院", "FYMCH", None),
    (19, "杭州市萧坎区妇幼保健中心", "GSMCH", None),
    (20, "嘉兴市第二医院", "JX2H", None),
    (21, "嘉兴市妇幼保健院", "JXMCH", None),
    (22, "海宁市人民医院", "HNH", None),
    (23, "海宁市妇幼保健院", "HNMCH", None),
    (24, "桐乡市第一人民医院", "TXH", None),
    (25, "海盐县人民医院", "HYH", None),
    (26, "嘉善县第一人民医院南部院区 嘉善县妇幼保健院", "JSMCH", None),
    (27, "湖州市中心医院", "HZCH", None),
    (28, "湖州市妇幼保健院", "HZMCH", None),
    (29, "湖州市南浔区人民医院", "NXH", None),
    (30, "湖州市吴兴区人民医院、湖州市吴兴区妇幼保健院", "WXH", None),
    (31, "宁波大学附属第一医院", "NBUH", None),
    (32, "宁波大学附属妇女儿童医院", "NBWMCH", None),
    (33, "宁波大学附属明州医院", "NBUYMH", None),
    (34, "宁波市北仑中心孝维科医院", "NHLH", None),
    (35, "宁波明州医院", "NMH", None),
    (36, "余姚市妇幼保健院", "YYMCH", None),
    (37, "慈溪市妇幼保健院", "CXMCH", None),
    (38, "宁海县妇幼保健院", "NHMCH", None),
    (39, "宁波市北仑区人民医院", "BLH", None),
    (40, "舟山市妇幼保健院", "ZSMCH", None),
    (41, "普陀医院", "PTH", None),
    (42, "温州医科大学附属第一医院", "WMU1H", None),
    (43, "温州医科大学附属第二医院", "WMU2H", None),
    (44, "温州市人民医院", "WZH", None),
    (45, "瑞安市人民医院", "RAH", None),
    (46, "瑞安市妇幼保健院", "SXMCH", None),
    (47, "瑞安市上塘人民医院", "SYH", None),
    (48, "瑞安市上塘妇幼保健院", "SYMCH", None),
    (49, "瑞安市妇幼保健院", "ZJMCH", None),
    (50, "浙江省台州医院", "TZH", None),
    (51, "台州市第一人民医院", "TZ1H", None),
    (52, "台州眼科中心（集团）黄岩医院", "TZEZH", None),
    (53, "台州市立医院", "TZLH", None),
    (54, "台州医院温岭妇产医院", "TZEFH", None),
    (55, "温岭市第一人民医院", "WLH", None),
    (56, "温岭市中医院", "WLTH", None),
    (57, "温岭市妇幼保健院", "WLMCH", None),
    (58, "仙居县人民医院", "XJH", None),
    (59, "浙江大学医学院附属第四医院", "ZJU4H", None),
    (60, "永康市第一人民医院", "YKH", None),
    (61, "永康市妇幼保健院", "YKMCH", None),
    (62, "衢州市人民医院", "QZH", None),
    (63, "龙游县人民医院", "LYH", None),
    (64, "丽水市人民医院", "LSH", None),
    (65, "丽水市中心医院", "LSCH", None),
    (66, "丽水市妇幼保健院", "LSMCH", None)
]

# 数据库连接配置
db_config = {
    'host': os.environ.get('MYSQL_ADDRESS').split(':')[0],
    'port': int(os.environ.get('MYSQL_ADDRESS').split(':')[1]),
    'user': os.environ.get('MYSQL_USERNAME'),
    'password': os.environ.get('MYSQL_PASSWORD'),
    'database': os.environ.get('MYSQL_DATABASE'),
}

# 连接数据库
connection = pymysql.connect(**db_config)

try:
    with connection.cursor() as cursor:
        # 先清空现有数据
        cursor.execute("SET FOREIGN_KEY_CHECKS=0")
        cursor.execute("TRUNCATE TABLE lsd_organization")
        cursor.execute("SET FOREIGN_KEY_CHECKS=1")
        
        # 获取当前时间
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 插入新数据
        for id, name, code, remark in data:
            try:
                cursor.execute(
                    "INSERT INTO lsd_organization (id, name, code, remark, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s)",
                    [id, name, code, remark, now, now]
                )
            except pymysql.err.IntegrityError as e:
                print(f"插入数据失败 (id={id}, name={name}): {str(e)}")
        
        connection.commit()
        
        # 验证导入结果
        cursor.execute("SELECT COUNT(*) FROM lsd_organization")
        count = cursor.fetchone()[0]
        print(f"\n成功导入 {count} 条记录到 lsd_organization 表")
        
        # 显示导入后的数据
        cursor.execute("SELECT id, name, code, remark FROM lsd_organization ORDER BY id")
        imported_data = cursor.fetchall()
        print("\n导入后的数据:")
        for row in imported_data:
            print(row)
finally:
    connection.close() 