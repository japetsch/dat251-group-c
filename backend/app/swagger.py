import json
import os

from fastapi import FastAPI


class SwaggerJsonGenerator:

    @staticmethod
    def save_openapi_schema(app: FastAPI):
        OUTPUT_DIR = "../frontend/openapi/"
        OUTPUT_FILE = "openapi.json"
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        schema = app.openapi()

        with open(os.path.join(OUTPUT_DIR, OUTPUT_FILE), "w") as f:
            json.dump(schema, f, indent=2)
