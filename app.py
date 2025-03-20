import json


from flask import Flask, request
from db_manage.mysql_connector.database import Database
from flask_cors import CORS

app = Flask(__name__)

CORS(app, supports_credentials=True)


@app.route("/projects", methods=["GET"])
def get_projects():
	filter = request.args.get("filter", "")
	db = Database("Project")
	objects = db.get_filtered_list_of_objects("Project", filter, inJson=True)
	return json.dumps(objects), 200


@app.route("/project", methods=["GET"])
def get_project():
	data = request.json
	db = Database("Project")
	objects = db.get_object_by_id("Project", data["id"], inJson=True)
	return json.dumps(objects), 200
	

@app.route("/project", methods=["POST"])
def create_project():
	data = request.json
	db = Database("Project")
	if db.get_list_of_objects('Project',conditions={"name": data["name"]}):
		return f"project with name '{data["name"]}' already exists", 400
	id = db.add_object("Project", data)
	return json.dumps({"id": id}), 201


@app.route("/project", methods=["PUT"])
def update_project():
	data = request.json
	db = Database("Project")
	id = data["id"]
	del data["id"]
	db.update_object("Project", id, data)
	return "", 204


@app.route("/project", methods=["DELETE"])
def delete_project():
	id = request.args.get("id")
	db = Database("Project")
	db.delete_object("Project", id)
	return "", 204

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)