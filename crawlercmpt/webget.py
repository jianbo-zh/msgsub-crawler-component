import requests
import const


class WebGet(object):
    """获取指定URL网页内容
    1, 获取静态网页内容
    2，获取JS动态渲染网页内容
    """

    def __init__(
        self,
        url,
        cb=None,
        passthrough=None,
        method=const.METHOD_GET,
        content_type=const.CT_HTML,
        render_type=const.RT_STATIC,
        timeout=10,
    ):
        self.url = url
        self.method = method
        self.content_type = content_type
        self.render_type = render_type
        self.timeout = 10

        self.passthrough = passthrough
        
        if callable(cb):
            self.cb = cb
        else:
            self.cb = lambda x: x

    def __call__(self):
        if self.render_type == const.RT_DYNAMIC:
            return self.get_dynamic_content()

        elif self.render_type == const.RT_STATIC:
            return self.get_static_content()

        else:
            raise ValueError("不支持的渲染类型[%s]" % self.render_type)

    def get_static_content(self):
        try:
            if self.method == const.METHOD_GET:
                res = requests.get(self.url, timeout=self.timeout)

            elif self.method == const.METHOD_POST:
                res = requests.post(self.url, timeout=self.timeout)

            else:
                raise ValueError("不支持的请求方法[%s]" % self.method)

        except Exception as err:
            self.cb(None, err, self.passthrough)

        else:
            self.cb(res, None, self.passthrough)

    def get_dynamic_content(self):
        return {"status": 200, "response": "html..."}
