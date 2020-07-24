#!/usr/bin/env bash
_helper_completions()
{
  if [ "${#COMP_WORDS[@]}" != "2" ]; then
    return
  fi

  COMPREPLY=($(compgen -W "$(helper | grep '{' | cut -d '{' -f2 | cut -d '}' -f1 | sed 's/,/ /g')" -- "${COMP_WORDS[1]}"))
}

complete -F _helper_completions helper
