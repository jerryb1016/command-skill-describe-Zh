from cli_describe_zh.main import DescribeZH

def test_describe_zh_initialization():
    app = DescribeZH()
    assert app.scanner is not None
    assert app.translator is not None
    assert app.cache is not None
