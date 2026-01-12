#!/bin/bash

echo "Deploying Smart Inbox System..."

sam build
sam deploy --guided

echo "Deployment complete!"
