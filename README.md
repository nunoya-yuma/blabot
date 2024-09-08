# nn-io-interact

## Overview

If development is proceeding in an environment configured as follows

```mermaid
graph LR
    Developer[Developer]

    subgraph Software[Software]
        CLI_Module[CLI Module]
        Module_A[Module A]
    end

    Developer -->|Command| CLI_Module
    CLI_Module -->|Print: result| Developer

    CLI_Module -->|Trigger| Module_A
    Module_A -->|Print: Result| CLI_Module
```

Our project can automatically control and check inputs and outputs instead of developer.

```mermaid
graph LR
    This_Project[This Project]

    subgraph Software[Software]
        CLI_Module[CLI Module]
        Module_A[Module A]
    end

    This_Project -->|Command| CLI_Module
    CLI_Module -->|Print: result| This_Project

    CLI_Module -->|Trigger| Module_A
    Module_A -->|Print: Result| CLI_Module
```

## Environment

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Examples

[Examples](./examples/README.md) are prepared. Please see it if necessary.
