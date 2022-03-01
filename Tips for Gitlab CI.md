# Tips for Gitlab CI

Some useful tips for Gitlab CI, including useful resources, an example `.gitlab-ci.yml` file, and how to set up a Gitlab CI runner on Ubuntu (EG if CI jobs require local hardware).

## Contents

- [Tips for Gitlab CI](#tips-for-gitlab-ci)
  - [Contents](#contents)
  - [Useful resources](#useful-resources)
  - [Example `.gitlab-ci.yml` file](#example-gitlab-ciyml-file)
  - [Setting up a Gitlab CI runner on Ubuntu](#setting-up-a-gitlab-ci-runner-on-ubuntu)
  - [A note on scheduled/manual jobs](#a-note-on-scheduledmanual-jobs)

## Useful resources

- [Documentation for "GitLab CI/CD"](https://docs.gitlab.com/ee/ci/)
- [Documentation for "Pipeline schedules"](https://docs.gitlab.com/ee/ci/pipelines/schedules.html)
- [Documentation for "GitLab Runner"](https://docs.gitlab.com/runner/)
- ["Keyword reference for the .gitlab-ci.yml file"](https://docs.gitlab.com/ee/ci/yaml/)
- ["Predefined variables reference"](https://docs.gitlab.com/ee/ci/variables/predefined_variables.html)
- Youtube tutorials by Valentin Despa:
  - ["Gitlab CI pipeline tutorial for beginners"](https://youtu.be/Jav4vbUrqII)
  - ["How to configure your own Gitlab CI Runner"](https://youtu.be/G8ZONHOTAQk)

## Example `.gitlab-ci.yml` file

```yaml
################################ GLOBAL CONFIG ################################

# Define custom stage names (default names are build, test, deploy)
stages:
    - build_stage_1
    - build_stage_2
    - unittest_stage_1
    - unittest_stage_2

############################### unittest_stage_1 ##############################

# Tests that start with `.` are template jobs: they do not run as part of the
# pipeline, but they can be extended by other jobs using the `extends` keyword,
# to avoid writing the same configuration for multiple different jobs
.unittest_stage_1_template:
    # Specify which stage this job will run in
    stage: unittest_stage_1
    # Always run this job, even if jobs in earlier pipelines did not succeed
    when: always
    # Use `dependencies` to specify which jobs to fetch artefacts from. In this
    # case, don't download dependencies from any jobs at all
    dependencies: []
    # Specify which jobs in previous stages to wait for before starting this
    # job. In this case, don't wait for any jobs in previous stages, and start
    # this job immediately
    needs: []
    # Specify tags, which determine which runners will be able to run this job
    tags:
        - my_tag_1

unit_test_1:
    # Extend the template job
    extends: .unit_test_template
    script:
        - test_script arg_1

unit_test_2:
    extends: .unit_test_template
    script:
        # Run multiple commands in this job
        - test_script arg_2
        - extra_command
        # Commands can use extra lines, no backslashes needed
        - this_command
            uses_multiple
            lines

unit_test_3:
    extends: .unit_test_template
    # Specify a Docker image
    image: my.website:project/name:master
    script:
        - test_script arg_1
    # Override tags
    tags:
        - my_tag_2_docker

############################### unittest_stage_2 ##############################

.unittest_stage_2_template:
    stage: unittest_stage_2
    dependencies: []
    needs: []
    tags:
        - my_tag_3
    # Configure this job to always run during scheduled pipelines (EG nightly
    # and weekly pipelines), but to still have the option to be triggered
    # manually in pipelines triggered by a push
    rules:
        - if: $CI_PIPELINE_SOURCE != "schedule"
          when: manual
          allow_failure: true
        - if: $CI_PIPELINE_SOURCE == "schedule"
          when: always

unittest_stage_2_job_1:
    extends: .unittest_stage_2_template
    script:
        - test_script arg_1 --stage 2
    # Specify which artefacts to export from this job and when
    artifacts:
        paths:
            - artefact_filename_job_1_*
        when: always

################################ build_stage_1 ################################

.build_stage_1_template:
    stage: build_stage_1
    variables:
        # Specify environment variables here. Note that environment variables
        # won't be picked up from ~/.bashrc on the runner
        PATH: "/bin:/home/me/.local/bin:/home/me/dir1/dir2/bin:"
        ENV_VAR_NAME_1: "ENV_VAR_VALUE_1"
        ENV_VAR_NAME_2: "ENV_VAR_VALUE_2"
    tags:
        - my_tag_4
    artifacts:
        paths:
            # Specify paths to artefacts using glob expression
            - "**/results.txt"
        when: always
    # After running this job, delete all object files (so they won't have to be
    # deleted automatically at the start of the next job and spam the job log)
    after_script:
        - find . -type f -name '*.o' -delete

build_stage_1_job_1:
    extends: .build_stage_1_template
    script:
        - cd dir1/dir2
        - make
    artifacts:
        paths:
            # Export a whole directory as an artefact
            - dir1/dir2/

build_stage_1_job_2:
    extends: .build_stage_1_template
    script:
        - scons -j4 platform=linux
    # Allow this job to fail, without causing later jobs to automatically fail
    allow_failure: true
    # Specify time out
    timeout: 2 hours 30 minutes
    rules:
        # CUSTOM_VAR can be set in the schedule configuration on Gitlab (EG to
        # specify if this is a nightly or a weekly test)
        - if: '$CI_PIPELINE_SOURCE == "schedule" && $CUSTOM_VAR == "CUSTOM_VAL"'
```

## Setting up a Gitlab CI runner on Ubuntu

Sometimes it might be desirable to run CI jobs on a specific local PC instead of using using cloud computing resources, for example, in case specific hardware needs to be connected to the machine that will run the CI jobs. This Gist describes how to set up and configure a Gitlab runner on an Ubuntu PC or VM.

Make sure `curl` is installed, using the following commands:

```
sudo apt update
sudo apt upgrade
sudo apt install curl
```

Note that if an error is displayed after running `sudo apt update` and before running `sudo apt upgrade`, it may be necessary to run the following command and try again:

```
sudo dpkg --configure -a
```

Install a Gitlab CI runner, as described in [the documentation for "Installing GitLab Runner"](https://docs.gitlab.com/runner/install/linux-repository.html#installing-gitlab-runner), using the following commands:

```
curl -L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh" | sudo bash
sudo apt-get install gitlab-runner
```

Make sure your account status for the project/repository on Gitlab is `maintainer`, so that you have access to CI settings.

Register a Gitlab runner, as described in [the documentation for "Registering runners"](https://docs.gitlab.com/runner/register/index.html#linux), using the following command:

```
sudo gitlab-runner register
```

Use the Gitlab instance URL and registration token provided by the "Runners" section of the "CI / CD Settings" page for the Gitlab project (this can be found under "Settings" in the left side-bar of the Gitlab project site, if your account status for the project/repository on Gitlab is `maintainer`).

For the description of the runner, enter any sensible description for the runner.

For tags for the runner, enter a unique and descriptive name (or multiple names) for the tag. This should match the tag used for the relevant jobs in the repository's `.gitlab-ci.yml` file, meaning that these jobs will only run on this custom runner.

For the executor for the runner, enter `shell` if the intention is to run commands like regular terminal commands on the test PC that will run the CI jobs.

By default, a new user will be created to run Gitlab CI jobs using `gitlab-runner`. To make the jobs run using a specific user (which might be necessary, for example to access files only accessible to that user), use the following commands, replacing `custom_username` with the desired username:

```
sudo gitlab-runner uninstall
sudo gitlab-runner install --user custom_username
sudo gitlab-runner start
rm ~/.bash_logout
sudo reboot
```

## A note on scheduled/manual jobs

For some longer-running jobs, it might be desirable for them to run automatically only during scheduled overnight and/or weekend pipelines, but to still have the option to trigger them to run manually during pipelines triggered by a push. This can be achieved using the following syntax in a `.gitlab-ci.yml` file:

```yaml
job_name:
    extends: .template_job
    stage: stage_name
    tags:
        - custom_tag
    script:
        - python3 my_test_script.py
    rules:
        - if: $CI_PIPELINE_SOURCE != "schedule"
          when: manual
          allow_failure: true
        - if: $CI_PIPELINE_SOURCE == "schedule"
          when: always
```

Note that when setting the job to be `when: manual` in a branch of `rules`, it is necessary to set `allow_failure: true`, otherwise the job will be considered to have failed every time it is not manually triggered, and therefore in this case the whole pipeline will be considered to have failed.
