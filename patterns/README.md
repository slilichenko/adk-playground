# ADK Design Patterns

The subdirectories in this folder contain fully functional ADK agents which illustrate a particular
design pattern. Currently, these patterns are implemented using Python SDK.

The code in these agents is not using all the [best practices](../best-practices/README.md) we
advocate for. We only provide bare minimum tool implementations to illustrate a specific
pattern/technique.

## Installation

In order to run these agents locally, follow
the [ADK Python installation instructions](https://google.github.io/adk-docs/get-started/installation/).

The code assumes that you will be using Google Cloud's Vertex AI models in `us-central1` region. You
would need
to [set up authentication](https://google.github.io/adk-docs/get-started/quickstart/#dev-ui-adk-web)
in order for the agent to be able to use the so-called Application Default Credentials when
connecting to Vertex AI.

> [!NOTE]
> Running against Google's models is not a requirement. You can these agents against any other model
> supported by ADK, assuming that the model has the functionality needed by the agent.

Once the Python environment is set up, run

```shell
export GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
export DEFAULT_MODEL=<model-to-try>
adk web
```

in this directory, select the agent you would to explore and use the prompts in the agent's README
file.

## Patterns by categories

### Binary file analysis

It's easy to process images or other binary files when they can be provided as part of the
prompt. [Here](https://github.com/gitrey/adk-samples/blob/main/agents/image-description/agent.py) is
one example of how to submit an image for analysis to a model.

But if the images are provided as references or need to be dynamically selected by the model based
on certain criteria - there is no simple solution.

* [Processing images using Cloud Storage references](image-processing-using-file-references)
* [Processing images using subabents](image-processing-using-subagent)
 
