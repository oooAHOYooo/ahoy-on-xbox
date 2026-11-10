# Connect Microsoft Store Developer CLI

Setup checked October 28, 2026. Microsoft Store Developer CLI 0.4.3 is installed on this Mac through Homebrew. Authentication has not been configured or verified.

## Account setup

1. Sign in to https://partner.microsoft.com/dashboard and select the Ahoy Indie Media Windows developer account.
2. Open Account settings → User management → Microsoft Entra applications. A Manager account with tenant global administrator permissions is needed to manage these applications.
3. Associate the correct Entra tenant if needed. Add or create a dedicated application for Store API access and assign the Manager role as required by Microsoft's submission API documentation.
4. Record its Tenant ID and Application (client) ID. These are the API application's identifiers; do not assume the MSA App ID in STORE-RELEASE.md is the same application.
5. Create an application key/client secret, or configure a supported certificate. Keep the secret in a password manager and enter it locally; do not paste it into chat or commit it.
6. Obtain the Seller ID from the Partner Center account details. The Seller ID is distinct from the Store product ID.

## Connect this Mac

Run the interactive configuration in your own terminal:

```sh
msstore reconfigure
```

Use the Entra credentials and account identifiers for the tenant linked to Partner Center. Follow its prompts. The CLI also supports explicit tenantId, sellerId, clientId and clientSecret options for CI, but avoid putting literal secrets in shell history.

Verify the connection with:

```sh
msstore apps list
```

Confirm the returned account contains AHOY TV, Store product ID `9N6QB77PD6RT`, and the identity matches `AhoyIndieMedia.AHOYTV`. Retrieve the current submission status using the CLI's submission commands after checking their help and the returned app identifiers. Do not create, replace, commit, or publish a submission just to test authentication.

## Existing build pipeline

`.github/workflows/ci.yml` builds Windows Debug and Release and uploads the Store package as a GitHub Actions artifact. It does not authenticate to Partner Center or submit packages. A successful build does not prove Store certification or Xbox playback.

Keep the existing build pipeline separate from publication. After local access works, credentials can be stored as GitHub Actions secrets for an explicitly authorized workflow. Typical names are PARTNER_CENTER_TENANT_ID, PARTNER_CENTER_SELLER_ID, PARTNER_CENTER_CLIENT_ID, and PARTNER_CENTER_CLIENT_SECRET. Do not add the secret values to repository files or workflow logs.

Microsoft requires an app's first publication through Partner Center before using the CLI for subsequent updates. Check the live status of the existing AHOY TV submission before planning an update. The October 26 certification status in STORE-RELEASE.md is a historical claim, not a live account check.

## Official references

- https://learn.microsoft.com/en-us/windows/apps/publish/msstore-dev-cli/overview
- https://learn.microsoft.com/en-us/windows/apps/publish/msstore-dev-cli/commands
- https://learn.microsoft.com/en-us/windows/apps/publish/partner-center/manage-azure-ad-applications-in-partner-center
- https://learn.microsoft.com/windows/uwp/monetize/create-and-manage-submissions-using-windows-store-services
