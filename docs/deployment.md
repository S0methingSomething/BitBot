# Deployment

This document outlines the steps required to deploy the BitBot landing page to GitHub Pages and Vercel.

## GitHub Pages

Deployment to GitHub Pages is fully automated. Every time a change is merged into the `main` branch, the `deploy_pages.yml` workflow will automatically build the site and deploy it.

## Vercel

Deployment to Vercel requires a one-time manual setup to link the project and set up the necessary secrets.

### 1. Install the Vercel CLI

```bash
npm install -g vercel
```

### 2. Link the Project

In the root of the project, run the following command:

```bash
vercel link
```

This will create a `.vercel/project.json` file. This file contains your `orgId` and `projectId`. **Do not commit this file to git.**

### 3. Create a Vercel Access Token

Go to your Vercel account settings and create a new access token.

### 4. Add GitHub Secrets

In your GitHub repository, go to "Settings" > "Secrets and variables" > "Actions" and add the following secrets:

*   `VERCEL_TOKEN`: The token you just generated.
*   `VERCEL_ORG_ID`: Your organization ID from the `.vercel/project.json` file.
*   `VERCEL_PROJECT_ID`: Your project ID from the `.vercel/project.json` file.

### 5. Deploy

Once the secrets are in place, you can manually trigger a deployment by running the "Deploy to Vercel" workflow in the "Actions" tab of the GitHub repository.
