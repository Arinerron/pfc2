# About

pfc2 is the second generation of [pfc](https://github.com/Arinerron/pfc). It is more modular and powerful than its successor.

**Note:** pfc2 is under heavy development and is likely very buggy.

# Features

TODO:
* `grep -ri '\(FIXME\|XXX\|HACK\|BUG\|TODO\)'`
* prefix all py files with the same comments (shebang and license, and maybe author?)
* write a script to scrape modules that have a `requirements.txt` and install those dependencies as well as the `requirements.txt` in the root directory
* add cool radare-style quotes and ascii art on start, see `core.py` and search for "radare"
* store the version info of pfc2 in `core.py` and print it on start with the banner.
* write documentation :(
  * document core.py, console.py, and module.py. I didn't document these because I wanted to get the painful work out of the way before I lost motivation. I did, but now I need to document it with comments.
* add support for auxiliary modules and configuration files
  * consider making auxiliary modules a `type` of module (e.g. `builtins`, `recon`, `exploit`, etc) and making the `auxiliary/` directory only contain configs that you can `include`
  * support`parameters`.`include` in `module.yml` (auxiliary configs)
* instead of looking for module.yml, just import all .yml files in each plugin dir. That way, people can make multiple commands use the same module (and just have a bunch of yaml files in the same dir).
* clean up the subdomains tool, it's pretty messy.
* create a config file for pfc2
  * create a module like `config set/get/list/delete/load/save/reset` that lets you mess with config temporarily or permanently mess with configuration settings. these settings should reflect in environmental variables (will be added later too)
  * you should be able to configure things like logging
    * output file, optional
    * strip colors?
    * print dates for debug messages too?
    * verbosity? (reflected across all modules)
* fix logging.
  * Right now, it prints the status like `INFO:` as text, but eventually I want it like `[+]`, `[-]`, `[*]`, `[!]`, etc.
  * Make the logging configuration global so that it's set once and reflects across all python modules
  * colors are broken too; all print out as green
* add features to the shell:
  * environmental variables
  * variables
  * two types of quotes, not just '
  * if the command doesn't exist but is an actual command on the system (outside of pfc shell), execute it like Metasploit does.
  * add a feature to execute a shell command instead of pfc command if it is prefixed with `!` or something
* Add modules like these:
  * `help` - every module has description and name/shortname. Just collect and pretty print everything. If the user specifies a specific module (or many modules), list the specific help info for each including the parameters and their descriptions.
  * `modules` - eventually will be able to `modules install` or `modules remove` modules. You'll be able to install by a git url and it will clone it for you. `modules update` git pulls the whole repo to update and pulls each of the modules that came from git.
  * `info`/`version` - lists the version info and current commit hash for debug info
  * `tee`/`write` - writes to a file (and stdout?)
  * `concat` - converts a set/list to a string with a user-defined separator. maybe support dicts too?
  * `eval` - evaluates a pfc shell string (not python like `exec`).

# Installation

```
git clone https://github.com/Arinerron/pfc2 && cd pfc2
pip3 install --user -r requirements.txt
```

# Documentation

TODO

For developers:
* check the `subdomains` module's `module.yml`, it's pretty heavily commented

# Development

open source! yay!

## Get Involved
todo add contact details or link to wiki on how to get involved and what needs to be changed/added

## Team
* Aaron Esau <[pfc@aaronesau.com](mailto:pfc@aaronesau.com)>
* todo list contributors here

## Donations

donations are not accepted, see https://github.com/gorhill/uBlock/wiki/Why-don't-you-accept-donations
