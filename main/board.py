from main import *
from flask import Blueprint, abort
from flask import send_from_directory

blueprint = Blueprint('board', __name__, url_prefix='/board')


@blueprint.route('/cafe_info', methods=['GET', 'POST'])
def cafe_info():
    if request.method == 'GET':
        cafe_id = request.args.get('cafe_id')
        print(cafe_id)
        cafe = db.get_cafe_info(cafe_id)
        print(cafe)
        reviews = db.get_cafe_review(cafe_id)
        url = reviews['naver_url']
        url_title = reviews['naver_url_title']
        print(reviews)
        boards = db.get_cafe_board(cafe_id)

        print(boards)
        return render_template('cafe_info.html', title=cafe['name'], cafe=cafe, url=url, url_title=url_title, boards=boards)
    else:

        return abort(404)


# 게시글 상세
@blueprint.route('view')
def board_view():
    board_id = request.args.get('board_id')
    page = request.args.get('page', 1, type=int)

    if board_id is not None:
        data = db.board_view(board_id)
        if data is not None:
            result = {
                'cafe_id': data.get("cafe_id"),
                "board_id": data.get("_id"),
                "name": data.get("name"),
                "title": data.get("title"),
                "contents": data.get("contents"),
                "pubdate": data.get("pubdate"),
                "writer_id": data.get("writer_id", ""),
            }
            return render_template('board_view.html', title='게시글 상세', page=page, result=result)
    return abort(404)


# 게시글 작성
@blueprint.route('/write', methods=['GET', 'POST'])
@login_required
def board_write():
    if session["id"] is None or session["id"] == "":
        return redirect(url_for("member_login"))

    if request.method == 'POST':
        cafe_id = request.form.get('cafe_id')
        name = request.form.get('name')
        writer_id = session.get('id')
        title = request.form.get('title')
        contents = request.form.get('contents')

        current_utc_time = round(datetime.utcnow().timestamp() * 1000)

        post = {
            'cafe_id': ObjectId(cafe_id),
            "writer_id": writer_id,
            "name": session["name"],
            "title": title,
            "contents": contents,
            "view": 0,
            "pubdate": current_utc_time,
        }

        post_board = db.board_post(post)
        flash('정상적으로 작성 되었습니다.')
        return redirect(url_for('board.board_view', board_id=post_board.inserted_id))
    else:
        cafe_id = request.args.get('cafe_id')
        return render_template('board_write.html', title='게시글 작성', name=session['name'], cafe_id=cafe_id)


@blueprint.route("/edit", methods=["POST"])
@blueprint.route("/edit/<board_id>", methods=["GET"])
def board_edit(board_id=None):
    if request.method == "GET":
        data = db.board_get(board_id)
        if data is None:
            flash("해당 게시물이 존재하지 않습니다.")
            return redirect(url_for("board.cafe_info", cafe_id=request.args.get('cafe_id')))
        else:
            if session.get("id") == data.get("writer_id"):
                return render_template('board_edit.html', data=data, title="글수정",)
            else:
                flash("글 수정 권한이 없습니다.")
                return redirect(url_for("board.lists"))
    else:
        board_id = request.form.get("board_id")
        title = request.form.get("title")
        contents = request.form.get("contents")

        data = db.board_get(board_id)

        if data.get("writer_id") == session.get("id"):
            db.board_update(board_id, title, contents)
            flash("수정되었습니다.")
            return redirect(url_for("board.board_view", board_id=board_id))
        else:
            flash("글 수정 권한이 없습니다.")
            return redirect(url_for("board.lists"))


@blueprint.route("/delete/<board_id>")
def board_delete(board_id):
    data = db.board_get(board_id)
    if data.get("writer_id") == session.get("id"):
        db.board_delete(board_id)
        flash("삭제 되었습니다.")
    else:
        flash("글 삭제 권한이 없습니다.")
    return redirect(url_for("board.cafe_info", cafe_id=request.args.get('cafe_id')))


@blueprint.route("/upload_image", methods=["POST"])
def upload_image():
    if request.method == "POST":
        file = request.files["image"]
        if file and allowed_file(file.filename):
            filename = "{}_{}.jpg".format(str(int(datetime.now().timestamp()) * 1000), rand_generator())
            savefilepath = os.path.join(app.config["BOARD_IMAGE_PATH"], filename)
            file.save(savefilepath)
            return url_for("board.board_images", filename=filename)


@blueprint.route('/images/<filename>')
def board_images(filename):
    return send_from_directory('static/board_images', filename)



