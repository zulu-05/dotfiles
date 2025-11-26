require('nvim-treesitter.configs').setup({
    -- A list of parser names, or "all"
    ensure_installed = {
        "python",
        "bash",
        "tmux",
        "powershell",
        "lua",
        "vim",
        "html",
        "css",
        "http",
        "json",
        "javascript",
        "typescript",
        "svelte",
        "vue",
        "c",
        "cpp",
        "rust",
        "java",
        "swift",
        "dockerfile",
        "git_config",
        "git_rebase",
        "gitignore",
        "markdown",
        "markdown_inline",
        "latex",
    },

    -- Installs parser synchronously (only applied to `ensure_installed`)
    sync_install = false,

    -- Automatically install missing parsers when entering buffer
    auto_install = true,

    highlight = {
        enable = true,
    },

    -- Enables Treesitter indentation
    indent = {
        enable = true,
    },
})
