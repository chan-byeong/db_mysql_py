# 검색 조건
# 영화 제목 , 제목(영문) , 제작연도 , 유형 , 제작 국가 , 제작회사 , 상태
# 감독 , 장르 

import pymysql

def search_movies(title=None, year=None, country=None, type=None, company = None, state=None , genre=None, director=None):
  #connect
  conn = pymysql.connect(host='localhost', user='root', password='livinla98',db='movie_info', charset='utf8')
  cursor = conn.cursor(pymysql.cursors.DictCursor)

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


# user
while True :
  title = None 
  year = None 
  country = None
  company = None
  state = None
  director = None
  type = None

  print("############영화 검색############")
  print()
  print("*입력을 생략하려면 아무것도 입력하지 않은 상태에서 Enter를 누르세요.")
  print()
  

  title = input("영화제목을 입력하세요 : ")
  director = input("영화감독을 입력하세요 : ")
  genre = input("영화 장르를 입력하세요 : ")
  company = input("영화 배급사를 입력하세요 : ")
  state = input("영화 상태를 입력하세요 : ")
  type = input("영화 유형을 입력하세요 : ")
  year = input("영화 개봉연도를 입력하세요 : ")
  country = input("영화 제작 국가를 입력하세요 : ")

  if genre == '' : genre = None
  if title == '' :title = None
  if year == '' : year = None
  if country == '' : country = None
  if state == '' : state = None
  if director == '' : director = None
  if type == '' : type = None
  if company == '' : company = None

  search_movies(title, year, country, type, company, state , genre, director)

  isBreak = input("종료하시겠습니까? (Y/N) : ")
  if isBreak.upper() == 'Y' : break