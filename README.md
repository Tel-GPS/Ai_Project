# Testing Framework Quickstart Guide

Welcome to this project's testing framework quickstart! This guide provides you with the essential information needed to get started with writing and running tests for our project.

## Quick Setup

1. **Install Dependencies**: Ensure all dependencies are installed by running `pip install -r requirements.txt`.
2. **Running Tests**: To run tests, execute `pytest` in the root directory of our project (adjust based on your testing framework).

## Writing New Tests

- Place your test files in the `tests/` directory.
- Name your test files following this pattern: `test_<feature>.py`.
- Use assertions to validate test conditions.

## CI Pipeline

Our tests automatically run on all branches upon commits and pull requests via our CI pipeline. See our [CI Pipeline Configuration]([link-to-your-ci-config-file](https://github.com/Tel-GPS/Ai_Project/blob/main/.github/workflows/cml.yaml)) for details.

## Further Resources

For a more detailed guide on our testing practices, including examples and conventions, please visit our [Comprehensive Testing Documentation in Confluence]([Confluence-Link](https://amhex01.atlassian.net/wiki/spaces/PFEAI/pages/9371649/Comprehensive+Testing+Guide+for+PFE)https://amhex01.atlassian.net/wiki/spaces/PFEAI/pages/9371649/Comprehensive+Testing+Guide+for+PFE).

---
