## File system format:

Each of the subsystems has its own subdirectory, please name these folders in snake case.
All the files in the subdirectories are to be named in camel case.


## Contributing:
No one is allowed to push to the master branch. All the changes must be made in a separate branch and then a pull request must be created to the master branch. The pull request will be reviewed by the maintainers and then merged to the master branch.

Create a branch with the name of the subsystem you are working on, if you are the only contributor working on that issue, use the format users/<your_username>/<subsystem_name>. If you are working on an issue with multiple contributors, use the format issues/<issue_number>/<subsystem_name>. If you are working on a subsystem that is not an issue, use the format features/<subsystem_name>.

When you are done with your work, create a pull request to the master branch. If you are working on an issue, please mention the issue number in the pull request description. If you are working on a feature, please mention the feature name in the pull request description. If you are working on a subsystem that is not an issue, please mention the subsystem name in the pull request description. Before merging, make sure that the current branch is up to date with the master branch.

## Code style:
<In Progress>
To maintain a consistent code style, we use linters. The linters are configured to run automatically on every pull request. If the linters fail, the PR will not be allowed to merge. If you want to run the linters manually, run the following command in the root directory of the project:
<To Be Added>
Please follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for python code.
Please follow for the [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html) for C++ code.
