#通用的管理任务
init:
    pip install -r requirements.txt
	
test:
    py.test tests

.PHONY: init test