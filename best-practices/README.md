# ADK Best Practices

A lot of best practices are documented in the ADK documentation. Consider this section an addendum
to the official docs.

## Agent Design

### Use good prompts

See [Gemini Prompting Strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies).

### Keep the number of functions per conversation turn limited

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
