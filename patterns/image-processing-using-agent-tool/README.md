# Processing images located on a Cloud Storage bucket using AgentTool

This is a variation on how images can be processed by a subagent wrapped in an AgentTool rather than
by the root agent ([details](../image-processing-using-file-references)).

There are several important points here:

* The code is simpler than other approaches. No need to use the state to pass the data between
  different agent components
* The root agent content is not "polluted" by the image references. This should prevent an
  accidental processing of the image.
* The subagent has an input schema defined and that schema includes references to the image URI and
  MIME type. This requires the LLM to construct the tool call with the references to the image in
  addition to the description of the required processing. It can also cause issues if there is some
  ambiguity as to which image to process or the LLM just hallucinates. If this becomes a problem,
  the approach can be changed and the image reference can be stored in a state with potentially an
  extra step to validate that the right image is used.