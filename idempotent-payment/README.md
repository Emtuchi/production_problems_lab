# What this project is about (big picture)

This project is about building a payment system that doesn’t break when things go wrong.

**In the real world:**

- Networks fail

- Requests get retried

- Users click “Pay” twice

- Mobile apps resend requests

- Servers time out but the payment actually went through

If you don’t design for this, users get double-charged and companies lose money and trust.

This project shows how to prevent that.

## How it works (simple terms)

Every payment request must include an Idempotency Key

Think of it like a receipt number for a payment attempt

When a payment comes in:

- The system tries to save it using that key

- The database enforces that the key can only exist once

If the same request is sent again:

- The database blocks the duplicate

- The system returns the original payment result

No extra money is taken

So even if:

- The request times out

- The client retries

- The user clicks twice

The outcome stays the same
