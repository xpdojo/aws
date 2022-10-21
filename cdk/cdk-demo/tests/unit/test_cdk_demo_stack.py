import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_demo.cdk_demo_stack import CdkDemoStack


def test_lambda_created():
    app = core.App()
    stack = CdkDemoStack(app, "cdk-demo")
    template = assertions.Template.from_stack(stack)
    template.has_resource_properties("AWS::Lambda::Function", {})

    json_template = template.to_json()
    assert type(json_template) == dict
    resources_key: str = "Resources"
    assert resources_key in json_template

    lambda_key: str = ""
    for key, value in json_template[resources_key].items():
        if value["Type"] == "AWS::Lambda::Function":
            lambda_key = key
            break

    assert lambda_key in json_template[resources_key]
    assert "lambda_function.handler" in json_template[resources_key][lambda_key]["Properties"]["Handler"]
