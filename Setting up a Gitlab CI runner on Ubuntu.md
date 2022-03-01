# Tips for Gitlab CI

- [Tips for Gitlab CI](#tips-for-gitlab-ci)
  - [Setting up a Gitlab CI runner on Ubuntu](#setting-up-a-gitlab-ci-runner-on-ubuntu)
  - [Useful resources](#useful-resources)
  - [A note on scheduled/manual jobs](#a-note-on-scheduledmanual-jobs)

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

## Useful resources

- [Documentation for "GitLab CI/CD"](https://docs.gitlab.com/ee/ci/)
- [Documentation for "Pipeline schedules"](https://docs.gitlab.com/ee/ci/pipelines/schedules.html)
- [Documentation for "GitLab Runner"](https://docs.gitlab.com/runner/)
- ["Keyword reference for the .gitlab-ci.yml file"](https://docs.gitlab.com/ee/ci/yaml/)
- ["Predefined variables reference"](https://docs.gitlab.com/ee/ci/variables/predefined_variables.html)
- Youtube tutorials by Valentin Despa:
  - ["Gitlab CI pipeline tutorial for beginners"](https://youtu.be/Jav4vbUrqII)
  - ["How to configure your own Gitlab CI Runner"](https://youtu.be/G8ZONHOTAQk)

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
