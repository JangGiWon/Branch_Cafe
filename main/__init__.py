import os
from flask import Flask
from flask import request
from flask import render_template
from flask import url_for, redirect, flash
from flask import session
from bson.objectid import ObjectId
from flask_cors import CORS
from datetime import datetime
from werkzeug.utils import secure_filename
import time
import math
from flask_wtf import CSRFProtect


app = Flask(__name__)
CORS(app)
csrf = CSRFProtect(app)

app.config['SECRET_KEY'] = 'branch_cafe'

BOARD_IMAGE_PATH = "main\\static\\board_images"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app.config['BOARD_IMAGE_PATH'] = BOARD_IMAGE_PATH
app.config['MAX_CONTENT_LENGTH'] = 15 * 1024 * 1024

except_cafe_list = ['스타벅스 Starbucks', '투썸플레이스 A TWOSOME PLACE', '메가커피', '이다야', '할리스', '빽다방',
                    '커피빈', '파스쿠찌', '엔제리너스 Angel-in-us', '탐앤탐스 TOM N TOMS', '풀바셋', '달콤커피',
                    '카페베네', '커피베이', '커피나무', '드롭탑', '커피에반하다', '셀렉토커피',
                    '커피스미스', '만랩커피', '매머드커피', '토프레소', '더카페', '더착한커피',
                    '커피마마', '커피명가', '빈스빈스', '전광수커피', '카페띠아모', '그라찌에',
                    '매머드커피', '드롭탑', '카페보니또', '더카페', '주커피', '엠즈씨드']

from .common import login_required, allowed_file, check_filename, hash_password, check_password, rand_generator
from .filter import format_datetime
from . import db
from . import home
from . import board
from . import member


app.register_blueprint(member.blueprint)
app.register_blueprint(home.blueprint)
app.register_blueprint(board.blueprint)

