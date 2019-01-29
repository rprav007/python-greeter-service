#!flask/bin/python
from flask import Flask
from flask_prometheus import monitor
from opentracing.ext import tags
from opentracing.propagation import Format
import random

app = Flask(__name__)

f = open('greetings.txt', 'r')
greetings = f.readlines()
f.close()

@app.route('/')
def index():
    tracer = init_tracer('greeting-service')
    getGreeter(tracer)

def getGreeter(tracer):
    span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
    span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER}
    with tracer.start_active_span('get-greeting', child_of=span_ctx, tags=span_tags):
        return random.choice(greetings).strip()

def init_tracer(service):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name=service,
    )
    return config.initialize_tracer()

if __name__ == '__main__':
    monitor(app, port=8000)
    app.run(host='0.0.0.0', port=8080)
