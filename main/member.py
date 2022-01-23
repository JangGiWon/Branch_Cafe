import json

from main import *
from flask import Blueprint


blueprint = Blueprint("member", __name__, url_prefix='/member')


# 회원가입
@blueprint.route('/join', methods=['GET', 'POST'])
def member_join():
    if request.method == 'GET':
        return render_template('join.html')
    else:
        name = request.form.get('name', type=str)
        id = request.form.get('id', type=str)
        password = request.form.get('password', type=str)
        current_utc_time = round(datetime.utcnow().timestamp() * 1000)

        member = {
            'name': name,
            'id': id,
            'password': hash_password(password),
            'join_date': current_utc_time
        }

        db.join(member)
        return redirect(url_for('member.member_login'))


# 아이디 체크
@blueprint.route('/idCheck', methods=['GET', 'POST'])
def member_idCheck():
    data = request.get_json()

    if db.id_check(data['uid']) is not None:
        check = 'no'
    else:
        check = 'ok'

    return check


# 로그인
@blueprint.route('/login', methods=['GET', 'POST'])
def member_login():
    if request.method == "GET":
        next_url = request.args.get("next_url", type=str)
        if next_url is not None:
            return render_template("login.html", next_url=next_url, title="로그인")
        else:
            return render_template("login.html", title="로그인")
    else:
        id = request.form.get('id');
        password = request.form.get('password')
        next_url = request.form.get("next_url", type=str)

        data = db.login(id)

        if data is None:
            flash('로그인에 실패했습니다.')
            return redirect(url_for("member.member_login"))
        else:
            if check_password(data.get("password"), password):
                session['name'] = data.get('name')
                session['id'] = id
                session['_id'] = str(data.get('_id'))
                print(session['id'])

                if next_url is not None:
                    return redirect(next_url)
                else:
                    return redirect(url_for('home.home'))
            else:
                flash('로그인에 실패했습니다.')
                return redirect(url_for('member.member_login'))


# 로그아웃
@blueprint.route('/logout')
def member_logout():
    session['name'] = ''
    session['id'] = ''
    session['_id'] = ''
    return redirect(url_for('home.home'))


@blueprint.route('/my_page', methods=['GET'])
@login_required
def member_page():
    if session["id"] is None or session["id"] == "":
        return redirect(url_for("member_login"))
    else:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 5, type=int)
        my_review = list(db.get_member_review(session['id'], page, limit))
        tot_count = db.member_review_tot_count(session['id'])
        last_page_num = math.ceil(tot_count / limit)

        block_size = 5
        block_num = int((page - 1) / block_size)
        block_start = int(block_size * block_num + 1)
        block_last = math.ceil(block_start + (block_size - 1))

        return render_template('member_page.html', my_review=my_review, limit=limit, page=page, block_start=block_start,
                               block_last=block_last, last_page=last_page_num, title="My Page")


# 좋아요
# @blueprint.route('/like/<cafe_id>')
# @login_required
# def member_like(cafe_id):
#     print(cafe_id)
#     print('heart')