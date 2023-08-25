# Conventional Commit Helper Script

This Python script helps streamline the process of creating conventional commits in a Git repository. Conventional commits follow a structured format that improves the clarity and context of commit messages.

It also adds ticket information to the commit message. This is useful for teams that use JIRA or other ticketing systems. The script will validate the branch name to ensure it matches the expected pattern. If the branch name is valid, the ticket number will be added to the commit message. This improves traceability and makes it easier to find commits related to a specific ticket. 

Conventional commits are helpful for determining the type of change that was made which can be used to automate tasks like semantic versioning, changelog generation, automated releases or just providing context at a glance when viewing the commit history.

Whiles you can manually create these, this script eases adding in proper formatting and ticket information. It also provides a list of staged files before committing to ensure you don't accidentally commit files you didn't intend to.

For more information on conventional commits, see the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) website.

## Features

- Validates branch names using a JIRA ticket pattern.
- Maps commit type aliases to conventional commit types.
- Generates formatted conventional commit messages.
- Provides a staged file list for confirmation before committing.

## Prerequisites

- Python 3.x
- Git

## Usage

1. Clone the repository or download the script.
2. Make the script executable if needed:
   
   ```bash
   chmod +x script_name.py
    ```
3. Add an alias to the script file by adding the following line to your `.bashrc` or `.zshrc` file:
    
    ```bash
    alias jcc='/path/to/script_name.py'
    ```

    Remember to replace `/path/to/script_name.py` with the actual path to the script file and `jcc` with the alias you want to use. You'll also need to restart your terminal or run `source ~/.bashrc` or `source ~/.zshrc` to apply the changes.

4. Run the script from the root of a Git repository:
    
    ```bash
    jcc [commit-type] [commit-message] [auto-confirm]
    ``` 
    - `commit-type` is the type of commit to create. This can be a conventional commit type or an alias defined in the script.
    - `commit-message` is the commit message to use. If this is not provided, the script will prompt for a message.
    - `auto-confirm` is an optional argument that will skip the confirmation prompt before committing. This is useful for scripts that commit automatically.


    examples
    ```
    jcc --feat "Add new feature" -y 
    // commits staged files with message: "feat: [TEAM-123] Add new feature"

    jcc --fix "Fix spaceship flux capacitor" -y
    // message: "fix: [NASA-3212] Fix spaceship flux capacitor"

    jcc c "Move autopilot behind paid wall" --yes
    // message: "chore: [TESLA-732] Move autopilot behind paid wall"
    ```
To ease use, arguments are strictly positional. This means you can omit the preceeding `--` and the script will still work. For example, the following command is equivalent to the first example above:

  ```
    jcc f "Add new feature" y
  ```

    You can also use abbreviations for the commit type. Below is the list of supported abbreviations:
    ```
    feat -> f, feature, ft, feat
    fix -> fx, fix
    docs -> d, docs
    style -> s, style, st
    refactor -> r, refactor, ref
    test -> t, test
    chore -> c, chore
    perf -> p, perf
    ci -> ci
    build -> b, build, bld, bl, bd
    revert -> rev, revert
    wip -> wip
    release -> rl, release
    hotfix -> hf, hfx, hotfix
    merge -> m, merge
    squash -> sq, squash
    ```
    


