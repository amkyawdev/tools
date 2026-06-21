# AI Brain Skills

📚 A comprehensive skill framework for AI agents - Claude, ChatGPT, and other AI assistants.

## 🎯 Overview

AI Brain Skills provides a structured, hierarchical knowledge base that AI agents can use to enhance their capabilities across various domains. The framework includes:

- **Core Infrastructure** - Foundational capabilities
- **Domain Expertise** - Specialized knowledge in various fields
- **Custom Skills** - Organization-specific patterns
- **Hooks System** - Pre/post execution automation
- **Shared Libraries** - Reusable utilities
- **CLI Tool** - Interactive command-line interface
- **VS Code Extension** - IDE integration
- **Dashboard** - Analytics and metrics visualization

## 📁 Structure

```
ai-brain-skills/
├── .amkyaw/                   # AI Brain Skills directory
│   ├── skills/
│   │   ├── 00-core/           # Base infrastructure (auto-loaded)
│   │   ├── 01-domains/        # Domain-specific expertise
│   │   └── 04-custom/         # User/organization specific
│   └── config/                # Configuration files
├── packages/
│   ├── cli/                   # CLI Tool (@amkyaw/cli)
│   ├── vscode-extension/      # VS Code Extension
│   └── dashboard/             # Analytics Dashboard
├── hooks/                      # Execution hooks
├── shared/                     # Shared resources
├── tests/                      # Test framework
├── docs/                       # Documentation
├── scripts/                    # Build scripts
└── examples/                   # Working examples
```

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Use the CLI
npx amkyaw skill:list
npx amkyaw skill:search react

# Run Dashboard
cd packages/dashboard && npm install && npm run dev

# Validate all skills
npm run validate

# Run tests
npm test

# Build skills
npm run build
```

## 🛠️ CLI Tool

```bash
# Install globally
npm install -g @amkyaw/cli

# Commands
amkyaw skill:list              # List all skills
amkyaw skill:search <query>    # Search skills
amkyaw skill:explore           # Interactive explorer
amkyaw skill:compare <s1> <s2> # Compare two skills
amkyaw skill:create <name>     # Create new skill
amkyaw validate                # Validate all skills
amkyaw build                  # Build for deployment
```

## 🔌 VS Code Extension

Install from `packages/vscode-extension/`:

- 🌳 Skills Tree View in Sidebar
- 🔍 Quick Search
- ➕ Create Skills
- 📄 Open Skill Docs

## 📊 Dashboard

Analytics dashboard with:

- Skills usage metrics
- Category distribution charts
- Recent activity feed
- Top skills ranking

```bash
cd packages/dashboard
npm install
npm run dev
```

## 📖 Documentation

- [Installation Guide](./docs/getting-started/installation.md)
- [Quick Start](./docs/getting-started/quick-start.md)
- [Basic Usage](./docs/getting-started/basic-usage.md)
- [Skill Creation Guide](./docs/guides/skill-creation-guide.md)

## 🎨 Skills Categories

### Core (00-core)
- System Foundation
- Context Orchestrator
- Memory Management
- Error Recovery

### Domains (01-domains)
- Web Frontend (React, Vue, Next.js, Angular, Svelte)
- Backend (Python, Node.js, Go, Rust)
- Database (SQL, MongoDB, Redis, ORMs)
- DevOps (Docker, Kubernetes, CI/CD)
- Testing, Security, AI/ML, and more...

### Custom (04-custom)
- Company Patterns
- Project Boilerplates
- Personal Workflows
- Legacy System Guide

## 🔧 Configuration

Configuration files in `.amkyaw/config/`:

- `skills.json` - Skill registry
- `priority-rules.json` - Conflict resolution
- `context-rules.json` - Context-based loading
- `performance-rules.json` - Performance settings
- `security-rules.json` - Security policies
- `telemetry-config.json` - Telemetry settings

## 🧪 Testing

```bash
npm test           # All tests
npm run test:unit # Unit tests
npm run test:e2e  # E2E tests
```

## 📦 Build & Deploy

```bash
npm run build     # Build skills
npm run deploy    # Deploy to target
```

## 🤝 Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## 📄 License

MIT - See [LICENSE](./LICENSE)
