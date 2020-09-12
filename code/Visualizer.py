import pymysql
import time
import numpy as np
from PIL import Image


class Visualizer:

    def __init__(self):
        """
        Draw a emoji by TiDB Dashboard
        """

        self.db = pymysql.connect(host='localhost',
                                  user="root",
                                  password="",
                                  port=4000,
                                  database="test",
                                  charset='utf8')

        self.cursor = self.db.cursor()

    def create(self, i: int):
        """
        create an table
        :param i: index
        :return: 
        """

        # 为了使图像明显，所以多添加了几个数据，使读取数据量增加
        sql_create = """create table if not exists graph_test{} (
                        id int PRIMARY KEY AUTO_INCREMENT,
                        name1 varchar(50) NOT NULL,
                        name2 varchar(50) NOT NULL,
                        name3 varchar(50) NOT NULL,
                        name4 varchar(50) NOT NULL,
                        name5 varchar(50) NOT NULL
                        )""".format(str(i))
        try:
            self.cursor.execute(sql_create)
            # 提交到数据库执行
            self.db.commit()
        except:
            # 发生错误时回滚
            self.db.rollback()

    def insert(self, table_name: str):
        """
        insert values to table
        :param table_name: 
        :return: 
        """
        sql_insert = "insert into {} values(null,'it is just a test'," \
                     "'it is just a test','it is just a test'," \
                     "'it is just a test','it is just a test')".format(table_name)
        try:
            self.cursor.execute(sql_insert)
            # 提交到数据库执行
            self.db.commit()
        except:
            # 发生错误时回滚
            self.db.rollback()

    def select(self, table_name: str, id_name: int, num: int):
        """
        access db
        :param table_name: 
        :param id_name: 
        :param num: number of access
        :return: 
        """
        if num == 0:
            return
        for i in range(num):
            sql_select = "select * from " + table_name + " where id = " + str(id_name)
            try:
                # 执行SQL语句
                self.cursor.execute(sql_select)
                # 获取所有记录列表
                results = self.cursor.fetchall()
            except:
                print("Error: unable to fecth data")

    @staticmethod
    def load_image(file: str):
        """
        convert image to gray and get matrix
        :param file: image name
        :return: matrix of gray image
        """
        im = Image.open(file)
        im.show()
        L = im.convert('L')
        L.show()
        image = np.array(L)
        return image

    def draw_image(self, image):
        """
        Draw a emoji by access db
        :param image: matrix of image
        :return:
        """
        pixel = image.shape[1] // 8
        for j in range(image.shape[1] * pixel + 20):
            self.create(j)
            self.insert("graph_test" + str(j))

        for j in range(image.shape[1]):
            time_start = time.time()
            for i in range(image.shape[0]):
                x = image.shape[0] - i - 1
                y = j
                for k in range(pixel):
                    self.select("graph_test" + str(i * pixel + k + 10), 1, image[x, y])

            time_end = time.time()
            time.sleep(60 - (time_end - time_start))


if __name__ == '__main__':
    vis = Visualizer()
    graph = vis.load_image("../image/TiDB_img.png")
    vis.draw_image(graph)
