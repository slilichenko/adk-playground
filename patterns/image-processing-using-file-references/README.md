# Processing images located on a Cloud Storage bucket

How can an agent process these images? Simply providing the URLs of the files to the model doesn't
work - the Gemini models don't know how to access these images. But Gemini models can process
so-called multimodal context if we provide it with the right Part.
See [product documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/inference#sample-requests-text-gen-multimodal-prompt)
for details.

Currently, ADK doesn't provide a native way to send Parts other than "text". A callback or a plug-in
can be used to add the required part to the LLM request. Here's at the high level how it can be done:

```mermaid
sequenceDiagram
    ADK->>Model: Request which causes image retrieval
    Model-->>ADK: invoke Image Retrieval Tool
    ADK->>Image Retrieval Tool: get images
    Image Retrieval Tool-->>Model: image metadata (URI and MIME type)

    Note right of ADK: potentially multiple conversational turns

    ADK->>Model: Request to process image details
    Note right of Model: Critical that the model is instructed to call this tool on this request 
    Model->>ADK: Call State Setting Tool(image metadata)
    
    ADK->>State Setting Tool: Invoke
    create participant Session State
    State Setting Tool->>Session State: store image metadata
    
    ADK->>Before Model Callback: run
    Before Model Callback->>Session State: get image metadata
    destroy Session State
    Before Model Callback-xSession State: clear state attribute

    Before Model Callback-->>Model: add Part(image metadata) to request
    Note right of ADK: This includes an empty functon response and Part with image metadata
    ADK->Model: Generate content
```