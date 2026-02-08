name: Feature Request
description: Suggest a new feature
title: "[FEATURE] "
labels: ["enhancement"]
body:
  - type: markdown
    attributes:
      value: |
        Thank you for suggesting a feature! Please fill in the information below.
  - type: textarea
    id: description
    attributes:
      label: Description
      description: Clear description of the feature
      placeholder: "Describe the feature..."
    validations:
      required: true
  - type: textarea
    id: motivation
    attributes:
      label: Motivation
      description: Why is this feature needed?
      placeholder: "This would help because..."
    validations:
      required: true
  - type: textarea
    id: example
    attributes:
      label: Example Usage
      description: How would this feature be used?
      render: python
