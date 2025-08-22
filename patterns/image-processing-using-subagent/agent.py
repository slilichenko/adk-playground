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

from typing import Optional

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse
from google.adk.tools import ToolContext
from google.genai.types import Part
from pydantic import Field, BaseModel, ConfigDict

IMAGE_URI_ATTR = 'image_uri'
IMAGE_MIME_ATTR = 'image_mime'


class ImageInfo(BaseModel):
    description: str = Field(description="Image description")
    cloud_storage_uri: str = Field(description="Cloud storage URI of the image")
    public_url: str = Field(description="Public URL of the image")
    mime_type: str = Field(description="Mime type of the image")
    model_config = ConfigDict(from_attributes=True)


def get_images_to_analyze() -> list[ImageInfo]:
    """Retrieves the list of the images to further analyze

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


def set_image_reference(
    image_cloud_storage_uri: str,
    image_mime_type: str,
    tool_context: ToolContext) -> None:
    tool_context.state[IMAGE_URI_ATTR] = image_cloud_storage_uri
    tool_context.state[IMAGE_MIME_ATTR] = image_mime_type
    return None


def before_model_callback(callback_context: CallbackContext,
    llm_request: LlmRequest) -> Optional[LlmResponse]:
    if callback_context.state.get(IMAGE_URI_ATTR, None):
        llm_request.contents[-1].parts.append(
            Part.from_uri(
                file_uri=callback_context.state[IMAGE_URI_ATTR],
                mime_type=callback_context.state[IMAGE_MIME_ATTR])
        )
        callback_context.state[IMAGE_URI_ATTR] = None
        callback_context.state[IMAGE_MIME_ATTR] = None
    return None

sub_agent = Agent(
    name="image_analyzing_agent",
    model="gemini-2.5-flash",
    description=(
        "Agent to analyze images"
    ),
    instruction=(
        """
        You are an agent who can analyze images. 
        """
    ),
    input_schema=ImageInfo,
    before_model_callback=before_model_callback
)


root_agent = Agent(
    name="image_processing_coordinator",
    model="gemini-2.5-flash",
    description=(
        "Agent to demo how images can be processed."
    ),
    instruction=(
        """
        You are an agent who can analyze images. 
        Use 'get_images_to_analyze' tool to get the list of available images.
        
        If you are asked to display the list of images - show image descriptions, public URLs and the MIME type.
        
        Before making a call to 'transfer_to_agent' function, make sure to call 'set_image_reference' function with the details of the image to be processed.
        """
    ),
    tools=[get_images_to_analyze, set_image_reference],
    sub_agents=[sub_agent]
)
