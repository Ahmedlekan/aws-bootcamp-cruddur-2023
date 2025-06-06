from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS, cross_origin
import os

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

# X-RAY
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

# """Initialize X-Ray Tracing"""
def init_xray(app):
    xray_url = os.getenv("AWS_XRAY_URL")
    xray_recorder.configure(
        service='backend-flask',
        daemon_address=os.getenv('AWS_XRAY_DAEMON_ADDRESS'),
        dynamic_naming=xray_url
    )
    XRayMiddleware(app, xray_recorder)

app = Flask(__name__)

# Initialize X-Ray
init_xray(app) 

# codespace_name = os.getenv("CODESPACE_NAME")
# Define actual frontend/backend origins
# frontend = f"https://3000-{codespace_name}.app.github.dev"
# backend = f"https://4567-{codespace_name}.app.github.dev"

frontend = "https://3000-ahmedlekan-awsbootcampc-lz857wdtkn3.ws-us118.gitpod.io"
backend = "https://4567-ahmedlekan-awsbootcampc-lz857wdtkn3.ws-us118.gitpod.io"

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

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', frontend)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@app.route("/api/message_groups", methods=['GET'])
def data_message_groups():
  user_handle  = 'andrewbrown'
  model = MessageGroups.run(user_handle=user_handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/messages/@<string:handle>", methods=['GET'])
def data_messages(handle):
  user_sender_handle = 'andrewbrown'
  user_receiver_handle = request.args.get('user_reciever_handle')

  model = Messages.run(user_sender_handle=user_sender_handle, user_receiver_handle=user_receiver_handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/messages", methods=['POST','OPTIONS'])
@cross_origin()
def data_create_message():
  user_sender_handle = 'andrewbrown'
  user_receiver_handle = request.json['user_receiver_handle']
  message = request.json['message']

  model = CreateMessage.run(message=message,user_sender_handle=user_sender_handle,user_receiver_handle=user_receiver_handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/activities/home", methods=['GET', 'OPTIONS'])
def data_home():
    if request.method == 'OPTIONS':
        return {}, 200
    data = HomeActivities.run()
    return jsonify(data), 200
    
@app.route("/api/activities/notifications", methods=['GET'])
def data_notifications():
  data = NotificationsActivities.run()
  print("📦 Returning data:", data) 
  return data, 200

@app.route("/api/activities/@<string:handle>", methods=['GET'])
def data_handle(handle):
  model = UserActivities.run(handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/activities/search", methods=['GET'])
def data_search():
  term = request.args.get('term')
  model = SearchActivities.run(term)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/activities", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities():
  user_handle  = 'andrewbrown'
  message = request.json['message']
  ttl = request.json['ttl']
  model = CreateActivity.run(message, user_handle, ttl)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/activities/<string:activity_uuid>", methods=['GET'])
def data_show_activity(activity_uuid):
  data = ShowActivity.run(activity_uuid=activity_uuid)
  return data, 200

@app.route("/api/activities/<string:activity_uuid>/reply", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities_reply(activity_uuid):
  user_handle  = 'andrewbrown'
  message = request.json['message']
  model = CreateReply.run(message, user_handle, activity_uuid)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

if __name__ == "__main__":
  app.run(debug=True)