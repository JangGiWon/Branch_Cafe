from main import *
import ssl
from pymongo import MongoClient


# connection = pymongo.MongoClient('localhost', 27017)
# db = connection['branch_cafe']
# collection = db['cafe']

CONNECTION_STRING = 'mongodb+srv://admin:1q2w3e4r5t@mycluster.laz0h.mongodb.net/MyCluster?retryWrites=true&w=majority'
# client = MongoClient(CONNECTION_STRING)
client = MongoClient(CONNECTION_STRING, ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
db = client.get_database('Branch_Cafe')
user_collection = db.User
cafe_info_collection = db.Cafe_info
board_collection = db.Board
review_collection = db.Cafe_reivew

# 회원가입
def join(member):
    return user_collection.insert_one(member)


# 로그인
def login(id):
    return user_collection.find_one({'id': id})


# ID CHECK
def id_check(uid):
    return user_collection.find_one({'id': uid})


# 자신의 리뷰
def get_member_review(writer_id, page, limit):
    return board_collection.find({'writer_id': writer_id}).skip((page - 1) * limit).limit(limit)


def member_review_tot_count(writer_id):
    return board_collection.find({'writer_id': writer_id}).count()


# 캐러셀 슬라이드
def home_carousel():
    pipeline = {'$sample': {'size': 6}}
    result = cafe_info_collection.aggregate([pipeline])
    return result


# 카페 검색
def search_cafe(keyword):
    return cafe_info_collection.find({'name': {'$regex': keyword}})


# 카페 개수
def cafe_tot_count():
    return cafe_info_collection.find().count()


# 카페 리스트
def cafe_list(page, limit):
    return cafe_info_collection.find().skip((page - 1) * limit).limit(limit)


# _id로 cafe 찾기
def get_cafe_info(cafe_id):
    return cafe_info_collection.find_one({'_id': ObjectId(cafe_id)})


# cafe_id로 review 찾기
def get_cafe_review(cafe_id):
    return review_collection.find_one({'cafe_id': ObjectId(cafe_id)})


# 게시글
def get_cafe_board(cafe_id):
    return list(board_collection.find({'cafe_id': ObjectId(cafe_id)}))


# 게시글 상세 페이지
def board_view(board_id):
    return board_collection.find_one_and_update({"_id": ObjectId(board_id)}, {"$inc": {"view": -1}}, return_document=True)


# 게시글 삭제
def board_delete(board_id):
    return board_collection.delete_one({'_id': ObjectId(board_id)})


# 게시글 상세
def board_get(board_id):
    return board_collection.find_one({'_id': ObjectId(board_id)})


# 게시글 작성
def board_post(post):
    return board_collection.insert_one(post)


# 게시글 수정
def board_update(board_id, title, contents):
    return board_collection.update_one({'_id': ObjectId(board_id)},
                                       {
                                           '$set': {
                                               'title': title,
                                               'contents': contents
                                           }
                                       })


# 최근 게시글
def board_last():
    return board_collection.find().sort('pubdate', -1).limit(5)


# 인기 게시글
def board_popular():
    return board_collection.find().sort('view', -1).limit(5)