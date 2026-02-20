# Requirements 

## Functional

### User-side

- Book appointments 
    - Verify no previous donation in the last 3-4 months
    - Verify exclusion rules (sickness, cuts, etc.)
    - Choose location
- See current appointments
- Change/Delete appointments
- Get notifications about appointment changes
- Get notification/reminder for appointment
- Notification on being able to donate blood again (only 4 times a year, 3-4 months between)
- Add notes to appointment (delay)

- Sign-up/Sign-in
- Questionnaire to verify eligibility

- See statistics 
- Get yearly review

- See available donation locations
- See closest donation location to you

- Change user data
    - address (home and work etc.)
    - email
    - phone-number
    - etc.

### Administration-side 

- See upcoming appointments
- Cancel appointment
    - Give reason
- Reschedule appointment
    - Give reason
- See if first time donor

- Send low blood-quantity warnings

- Upload statistic data

- Create new admin account/user
- Access control

- Block user
- Add notes to user (internal)
- Add notes to appointment 
- See phone number/email for appointments
- Send notification to user

- Manually create/book appointment for a user
- Change user data (address etc.)
- Get donation history of user
    - number of donations
    - test results of donations

### Algorithmic part

- Low on blood reserves: 
    - Query DB of Users 
    - take in account donation frequency 
    - Only notify users that are "available" to donate again also important monitor blood quality and take in account
    - Then take "likely" donors in account -> usually donate on this day etc.
    - Don't call people that don't always agree frequently (someone who only donates every 6 month, don't notify every 3 months)

## Non-Functional

### Security

- Confidentiality
- Integrity
- Regulatory/Compliance

### Manageability

- Recoverability
- Serviceability/Maintainability
- Scalability
- Sustainability
- Availability
- Usability
- Interoperability
- Manageability
- Regulatory/Compliance
- Testability

### Performance 

- Performance (should not be annoying to use)
    - Create benchmarks and act accordingly

### Accessibility 

- Accessibility 
    - Screen reader support
    - Colour contrast
    - Colour blind save
    - Dark-/Light-mode
