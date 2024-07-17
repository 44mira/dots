
function yy() {
	local tmp="$(mktemp -t "yazi-cwd.XXXXXX")"
	yazi "$@" --cwd-file="$tmp"
	if cwd="$(cat -- "$tmp")" && [ -n "$cwd" ] && [ "$cwd" != "$PWD" ]; then
		cd -- "$cwd"
	fi
	rm -f -- "$tmp"
}


# bat as man
export MANPAGER="sh -c 'col -bx | bat -l man -p'"
export MANROFFOPT="-c"

alias nv="nvim"
alias ls="exa"
alias ll="exa -l"
alias ff="fastfetch"
alias lg="lazygit"

eval "$(zoxide init zsh)"

eval "$(oh-my-posh init zsh --config ~/.thm.omp.json)"

# tty colors
(cat ~/.config/wpg/sequences &)
