#!/bin/bash
set -e

# Get AWS account ID and region
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION=$(aws configure get region || echo "us-east-1")

echo "Setting up for account: $ACCOUNT_ID, region: $REGION"

# Update harness.json with the correct bucket name
BUCKET_NAME="awsnews-skills-${ACCOUNT_ID}-${REGION}"
HARNESS_FILE="agentcore/awsnews/app/awsnews/harness.json"

if [[ "$OSTYPE" == "darwin"* ]]; then
  sed -i '' "s|s3://awsnews-skills-[^/]*/|s3://${BUCKET_NAME}/|g" "$HARNESS_FILE"
else
  sed -i "s|s3://awsnews-skills-[^/]*/|s3://${BUCKET_NAME}/|g" "$HARNESS_FILE"
fi

# Update aws-targets.json with account and region
TARGETS_FILE="agentcore/awsnews/agentcore/aws-targets.json"
cat > "$TARGETS_FILE" << EOF
[
  {
    "name": "default",
    "account": "$ACCOUNT_ID",
    "region": "$REGION"
  }
]
EOF

echo "Done. Files updated:"
echo "  - $HARNESS_FILE"
echo "  - $TARGETS_FILE"
echo ""
echo "Next: cd agentcore/awsnews && agentcore deploy"
