# ADK Design Patterns

The subdirectories in this folder contain fully functional ADK agents which illustrate a particular
design pattern. Currently, these patterns are implemented using Python SDK.

## Installation

In order to run these agents locally, follow
the [ADK Python installation instructions](https://google.github.io/adk-docs/get-started/installation/).

The code assumes that you will be using Google Cloud's Vertex AI models in `us-central1` region. You
would need
to [set up authentication](https://google.github.io/adk-docs/get-started/quickstart/#dev-ui-adk-web)
in order for the agent to be able to use the so-called Application Default Credentials when
connecting to Vertex AI.

Once the Python environment is set up, run

```shell
export GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
adk web
```

in this directory, select the agent you would to explore and use the prompts in the agent's README
file.

## Patterns by categories

### Binary file analysis

It's easy to process images or other binary files when they can be provided as part of the prompt.
But if the images are provided as references or need to be dynamically selected by the model based
on certain criteria - there is no simple solution.

* [Processing images using Cloud Storage references](image-processing-using-file-references)
* [Processing images using subabents](image-processing-using-subagent)
 
