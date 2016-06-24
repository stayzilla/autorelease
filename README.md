# Github Auto Release Candidate creator

This script goes through all the repositories
under a configured Organization name, and
creates a new Release Candidate branch from a
Devel branch, and sends out a pull request from
this RC branch to the main branch.

All settings that can be configured are present in
the file `settings.cfg`.

A new token can be generated under Github Settings [Personal Access Tokens](https://github.com/settings/tokens).

# Authors

Ananth SNC <ananth.srirangam@stayzilla.com>
