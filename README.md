# mcp-rag

RAG in [MCP](https://modelcontextprotocol.io/). This is a example MCP server for vanilla RAG.

<iframe width="560" height="315" src="https://www.youtube.com/embed/L8DXQJMJayE?si=nuVdrY_ZUL0mNaNC" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen>
</iframe>

## Tools

The server implements one tool:
- retrieve: Retrieves the docs based on the query

## Quickstart - Claude Desktop

In Claude Desktop, go to `File` -> `Settings` -> `Developer` -> `Edit Config`

or

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

In claude_desktop_config.json, add JSON given in config.json in this repo.

### Debugging

Since MCP servers run over stdio, debugging can be challenging. For the best debugging
experience, we strongly recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).
