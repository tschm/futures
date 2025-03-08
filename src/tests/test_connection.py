from futures.bloomberg.conn import connect


def test_connect():
    with connect() as session:
        assert session is not None
