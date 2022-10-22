import json
import textwrap
import inspect
from ariadne import ObjectType, make_executable_schema, graphql_sync
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify


type_defs = """
    type Query {
        hello: String!
    }
"""

query = ObjectType("Query")

@query.field("hello")
def resolve_hello(_, info):
    request = info.context
    user_agent = request.headers.get('User-Agent', 'Guest')
    return f"Hello, {user_agent}!"


schema = make_executable_schema(type_defs, query)

print(vars(schema.to_kwargs()['query']))


app = Flask(__name__)

@app.route("/graphql", methods=['GET'])
def graphql_playground():
    return PLAYGROUND_HTML, 200

@app.route("/graphql", methods=['POST'])
def graphql_server():
    data = request.get_json()
    print(data)
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug,
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == '__main__':
    print(json.dumps({
        'foo': 'bar'
    }))
    # app.run(debug=True)
