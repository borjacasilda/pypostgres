name: Bug Report
description: Report a bug or issue
title: "[BUG] "
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: |
        Thank you for reporting a bug! Please fill in the information below.
  - type: textarea
    id: description
    attributes:
      label: Description
      description: Clear description of the issue
      placeholder: "Describe the bug..."
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: Steps to reproduce the behavior
      placeholder: "1. ... 2. ... 3. ..."
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What should happen
    validations:
      required: true
  - type: textarea
    id: actual
    attributes:
      label: Actual Behavior
      description: What actually happened
    validations:
      required: true
  - type: textarea
    id: environment
    attributes:
      label: Environment
      description: |
        Python version:
        PostgreSQL version:
        OS:
      placeholder: "Python 3.9, PostgreSQL 13, Ubuntu 20.04"
    validations:
      required: true
  - type: textarea
    id: logs
    attributes:
      label: Error Logs
      description: Any error messages or logs
      render: python
