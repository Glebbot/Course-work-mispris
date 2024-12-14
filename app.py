from flask import Flask, request
from database import db_select_query, db_execute_query
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/classification', methods=['GET'])
def get_classification_tree():
    classification_tree = db_select_query("select * from show_classification_tree();")
    return classification_tree.model_dump_json(by_alias=True)


@app.route('/classification', methods=['POST'])
def add_classification():
    json_data = request.json
    params = (json_data['short_name'], json_data['full_name'], json_data.get('id_unit'), json_data.get('parent_class_id'))
    db_execute_query("select * from add_classification(%s, %s, %s, %s);", params)
    return '', 200


@app.route('/classification/<int:id_classification>', methods=['PUT'])
def update_classification(id_classification):
    json_data = request.json
    params = (json_data['short_name'], json_data['full_name'], json_data.get('id_unit'), json_data.get('parent_class_id'), id_classification)
    db_execute_query(
        "update classification set short_name = %s, full_name = %s, id_unit = %s, id_parent_class = %s where id_classification = %s",
        params)
    return '', 200


@app.route('/classification/<int:id_classification>', methods=['DELETE'])
def delete_classification(id_classification):
    db_execute_query("delete from classification where id_classification = %s", (id_classification,))
    return '', 200


if __name__ == '__main__':
    app.run()
