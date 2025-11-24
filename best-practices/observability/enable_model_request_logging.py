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

# See https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/request-response-logging

# Script expects three parameters - project ID, location (region or "global")
# and the model name or model endpoint.
import sys

import vertexai
from vertexai.preview.generative_models import GenerativeModel

def enable_logging(project_id: str, location: str, model_name: str):
    vertexai.init(project=project_id, location=location)

    model = GenerativeModel(model_name=model_name)
    model.set_request_response_logging_config(
        enabled=True,
        sampling_rate=1.0,
        bigquery_destination="bq://event-processing-demo.agent_logs.llm_request_response",
        enable_otel_logging=False
    )

if __name__ == "__main__":
    enable_logging(sys.argv[1], sys.argv[2], sys.argv[3])