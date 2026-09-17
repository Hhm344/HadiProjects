"""
generate_dataset.py
-------------------
Generates a realistic banking-focused phishing email dataset for the
CMPS354 project. The dataset mixes templates with substantial cross-class
noise so models do NOT trivially separate the classes:

  - About 20% of phishing emails are "polished" (no obvious red flags).
  - About 30% of legitimate emails contain noisy phishing-like cues.
  - Senders come from a shared pool used by both classes.

Columns:
    email_id, sender, subject, body, num_links, has_urgent_words,
    has_money_words, has_suspicious_url, num_misspellings, label

Label: 1 = phishing, 0 = legitimate (ham)
"""

import csv
import random
import os

random.seed(42)

OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "phishing_emails.csv")

COMMON_SENDERS = [
    "alerts@bankofamerica.com",
    "no-reply@bankofamerica.com",
    "service@chase.com",
    "customer.service@chase.com",
    "secure@wellsfargo.com",
    "alerts@wellsfargo.com",
    "info@hsbc.com",
    "support@hsbc.com",
    "service@citi.com",
    "alerts@citi.com",
    "no-reply@barclays.com",
    "support@paypal.com",
    "secure@paypal.com",
    "noreply@capitalone.com",
    "alerts@usbank.com",
    "service@americanexpress.com",
    "support@bankofamerica-online.com",
    "alerts@chase-secure.com",
    "service@wellsfargo-verify.net",
]

PHISH_SUBJECTS = [
    "Account security update",
    "Action required on your account",
    "Verify your identity",
    "Important notice regarding your account",
    "Card temporarily restricted",
    "Confirm recent transaction",
    "Online banking access expires soon",
    "Unusual activity detected",
    "Reactivate your suspended account",
    "Confirm your details",
    "Wire transfer pending verification",
    "New device login detected",
    "Your account statement",
    "Security check required",
    "Update your security questions",
]

PHISH_BODIES = [
    ("Dear valued customer, we have detected unusual activity on your account. "
     "Please click {URL} to verify your identity. Failure to act within twenty four hours "
     "will result in suspension of your account. Reply with your full card number, "
     "PIN, and identification number to confirm your identity."),
    ("Notice your online banking has been temporarily locked due to suspicious login attempts. "
     "Confirm your account details at {URL} to restore access. We need your password and "
     "card verification value to verify."),
    ("Congratulations you have qualified for a customer reward. Click {URL} to claim the offer. "
     "Provide your bank account number and routing number to receive funds. "
     "This offer expires soon."),
    ("Dear customer please update your banking informations. Visit {URL} and enter your "
     "username password and security questions. Your account will be deactivated if you do not respond."),
    ("Alert a withdrawl of two thousand dollars was attempted from your account. If this was not you click {URL} "
     "and verify your identity by providing your full credit card details and PIN."),
    ("Your tax refund is ready. To recieve your money click {URL} and submit your bank "
     "account details. This is only valid for twenty four hours."),
    ("Dear client our security team noticed a problem with you account. Please re-confirm your "
     "informations via {URL}. Provide passowrd and card number to avoid closure."),
    ("Notice your wire transfer is on hold. Click {URL} to release the funds. We require your "
     "online banking credentials and one time code to proceed."),
    ("Securty alert. New device login detected. Verify it was you at {URL}. Enter password security "
     "code and date of birth. If ignored your account will be closed permanently."),
    ("You have a new secure message from your bank. Login at {URL} using your account credentials "
     "to view. Failure to login will block your account."),
]

PHISH_URLS = [
    "http://bank-verify-login.tk/secure",
    "http://secure-bankupdate.xyz/login",
    "http://chase-bank-secure-portal.com/verify",
    "http://192.168.45.21/bank-login.php",
    "http://wellsfargo.secure-update.info/auth",
    "http://bit.ly/3xPhish9",
    "http://tinyurl.com/bank-secure-99",
    "http://account-verification.online/click",
    "http://citi-bank.login-securely.co/index",
    "http://hsbc-alerts.verify-now.xyz",
]

