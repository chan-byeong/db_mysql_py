import pymysql
import pandas as pd

def sql_connect() :
  conn = pymysql.connect(host='localhost', user='root', password='livinla98',db='movie_info', charset='utf8')
  cursor = conn.cursor(pymysql.cursors.DictCursor)

  return conn ,cursor

def commit_n_close(conn) :
  conn.commit()
  conn.close()

def xls_to_table() :
  conn , cursor = sql_connect()

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
              sql = "SELECT d_id from director where d_name = %s"
              val = (d_name,)
              cursor.execute(sql,val)
              res = cursor.fetchone()

              #감독 아이디가 없는 경우
              if res is None : 
                  sql = "INSERT INTO director (d_name) values (%s)"
                  val = (d_name,)
                  cursor.execute(sql,val)

                  d_id = cursor.lastrowid


                  sql = f"Select * from mdinter where m_id = {m_id} and d_id ={d_id}"
                  cursor.execute(sql)

                  if cursor.fetchone() is None :
                      sql = "INSERT INTO mdinter (m_id,d_id) values (%s,%s)"
                      val =(m_id,d_id)
                      cursor.execute(sql,val)
                  else :
                    print(m_name , d_name , m_id , d_id)
              # 감독 아이디가 이미 존재하는 경우
              else :
                  sql = f"Select * from mdinter where m_id = {m_id} and d_id ={res['d_id']}"
                  cursor.execute(sql)
                  if cursor.fetchone() is None :
                      sql = "INSERT INTO mdinter (m_id,d_id) values (%s,%s)"
                      val = (m_id,res['d_id'])
                      cursor.execute(sql,val)
                  else :
                      print(m_name , d_name , m_id , d_id)

      #mdinter 중복 키 들어올 시 예외처리

      #장르 테이블
      g_names = row['장르'].split(',')
      for g_name in g_names :
          g_name = g_name.strip()

          sql = "INSERT INTO genre (m_id,g_name) values (%s,%s)"
          val = (m_id,g_name)
          cursor.execute(sql,val)

      if (idx+1) % 10000 == 0 :
          print(f"-----------{idx+1} movies updated--------------")

  commit_n_close(conn)

# 인덱스 생성
def create_idx() :
  conn ,cursor = sql_connect()

  cursor.execute("CREATE INDEX idx_m_name on movie (m_name)")
  cursor.execute("CREATE INDEX idx_d_name on director (d_name)")
  cursor.execute("CREATE INDEX idx_g_name on genre (g_name)")

  commit_n_close(conn)

def search_movies(title=None, year=None, country=None, type=None, company = None, state=None , genre=None, director=None):
  #connect
  conn,cursor = sql_connect()

  sql="""
    SELECT m.m_name , m.m_year , d.d_name , g.g_name , m.m_country , m.type ,m.state , m.company
    FROM movie m, director d , genre g , mdinter md
    WHERE m.m_id = md.m_id and d.d_id = md.d_id and m.m_id = g.m_id
  """

  if title : 
    sql += f"AND m.m_name LIKE '%{title}%'"
  if year :
    sql += f"AND m.m_year = {year}"
  if country :
    sql += f"AND m.m_country = '{country}'"
  if genre :
    sql += f"AND g.g_name = '{genre}'"
  if director :
    sql += f"AND d.d_name = '{director}'"

  cursor.execute(sql)
  res = cursor.fetchall()

  print("영화제목 | 감독 | 제작연도 | 장르 | 유형 | 상태 | 회사 | 국가")
  
  for movie in res :

    print()
    print(f"{movie['m_name']} | {movie['d_name']} | {movie['m_year']} | {movie['g_name']} | {movie['state']} | {movie['company']} | {movie['m_country']}")
    print()

  conn.close()