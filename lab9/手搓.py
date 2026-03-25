from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

# 从 flask 导入 Flask 这个类、显示 html 界面
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
# 使用 SQLite 数据库，数据库文件叫 project.db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# 创建数据库对象，让 Flask 与数据库连接起来


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 自动编号，主键
    title = db.Column(db.String(300), nullable=False)  # 项目名称
    repo_link = db.Column(db.String(500), nullable=False)  # 仓库链接


@app.route('/', methods=['GET', 'POST'])  # 给函数绑定路径
def main():  # 如果用户访问网站，就执行函数
    if request.method == 'POST':  # 如果这次请求是提交表单，执行代码
        title = request.form['title']  # 从表单提取 title 内容
        repo_link = request.form['repo_link']  # 提取链接框内容

        project = Project(title=title, repo_link=repo_link)
        db.session.add(project)  # 保存到数据库
        db.session.commit()  # 提交到数据库

        return redirect(url_for('main'))  # 保存成功后返回主页

    projects = Project.query.all()
    return render_template('index.html', projects_list=projects)
    # 如果不是 POST，正常显示页面，并把所有项目传给 HTML


@app.route('/clear', methods=['POST'])
def clear():
    Project.query.delete()  # 删除 Project 所有记录
    db.session.commit()  # 删除操作保存到数据库
    return redirect(url_for('main'))  # 删除之后返回主页


if __name__ == '__main__':  # 直接运行此文件，启动网站
    with app.app_context():
        db.create_all()
    # 如果数据库和表不存在，自动创建
    app.run(debug=True)  # 启动 flask 浏览器