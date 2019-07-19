# Custom Jenkins agent

The custom Jenkins agent provides a way to add functionality and permissions to the default cloud Jenkins agent.


## Customisation

### Package dependencies

Additional packages can be installed on the Jenkins agent by adding `Requires:` lines to [SPECS/custom-jenkins-agent.spec](SPECS/custom-jenkins-agent.spec).  If the package isn't part of the standard CentOS distribution it may be necessary to add [extra repositories](https://confluence.dev.bbc.co.uk/display/platform/Repositories) to the service.

The default agent release is actually composed of multiple RPMs, which layer on extra dependencies and configuration over the base `cloud-jenkins-agents` package.  These are not pulled in by [SPECS/custom-jenkins-agent.spec](SPECS/custom-jenkins-agent.spec) out of the box but can be added if desired.  Depending on the OS version the list of available subpackages can be found at one of the following:

* CentOS 6: https://repository.api.bbci.co.uk/cloud-jenkins-agent-seed-el6/revisions/stable/packages
* CentOS 7: https://repository.api.bbci.co.uk/cloud-jenkins-agent-seed-el7/revisions/stable/packages

### Bake scripts

Add bake scripts under [src/etc/bake-scripts/custom-agent/](src/etc/bake-scripts/custom-agent/).  Note that only executable files are actually run by the bakery, so it may be necessary to make them executable before (`chmod +x ...`), or while (`git add --chmod=+x ...`), adding them.

See the [bake scripts documentation](https://confluence.dev.bbc.co.uk/display/platform/Bake+Scripts) for more information.

### Hooks

Any executable files under the [src/usr/libexec/cloud-jenkins/before-agent-start.d/](src/usr/libexec/cloud-jenkins/before-agent-start.d/) directory will be run (as the root user) just before the agent starts.  Under CentOS 6 this can only be relied on during the boot sequence, but under CentOS 7 it will happen whenever the agent service (re-)starts.

If any of the scripts return a non-zero exit code (ie, they error and fail) the agent will not start.

Under CentOS 7 executable files can also be dropped under [src/usr/libexec/cloud-jenkins/after-agent-stop.d/](src/usr/libexec/cloud-jenkins/after-agent-stop.d/) to be triggered when the agent service stops.  Be aware that an EC2 instance can be terminated suddenly for a variety of reasons, bypassing the usual service shutdown process, so you must not rely on these scripts executing.

### Sudo

On rare occasions it may be necessary to permit Jenkins jobs to run some commands as the root user, so extra `sudo` configuration files can be added under the [src/etc/sudoers.d/](src/etc/sudoers.d/) directory.  For example, to allow a Jenkins job to restart the local Apache:

```
jenkins ALL= (root) NOPASSWD: /sbin/service httpd graceful
```

### IAM role policies

The IAM role used by the agent is exported under the name `<stack-name>-AgentRole`, allowing extra policies to be attached in another stack (or stacks).  The [stacks/role_policies.json](stacks/role_policies.json) template contains a minimal example, adding permission to use `s3:ListBucket` on `arn:aws:s3:::examplebucket`.

The source for this template can be found in [stacks/src/role_policies.py](stacks/src/role_policies.py), and it can be rebuilt by running `make` in the [stacks](stacks/) directory.


## Building new releases

In a Jenkins deployed from one of the "seed" releases, or from a recent fork of the bbc/cloud-jenkins repository, a `jenkins-agent` job will be added (if not already present) the first time it starts.  If not, a new "Freestyle project" of that name can be created manually.

Either way, the git repository URL should point to the appropriate fork of bbc/custom-cloud-jenkins, and the build step should contain the following commands, with `@NAME@` replaced by the name of the "agent" service in Cosmos, and `@OS@` replaced by `6` or `7` for CentOS 6 or CentOS 7 respectively.

```
n=$(cosmos-release generate-version @NAME@)
make -C agent release OS=@OS@ SERVICE=@NAME@ BUILD_NUMBER=$n
```

A CentOS 6 agent provides access to older, deprecated tools such as cosmos-build and mbt that aren't supported under CentOS 7.  On the other hand, a CentOS 7 agent includes newer upstream packages and can run Docker.

If migrating jobs from an existing Jenkins setup a CentOS 6 agent is the safest starting point.  If setting up a new Jenkins a CentOS 7 agent is worth considering.


## Deployment

The deployment requirements are identical to that of the base cloud Jenkins agent.  However, ensure that the appropriate "seed-agent" repository has been added first:

### CentOS 6

| Name | Type | URL |
| ---- | ---- | --- |
| seed-agent | mirrorlist | <https://repository.api.bbci.co.uk/cloud-jenkins-agent-seed-el6/revisions/stable> ([GPG key](https://github.com/bbc/cloud-jenkins/blob/16b8dd3d19173d0953ae1a33ab68db956c3dffa1/cloudteam-key.gpg)) |

### CentOS 7

| Name | Type | URL |
| ---- | ---- | --- |
| seed-agent | mirrorlist | <https://repository.api.bbci.co.uk/cloud-jenkins-agent-seed-el7/revisions/stable> ([GPG key](https://github.com/bbc/cloud-jenkins/blob/16b8dd3d19173d0953ae1a33ab68db956c3dffa1/cloudteam-key.gpg)) |
