# -*- coding: utf-8 -*-
import sys
import os
import jsonpickle as jsonpickle
from flask import Flask, request,jsonify
from flask_restful import Api
from flask_cors import CORS
from test import test
from detect_module import detect
from llm_module import llm_request_handler


def create_app(config_filename):
    app = Flask(__name__)
    app.secret_key = "super secret key"
    CORS(app)

    @app.route('/')
    def home():
        return "Cancer Detection Service is running"
    
        
    @app.route("/process_text", methods=['POST'])
    def process():
        try:
            return detect(request)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route("/process_from_llm", methods=['POST'])
    def llm_process():
        try:
            return llm_request_handler(request)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    app.config.from_object(config_filename)
    api = Api(app)

    api.add_resource(test, '/test')

    return app