PHISH_URLS_POLISHED = [
    "https://onlinebanking.bankofamerica.com/auth",
    "https://chase.com/secure/verify",
    "https://wellsfargo.com/account",
    "https://citi.com/login",
]

HAM_SUBJECTS = [
    "Your monthly account statement is ready",
    "Thank you for your recent transaction",
    "Welcome to your new savings account",
    "Reminder review meeting tomorrow",
    "Your scheduled payment was processed",
    "New features available in our mobile app",
    "Customer satisfaction survey",
    "Branch hours update",
    "Travel notification received",
    "Tips for managing your budget",
    "Your direct deposit has arrived",
    "Statement for credit card ending 4421",
    "Annual security review reminder",
    "Your new debit card is on its way",
    "Thank you for banking with us",
]

HAM_BODIES = [
    ("Dear customer your monthly statement for the period ending last week is now available "
     "in your online banking portal. You can view it by logging in through our official website "
     "or mobile app. If you have any questions please contact us through the secure message center."),
    ("Thank you for your recent transaction. Your payment has been processed "
     "successfully. The transaction reference number is included in your statement. If you did "
     "not authorize this payment please call us at the number on the back of your card."),
    ("Welcome to your new savings account. We are delighted to have you as a customer. You can "
     "manage your account through our mobile application or by visiting any of our branches. "
     "Our customer service team is available to assist you during business hours."),
    ("This is a reminder that your quarterly review meeting with your financial advisor is "
     "scheduled for tomorrow at ten in the morning. Please bring your most recent financial "
     "statements. The meeting will be held at the branch on Main Street."),
    ("Your scheduled bill payment was processed on schedule. The amount has been debited from "
     "your checking account. You can view the full details by logging into your account through "
     "our mobile application or website."),
    ("We are excited to announce new features in our mobile banking application. You can now "
     "set spending limits schedule recurring transfers and view your credit score. "
     "Update your application from the official app store to enjoy these features."),
    ("We value your feedback. Please take two minutes to complete our customer satisfaction "
     "survey. Your responses help us improve our services. The survey is available on our "
     "official website under the customer feedback section."),
    ("Please note that our branch hours will be modified during the upcoming holiday season. "
     "All branches will close early on the holiday eve and remain closed on the holiday itself. "
     "Online and mobile banking remain available at all times."),
    ("We have received your travel notification. Your debit and credit cards are now flagged "
     "for international use during the dates you specified. Have a safe trip. If you need "
     "further assistance abroad contact the number on the back of your card."),
    ("Managing a monthly budget can be easier with our budgeting tools. Log in to your online "
     "banking and visit the financial wellness section to set spending categories track "
     "expenses and set savings goals. This service is included with your account."),
]

HAM_URLS = [
    "https://www.bankofamerica.com/online-banking/security",
    "https://www.chase.com/personal/credit-cards/secure",
    "https://www.wellsfargo.com/online-banking/update-profile",
    "https://www.citi.com/login",
    "https://www.hsbc.com/help/security",
]

URGENT_WORDS = ["urgent", "immediately", "asap", "final notice", "warning", "alert", "act now",
                "twenty four hours", "expires today", "hurry", "action required",
                "do not delay", "respond now"]
MONEY_WORDS = ["refund", "reward", "won", "claim", "wire transfer", "withdrawal", "withdrawl",
               "credit card", "pin", "routing number", "thousand dollars", "$", "dollars",
               "cash", "prize"]
SUSPICIOUS_URL_PATTERNS = [".tk/", ".xyz/", ".info/", ".online/", "bit.ly", "tinyurl",
                          "192.168.", "10.0.", "-secure", "-verify",
                          "-update", "-login"]
MISSPELLINGS = ["urgenlty", "informations", "withdrawl", "recieve", "passowrd", "securty",
                "you account"]


def count_words(text, words):
    text_lower = text.lower()
    return sum(text_lower.count(w) for w in words)


def has_suspicious_url(body):
    body_lower = body.lower()
    return int(any(s in body_lower for s in SUSPICIOUS_URL_PATTERNS))


