-- ============================================================================
-- core/keymaps.lua: Core Key Mappings
-- ============================================================================

local keymap = vim.api.nvim_set_keymap
local opts = { noremap = true, silent = true }

-- Fast exit from insert mode.
keymap('i', 'jk', '<Esc>', opts)
