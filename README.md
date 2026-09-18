# Payment Due Login Popup

Odoo 19 addon that shows a popup after the backend web client is ready when the logged-in user has due customer invoices or vendor bills.

## What counts as due

The popup includes documents that are:

- Posted.
- Customer invoices (`out_invoice`) or vendor bills (`in_invoice`).
- Due today or earlier.
- Still carrying a positive residual amount.
- In one of these payment states: Not Paid, Partially Paid, In Payment, or Blocked.

Credit notes/refunds and fully paid documents are not included.

## Popup controls

- **Minimize** closes the modal overlay and places a small **Payments Due** box at the bottom-left of the screen.
- The minimized box does not use a backdrop and does not block other Odoo work.
- Click the mini-box to restore the full payment list.
- Click the `X` on the mini-box to close the reminder for the current login session.
- Closing the full popup is remembered across browser refreshes.
- Logging out clears the dismissal state, so the popup is shown again after the next login.
- Each payment row has an **Open** button for the related invoice or bill; the reminder is minimized rather than closed while navigating.

## Access behavior

The search runs with the logged-in user's normal Odoo access rights, record rules, and allowed companies. The addon does not use `sudo()` and therefore does not expose accounting amounts to users who are not allowed to read the corresponding accounting records.

## Installation

1. Restart the Odoo 19 server.
2. Update the Apps list in developer mode.
3. Search for **Payment Due Login Popup** and install it.
4. Alternatively, update it from the command line:

   ```text
      odoo-bin -c odoo.conf -d <database_name> -u payment_due_login_popup
         ```

         5. Refresh the browser with a hard reload if the popup assets are cached.

         The popup is checked once for each login session. It is only shown when at least one due document exists.
         
