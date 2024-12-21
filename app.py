from flask import Flask, request
from database import db_select_query, db_execute_query
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/classification/tree', methods=['GET'])
def get_classification_tree():
    classification_tree = db_select_query("select * from show_classification_tree();")
    return classification_tree.model_dump_json(by_alias=True)


@app.route('/classification', methods=['GET'])
def get_classification():
    classification = db_select_query("select * from classification;")
    return classification.model_dump_json(by_alias=True)


@app.route('/classification', methods=['POST'])
def add_classification():
    json_data = request.json
    params = (json_data['short_name'], json_data['full_name'], json_data.get('id_unit'), json_data.get('id_parent_class'))
    db_execute_query("select * from add_classification(%s, %s, %s, %s) ;", params)
    return '',200


@app.route('/classification/<int:id_classification>', methods=['PUT'])
def update_classification(id_classification):
    json_data = request.json
    params = (json_data['short_name'], json_data['full_name'], json_data.get('id_unit'), json_data.get('id_parent_class'), id_classification)
    db_execute_query(
        "update classification set short_name = %s, full_name = %s, id_unit = %s, id_parent_class = %s where id_classification = %s",
        params)
    return '', 200


@app.route('/classification/<int:id_classification>', methods=['DELETE'])
def delete_classification(id_classification):
    db_execute_query("delete from classification where id_classification = %s", (id_classification,))
    return '', 200


@app.route('/product', methods=['GET'])
def get_products():
    classification_tree = db_select_query("select * from product;")
    return classification_tree.model_dump_json(by_alias=True)


@app.route('/product/<int:id_classification>', methods=['GET'])
def get_products_by_classification(id_classification):
    classification_tree = db_select_query("select * from show_products_by_classification(%s);", (id_classification,))
    return classification_tree.model_dump_json(by_alias=True)


@app.route('/product', methods=['POST'])
def add_product():
    json_data = request.json
    params = (json_data['short_name'], json_data['full_name'], json_data.get('id_classification'), json_data.get('price'), json_data.get('id_unit'))
    db_execute_query("select * from add_product(%s, %s, %s, %s, %s);", params)
    return json_data


@app.route('/product/<int:id_product>', methods=['PUT'])
def update_product(id_product):
    json_data = request.json
    params = (json_data['short_name'], json_data['full_name'], json_data.get('id_classification'), json_data.get('price'), json_data.get('id_unit'), id_product)
    db_execute_query(
        "update product set short_name = %s, full_name = %s, id_classification = %s, price = %s, id_unit = %s where id_product = %s",
        params)
    return '', 200


@app.route('/product/<int:id_product>', methods=['DELETE'])
def delete_product(id_product):
    db_execute_query("delete from product where id_product = %s", (id_product,))
    return '', 200


@app.route('/product/<int:id_product>', methods=['POST'])
def copy_product(id_product):
    to_copy = db_select_query("select * from product where id_product=%s;", (id_product,))
    params = (to_copy.data[0]['short_name'], to_copy.data[0]['full_name'], to_copy.data[0]['id_classification'], to_copy.data[0]['price'], to_copy.data[0]['id_unit'])
    db_execute_query("insert into product (short_name, full_name, id_classification, price, id_unit) values (%s, %s, %s, %s, %s);",params)
    to_copy.data[0].pop('key')
    return to_copy.data[0]


@app.route('/spec/<int:id_product>', methods=['GET'])
def get_product_spec(id_product):
    spec_tree = db_select_query("select * from show_spec_tree(%s);", (id_product,))
    return spec_tree.model_dump_json(by_alias=True)


@app.route('/spec', methods=['POST'])
def add_spec():
    json_data = request.json
    params = (json_data['id_product'], json_data['id_position'], json_data['id_part'], json_data['quantity'])
    db_execute_query("select * from add_spec_product(%s, %s, %s, %s);", params)
    return json_data


@app.route('/spec', methods=['GET'])
def get_spec():
    spec_list = db_select_query("SELECT product.full_name AS full_product_name, spec_product.id_product, spec_product.id_part, spec_product.id_position, spec_product.quantity,part_product.full_name AS full_part_name FROM spec_product JOIN product ON spec_product.id_product = product.id_product LEFT JOIN product AS part_product ON spec_product.id_part = part_product.id_product;")
    return spec_list.model_dump_json(by_alias=True)


@app.route('/spec/id_products', methods=['GET'])
def get_id_products():
    spec_list = db_select_query("SELECT distinct id_product FROM spec_product;")
    return spec_list.model_dump_json(by_alias=True)


@app.route('/classification/id_classifications', methods=['GET'])
def get_id_products():
    class_list = db_select_query("SELECT distinct id_classification FROM classification;")
    return class_list.model_dump_json(by_alias=True)


@app.route('/classification/summary_rates/<int:id_classification>', methods=['GET'])
def get_classification_tree(id_classification):
    summary_rates = db_select_query("select * from calculation_summary_rates(%s);", (id_classification,))
    return summary_rates.model_dump_json(by_alias=True)


if __name__ == '__main__':
    app.run()
