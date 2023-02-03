import logging
import os

import bson
from bson import ObjectId
from pymongo import MongoClient


class DB:
    def __init__(self):
        self.client = MongoClient(os.getenv("DB_CONNECTION_STR"))
        self.db = self.client["pizzeria"]
        self.reports_collection = self.db["reports"]

    def save_report(self, report):
        db_id = self.reports_collection.insert_one(report).inserted_id
        print("report saved to db with id: ", db_id)

    def get_report(self, report_id):
        try:
            object_id = ObjectId(report_id)
        except bson.errors.InvalidId:
            logging.error("Invalid id provided", report_id)
            return
        report = self.reports_collection.find_one(object_id)
        if report is None:
            logging.info("Report %s not found", report_id)
            return
        logging.info("Report: %s", report)
