-- ============================================================================
-- plugins/config/telescope.lua
-- ============================================================================

-- Initialise Telescope with its default settings.
require('telescope').setup({})

-- Plugin-specific shortcuts
local builtin = require('telescope.builtin')
local keymap = vim.keymap.set -- Use the modern vim.keymap.set
local opts = { noremap = true, silent = true }

-- Find files in the current working directory
keymap('n', '<leader>ff', builtin.find_files, opts)

-- Live grep for text in the current working directory
keymap('n', '<leader>fg', builtin.live_grep, opts)

-- Find files in your git repository
keymap('n', '<leader>gf', builtin.git_files, opts)

-- Search for a string in the current buffer
keymap('n', '<leader>fb', builtin.buffers, opts)
