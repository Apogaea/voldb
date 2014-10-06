#Development

To start developing on the Volunteer Database clone the repository:

```bash
$ git clone git@github.com/Apogaea/voldb.git
```

##Django Codebase

- Follow [PEP8](http://www.python.org/dev/peps/pep-0008/).  Highly recommend
  getting your editor setup to automatically indicate pep8 violations.
- Include tests.  Not everything is testable or should be tested, but the
  general rule is that all new code should include tests.


#Pull Requests

It's a good idea to make pull requests early on.  A pull request represents the
start of a discussion, and doesn't necessarily need to be the final, finished
submission.

It's also always best to make a new branch before starting work on a pull
request.  This means that you'll be able to later switch back to working on
another seperate issue without interfering with an ongoing pull requests.

It's also useful to remember that if you have an outstanding pull request then
pushing new commits to your GitHub repo will also automatically update the pull
requests.

GitHub's documentation for working on pull requests is [available here][pull-requests].

Always run the tests before submitting pull requests, and ideally run `tox` in
order to check that your modifications don't break anything.

Once you've made a pull request take a look at the travis build status in the
GitHub interface and make sure the tests are runnning as you'd expect.

#Documentation

> TODO: once the documentation branch and readthedocs builds are up.
