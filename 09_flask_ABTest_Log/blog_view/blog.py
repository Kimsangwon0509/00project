from flask import Flask, Blueprint, request, render_template, make_response, jsonify, redirect, url_for, session
from flask_login import login_user, current_user, logout_user
from blog_control.user_mgmt import User
from blog_control.session_mgmt import BlogSession
import datetime

blog_abtest = Blueprint('blog', __name__)


@blog_abtest.route('/set_email', methods=['GET', 'POST'])
def set_email():
    if request.method == 'GET':
        # print('set_email', request.headers)
        print('set_email', request.args.get('user_email'))
        return redirect(url_for('blog.test_blog'))
    else:
        # print('set_email', request.headers)
        # content type 이 application/json 인 경우
        # 202403 업데이트: 최근에는 content type 이 application/json 이 아닌 경우, 영상과 기존 버전에서는 None 을 출력하지만,
        # 최근 버전에서는 request.get_json() 를 호출하면 Bad Request 에러를 냅니다.
        # 사용하지 않을 부분이지만 영상에서는 None 으로 나오는 부분을 테스트하시다가 당황하실 듯하여 주석을 업데이트합니다.
        # print('set_email', request.get_json()))
        # print('set_email', request.form['user_email'])
        # print('set_email', request.form['blog_id'])
        user = User.create(request.form['user_email'], request.form['blog_id'])
        # https://docs.python.org/3/library/datetime.html#timedelta-objects
        login_user(user, remember=True, duration=datetime.timedelta(days=365))

        return redirect(url_for('blog.blog_fullstack1'))

    # return redirect('/blog/test_blog')
    # return make_response(jsonify(success=True), 200)


@blog_abtest.route('/logout')
def logout():
    User.delete(current_user.id)
    logout_user()
    return redirect(url_for('blog.blog_fullstack1'))


@blog_abtest.route('/blog_fullstack1')
def blog_fullstack1():
    if current_user.is_authenticated:
        webpage_name = BlogSession.get_blog_page(current_user.blog_id)
        BlogSession.save_session_info(
            session['client_id'], current_user.user_email, webpage_name)
        return render_template(webpage_name, user_email=current_user.user_email)
    else:
        webpage_name = BlogSession.get_blog_page()
        BlogSession.save_session_info(
            session['client_id'], 'anonymous', webpage_name)
        return render_template(webpage_name)
