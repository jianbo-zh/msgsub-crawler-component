import re


def is_valid_url(url):
    """
    判断URL地址是否有效
    """
    return re.match(
        r"https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]", url
    )

