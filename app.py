# -*- encoding: utf-8 -*-
"""
@File    : app.py
@Time    : 2020/5/20 11:10
@Author  : 陈华
@Description:
"""
import random
from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from

app = Flask(__name__)
Swagger(app)


@app.route('/api/<string:language>', methods=['GET'])
@swag_from("yml/api_get.yml")
def index(language):

    language = language.lower().strip()
    features = [
        "awesome", "great", "dynamic",
        "simple", "powerful", "amazing",
        "perfect", "beauty", "lovely"
    ]
    size = int(request.args.get('size', 1))
    if language in ['php', 'vb', 'visualbasic', 'actionscript']:
        return "An error occurred, invalid language for awesomeness", 500
    return jsonify(
        language=language,
        features=random.sample(features, size)
    )

# @app.route('/api/getReportList/', methods=['GET'])
# @swag_from("yml/getreportList.yml")
# def reportList():
#     reportList=['基础信用报告','深度信用报告','企业经营报告']
#     return jsonify(
#         reportList=reportList
#     )

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=8080)