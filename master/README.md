# Custom Jenkins master

The custom Jenkins master provides a way to add functionality to the default cloud Jenkins master.


## Customisation

### Package dependencies

Additional packages can be installed on the Jenkins master by adding `Requires:` lines to [SPECS/custom-jenkins-master.spec](SPECS/custom-jenkins-master.spec).  If the package isn't part of the standard CentOS distribution it may be necessary to add [extra repositories](https://confluence.dev.bbc.co.uk/display/platform/Repositories) to the service.

### Bake scripts

Add bake scripts under [src/etc/bake-scripts/custom-master/](src/etc/bake-scripts/custom-master/).  Note that only executable files are actually run by the bakery, so it may be necessary to make them executable before (`chmod +x ...`), or while (`git add --chmod=+x ...`), adding them.

See the [bake scripts documentation](https://confluence.dev.bbc.co.uk/display/platform/Bake+Scripts) for more information.

### Public endpoints

Some plugins require Jenkins to accept HTTP requests from external systems without a client certificate.  For example, the GitHub Plugin (supported by default) receives POST requests from GitHub at `/github-webhook`.

Additional paths can be exposed in this way by dropping files under [src/etc/bake-scripts/public-endpoints/](src/etc/bake-scripts/public-endpoints/).  Each file should contain one or more paths, each on a separate line.  For example:
```
/ghprbhook
```

The names of the files are irrelevant, only the content matters.

*Warning: Everyone on the Internet will potentially have access to these paths and everything under them. Be very, very careful about what you expose.*

### Hooks

Any executable files under the [src/usr/libexec/cloud-jenkins/before-master-start.d/](src/usr/libexec/cloud-jenkins/before-master-start.d/) directory will be run (as the root user) just before the master starts.  Under CentOS 6 if a script fails (ie, exits with a non-zero return code) no further files from the directory will be run, but Jenkins itself will still attempt to start which may not be desirable.  Under CentOS 7 any script failure will block Jenkins from starting.

Under CentOS 7 executable files can also be dropped under [src/usr/libexec/cloud-jenkins/after-master-stop.d/](src/usr/libexec/cloud-jenkins/after-master-stop.d/) to be triggered when the Jenkins master stops.  Be aware that an EC2 instance can be terminated suddenly for a variety of reasons, bypassing the usual service shutdown process, so you must not rely on these scripts executing.

Finally, any executable files under [src/usr/libexec/cloud-jenkins/after-master-start.d/](src/usr/libexec/cloud-jenkins/after-master-start.d/) will be run (as the *jenkins* user) shortly after the Jenkins master has finished starting and its API is accessible.  Note that build agents may not have had a chance to register with the master at this point.


## Building new releases

In a Jenkins deployed from one of the "seed" releases, or from a recent fork of the bbc/cloud-jenkins repository, a `jenkins-master` job will be added (if not already present) the first time it starts.  If not, a new "Freestyle project" of that name can be created manually.

Either way, the git repository URL should point to the appropriate fork of bbc/custom-cloud-jenkins, and the build step should contain the following commands, with `@NAME@` replaced by the name of the "agent" service in Cosmos, and `@OS@` replaced by `6` or `7` for CentOS 6 or CentOS 7 respectively.

```
n=$(cosmos-release generate-version @NAME@)
make -C master release OS=@OS@ SERVICE=@NAME@ BUILD_NUMBER=$n
```

Unless you know you have a specific requirement for a CentOS 6 master, using CentOS 7 here is a safe choice.
