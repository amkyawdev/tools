---
name: browser-testing-with-devtools
description: Tests in real browsers via Chrome DevTools MCP. Use when building or debugging anything that runs in a browser.
---

# Browser Testing with DevTools

## Overview

Use Chrome DevTools MCP to give your agent eyes into the browser. Bridge the gap between static code analysis and live browser execution.

## When to Use

- Building or modifying anything that renders in a browser
- Debugging UI issues
- Analyzing network requests and API responses
- Profiling performance

## Setting Up Chrome DevTools MCP

Add to your project's MCP config:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest", "--isolated"]
    }
  }
}
```

## The DevTools Debugging Workflow

1. REPRODUCE: Navigate to page, trigger bug, screenshot
2. INSPECT: Check console, DOM, network, styles
3. DIAGNOSE: Identify root cause
4. FIX: Implement fix in source
5. VERIFY: Reload, screenshot, confirm clean
