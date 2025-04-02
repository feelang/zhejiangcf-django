import os
import pymysql

# 要导入的数据
data = [
    (1, None, 1), (2, 2, 1), (7, 1, 6), (8, 66, 7), (11, 65, 8),
    (12, 64, 10), (13, 63, 11), (14, 62, 13), (17, 61, 14), (18, 60, 15),
    (19, 59, 16), (20, 3, 17), (21, 4, 18), (22, 5, 19), (23, 6, 20),
    (24, 7, 21), (25, 8, 22), (26, 9, 23), (27, 10, 24), (28, 11, 25),
    (29, 12, 26), (30, 13, 28), (31, 14, 29), (32, 15, 30), (33, 16, 31),
    (34, 17, 32), (35, 18, 33), (36, 19, 34), (37, 20, 35), (38, 21, 36),
    (39, 22, 37), (40, 23, 38), (41, 58, 39), (42, 57, 40), (43, 56, 41),
    (44, 55, 42), (45, 54, 43), (46, 53, 44), (47, 52, 45), (48, 51, 46),
    (49, 50, 47), (50, 49, 48), (51, 48, 49), (52, 47, 50), (53, 46, 51),
    (54, 45, 52), (55, 44, 53), (56, 43, 54), (57, 42, 55), (58, 41, 56),
    (59, 40, 57), (60, 39, 58), (61, 38, 59), (62, 37, 60), (63, 36, 61),
    (64, 35, 62), (65, 24, 63), (66, 34, 64), (67, 33, 65), (68, 32, 66),
    (69, 31, 67), (70, 30, 68), (71, 29, 69), (72, 28, 70), (73, 27, 71),
    (74, 26, 72), (79, 25, 75)
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
        # 检查 lsd_organization 表的数据
        cursor.execute("SELECT * FROM lsd_organization")
        results = cursor.fetchall()
        print("\nlsd_organization 表数据:")
        for row in results:
            print(row)
        
        # 检查 auth_user 表的数据
        cursor.execute("SELECT id, username FROM auth_user")
        results = cursor.fetchall()
        print("\nauth_user 表数据:")
        for row in results:
            print(row)
        
        # 先检查现有数据
        cursor.execute("SELECT id, organization_id, user_id FROM lsd_user_profile")
        existing_data = cursor.fetchall()
        print("\n现有数据:")
        for row in existing_data:
            print(row)
        
        # 清空现有数据
        cursor.execute("SET FOREIGN_KEY_CHECKS=0")
        cursor.execute("TRUNCATE TABLE lsd_user_profile")
        cursor.execute("SET FOREIGN_KEY_CHECKS=1")
        
        # 插入新数据
        for id, org_id, user_id in data:
            try:
                cursor.execute(
                    "INSERT INTO lsd_user_profile (id, organization_id, user_id) VALUES (%s, %s, %s)",
                    [id, org_id, user_id]
                )
            except pymysql.err.IntegrityError as e:
                print(f"插入数据失败 (id={id}, organization_id={org_id}, user_id={user_id}): {str(e)}")
        
        connection.commit()
        
        # 验证导入结果
        cursor.execute("SELECT COUNT(*) FROM lsd_user_profile")
        count = cursor.fetchone()[0]
        print(f"\n成功导入 {count} 条记录到 lsd_user_profile 表")
        
        # 显示导入后的数据
        cursor.execute("SELECT id, organization_id, user_id FROM lsd_user_profile ORDER BY id")
        imported_data = cursor.fetchall()
        print("\n导入后的数据:")
        for row in imported_data:
            print(row)
finally:
    connection.close() 