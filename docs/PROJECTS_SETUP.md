# GitHub Projects Setup

This document explains how to set up automatic addition of issues and pull requests to a GitHub Project board.

## Prerequisites

1. Create a GitHub Project (either classic or new Projects beta)
2. Note the project number from the URL (e.g., for `https://github.com/orgs/YourOrg/projects/5`, the number is `5`)

## Setup Steps

### Step 1: Create Project Variables

Go to your repository Settings → Secrets and variables → Actions → Variables tab.

Create a new repository variable:
- **Name**: `PROJECT_NUMBER`
- **Value**: Your project number (e.g., `5`)

### Step 2: Create Access Token

1. Go to GitHub Settings (your personal settings) → Developer settings → Personal access tokens → Fine-grained tokens
2. Create a new token with the following permissions:
   - Repository access: Select your repository
   - Permissions:
     - Contents: Read
     - Issues: Write
     - Pull requests: Write
     - Project: Write

3. Go to your repository Settings → Secrets and variables → Actions → Secrets tab
4. Create a new repository secret:
   - **Name**: `ADD_TO_PROJECT_TOKEN` 
   - **Value**: Your personal access token

### Step 3: Configure Project

Make sure your GitHub Project is configured to accept new items:
1. Open your project
2. Go to Settings (if using Projects beta)
3. Ensure the project can receive issues and pull requests from your repository

## How It Works

Once configured, the workflow (`.github/workflows/add-to-project.yml`) will automatically:
- Add new issues to your project when they are opened
- Add new pull requests to your project when they are opened

The workflow only runs if the `PROJECT_NUMBER` variable is set, so it's completely optional.

## Troubleshooting

### Workflow not running
- Check that `PROJECT_NUMBER` variable is set correctly
- Verify the project number matches your actual project

### Permission errors
- Ensure the `ADD_TO_PROJECT_TOKEN` has the right permissions
- Make sure the token hasn't expired
- Verify the token has access to your repository and project

### Items not being added
- Check the project settings to ensure it accepts items from your repository
- Verify the project URL format matches the expected pattern

## Alternative Setup

If you prefer organization-level project access:
1. Use an organization-owned project
2. Set up the token with organization permissions
3. Adjust the `project-url` in the workflow to match your organization structure

## Disabling Project Automation

To disable the automatic project addition:
1. Delete the `PROJECT_NUMBER` variable from repository settings
2. The workflow will automatically skip execution when this variable is not set