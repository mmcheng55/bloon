from jinja2 import Template, Environment, FileSystemLoader, select_autoescape
from ..settings import SettingsLoader
import datetime
import logging
import locale
import re
import os

settings = SettingsLoader(os.getcwd())
template_env = Environment(loader=FileSystemLoader(searchpath=os.getcwd() + '//' + settings.get("TEMPLATE_FOLDER")))


class ResponseBase:
    status_code = 200

    def __init__(self, content_type: str, **conf):
        self.content_type = content_type
        self.conf = conf
        self.body = ""
        self._cookies = []

        self.logger = logging.Logger("Bloon")

        self._encode = lambda text: text if type(text) == str else text
        self._encode_batch = lambda *args: [self._encode(a) for a in args]

    def head(self):
        return {
            "type": "http.response.start",
            "status": self.status_code,
            "headers": [
                [b"content-type", self.content_type.encode("utf8")],
                *[[k.encode(), v.encode()] for k, v in self.conf],
                *self._cookies
            ],
        }

    def set_cookie(
        self,
        key,
        value,
        secured: bool = False,
        domain: str = None,
        http_only: bool = False,
        same_site: str = None,
        path: str = None,
        max_age: int = None,
        expires: datetime.datetime = None,
    ):
        """
        Set Cookie.
        :param key:
        :param value:
        :param secured:
        :param domain:
        :param http_only:
        :param same_site:
        :param path:
        :param max_age:
        :param expires:
        :return:
        """
        ILLEGAL_CHAR = "()<>@,;:\\\"/[]?={}".split()
        r, d = "", {}
        if key in ILLEGAL_CHAR or value in ILLEGAL_CHAR:
            raise TypeError("Key or Value cannot contain these illegal characters: ()<>@,;:\\\"/[]?={}")

        d |= {k: v}
        if max_age and expires:
            self.logger.warning("Both Expires and Max-Age are set, Max-Age has precedence. "
                                "More info can check this page -> https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie")

        # d |= {"Expires": expires.strftime("%a")}

        self._cookies.append([b"set-cookies", '; '.join([f'{k}={v}' for k, v in d.items()])])

    def body_(self):
        return {
            "type": "http.response.body",
            "body": self.body,
        }


class TextResponse(ResponseBase):
    def __init__(self, text: str = ""):
        super().__init__(text)
        self.body = text.encode()


class RenderResponse(ResponseBase):
    def __init__(self, template_file: str = None, template_str: str = "", **kwargs):
        super().__init__("text/html")

        self.body = Template(template_str).render(**kwargs).encode() if template_str != "" else template_env.get_template(template_file).render(**kwargs).encode()


class ImageResponse(ResponseBase):
    def __init__(self, file):
        super().__init__("")
        with open(file, "rb") as f:
            self.body = f.read()

        self.content_type = f"image/{os.path.splitext(file)[1][1:]}"


class ErrorResponse(ResponseBase):
    pass
