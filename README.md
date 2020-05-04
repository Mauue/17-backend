# 开发环境运行方式

- 安装环境库

  `pip freeze >requirements.txt`

- 设置环境变量
  - windows
    ```bash
        C:\17-backend>set FLASK_APP=app
    ```
  - Linux
    ```bash
        $ export FLASK_APP=app
    ```


- 运行

  `$ flask run`
  
  或
  
  `$ python -m flask run`