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
import os
from typing import Optional

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse
from google.adk.tools import AgentTool
from google.genai.types import Part, Content
from pydantic import Field, BaseModel, ConfigDict


class ImageInfo(BaseModel):
    description: str = Field(description="Image description")
    cloud_storage_uri: str = Field(description="Cloud storage URI of the image")
    public_url: str = Field(description="Public URL of the image")
    mime_type: str = Field(description="Mime type of the image")
    model_config = ConfigDict(from_attributes=True)


class ImageProcessingRequest(BaseModel):
    request: str = Field(
        description="What kind of analysis needs to be done on the image?")
    cloud_storage_uri: str = Field(description="Cloud storage URI of the image")
    mime_type: str = Field(description="Mime type of the image")
    model_config = ConfigDict(from_attributes=True)


def get_images_to_analyze() -> list[ImageInfo]:
    """Retrieves the list of the images to analyze

    Returns:
         list: list of images
    """
    return [
        ImageInfo(
            description="Duck and truck",
            cloud_storage_uri="gs://cloud-samples-data/vision/duck_and_truck.jpg",
            public_url="https://storage.googleapis.com/cloud-samples-data/vision/duck_and_truck.jpg",
            mime_type="image/png"),
        ImageInfo(
            description="Handwritten note",
            cloud_storage_uri="gs://cloud-samples-data/vision/handwritten.jpg",
            public_url="https://storage.googleapis.com/cloud-samples-data/vision/handwritten.jpg",
            mime_type="image/png"
        )
    ]


def convert_text_request_into_multimodal_call(callback_context: CallbackContext,
    llm_request: LlmRequest) -> Optional[LlmResponse]:
    try:
        image_processing_request = ImageProcessingRequest.model_validate_json(
            llm_request.contents[0].parts[0].text)
        llm_request.contents[0].parts[0].text = image_processing_request.request
        llm_request.contents[0].parts.append(
            Part.from_uri(
                file_uri=image_processing_request.cloud_storage_uri,
                mime_type=image_processing_request.mime_type)
        )
    except ValueError as e:
        print("Failed to parse the image_processing_request: ", e)
        return LlmResponse(
            content=Content(
                role="model",
                parts=[Part(text="Unable to process the image_processing_request because some parameters are missing")],
            ))

    return None


sub_agent = Agent(
    name="image_analyzing_agent",
    model=os.getenv("DEFAULT_MODEL"),
    description=(
        "Agent to analyze images"
    ),
    instruction=(
        """
        You are an agent who can analyze images. 
        """
    ),
    input_schema=ImageProcessingRequest,
    before_model_callback=convert_text_request_into_multimodal_call
)

image_analyzer_tool = AgentTool(sub_agent)

root_agent = Agent(
    name="image_processing_coordinator",
    model=os.getenv("DEFAULT_MODEL"),
    description=(
        "Agent to demo how images can be processed."
    ),
    instruction=(
        """
        You are an agent who can analyze images. 
        Use 'get_images_to_analyze' tool to get the list of available images.
        
        If you are asked to display the list of images - show image descriptions, public URLs and the MIME type.
        
        If you are asked any other questions - try to find the image corresponding to the question and analyze it. 
        You MUST call 'get_image_reference' tool before analyzing the image, which will return the image details.
        
        Don't use general knowledge to answer questions - the answer MUST be based on the image analysis.
        """
    ),
    tools=[get_images_to_analyze, image_analyzer_tool]
)
