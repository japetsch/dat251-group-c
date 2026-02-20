# Sign in and questionaire

As a registered donor, I want to sign in and complete a health questionnaire before donating so that the system can confirm I am eligible and safe to donate blood.

## Acceptance criteria

- User must sign in before accessing donation features.
- Health questionnaire appears after successful login.
- Questionnaire must be completed before booking a donation.
- System displays eligibility result after submission.
- Booking is blocked if questionnaire is incomplete.Error message is shown if submission fails.

# Secure sign in

As a donor, I want to securely sign into the app so that my personal donation history and eligibility status are protected.

## Acceptance Criteria:

- User can sign in using valid credentials (Email/Password or OTP).
Incorrect credentials display an error message.

User session expires after inactivity.

User must re-authenticate to access sensitive information.

Personal data is encrypted in transit.

User can securely log out of the application.