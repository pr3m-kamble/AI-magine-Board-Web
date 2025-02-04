from serverless_wsgi import handle_request  # Correct import name
from app import app

def handler(request, context):
    return handle_request(app, request, context)