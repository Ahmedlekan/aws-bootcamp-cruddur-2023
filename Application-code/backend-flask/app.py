from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS, cross_origin
import os

import tracing
from tracing import tracer, meter, http_requests_total, http_errors_total, http_request_duration_seconds, http_active_requests, activities_created_total, messages_sent_total
from opentelemetry.instrumentation.flask import FlaskInstrumentor

from services.home_activities import *
from services.notifications_activities import *
from services.user_activities import *
from services.create_activity import *
from services.create_reply import *
from services.search_activities import *
from services.message_groups import *
from services.messages import *
from services.create_message import *
from services.show_activity import *

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
frontend = os.getenv('FRONTEND_URL', 'http://localhost:3000')
backend = os.getenv('BACKEND_URL', 'http://localhost:5000')
origins = [frontend, backend]

cors = CORS(
  app, 
  resources={r"/api/*": {"origins": origins}},
  supports_credentials=True,
  expose_headers=["location", "link"],
  allow_headers=[
        "Content-Type",
        "Authorization",
        "Access-Control-Allow-Credentials"
    ],
  methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
)

# ========== METRICS MIDDLEWARE ==========
@app.before_request
def before_request():
    # Track active requests
    http_active_requests.add(1)
    # Store start time for duration calculation
    request.start_time = time.time()

@app.after_request
def after_request(response):
    # Calculate duration
    duration = time.time() - getattr(request, 'start_time', time.time())
    
    # Get route pattern (e.g., "/api/activities/home")
    route = request.endpoint or "unknown"
    
    # Record metrics
    http_requests_total.add(1, {
        "method": request.method,
        "route": route,
        "status": str(response.status_code)
    })

    http_request_duration_seconds.record(duration, {
        "method": request.method,
        "route": route
    })

    # Track errors (4xx and 5xx)
    if response.status_code >= 400:
        http_errors_total.add(1, {
            "method": request.method,
            "route": route,
            "status": str(response.status_code)
        })
    
    # Decrease active requests
    http_active_requests.add(-1)

    response.headers.add('Access-Control-Allow-Origin', frontend)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@app.route("/api/message_groups", methods=['GET'])
def data_message_groups():
    with tracer.start_as_current_span("get_message_groups") as span:
        span.set_attribute("user.handle", "andrewbrown")
        user_handle = 'andrewbrown'
        model = MessageGroups.run(user_handle=user_handle)
        if model['errors'] is not None:
            span.set_attribute("error", True)
            span.set_attribute("error.message", str(model['errors']))
            return model['errors'], 422
        span.set_attribute("message_groups.count", len(model['data']))
        return model['data'], 200

@app.route("/api/messages/@<string:handle>", methods=['GET'])
def data_messages(handle):
    with tracer.start_as_current_span("get_messages") as span:
        span.set_attribute("user.sender", "andrewbrown")
        span.set_attribute("user.receiver", handle)
        user_sender_handle = 'andrewbrown'
        user_receiver_handle = request.args.get('user_reciever_handle')
        
        with tracer.start_as_current_span("fetch_messages_from_db"):
            model = Messages.run(user_sender_handle=user_sender_handle, 
                               user_receiver_handle=user_receiver_handle)
        
        if model['errors'] is not None:
            span.set_attribute("error", True)
            return model['errors'], 422
        return model['data'], 200

@app.route("/api/messages", methods=['POST','OPTIONS'])
@cross_origin()
def data_create_message():
    if request.method == 'OPTIONS':
        return {}, 200
        
    with tracer.start_as_current_span("create_message") as span:
        user_sender_handle = 'andrewbrown'
        user_receiver_handle = request.json['user_receiver_handle']
        message = request.json['message']
        
        span.set_attribute("message.sender", user_sender_handle)
        span.set_attribute("message.receiver", user_receiver_handle)
        span.set_attribute("message.length", len(message))
        
        with tracer.start_as_current_span("persist_message"):
            model = CreateMessage.run(message=message,
                                    user_sender_handle=user_sender_handle,
                                    user_receiver_handle=user_receiver_handle)
        
        if model['errors'] is not None:
            span.set_attribute("error", True)
            return model['errors'], 422
        
        # BUSINESS METRIC: Message sent
        messages_sent_total.add(1, {
            "sender": user_sender_handle,
            "receiver": user_receiver_handle,
            "message_length_bucket": "short" if len(message) < 50 else "long"
        })

        return model['data'], 200

