from inventory_optimizer.utils import seeded_rng


def test_seeded_rng_reproducible() -> None:
    a = seeded_rng(10).normal(0, 1, 5)
    b = seeded_rng(10).normal(0, 1, 5)
    assert (a == b).all()
