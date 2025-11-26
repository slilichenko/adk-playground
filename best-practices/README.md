# ADK Best Practices

A lot of best practices are documented in the ADK documentation. Consider this section an addendum
to the official docs.

## Agent Design

### Use good prompts

See [Gemini Prompting Strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies), [Anthropic Prompt Engineering](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview),
or [OpenAI Prompt Engineering](https://platform.openai.com/docs/guides/prompt-engineering)
documentation for details.

### Chose the right model for your agent

Different models have different characteristics. Depending on the agent’s goals you might need to
choose a specific model or a family of models that are most suitable. If you are working with
Gemini, use [this page](https://ai.google.dev/gemini-api/docs/models) as an initial guidance.
Ultimately, the goal is to find the cheapest and fastest model that can do the job. But there is a
high chance you might end up using the latest Pro model (which is costlier and requires more time to
come up with responses) if your agent needs advanced reasoning. Test your instructions against the
target model - they can differ quite a bit. Always explicitly specify the model and never rely on a
default agent's model - when you update the ADK and the default model changed in the new release you
might not know that you need to retest, and potentially fix, your agent.

Many sophisticated agents will end up using different sub agents or will use agents as tools. In
ADK, you can use different LLM models to power different agents.

### Keep the number of tools per conversation turn limited

Why is it important? There are multiple reasons:

* Simplify LLM reasoning (and reduce hallucinations) by giving the model fewer choices.
* Reduce token count. Tool descriptions passed to the model are part of the context processed.
* Reduce the response latency. Less data passed in the request to the LLM API call, potentially
  faster LLM response.

What specific steps can be taken to actually keep the number of tools to the minimum?

* For simple agents, only add the functions as needed, one at a time.
* Don't add complete Toolsets with multiple functions, unless you are sure the agent might need all
  of them. Filter out the functions that are not needed.
* Once you see that the agent has groups of functions that are logically grouped and that functions
  in these groups should be executed one after another - it's a sign that your agent might benefit
  from refactoring (using AgentTools or subagents).

Sophisticated agents can use custom Toolsets which return the list of functions dependent of on the
session's state.

Additional steps in limiting tools' "footprint" on the context windows - tool and parameter
descriptions. Using good tool and parameter names can reduce the need to produce verbose
descriptions and, consequently, reduce the size of the LLM request/token count. But test how the
model selects the tool when needed.

## Tool design

### Follow the official best practices

The [ADK docs](https://google.github.io/adk-docs/tools/function-tools/#best-practices) are a
must-read. If your tools are resource intensive or long-running - read
the [tool performance](https://google.github.io/adk-docs/tools/performance/) section.

### Start with tool mocks to determine the most model friendly shape of the tool

Three things are important for tool interaction with the model - description, input parameters and
output. The description is critical for the model to select the tool at the right point.

Once a tool is selected, the model will provide the tool with parameters. Make sure that the model
does this consistently. The typical problem is the tool which expects some fixed values, let's say
upper-cased status values, but the model provides lower-cased values. You can make explicit
instructions in parameter descriptions or model prompt, or you can skip them and make the tool
resilient and include a small "parameter normalization" step.

The output shape is important - it needs to be "understandable" by the model. Don't include anything
that your model wouldn't need to use. Think of anything that's duplicated in the output and see if
you can a) group the data under the same key and b) reduce the size of the output.
See [this example](https://github.com/GoogleCloudPlatform/data-to-ai/blob/ce2bc64f84fd7bbfed2d3d738fa24779f811ae3f/agents/maintenance-scheduler/maintenance_scheduler/tools/tools.py#L131).

### Handle errors

If the tool throws an exception, ADK wouldn't know what to return to the model and the flow has to
stop. Depending on how the agent is deployed, the end user will see either a generic message along
the lines of "System is unavailable", or a cryptic message with the details of the failure. From the
end user point of view, the agent is broken. In most cases, it's better to handle all exceptions in
the tool and let the model know that the tool has failed to produce the result.

* Always produce the "status" node in your response with two possible values, "success" and "
  failure".
* If possible, add "failure_reason" node with the end user-friendly description. The model may
  decide to show that description to the user, which can improve user experience.
* Log the error and do the typical application monitoring to track failures and react to them
  quickly

Here's
an [example](https://github.com/GoogleCloudPlatform/data-to-ai/blob/ce2bc64f84fd7bbfed2d3d738fa24779f811ae3f/agents/maintenance-scheduler/maintenance_scheduler/tools/tools.py#L131)
of a function that follows these guidelines.

# Observability

How do you debug your agent or see how the agent performs in production? Depending on how you deploy
your agent, you can get a lot of answers ready for you. For example Google Cloud's Agent Engine
provides a lot of metrics out of the box.

## Low level details

Remember, ADK is just a sophisticated wrapper around LLM models. It does a lot of tricks to make
certain constructs to appear simple, but at the end of the day it all results in an LLM call. It is
often extremely useful to see request/response payloads of the LLM API calls. Depending on the model
this can be done differently.

For Gemini models accessed via Vertex AI you
can [configure request/response logging](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/request-response-logging).
If enabled, requests and responses are sent to BigQuery with minimal delay. Because they are stored
in columns of JSON type you can easily extract all kinds of data from these logs. You can
use [this script](observability/model_request_logging.py) to enable/disable/show logging
configuration.

