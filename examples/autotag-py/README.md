# AWS Auto-tagging Example

Sample Pulumi program demonstrating auto-tagging of AWS resources.

## Deploying and running the program

1. Create a new stack:

    ```bash
    pulumi stack init aws-tags-example-dev
    ```

1. Set the AWS region:

    ```bash
    pulumi config set aws:region eu-central-1
    ```

1. Create a Python virtual environment:

    ```bash
    python3 -m venv venv
    ./venv/bin/pip install -r requirements.txt
    ```

1. Run `pulumi up` to preview and deploy changes:

    ```bash
    pulumi up
    ```

    ```
    Previewing update (aws-tags-example-dev):
         Type                      Name                                   Plan
     +   pulumi:pulumi:Stack       aws-tags-example-aws-tags-example-dev  create
     +   ├─ aws:ec2:SecurityGroup  web-secgrp                             create
     +   ├─ aws:s3:Bucket          my-bucket                              create
     +   └─ aws:ec2:Instance       web-server                             create

    Resources:
        + 4 to create

    Do you want to perform this update?
      yes
    > no
      details
    ```

1. To see the resources that were created, run `pulumi stack output`:

    ```bash
    pulumi stack output
    ```

    ```
    Current stack outputs (2):
        OUTPUT       VALUE
        bucket_name  my-bucket-***
        server_dns   ec2-***.eu-central-1.compute.amazonaws.com
    ```

1. To clean up resources, run `pulumi destroy`.

1. To delete the stack, run `pulumi stack rm aws-tags-example-dev`.