def count_misspellings(body):
    body_lower = body.lower()
    return sum(body_lower.count(w) for w in MISSPELLINGS)


def add_random_filler(body, label):
    """Add random conversational filler shared across both classes."""
    fillers = [
        "We appreciate your business.",
        "Thank you for choosing us.",
        "If you have any questions please reply to this email.",
        "Have a great day.",
        "Sincerely the customer service team.",
        "Reference number " + str(random.randint(100000, 999999)) + ".",
        "Sent on " + random.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]) + ".",
        "Please do not reply to this automated message.",
        "Your privacy is important to us.",
        "Visit our website for more information.",
    ]
    n = random.randint(0, 3)
    chosen = random.sample(fillers, k=min(n, len(fillers)))
    if chosen:
        body = body + " " + " ".join(chosen)
    return body


def compute_features(row):
    # Optionally inject filler before computing features
    if random.random() < 0.5:
        row["body"] = add_random_filler(row["body"], row["label"])
    body = row["body"]
    subject = row["subject"]
    text = subject + " " + body
    row["num_links"] = body.count("http")
    row["has_urgent_words"] = int(count_words(text, URGENT_WORDS) > 0)
    row["has_money_words"] = int(count_words(body, MONEY_WORDS) > 0)
    row["has_suspicious_url"] = has_suspicious_url(body)
    row["num_misspellings"] = count_misspellings(body)
    return row


def generate_phishing_email(idx):
    subject = random.choice(PHISH_SUBJECTS)
    sender = random.choice(COMMON_SENDERS)
    body_template = random.choice(PHISH_BODIES)
    url = random.choice(PHISH_URLS)
    body = body_template.format(URL=url)
    if random.random() < 0.35:
        body += " Also see " + random.choice(PHISH_URLS)
    row = {
        "email_id": idx,
        "sender": sender,
        "subject": subject,
        "body": body,
        "label": 1,
    }

    # Polish a subset of phishing emails
    if random.random() < 0.22:
        for w in ["URGENT", "WARNING", "ALERT", "Hurry", "immediately",
                  "final warning", "Final notice", "do not delay", "respond now",
                  "twenty four hours"]:
            row["body"] = row["body"].replace(w, "")
        if random.random() < 0.7:
            for u in PHISH_URLS:
                row["body"] = row["body"].replace(u, random.choice(PHISH_URLS_POLISHED))
        if random.random() < 0.5:
            for w in ["reward", "won", "claim", "two thousand dollars", "refund"]:
                row["body"] = row["body"].replace(w, "")
        if random.random() < 0.5:
            replacements = {"urgenlty": "urgently", "informations": "information",
                            "withdrawl": "withdrawal", "recieve": "receive",
                            "passowrd": "password", "securty": "security",
                            "you account": "your account"}
            for k, v in replacements.items():
                row["body"] = row["body"].replace(k, v)

    return compute_features(row)


def generate_ham_email(idx):
    subject = random.choice(HAM_SUBJECTS)
    sender = random.choice(COMMON_SENDERS)
    body = random.choice(HAM_BODIES)
    row = {
        "email_id": idx,
        "sender": sender,
        "subject": subject,
        "body": body,
        "label": 0,
    }

    # Inject phishing-like noise into a subset of legitimate emails
    r = random.random()
    if r < 0.10:
        row["body"] += " Please update your account information at " + random.choice(HAM_URLS)
    elif r < 0.18:
        row["body"] += " Action required please verify your contact details before the end of the month."
    elif r < 0.24:
        row["body"] += " You may receive a $25 statement credit this quarter."
    elif r < 0.28:
        row["body"] += " More info https://bit.ly/bank-news"
    elif r < 0.32:
        row["body"] += " For your security please confirm your identity by logging in to your online banking."

    return compute_features(row)


