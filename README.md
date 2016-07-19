# git-worker
Customizable tool for automate git operations on your projects.

## Current state
The project state is *Work In Progress*.

The usage on real repositories is not suggested and should be done on your *risk*. If you like the idea please help me to make it stabe and usable for everyone :smiley:.

## Rationale
As developer on a different projects often happen that you're working on your [feature branch](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow) and due to ofter updates of the master branch your tests will fail.

The objective of this problem is to try to **handle this issue**.

## How it works
The worked is a fully customizable application which as soon as it is executed will run the test suite on the current branch. In case of test failure the worker will try to perform some activities that could help in fixing it.

The self explaining flow chart will help you understanding the fixing process.
![Alt text](http://g.gravizo.com/g?
digraph G {
   START;
   END;
   fetch_master [label="git fetch"];
   is_master [label="is master branch", shape="rectangular"];
   is_your_feature [label="is your feature branch", shape="rectangular"];
   merge_rebase [label="merge / rebase master", shape="rectangular"];
   merge_rebase_abort [label="abort merge / rebase", shape="rectangular"];
   run_build [label="run build", shape="rectangular"];
   run_tests_1 [label="run tests", shape="rectangular"];
   run_tests_2 [label="run tests", shape="rectangular"];
   pull_master [label="git pull", shape="rectangular"];
   START -> is_master;
  is_master -> pull_master [ label="YES" ];
  pull_master -> END;
  is_master -> is_your_feature [ label="NO" ];
  is_your_feature -> run_tests_1 [ label="YES" ];
  is_your_feature -> END [ label="NO" ];
  run_tests_1 -> END [label="SUCCESS"];
  run_tests_1 -> fetch_master [label="FAILURE"];
  fetch_master -> merge_rebase;
  merge_rebase -> run_build [label="NO CONFLICTS"];
  run_build -> run_tests_2 [label="SUCCESS"];
  run_build -> merge_rebase_abort [label="FAILURE"];
  merge_rebase -> merge_rebase_abort [label="CONFLICTS"];
  merge_rebase_abort -> END;
  run_tests_2 -> END [label="SUCCESS"];
  run_tests_2 -> merge_rebase_abort [label="FAILURE"];
}
)

## Initial Setup
The environment setup is realized by ``make`` or alternativelly ``make install-hooks``. It will create the needed python virtual environment and install the [``pre_commit``](https://github.com/pre-commit/pre-commit) package on your ``venv``.

## Use - Command Line Parameters
```
$python main.py -h
usage: main.py [-h] [-c CONFIG] [-s] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Configuration file. Default: config.json
  -s, --show-schema     Get the Schema of the configuration file
  -v, --validate-configuration
                        Validate the configuration file
```

## Configuration
The configurations should be provided through a JSON file compliant to the schema defined [here](src/configuration.json.schema).
