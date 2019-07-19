import sys

from troposphere import ImportValue, Parameter, Ref, Sub, Template
from troposphere.iam import PolicyType


def param(type, name, Description=None, **kwargs):
    k = {
        str: {"Type": "String"},
        int: {"Type": "Number"},
        list: {"Type": "CommaDelimitedList"},
        "ssh": {"Type": "AWS::EC2::KeyPair::KeyName"},
    }[type]
    k["Description"] = Description or name
    k.update(kwargs)
    p = t.add_parameter(Parameter(name, **k))
    param_refs[name] = Ref(p)
    return p


param_refs = {}
t = Template()

t.add_description("Extra role policies for the Jenkins agent")

param(str, "AgentStack")


t.add_resource(PolicyType(
    "Policy",
    PolicyName="ExtraPolicy",
    PolicyDocument={
        "Statement": [
            {
                "Action": "s3:ListBucket",
                "Resource": "arn:aws:s3:::examplebucket",
                "Effect": "Allow"
            }
        ]
    },
    Roles=[ImportValue(Sub("${AgentStack}-AgentRole"))]
))


template = t.to_json(indent=2)
if len(sys.argv) > 1:
    open(sys.argv[1], "w").write(template + "\n")
else:
    print(template)
