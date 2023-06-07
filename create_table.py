#데이터베이스 및 테이블 생성

import pymysql

conn = pymysql.connect(host='localhost', user='root', password='livinla98',db='movie_info', charset='utf8')
cursor = conn.cursor(pymysql.cursors.DictCursor)

sql = '''CREATE TABLE movie (
m_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
m_name varchar(255),
m_ename varchar(255),
m_year int,
m_country varchar(255),
type varchar(255),
state varchar(255),
company varchar(255)
);
'''

cursor.execute(sql)

sql = '''CREATE TABLE director (
d_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
d_name varchar(255)
);
'''

cursor.execute(sql)

sql = '''CREATE TABLE genre (
m_id int not null,
g_name varchar(255),
primary key(m_id,g_name),
foreign key (m_id) references movie(m_id)
);
'''
cursor.execute(sql)

sql = '''CREATE TABLE mdInter(
m_id int,
d_id int,
primary key (m_id,d_id),
foreign key (m_id) references movie(m_id),
foreign key (d_id) references director(d_id)
);
'''
cursor.execute(sql)

conn.commit()
conn.close()

# Table에 데이터 insert sql문 작성