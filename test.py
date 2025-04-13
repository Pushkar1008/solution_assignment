from flask_restful import Resource
import os, sys, re, getpass
class test(Resource):
    def get(self):

        return {'message': 'success', 'user': getpass.getuser(), 'python version': sys.version_info[0]}