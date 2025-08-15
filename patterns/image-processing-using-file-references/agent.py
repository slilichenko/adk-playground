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


def get_image_reference(
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


root_agent = Agent(
    name="image_processing_agent",
    model="gemini-2.5-flash",
    description=(
        "Agent to demo how images can be processed."
    ),
    instruction=(
        """
        You are an agent who can analyze images. 
        Use 'get_images_to_analyze' tool to get the list of available images.
        Display the list of images using their description and public URL.
        
        When asked what's the color of an object, analyze the provided image.
        
        Call 'get_image_reference' tool before processing the image.
        """
    ),
    tools=[get_images_to_analyze, get_image_reference],
    before_model_callback=before_model_callback
)
