from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# client = MongoClient('mongodb+srv://test:sparta@cluster0.gxa02vr.mongodb.net/?retryWrites=true&w=majority',tls=True,
#                              tlsAllowInvalidCertificates=True)
# db = client.dbsparta
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


#로그인,회원가입 페이지 이동시키기이
@app.route('/Log_in.html')
def Login():
    return render_template('Log_in.html')

@app.route('/Sign_up.html')
def Signup():
    return render_template('Sign_up.html')

#키워드로 영화 리스트 검색해주는 api
@app.route("/search_movie",methods=["post"])
def search_movie():
    keyword = request.form['keyword']


    # 예외처리
    try:
        data = requests.get('https://movie.naver.com/movie/search/result.naver?query='+keyword+'&section=movie&ie=utf8', headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')

        # old_content > ul.search_list_1 > li:nth-child(1) > dl > dt > a
        # old_content > ul.search_list_1.fixed > li:nth-child(1) > dl > dt > a

        data1 = soup.find('ul', {'class': 'search_list_1'})
        data2 = data1.findAll('dt')
        movie = []
        for movies in data2:
            title = movies.text
            code = movies.find('a')['href'].split('=')[1]
            doc = {
                'title':title,
                'code':code
            }
            movie.append(doc)

        return jsonify({ 'movie':movie,'msg': 'o'})

    except AttributeError:
        return jsonify({'msg': '검색 결과가 없습니다.'})




@app.route("/print_movie",methods=["post"])
def print_movie():
    code = request.form['code']
    try:
        data = requests.get('https://movie.naver.com/movie/bi/mi/basic.naver?code='+code, headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')

        data = soup.select('#content > div.article > div.mv_info_area > div.mv_info')
        for movie_info in data:
            title = movie_info.select_one('h3 > a').text
            minititle = movie_info.select_one('strong').text
            doc ={
                'code':code,
                'title':title,
                'minititle':minititle
            }

        data2 = soup.select('#content > div.article > div.mv_info_area > div.mv_info > dl ')
        for outline in data2:
            outline_1 = outline.select_one('dd:nth-child(2) > p > span:nth-child(2) > a').text #국내/해외
            outline_release = outline.select_one('dd:nth-child(2) > p > span:nth-child(4)').text.strip().replace("\n", '') #개봉일
            outline_genre = outline.select_one('dd:nth-child(2) > p > span:nth-child(1)').text.replace("\n", '').replace("\r", '').replace("\t", '') #장르
            outline_director = outline.select_one('dd:nth-child(4) > p').text
            outline_age = outline.select_one('dd:nth-child(8) > p').text.replace("\n", '').replace("\r", '').replace("\t", '')
            doc2 ={
                'outline_1':outline_1,
                'outline_release':outline_release,
                'outline_genre':outline_genre,
                'outline_director':outline_director,
                'outline_age':outline_age
            }

        data3 = soup.select('#content > div.article > div.section_group.section_group_frst > div:nth-child(2) > div > ul > li')
        doc3 =[]
        for actor in data3:
            actimgurl = actor.select_one('a.thumb_people > img')['src']
            actname = actor.select_one('a.tx_people')['title']
            doc3.append({'actimgurl':actimgurl,'actname':actname})

        data5 =soup.find('p',{'class':'con_tx'}).find_all(text=True)
        doc5 = {'des_title':data5[0],'des_content':data5[1]}

        return jsonify({'movie_info': doc, 'outline':doc2,'actors':doc3,'description':doc5})
    except :
        return jsonify({'msg': '에러.'})



# 닉네임 별점, 한줄평 저장 db서버 이름필요
# @app.route("/comment", methods=["POST"])
# def save_comment():
#     name_receive = request.form['name_give']
#     rank_receive = request.form['rank_give']
#     comment_receive = request.form['comment_give']
#
#     doc = {
#         "name" : name_receive,
#         "rank" : rank_receive,
#         "comment" : comment_receive
#     }
#     db..insert_one(doc)
#
#     return jsonify({'msg': '기록 완료'})
#
# @app.route("/comment", methods=["GET"])
# def show_comment():
#     comment_list = list(db..find({}, {'_id': False}))
#     return jsonify({'comments': comment_list})




if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
