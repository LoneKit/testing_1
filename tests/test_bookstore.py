
import pytest
from bookstore_app import Users, Catalog, Cart


# ============================ SMOKE TESTS ============================
# Must PASS on the shipped code and FAIL on the five broken variants.

@pytest.mark.smoke
def test_smoke_register_new_user():
    """Author: <Member1>. Smoke: a new user can register (variant 1: always fails)."""
    u = Users()
    assert u.register("newuser", "password123") is True
    assert u.register("another", "pw456") is True


@pytest.mark.smoke
def test_smoke_login_correct_password_works():
    """Author: <Member1>. Smoke: registered user can log in with the right password."""
    u = Users()
    u.register("alice", "secret1")
    assert u.login("alice", "secret1") is True
    assert u.login("nobody", "secret1") is False


@pytest.mark.smoke
def test_smoke_login_rejects_wrong_password():
    """Author: <Member2>. Smoke: wrong password is refused (variant 2: accepts any password)."""
    u = Users()
    u.register("bob", "secret1")
    assert u.login("bob", "totallywrong") is False
    assert u.login("bob", "secret2") is False


@pytest.mark.smoke
def test_smoke_add_product_is_saved():
    """Author: <Member2>. Smoke: an added product is stored and findable (variant 3)."""
    cat = Catalog()
    cat.add_product(1, "Python Testing", 30)
    assert 1 in cat.products
    assert cat.products[1]["title"] == "Python Testing"
    assert cat.products[1]["price"] == 30
    assert cat.search("Python") == [1]


@pytest.mark.smoke
def test_smoke_add_to_cart_puts_item_in_cart():
    """Author: <Member3>. Smoke: items really reach the cart (variant 4)."""
    cat = Catalog()
    cat.add_product(1, "A", 10)
    cat.add_product(2, "B", 20)
    c = Cart(cat)
    assert c.add(1) is True
    assert c.add(2) is True
    assert c.items == [1, 2]
    assert c.add(999) is False          # unknown product is refused
    assert c.items == [1, 2]


@pytest.mark.smoke
def test_smoke_checkout_nonempty_cart_returns_order():
    """Author: <Member3>. Smoke: checkout returns the order and empties the cart (variant 5)."""
    cat = Catalog()
    cat.add_product(1, "A", 10)
    cat.add_product(2, "B", 20)
    c = Cart(cat)
    c.add(1)
    c.add(2)
    order = c.checkout()
    assert order == [1, 2]
    assert c.items == []
    assert c.history() == [[1, 2]]


@pytest.mark.smoke
def test_smoke_end_to_end_shopping_flow():
    """Author: <Member4>. Smoke: register -> login -> add product -> cart -> checkout."""
    u, cat = Users(), Catalog()
    assert u.register("carol", "pw12345")
    assert u.login("carol", "pw12345")
    cat.add_product(7, "Clean Code", 40)
    c = Cart(cat)
    assert c.add(7)
    assert c.checkout() == [7]

# ========================= REGRESSION TESTS ==========================
# Must FAIL on the shipped code, PASS after the fix. Write/commit the test
# BEFORE committing the fix.



# ========================= REGRESSION TESTS ==========================
# Each test must FAIL on the unfixed code and PASS after the fix.

@pytest.mark.regression
def test_regression_cart_total_includes_last_item():
    """Author: <Your Real Name>.
    Function: Cart.total().
    Wrong behaviour: the last item in the cart is not counted. With products
    priced 10, 20 and 30 in the cart, total() returned 30.
    Correct behaviour: the total is the sum of every item, so 60."""
    catalog = Catalog()
    catalog.add_product(1, "A", 10)
    catalog.add_product(2, "B", 20)
    catalog.add_product(3, "C", 30)
    cart = Cart(catalog)
    for product_id in (1, 2, 3):
        cart.add(product_id)
    assert cart.total() == 60

# ============================ SLOW TESTS =============================
# Slow = large data volumes / many loop iterations. They must PASS on the
# shipped code (so they assert things that are not affected by the bugs).

@pytest.mark.slow
def test_slow_bulk_import_100k_products_are_stored():
    """Author: <Member2>. Slow: imports 100,000 products. Slow because the
    import loop does per-item work (and a time.sleep(0) syscall) 100k times,
    then verifies every record landed in the catalogue."""
    cat = Catalog()
    data = [(i, f"Book {i}", i % 50 + 1) for i in range(100_000)]
    Cart(cat).import_products(data)
    assert len(cat.products) == 100_000
    assert cat.products[99_999]["title"] == "Book 99999"


@pytest.mark.slow
def test_slow_search_large_catalogue_repeated():
    """Author: <Member3>. Slow: 50,000 products searched 300 times, i.e. fifteen
    million title comparisons (search is a linear scan)."""
    cat = Catalog()
    for i in range(50_000):
        cat.add_product(i, "Title%d" % i, 1)
    for _ in range(300):
        assert cat.search("Title49999") == [49_999]


@pytest.mark.slow
def test_slow_many_registrations_and_logins():
    """Author: <Member4>. Slow: 300,000 registrations followed by 300,000 logins
    (each login walks the password string)."""
    u = Users()
    for i in range(300_000):
        assert u.register("user%d" % i, "pw%d" % i)
    for i in range(300_000):
        assert u.login("user%d" % i, "pw%d" % i)


# ======================== BONUS: TWO MARKERS =========================
# Needs the bundled-in explanation in REPORT.md (regression AND slow).

@pytest.mark.regression
@pytest.mark.slow
def test_large_order_processing():
    """Author: <Member1>. Regression + slow. Regression: guards the total()
    last-item bug (fails on shipped code). Slow: builds a 20,000-line order,
    checks out and totals it. Belongs in the nightly pipeline."""
    cat = Catalog()
    for i in range(20_000):
        cat.add_product(i, "B%d" % i, 2)
    c = Cart(cat)
    for i in range(20_000):
        c.add(i)
    assert c.total() == 40_000
    assert len(c.checkout()) == 20_000
