#!flask/bin/python
from flask import Flask, request
from flask_prometheus import monitor
from opentracing.ext import tags
from opentracing.propagation import Format
from jaeger_client import Config
import random
import logging
import sys
import time

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)

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

tracer = init_tracer('greeting-service')

f = open('greetings.txt', 'r')
greetings = f.readlines()
f.close()

@app.route('/')
def index():
    span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
    span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER}
    with tracer.start_span('get-greeting', child_of=span_ctx, tags=span_tags):
        global misbehave
        global delay
        
        time.sleep(int(delay))
        
        greeting = random.choice(greetings).strip()
        app.logger.debug('GREETING: ' + greeting)
        app.logger.debug('MISBEHAVE: %s', bool(misbehave))
        if misbehave:
            return "Unavailable", 503
        
        return greeting, 200

@app.route('/misbehave')
def misbehave():
    global misbehave 
    misbehave = True
    return "Misbehaving"

@app.route('/behave')
def behave():
    global misbehave 
    misbehave = False
    return "behaving"

@app.route('/healthz')
def healthz():
    global misbehave
    if misbehave:
        return "Unavailable", 503

    return "OK", 200

@app.route('/setDelay')
def setDelay():
    global delay
    delay = request.args.get("delay")
    return 'delay set for {0}'.format(delay)

if __name__ == '__main__':
    misbehave = False
    delay = 0
    monitor(app, port=8000)
    app.run(host='0.0.0.0', port=8080)
