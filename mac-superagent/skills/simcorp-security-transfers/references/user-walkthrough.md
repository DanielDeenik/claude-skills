# End user walkthrough for reallocation windows

This is the procedure to show users. It is the shared skeleton that the help describes window
by window across the reallocation family, written once in show and tell order. Adapt step 4 to
the window at hand using `window-catalogue.md`. The wording below sticks to what the help
states; anything a user asks beyond it is checked against `gap-register.md` before answering.

## Before you start

Confirm two things with whoever owns the configuration. First, that the dimension you are
about to change is part of the holding key, meaning the Financial Accounting Principle for the
security sets split on that dimension. The help states for custody, special instance mark,
free codes, purpose and blocking that the reallocation makes no sense otherwise. Second, that
you know which business transaction code the desk expects, because several windows offer both
a standard and a start of day variant.

## Step 1. Identify the source position

In the Positions from section, fill enough key fields to find the position, for example the
security identification and the portfolio. For windows that carry them, the custodian and
custody of the source position narrow the search further.

## Step 2. Select the position

Choose Functions, then Positions. The window lists the positions matching your key fields.
Select the position that is to be reallocated. This step is mandatory; the reallocation always
runs against a selected position, not against typed values alone.

## Step 3. Specify the destination

In the Position to section, fill only the dimension that changes. For a portfolio move that is
the new Portfolio and portfolio Group. For a custody move it is the new Custody. For a
security number move it is the new security identification, which must already exist in the
static data. For mark, free code, compound and purpose moves it is the new code value.

## Step 4. Specify how much moves and under which code

In the Reallocation section, enter the Date and the Nominal, meaning the amount or the number
of shares, to state how big a part of the original position is reallocated. A partial amount
splits the position; the full amount moves it entirely. Confirm the business transaction code
in the Trans. code field against the catalogue for the window you are in.

## Step 5. Save and read the Balance section

Save the transaction with the target status level set in the Request field; the Actual field
shows what was actually saved and matches Request when the user is authorised and the
transaction is valid. The standard ladder from the Transaction Process manual runs Entry,
then Position or Free deal where positions are affected but nothing is final, then Fin calc
where it is finally booked, then Trade GL and Settle GL. The holding key locks at Position
status or higher, so a wrong portfolio or custody must be caught at Entry. The Balance
section then displays how the position from the original
holding splits into the old and the new holding, with before and after values for both sides.
This is the immediate visual check that the reallocation did what was intended. Remind users
that one saved business transaction has produced two elementary transactions, an outgoing leg
from the source and an ingoing leg into the destination, and both will appear downstream.

## Step 6. Further processing of an existing reallocation

Existing reallocation transactions are processed by searching them into the window with the
search functions and saving them again, possibly at a higher status level. The Main status
section carries the Request field for the target status and shows the actual status. The
status ladder itself is client configuration; read it from the environment.

## Step 7. Modifying

Where the help documents modification, the route is File, then Modify. After choosing Modify
the user must choose Functions, then Positions again before saving. The help states this
explicitly for the custody, special holding mark and security number windows; treat it as the
safe habit for the whole family.

## Common questions to be ready for

When a user asks why their reallocation changed nothing economically, the answer is that a
reallocation moves a holding across the holding key and books no market trade; profit or loss
arises only in the specific cases the help documents, such as currency conversions on the out
leg of a conversion or a priced purpose reallocation. When a user asks why the window seems to
have no effect, check the holding key split first. When a user asks about moving a security in or out of external custody rather than inside
the books, route them to the Security Transfers window family in
`security-transfers-window.md` instead. When a user asks what a code such as
RalocCdyPorSD stands for, give the verified family pattern and flag that the exact expansion
awaits the help page, per the gap register.
