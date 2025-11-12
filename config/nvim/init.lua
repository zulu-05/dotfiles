-- ============================================================================
-- init.lua: The Coordinator
-- ============================================================================
-- This file's only job is to load the rest of the configuration modules
-- in the correct order.

-- Set leader key before any keymaps are set
vim.g.mapleader = " "
vim.g.maplocalleader = " "

-- Load core configuration
require("user.core.options")
require("user.core.keymaps")

-- Load plugin manager and plugin configurations
require("user.plugins")
