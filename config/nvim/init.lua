-- =============================================================================
-- init.lua: A Fresh and Modern Neovim Configuration (Phase 2)
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Section 1: Leader Key
-- -----------------------------------------------------------------------------
vim.g.mapleader = " "
vim.g.maplocalleader = " "

-- -----------------------------------------------------------------------------
-- Section 2: Core Editor Settings
-- -----------------------------------------------------------------------------
do
  local opt = vim.opt
  opt.number = true
  opt.relativenumber = true
  opt.expandtab = true
  opt.tabstop = 4
  opt.shiftwidth = 4
  opt.softtabstop = 4
  opt.autoindent = true
  opt.smartindent = true
  opt.ignorecase = true
  opt.smartcase = true
  opt.incsearch = true
  opt.hlsearch = false
  opt.termguicolors = true
  opt.scrolloff = 8
  opt.wrap = false
  opt.clipboard = "unnamedplus"
  opt.undofile = true
end

-- -----------------------------------------------------------------------------
-- Section 3: Core Key Mappings
-- -----------------------------------------------------------------------------
do
  local keymap = vim.api.nvim_set_keymap
  local opts = { noremap = true, silent = true }
  -- Fast exit from insert mode.
  keymap('i', 'jk', '<Esc>', opts)
end

-- -----------------------------------------------------------------------------
-- Section 4: Plugin Management (Packer)
-- -----------------------------------------------------------------------------
do
  local fn = vim.fn
  local install_path = fn.stdpath('data')..'/site/pack/packer/start/packer.nvim'
  if fn.empty(fn.glob(install_path)) > 0 then
    fn.system({'git', 'clone', '--depth', '1', 'https://github.com/wbthomason/packer.nvim', install_path})
    vim.cmd [[packadd packer.nvim]]
    return
  end

  require("packer").startup(function(use)
    -- Packer can manage itself
    use "wbthomason/packer.nvim"

    -- Theme
    use "gruvbox-community/gruvbox"

    -- Fuzzy Finder (Telescope) and its dependency
    use "nvim-lua/plenary.nvim" -- Required for telescope
    use {
      'nvim-telescope/telescope.nvim', tag = '0.1.x',
    }
  end)
end

-- -----------------------------------------------------------------------------
-- Section 5: Plugin Configurations
-- -----------------------------------------------------------------------------
-- Initialize Telescope with its default settings.
require('telescope').setup({})

-- -----------------------------------------------------------------------------
-- Section 6: Plugin Key Mappings
-- -----------------------------------------------------------------------------
-- This section is for plugin-specific shortcuts.
-- They are commented out by default. You can uncomment them when you are ready.
do
  -- local builtin = require('telescope.builtin')
  -- local keymap = vim.api.nvim_set_keymap
  -- local opts = { noremap = true, silent = true }
  --
  -- -- Find files in the current working directory
  -- keymap('n', '<leader>ff', function() builtin.find_files() end, opts)
  --
  -- -- Live grep for text in the current working directory
  -- keymap('n', '<leader>fg', function() builtin.live_grep() end, opts)
end

-- -----------------------------------------------------------------------------
-- Section 7: Appearance & Theming
-- -----------------------------------------------------------------------------
-- This must be loaded AFTER plugins to ensure the colorscheme is available.
vim.cmd("colorscheme gruvbox")
