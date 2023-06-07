import pymysql
import pandas as pd

conn = pymysql.connect(host='localhost', user='root', password='livinla98',db='movie_info', charset='utf8')
cursor = conn.cursor(pymysql.cursors.DictCursor)


df = pd.read_excel('./movie_list.xls')

df = df.fillna('N/A')

for idx, row in df.iterrows() :
    # 영화 테이블
    m_name = row['영화명']
    m_ename= row['영화명(영문)']

    m_year = row['제작연도']
    if m_year=='N/A' : m_year = None

    m_country = row['제작국가']
    type = row['유형']
    state = row['제작상태']
    company = row['제작사']

    sql = '''insert into movie (m_name,m_ename,m_year,m_country,type,state,company)
    values (%s,%s,%s,%s,%s,%s,%s)'''


    val = (m_name,m_ename,m_year,m_country,type,state,company)
    cursor.execute(sql,val)

    m_id = cursor.lastrowid


    # 감독 테이블 , 중간테이블
    d_names = row['감독'].split(',')
    for d_name in d_names :
        d_name = d_name.strip()
        if d_name != 'N/A' : 
            sql = f"SELECT d_id from director where d_name='{d_name}'"
            cursor.execute(sql)
            res = cursor.fetchone()

            if res is None :
                sql = "INSERT INTO director (d_name) values (%s)"
                val = (d_name,)
                cursor.execute(sql,val)

                d_id = cursor.lastrowid

                sql = "INSERT INTO mdinter (m_id,d_id) values (%s,%s)"
                val =(m_id,d_id)
                cursor.execute(sql,val)
            else :
                sql = "INSERT INTO mdinter (m_id,d_id) values (%s,%s)"
                val = (m_id,res['d_id'])
                cursor.execute(sql,val)
            
            
    

    #장르 테이블
    g_names = row['장르'].split(',')
    for g_name in g_names :
        g_name = g_name.strip()

        sql = "INSERT INTO genre (m_id,g_name) values (%s,%s)"
        val = (m_id,g_name)
        cursor.execute(sql,val)

    if(idx % 100 == 0 ) :
        print(f"-----------{idx} movies updated--------------")

conn.commit()

conn.close()