# Adversarial templates that look extremely similar to ham but are phishing.
# These reuse legitimate-style phrasing while still being malicious.
HARD_PHISH_BODIES = [
    ("Dear customer thank you for banking with us. As part of our annual security review "
     "we kindly ask you to confirm your account by visiting {URL}. This helps us keep your "
     "account safe and active. We appreciate your cooperation."),
    ("Hello and thank you for your recent transaction. We noticed that your contact "
     "information may be out of date. To make sure you continue to receive important "
     "notifications please update your details through your online banking at {URL}."),
    ("Your monthly statement is now available. To make sure you can continue accessing "
     "the statements online please re-confirm your login details at {URL}. We value your "
     "continued trust in our services."),
    ("Welcome back. As part of our ongoing improvements to mobile banking we are asking "
     "customers to log in once via {URL} so that the new features can be linked to your "
     "profile. Thank you for your patience."),
]

# Hard ham emails that mention security and verification but are legitimate.
HARD_HAM_BODIES = [
    ("Thank you for completing the annual security review. Your account credentials and "
     "security questions have been refreshed. No further action is required from you at "
     "this time. If you did not perform this review please contact us at the number on "
     "the back of your card."),
    ("Reminder twenty four hours remain to RSVP for the customer appreciation event at "
     "our downtown branch. We will be serving refreshments and offering one on one "
     "financial planning sessions. Please respond at your earliest convenience."),
    ("This is an alert about your new credit card. Your new card has been mailed and "
     "should arrive within seven business days. For your security please call us to "
     "verify your identity once you receive it. Standard activation procedures apply."),
    ("Our records show that a wire transfer of one thousand dollars has been deposited "
     "to your account. The transaction is complete and the funds are now available. If "
     "this was unexpected please contact your branch manager."),
]


def generate_hard_phishing(idx):
    subject = random.choice(["Account confirmation request", "Quick account check",
                             "Annual review of your details", "Help us keep your account secure",
                             "Your statement and a small request"])
    sender = random.choice(COMMON_SENDERS)
    url = random.choice(PHISH_URLS_POLISHED)
    body = random.choice(HARD_PHISH_BODIES).format(URL=url)
    row = {"email_id": idx, "sender": sender, "subject": subject, "body": body, "label": 1}
    return compute_features(row)


def generate_hard_ham(idx):
    subject = random.choice(["Security review completed", "Reminder customer appreciation event",
                             "Your new card is on its way", "Wire transfer received",
                             "Action confirmation"])
    sender = random.choice(COMMON_SENDERS)
    body = random.choice(HARD_HAM_BODIES)
    row = {"email_id": idx, "sender": sender, "subject": subject, "body": body, "label": 0}
    return compute_features(row)


def main():
    rows = []
    n_phish = 1000
    n_ham = 1300
    n_hard_phish = 150   # phishing emails that look polite and ham-like
    n_hard_ham = 150     # ham emails that contain security/wire/credential phrasing
    n_label_noise = 90   # genuine label noise (mislabeled annotations)

    for i in range(n_phish):
        rows.append(generate_phishing_email(i))
    for i in range(n_ham):
        rows.append(generate_ham_email(n_phish + i))
    for i in range(n_hard_phish):
        rows.append(generate_hard_phishing(n_phish + n_ham + i))
    for i in range(n_hard_ham):
        rows.append(generate_hard_ham(n_phish + n_ham + n_hard_phish + i))

    # Flip a small fraction of labels to simulate annotation noise
    for _ in range(n_label_noise):
        idx = random.randrange(len(rows))
        rows[idx]["label"] = 1 - rows[idx]["label"]

    random.shuffle(rows)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    fieldnames = ["email_id", "sender", "subject", "body", "num_links",
                  "has_urgent_words", "has_money_words", "has_suspicious_url",
                  "num_misspellings", "label"]
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in fieldnames})

    print(f"Wrote {len(rows)} rows to {OUT_PATH}")
    phish_count = sum(1 for r in rows if r["label"] == 1)
    ham_count = len(rows) - phish_count
    print(f"  Phishing:   {phish_count}  ({phish_count/len(rows)*100:.1f}%)")
    print(f"  Legitimate: {ham_count}  ({ham_count/len(rows)*100:.1f}%)")


if __name__ == "__main__":
    main()
