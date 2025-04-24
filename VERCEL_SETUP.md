# Vercel Deployment Guide

This guide will help you set up your environment variables correctly on Vercel to ensure your application works properly.

## Setting Up Service Account Credentials

Since we've removed the credentials file from Git for security reasons, you need to set up service account credentials as environment variables in Vercel:

1. Go to your [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project
3. Navigate to "Settings" > "Environment Variables"
4. Add the following environment variables from your service account JSON file:

| Environment Variable | Description | Example |
|----------------------|-------------|---------|
| `GOOGLE_SERVICE_ACCOUNT_EMAIL` | Email address of your service account | your-service-account@your-project.iam.gserviceaccount.com |
| `GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY` | The private key from your service account JSON | "-----BEGIN PRIVATE KEY-----\nYour key here\n-----END PRIVATE KEY-----\n" |
| `GOOGLE_PROJECT_ID` | Your Google Cloud project ID | your-project-id |
| `GOOGLE_PRIVATE_KEY_ID` | The private key ID | a1b2c3d4e5f6... |
| `GOOGLE_CLIENT_ID` | Client ID from service account | 123456789012345678901 |
| `GOOGLE_CLIENT_X509_CERT_URL` | Certificate URL | https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com |
| `GOOGLE_CALENDAR_ID` | Your Google Calendar ID | your-calendar-id@group.calendar.google.com |
| `ENABLE_GCAL` | Set to "true" to enable Google Calendar integration | true |

## Important Notes for `GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY`

When copying the private key:

1. Include the entire key including `-----BEGIN PRIVATE KEY-----` and `-----END PRIVATE KEY-----`
2. Make sure newlines are preserved - in the environment variable, replace actual newlines with `\n`
3. Include the quotes around the key value

## Redeploying

After setting all environment variables:

1. Go to the "Deployments" tab
2. Click "Redeploy" on your latest deployment or push a new commit

## Testing

After redeployment, verify that:

1. The main app loads without errors
2. The calendar functionality works
3. Event submissions that use Google Calendar integration work correctly

## Troubleshooting

If you still see 500 errors:

1. Check Vercel logs for detailed error messages
2. Verify all environment variables are correctly set
3. Try adding the credentials file back temporarily to see if it resolves the issue
4. If all else fails, disable Google Calendar integration by setting `ENABLE_GCAL=false` 