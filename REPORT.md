# REPORT.md

Group: Solo practice (update before submission)   Members: (add names before submission)

## Part A -- Test types

### 1. Smoke testing
Smoke testing checks whether the application's most important features work at a basic level. It should run after a new build or deployment to detect major problems quickly.

**Examples:**
- Check that a new user can register and log in successfully.
- Check that a customer can add a product to the cart and complete checkout.

### 2. Regression testing
Regression testing checks that existing features still work correctly after code changes or bug fixes. It should run after changes that could affect existing functionality, especially before merging or releasing code.

**Examples:**
- After fixing a cart-total bug, verify that the total includes every item.
- After changing login validation, verify that an incorrect password is still rejected.

### 3. Slow testing
Slow testing exercises the application with large amounts of data or many operations and takes noticeably longer to run. In this project, slow tests should run during scheduled full test runs, such as the nightly CI run, rather than every quick smoke-test run.

**Examples:**
- Import tens of thousands of products and verify the number imported.
- Perform many cart operations in a loop and verify that the final results are correct.

## Part B -- Scenario classification

### 1. Verify that a password-reset email is delivered within one minute.
**Classification: Smoke; potentially slow, depending on implementation.**

Password reset is an important user feature, so a quick check that the email is delivered can be a smoke test. If the test must wait for email delivery for up to a minute, it may also be slow in practice because of its execution time.

### 2. Verify that a previously fixed bug in shipping-cost calculation has not returned.
**Classification: Regression.**

This test checks whether a previously corrected defect has reappeared after code changes. It should verify that shipping costs are calculated correctly for the relevant inputs.

### 3. Verify that a nightly job can generate a sales report from ten years of orders.
**Classification: Slow.**

Processing ten years of orders can involve a large amount of historical data and take considerable time. It is suitable for a scheduled test run to check that the report can be generated correctly at that scale.

### 4. Verify that the payment page loads after every deployment.
**Classification: Smoke.**

The payment page is a critical part of an e-commerce system, so checking that it loads after deployment helps identify major failures quickly. This test verifies basic availability rather than every payment scenario.

### 5. Verify that a refund issued twice does not credit the customer twice — a fault reported by a customer last quarter.
**Classification: Regression.**

The scenario describes a previously reported defect, so the test should confirm that the defect does not return. It should verify that processing the same refund twice does not result in duplicate credit to the customer.

### 6. Verify that the recommendation engine still responds when the catalogue holds one million titles.
**Classification: Slow.**

The test exercises the recommendation engine with a very large catalogue. It helps verify that the system continues to respond correctly at scale, making it appropriate for a scheduled test run.


## Part F -- Team reflection

## Part C -- Smoke and slow test suite

All tests are located in `tests/test_bookstore.py`. The following results were collected against the original application before fixing the planted bugs.

### Smoke tests

Command: `python -m pytest -m smoke -v --durations=0`

| Test | What it checks | Result |
|---|---|---|
| `test_smoke_register_new_user` | A new user can register | PASSED |
| `test_smoke_login_correct_password_works` | A registered user can log in with the correct password | PASSED |
| `test_smoke_login_rejects_wrong_password` | Incorrect passwords are rejected | PASSED |
| `test_smoke_add_product_is_saved` | Products are stored and searchable | PASSED |
| `test_smoke_add_to_cart_puts_item_in_cart` | Products can be added to the cart | PASSED |
| `test_smoke_checkout_nonempty_cart_returns_order` | Checkout returns and records the order | PASSED |
| `test_smoke_end_to_end_shopping_flow` | Registration, login, adding a product, and checkout work together | PASSED |

**Smoke suite result:** 7 passed, 0 failed, in 0.04 seconds.

### Slow tests

Command: `python -m pytest -m slow -vv --durations=0`

| Test | Workload | Execution time | Result |
|---|---|---:|---|
| `test_slow_bulk_import_100k_products_are_stored` | Imports 100,000 products and checks the stored data | 0.11 s | PASSED |
| `test_slow_search_large_catalogue_repeated` | Searches a catalogue of 50,000 products 300 times | 0.63 s | PASSED |
| `test_slow_many_registrations_and_logins` | Registers 300,000 users and logs each one in | 0.53 s | PASSED |

**Slow suite result:** 3 passed, 0 failed, in 1.31 seconds.

### Comparison and observations

The smoke suite completed in 0.04 seconds, while the slow suite completed in 1.31 seconds. The slow suite took approximately 32.8 times as long overall. The individual slow tests took between 0.11 and 0.63 seconds.

These measurements were collected on the local Windows environment using Python 3.14.7 and pytest 9.1.1. Execution times may differ on other machines.

The smoke tests check essential application features quickly. The slow tests exercise larger datasets and repeated operations to check behavior under heavier workloads.