-- ============================================================================
-- core/options.lua: Core Editor Settings
-- ============================================================================

local opt = vim.opt

-- Core editor functionality
opt.number = true
opt.relativenumber = true
opt.clipboard = "unnamedplus"
opt.undofile = true
opt.wrap = false

-- Indentation
opt.expandtab = true
opt.tabstop = 4
opt.shiftwidth = 4
opt.softtabstop = 4
opt.autoindent = true
opt.smartindent = true

-- Search
opt.ignorecase = true
opt.smartcase = true
opt.incsearch = true
opt.hlsearch = false

-- UI
opt.termguicolors = true
opt.scrolloff = 8
