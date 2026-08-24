# New Copilot Studio and Skills

[Back to the repository overview](../README.md)

This directory contains the examples demonstrated in the YouTube video about the new Microsoft Copilot Studio agent-building experience and its support for reusable Skills.

The examples illustrate how Skills can extend an agent with focused instructions, supporting resources, and executable scripts. They also demonstrate how several small Skills can work together to complete a larger task.

## Topics demonstrated in the video

The video provides an overview of the redesigned Copilot Studio interface and explains several important changes and capabilities:

- The new, structured agent-building interface
- Agent instructions and model selection
- Knowledge sources and uploaded files
- Tools, connectors, and MCP servers
- Reusable Skills
- Script execution inside Skills
- Memory and connected agents
- Previewing and testing an agent
- Evaluation with prepared test data
- Publishing and monitoring agents
- Using workflows instead of agent-level triggers
- Invoking a Copilot agent from a trigger inside a workflow

## Examples in this directory

The demonstrated scenario analyzes a supplied text and creates several outputs by combining focused Skills.

### 1. Word statistics

The first Skill processes a plain-text input and creates a word-frequency analysis. A script counts the words and returns the result as structured data or a table.

### 2. Chart generation

Another Skill uses the word statistics to generate a downloadable bar chart. This Skill concentrates only on visualization and can therefore be reused with compatible data from other sources.

### 3. Excel export

A separate Skill converts the statistics into an Excel workbook. Once the original text analysis has finished, the chart and Excel Skills can be executed independently or in parallel.

This modular approach keeps the individual capabilities easier to understand, test, maintain, combine, and reuse.

## Skills and script execution

A Skill is a reusable capability that explains how an agent should complete a particular task. A Skill package can contain instructions, scripts, templates, references, and other supporting files.

One of the most important features demonstrated in the video is the ability to include executable scripts in a Skill.

Depending on the compilers and runtimes installed and available in the isolated execution environment, Skills can use technologies such as:

- Python
- JavaScript and Node.js
- Go
- Bash and Shell scripts
- Other languages supported by an available compiler or runtime

Runtime availability, package installation, network access, and resource limits can differ between environments. Verify these requirements before relying on a particular technology in a production solution.

## Recommended Skill design

Create small Skills that each perform one clearly defined task.

For example:

```text
Text input
   |
   v
Word statistics Skill
   |
   +----> Chart Skill ----> PNG chart
   |
   +----> Excel Skill ----> XLSX workbook
```

Although all three operations could be implemented in one large Skill, separating them provides several advantages:

- Each Skill has a clear responsibility.
- Skills can be tested independently.
- A capability can be reused by another agent.
- Outputs are created only when they are required.
- Independent Skills can potentially run in parallel.
- Maintenance and troubleshooting become easier.

## Typical Skill package structure

A Skill package normally uses a structure similar to the following:

```text
Example-Skill/
├── SKILL.md
├── scripts/
│   └── example-script.py
├── references/
└── assets/
```

Only `SKILL.md` is required. The other directories are optional and depend on the purpose of the Skill.

The `SKILL.md` file normally defines:

- The Skill name
- A description that helps the agent decide when to use it
- The task the Skill should perform
- Required input information
- Instructions for using supporting scripts or resources
- The expected output
- Any validation or error-handling requirements

When a complete Skill directory is packaged as a ZIP file, keep `SKILL.md` at the root of the package unless the example explicitly specifies a different structure.

## Triggers and workflows

In the new Copilot Studio experience, event-based triggers are configured in workflows rather than directly inside the agent.

A typical process can look like this:

1. A workflow starts when an event occurs.
2. The event might be an incoming email, an HTTP request, or another supported trigger.
3. The workflow prepares the information required by the agent.
4. The workflow invokes a published Copilot agent.
5. The agent uses its instructions, knowledge, tools, and Skills to process the request.
6. The workflow continues with the agent's result.

This separation allows the same agent to be invoked from different processes and channels without embedding every possible trigger in the agent itself.

## Requirements

Depending on which example you want to use, you may need:

- Access to Microsoft Copilot Studio
- A suitable Copilot Studio environment
- Permissions to create and publish agents and workflows
- Copilot Credits or another applicable license
- A supported Python runtime
- Node.js and npm
- Go
- Bash or another compatible Shell
- Libraries or packages referenced by an individual script

Not every example requires every runtime. Review the supplied Skill and script files before installing additional software.

## Using the examples

1. Review all files in this directory.
2. Open the relevant Skill directory and inspect its `SKILL.md`.
3. Review any scripts before executing or uploading the Skill package.
4. Check whether the required runtime and dependencies are supported.
5. Package the complete Skill directory as a ZIP file when required.
6. Add the Skill to an agent created with the new Copilot Studio experience.
7. Test the Skill in the agent preview.
8. Confirm that the expected Skill is selected for the request.
9. Validate generated tables, charts, Excel workbooks, and other outputs.
10. Use an evaluation test set before publishing the agent for broader use.

## Security and production considerations

- Treat every included script as executable code and review it before use.
- Test the examples in a non-production environment.
- Do not store credentials or confidential values in Skill packages.
- Validate and sanitize external input before passing it to a script.
- Restrict package installation and network access according to organizational policies.
- Review generated files before distributing or processing them further.
- Apply appropriate logging, monitoring, and error handling.
- Confirm licensing, feature availability, and preview limitations for your environment.

## Additional information

These examples accompany the video and are intended to explain the underlying concepts. Product behavior and interface elements may change as Microsoft continues to develop the new Copilot Studio experience.

For an overview of all video examples, return to the [repository README](../README.md).

