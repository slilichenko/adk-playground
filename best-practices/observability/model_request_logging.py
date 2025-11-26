#  Copyright 2025 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import argparse
import os

import vertexai
from vertexai.preview.generative_models import GenerativeModel


# Script expects three parameters - project ID, location (region or "global"),
# the model name or model endpoint, the dataset name .


# See https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/request-response-logging


def enable_logging(
    vertex_ai_project_id: str,
    location: str,
    model_name: str,
    bigquery_project_id: str,
    dataset: str,
    table_name: str,
    rate: float):
    vertexai.init(project=vertex_ai_project_id, location=location)

    model = GenerativeModel(model_name=model_name)
    model.set_request_response_logging_config(
        enabled=True,
        sampling_rate=rate,
        bigquery_destination=f"bq://{bigquery_project_id}.{dataset}.{table_name}",
        enable_otel_logging=False
    )


def disable_logging(
    vertex_ai_project_id: str,
    location: str,
    model_name: str):
    vertexai.init(project=vertex_ai_project_id, location=location)

    model = GenerativeModel(model_name=model_name)
    model.set_request_response_logging_config(
        enabled=False,
        sampling_rate=1.,
        bigquery_destination=f"bq://none.none.none"
    )


def show_logging_configuration(
    vertex_ai_project_id: str,
    location: str,
    model_name: str):
    vertexai.init(project=vertex_ai_project_id, location=location)

    url = f"https://aiplatform.googleapis.com/v1beta1/projects/{vertex_ai_project_id}/locations/{location}/publishers/google/models/{model_name}:fetchPublisherModelConfig"
    os.system(
        f"curl -X GET -H \"Authorization: Bearer $(gcloud auth print-access-token)\" {url}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=['enable', 'disable', 'show'])
    parser.add_argument("--vertex_ai_project_id", "-v",
                        type=str,
                        help="Vertex AI project id where the Gemini calls will be made")
    parser.add_argument("--location", "-l", type=str,
                        help="Either Google Cloud region or 'global'")
    parser.add_argument("--model", "-m", type=str,
                        help="Model name or endpoint id")
    parser.add_argument("--bigquery_project_id", "-b", type=str,
                        help="Project id where BigQuery dataset resides")
    parser.add_argument("--dataset", "-d", type=str,
                        help="BigQuery dataset id")
    parser.add_argument("--table", "-t", type=str,
                        help="BigQuery table name"),
    parser.add_argument("--rate", "-r", type=float,
                        help="Sampling rate. Must be between 0 and 1.")
    args = parser.parse_args()

    match args.action:
        case 'enable':
            enable_logging(
                vertex_ai_project_id=args.vertex_ai_project_id,
                location=args.location,
                model_name=args.model,
                bigquery_project_id=args.bigquery_project_id if args.bigquery_project_id else args.vertex_ai_project_id,
                dataset=args.dataset,
                table_name=args.table,
                rate=args.rate)
        case 'disable':
            disable_logging(
                vertex_ai_project_id=args.vertex_ai_project_id,
                location=args.location,
                model_name=args.model,
            )

        case 'show':
            show_logging_configuration(
                vertex_ai_project_id=args.vertex_ai_project_id,
                location=args.location,
                model_name=args.model)
