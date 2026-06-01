# Superlist — To-Do List Web App

基于 Django 的在线待办事项应用，支持多用户独立清单。使用 TDD（测试驱动开发）方法构建，Bootstrap 美化界面，Gunicorn + Nginx 部署，Fabric 实现自动部署。

## 技术栈

- **后端**：Django 4.2
- **数据库**：SQLite
- **前端**：Bootstrap 3.3.4
- **测试**：Selenium + Django TestCase
- **部署**：Gunicorn + Nginx + Systemd + Fabric

## 项目结构

```
notes/
├── notes/               # Django 项目配置
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── lists/               # 待办事项应用
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   └── list.html
│   └── static/
│       └── bootstrap/   # Bootstrap 3.3.4
├── functional_tests/    # Selenium 功能测试
│   └── tests.py
├── deploy_tools/        # 部署配置模板
│   ├── nginx.template.conf
│   └── gunicorn-systemd.template.service
├── fabfile.py           # Fabric 自动部署脚本
├── requirements.txt
└── manage.py
```

## 本地开发

```bash
# 1. 创建虚拟环境
python -m venv venv
venv\Scripts\activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 数据库迁移
python manage.py migrate

# 4. 启动开发服务器
python manage.py runserver

# 5. 访问 http://localhost:8000
```

## 运行测试

```bash
# 本地功能测试
python manage.py test functional_tests

# 对远程服务器运行功能测试
REAL_SERVER=39.105.88.230 python manage.py test functional_tests
```

## 自动部署

```bash
# 修改代码后 push 到 GitHub，然后：
python -m fabric -H yyy@39.105.88.230 -i F:/a_key/lty001.pem deploy
```

## 验收指令

```bash
# 1. 自动部署
python -m fabric -H yyy@39.105.88.230 -i F:/a_key/lty001.pem deploy

# 2. SSH 到服务器
ssh -i F:/a_key/lty001.pem root@39.105.88.230

# 3. 验证服务配置（四行均不报错）
sudo systemctl daemon-reload
sudo systemctl reload nginx
sudo systemctl enable gunicorn-39.105.88.230
sudo systemctl start gunicorn-39.105.88.230

# 4. 退出服务器
exit

# 5. 浏览器访问 http://39.105.88.230 验证：
#    - 新用户 -> 输入事项 -> "Your To-Do list" + 唯一 URL
#    - 新窗口 -> 新用户不受影响，URL 不同
#    - 旧 URL 回访 -> 数据仍然存在
```

## 服务器信息

| 项目 | 值 |
|------|-----|
| 公网 IP | 39.105.88.230 |
| 系统 | Ubuntu 22.04 |
| 用户 | yyy |
| SSH 密钥 | F:/a_key/lty001.pem |
| 站点路径 | /home/yyy/sites/39.105.88.230/ |
| Gunicorn 服务 | gunicorn-39.105.88.230 |
