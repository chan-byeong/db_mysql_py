import pymysql

from table_insert import xls_to_table , create_idx ,search_movies
from create_table import create_table

# create_table()
# xls_to_table()
# create_idx()

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