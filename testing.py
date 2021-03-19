import pytest


class BadRequestTypeError(Exception):
    pass


class BadHTTPVersion(Exception):
    pass


class HttpRequestTwo:
    def __init__(self, request_string):
        self.request_string = request_string


class HttpRequest:
    def __init__(self, request_type, path, protocol):
        self.request_type = request_type
        self.path = path
        self.protocol = protocol


def reqstr2obj(request_string):
    if not isinstance(request_string, str):
        raise TypeError
    three_values = request_string.split(" ")
    types = ["GET", "HEAD", "POST", "PUT", "CONNECT", "POST", "TRACE"]
    http_versions = ["HTTP1.0", "HTTP1.1", "HTTP2.0"]
    if len(three_values) == 3:
        a, b, c = three_values
        if a in types and str(b).strip()[0] == "/" and c in http_versions:
            return HttpRequest(a, b, c)
        elif str(b).strip()[0] != "/":
            raise ValueError
        elif c not in http_versions:
            raise BadHTTPVersion
        elif a not in types:
            raise BadRequestTypeError
    else:
        return None


class TestHttp:

    def test_1(self):
        with pytest.raises(TypeError):
            assert reqstr2obj(123)

    def test_2(self):
        assert isinstance(reqstr2obj("GET / HTTP1.1"), HttpRequestTwo)

    def test_3(self):
        obj = reqstr2obj("GET / HTTP1.1")
        assert obj.request_type == "GET"
        assert obj.path == "/"
        assert obj.protocol == "HTTP1.1"

    def test_4(self):
        assert isinstance(reqstr2obj("GET / HTTP1.1"), HttpRequest)

    def test_5(self):
        assert reqstr2obj("GET /HTTP1.1") is None

    def test_6(self):
        with pytest.raises(BadRequestTypeError):
            reqstr2obj("DOWNLOAD /movie.mp4 HTTP1.1")

    def test_7(self):
        with pytest.raises(BadHTTPVersion):
            assert reqstr2obj("GET / HTTP0.1")

    def test_8(self):
        with pytest.raises(ValueError):
            reqstr2obj("GET % HTTP1.1")