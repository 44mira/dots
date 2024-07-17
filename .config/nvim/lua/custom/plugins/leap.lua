return {
  'ggandor/leap.nvim',
  dependencies = {
    'tpope/vim-repeat',
  },
  config = function()
    local leap = require 'leap'
    local bind = vim.keymap.set

    bind({ 'n', 'x', 'o' }, '<leader>t', '<Plug>(leap)')
    -- bind({ 'n', 'x', 'o' }, '<leader>gd', '<Plug>(leap-from-window)')

    leap.setup {}
  end,
}
