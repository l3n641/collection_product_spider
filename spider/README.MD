###

windows PowerShell 设置scrapy全局代理:
$Env:http_proxy="http://127.0.0.1:8080";$Env:https_proxy="https://127.0.0.1:8080"

###

windows PowerShell 取消scrapy全局代理:  
$Env:http_proxy="";$Env:https_proxy=""

###

启动爬虫项目：
scrapy crawl project_name -a category_file=project_category_file.xlsx

