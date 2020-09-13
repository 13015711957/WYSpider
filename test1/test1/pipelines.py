import pymysql
from itemadapter import ItemAdapter


class Test1Pipeline:
    def open_spider(self, spider):
        print('爬取开始...')

    def __init__(self):
        # connection database
        self.connect = pymysql.connect(host='127.0.0.1', user='root', passwd='123456',
                                       db='info36')  # 后面三个依次是数据库连接名、数据库密码、数据库名称
        # get cursor
        self.cursor = self.connect.cursor()
        print("连接数据库成功")

    def process_item(self, item, spider):
        # sql语句
        insert_sql = """
               INSERT INTO `info_news`(create_time, update_time, title, source,digest, content, clicks, index_image_url,category_id, user_id, status, reason) VALUES
                ('%s','%s','%s','%s','%s','%s',%s,'%s',%s,%s,%s,%s)
               """%\
                (item['create_time'], item['create_time'], item['title'], item['source'], item['digest'],
                 item['content'], 0, item['img_url'], 1, "NULL", 0, "NULL")
        print(insert_sql)
        try:
            # 执行插入数据到数据库操作
            self.cursor.execute(insert_sql)
            # 提交，不进行提交无法保存到数据库
            self.connect.commit()
        except Exception as e:
            self.connect.rollback()
            print(e)

        return item

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.connect.close()
        print('爬取结束')
