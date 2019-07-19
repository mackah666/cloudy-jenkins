# Custom Cloud Jenkins
A small layer over the top of the Vanilla Cloud Jenkins, providing several
customisation hooks.

## Prerequisites

A running Cloud Jenkins. See https://github.com/bbc/cloud-jenkins for more
information.

## Quick start

1) Fork this repository.
2) Read the [master](master/README.md) and [agent](agent/README.md) READMEs.
3) Customise your fork.
4) Create a Jenkins build job pointing to your fork.
5) Build and release to your **existing (vanilla) services**.
4) Deploy.

## Migrating from a forked Vanilla Cloud Jenkins

If you maintain an existing Vanilla Cloud Jenkins fork, you can follow the
quick start above, then deploy to your testing environment; building up your
customisation fork until it is compatible with your current live setup before
deploying it to live. For a more detailed overview of a potential migration
path see:
https://confluence.dev.bbc.co.uk/display/platform/Cloud+Jenkins+Customisation

## Contributing
If you'd like to help shape the project, pull requests are welcome. Please
raise any issues as a GitHub issue.
