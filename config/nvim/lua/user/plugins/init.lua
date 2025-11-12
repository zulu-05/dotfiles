-- ============================================================================
-- plugins/init.lua: PLugin Manager (Packer)
-- ============================================================================

local fn = vim.fn
local install_path = fn.stdpath('data')..'/site/pack/packer/start/packer.nvim'
if fn.empty(fn.glob(install_path)) > 0 then
    fn.system({'git', 'clone', '--depth', 'i', 'https://github.com/wbthomason/packer.nvim', install_path})
    vim.cmd [[packadd packer.nvim]]
    return
end

-- Autocommand that reloads neovim whenever you save this file
vim.cmd([[
    augroup packer_user_config
        autocmd!
        autocmd BufWritePost plugins.lua source <afile> | PackerSync
    augroup end
]])

require("packer").startup(function(use)
    -- Packer can manage itself
    use "wbthomason/packer.nvim"

    -- Theme
    use {
        "gruvbox-community/gruvbox",
        config = function()
            require("user.plugins.config.gruvbox")
        end
    }

    -- Fuzzy Finder (Telescope) and its dependencies
    use "nvim-lua/plenary.nvim" -- Required for telescope
    use {
        'nvim-telescope/telescope.nvim', tag = '0.1.x',
        config = function()
            require("user.plugins.config.telescope")
        end
    }
end)
