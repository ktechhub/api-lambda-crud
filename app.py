from chalice import Chalice
import boto3
from boto3.dynamodb.conditions import Key

app = Chalice(app_name='api-crud-sample')

def get_app_db():
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table('my-demo-table')
    return table


@app.route('/book', methods=['POST'])
def add_book():
    data = app.current_request.json_body
    try:
        get_app_db().put_item(Item={
            'id': data['id'],
            "title": data['title'],
            "author": data['author']
        })
        return {'message': 'ok - CREATED', 'status': 201, "id": data['id'], "title": data['title'], "author": data['author']}
    except Exception as e:
        return {'message': str(e)}

@app.route('/', methods=['GET'])
def index():
    response = get_app_db().scan()
    data = response.get('Items', None)
    return {'data': data}

app.route('/book/{id}', methods=['GET'])
def get_book(id):
    response = get_app_db().query(
        KeyConditionExpression=Key("id").eq(id)
    )
    data = response.get('Items', None)
    return {'data': data}


@app.route('/book/{id}', methods=['PUT'])
def update_book(id):
    data = app.current_request.json_body
    try:
        get_app_db().update_item(Key={
            "id": data['id'],
            "author": data['author']
        },
            UpdateExpression="set title=:r",
            ExpressionAttributeValues={
            ':r': data['title']
        },
            ReturnValues="UPDATED_NEW"
        )
        return {'message': 'ok - UPDATED', 'status': 201}
    except Exception as e:
        return {'message': str(e)}

@app.route('/book/{id}', methods=['DELETE'])
def delete_book(id):
    data = app.current_request.json_body
    try:
        response = get_app_db().delete_item(
            Key={
                "id": data['id'],
                "author": data['author']
            }
        )
        return {'message': 'ok - DELETED', 'status': 201}

    except Exception as e:
        return {'message': str(e)}


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
