from main import *
from flask import Blueprint

blueprint = Blueprint('home', __name__, url_prefix='/home')


@app.route('/')
@blueprint.route('/home')
def home():
    cafe_list = list(db.home_carousel())
    last_boards = list(db.board_last())
    popular_boards = list(db.board_popular())
    return render_template('index.html', title='Home', cafes=cafe_list, last_boards=last_boards, popular_boards=popular_boards)


@blueprint.route('/search', methods=['GET', 'POST'])
def cafe_search():
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        cafes = list(db.search_cafe(keyword))

        if cafes is not None or cafes != []:
            page = request.args.get('page', 1, type=int)
            limit = request.args.get('limit', 5, type=int)

            tot_count = len(cafes)
            last_page_num = math.ceil(tot_count / limit)

            block_size = 5
            block_num = int((page - 1) / block_size)
            block_start = int(block_size * block_num + 1)
            block_last = math.ceil(block_start + (block_size - 1))

            return render_template('cafe_list.html', cafes=cafes, limit=limit, page=page,
                                   block_start=block_start, block_last=block_last, last_page=last_page_num,
                                   title='카페 찾기')


@blueprint.route('/cafe_list', methods=['GET'])
def cafe_list():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 5, type=int)

    cafes = list(db.cafe_list(page, limit))
    tot_count = db.cafe_tot_count()
    last_page_num = math.ceil(tot_count / limit)

    block_size = 5
    block_num = int((page - 1) / block_size)
    block_start = int(block_size * block_num + 1)
    block_last = math.ceil(block_start + (block_size - 1))

    return render_template('cafe_list.html', cafes=cafes, limit=limit, page=page,
                           block_start=block_start, block_last=block_last, last_page=last_page_num,
                           title='카페 찾기')

# @app.route('/cafe_info/<cafe_name>')
# def cafe_info(cafe_name):
#     cafe_info = db.search_cafe_info(cafe_name)
#     return render_template('cafe_info.html',
#                            cafe_name=cafe_info['name'],
#                            img_url=cafe_info['main_img_url'],
#                            cafe_address=cafe_info['address'])