@app.route("/api/activities/home", methods=['GET', 'OPTIONS'])
def data_home():
  # create a span
  with tracer.start_as_current_span("get_home_activities") as span:
    if request.method == 'OPTIONS':
        return {}, 200
    span.set_attribute("http.method", request.method)
    span.set_attribute("http.route", "/api/activities/home")
    # child span: business logic
    with tracer.start_as_current_span("fetch_home_activities"):
      data = HomeActivities.run()
    # child span: formatting response
    with tracer.start_as_current_span("format_home_response"):
      return jsonify(data), 200
    
@app.route("/api/activities/notifications", methods=['GET'])
def data_notifications():
    with tracer.start_as_current_span("get_notifications") as span:
        with tracer.start_as_current_span("fetch_notifications"):
            data = NotificationsActivities.run()
        span.set_attribute("notifications.count", len(data) if isinstance(data, list) else 0)
        return data, 200

@app.route("/api/activities/@<string:handle>", methods=['GET'])
def data_handle(handle):
    with tracer.start_as_current_span("get_user_activities") as span:
        span.set_attribute("user.handle", handle)
        
        with tracer.start_as_current_span("fetch_user_profile"):
            model = UserActivities.run(handle)
        
        if model['errors'] is not None:
            span.set_attribute("error", True)
            return model['errors'], 422
        span.set_attribute("activities.count", len(model['data']))
        return model['data'], 200

@app.route("/api/activities/search", methods=['GET'])
def data_search():
    with tracer.start_as_current_span("search_activities") as span:
        term = request.args.get('term')
        span.set_attribute("search.term", term)
        span.set_attribute("search.term_length", len(term) if term else 0)
        
        with tracer.start_as_current_span("execute_search_query"):
            model = SearchActivities.run(term)
        
        if model['errors'] is not None:
            span.set_attribute("error", True)
            return model['errors'], 422
        span.set_attribute("search.results_count", len(model['data']))
        return model['data'], 200

@app.route("/api/activities", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities():
    if request.method == 'OPTIONS':
        return {}, 200
        
    with tracer.start_as_current_span("create_activity") as span:
        user_handle = 'andrewbrown'
        message = request.json['message']
        ttl = request.json['ttl']
        
        span.set_attribute("activity.user", user_handle)
        span.set_attribute("activity.ttl", ttl)
        span.set_attribute("activity.message_length", len(message))
        
        with tracer.start_as_current_span("insert_activity"):
            model = CreateActivity.run(message, user_handle, ttl)
        
        if model['errors'] is not None:
            span.set_attribute("error", True)
            return model['errors'], 422
        
        # BUSINESS METRIC: Activity created
        activities_created_total.add(1, {
            "user": user_handle,
            "ttl": str(ttl),
            "has_message": str(len(message) > 0)
        })
        return model['data'], 200

@app.route("/api/activities/<string:activity_uuid>", methods=['GET'])
def data_show_activity(activity_uuid):
    with tracer.start_as_current_span("show_activity") as span:
        span.set_attribute("activity.uuid", activity_uuid)
        
        with tracer.start_as_current_span("fetch_activity_details"):
            data = ShowActivity.run(activity_uuid=activity_uuid)
        
        return data, 200

@app.route("/api/activities/<string:activity_uuid>/reply", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities_reply(activity_uuid):
    if request.method == 'OPTIONS':
        return {}, 200
        
    with tracer.start_as_current_span("create_reply") as span:
        user_handle = 'andrewbrown'
        message = request.json['message']
        
        span.set_attribute("reply.activity_uuid", activity_uuid)
        span.set_attribute("reply.user", user_handle)
        
        with tracer.start_as_current_span("persist_reply"):
            model = CreateReply.run(message, user_handle, activity_uuid)
        
        if model['errors'] is not None:
            span.set_attribute("error", True)
            return model['errors'], 422
        return model['data'], 200

if __name__ == "__main__":
  app.run(debug=True)