# Cheatsheet: Markdown Workflow

This environment utilises a three-plugin stack to provide a comprehensive Markdown editing experience:
1. **markdown-preview.nvim**: For high-fidelity, live browser rendering.
2. **glow.nvim**: For quick, in-terminal reading.
3. **headlines.nvim**: For a "Notion-like" writing experience inside the editor.

## 1. Live Browser Preview (`markdown-preview.nvim`)

This plugin uses a local Node.js server to render the current buffer in the default web browser. It synchronises scrolling between the editor and the browser and updates in real-time.

| Command | Description |
| :--- | :--- |
| `:MarkdownPreview` | **Start.** Opens the current file in a new browser tab. |
| `:MarkdownPreviewStop` | **Stop.** Kills the local server and closes the preview connection. |
| `:MarkdownPreviewToggle` | **Switch.** Toggles the preview on or off. |

### Use Case
Use this for **heavy editing** or **final polish**.
*   Checking complex layouts (tables, mermaid diagrams).
*   Verifying image links.
*   Reading long-form documentation where browser typography is preferred.

## 2. Terminal Preview (`glow.nvim`)

This plugin wraps the `glow` CLI tool to render Markdown directly inside a floating Neovim window. It provides styling (bold, italics, code blocks) using terminal colours.

| Command | Description |
| :--- | :--- |
| `:Glow` | **View Current.** Opens a floating window rendering the current buffer. Press `q` to close it. |
| `:Glow [file]` | **View File.** Renders a specific file without opening it for editing (e.g., `:Glow README.md`). |

### Use Case
Use this for **quick reference**.
*   Previewing a `README.md` without leaving the terminal context.
*   Quickly checking how a list or code block renders while coding.

## 3. Editor Aesthetics (`headlines.nvim`)

This plugin runs automatically in the background. It uses **Treesitter** queries to inject improved styling directly into the code buffer.
hj
**Features:**
*   **Header Backgrounds:** Adds coloured background highlights to `# H1`, `## H2`, etc., making document structure visible at a glance.
*   **Code Blocks:** Adds a slighlty lighter background to code blocks for visual separation.
*   **Dashes:** Replaces standard dashes (`---`) with horizontal rules.

### Configuration Note
In `plugins/init.lua`, this plugin is configured to load **after** `nvim-treesitter`. If the highlights disappear, verify that Treesitter is working correctly with `:checkhealth nvim-treesitter`.
