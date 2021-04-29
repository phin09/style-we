# uwsgi 테스트용
# https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html#basic-test

def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return [b"testtest"] # python3