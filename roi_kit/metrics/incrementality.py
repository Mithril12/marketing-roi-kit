from dataclasses import dataclass
import math


@dataclass
class ABLiftResult:
    incremental_conversions: float
    incremental_cost_per_conversion: float | None
    incremental_revenue: float | None
    incremental_roi: float | None
    lift: float
    standard_error: float
    z_score: float
    ci_lower: float
    ci_upper: float


def ab_lift(
    test_conversions: int,
    test_users: int,
    control_conversions: int,
    control_users: int,
    spend_increment: float | None = None,
    revenue_per_conversion: float | None = None,
    alpha: float = 0.05,
) -> ABLiftResult:
    """
    Basic A/B lift calculation using a normal approximation for proportions.
    """

    if test_users <= 0 or control_users <= 0:
        raise ValueError("User counts must be positive.")

    p_test = test_conversions / test_users
    p_control = control_conversions / control_users
    lift = (p_test - p_control) / max(p_control, 1e-9)

    # standard error for difference in proportions
    se = math.sqrt(
        (p_test * (1 - p_test) / max(test_users, 1)) +
        (p_control * (1 - p_control) / max(control_users, 1))
    )

    # z for two-sided CI
    z = abs(_z_from_alpha(alpha))

    diff = p_test - p_control
    ci_lower = diff - z * se
    ci_upper = diff + z * se

    incremental_conversions = diff * test_users

    incr_revenue = None
    incr_roi = None
    incr_cpc = None

    if revenue_per_conversion is not None:
        incr_revenue = incremental_conversions * revenue_per_conversion

    if spend_increment is not None:
        if incremental_conversions != 0:
            incr_cpc = spend_increment / incremental_conversions
        if incr_revenue is not None and spend_increment != 0:
            incr_roi = (incr_revenue - spend_increment) / spend_increment

    return ABLiftResult(
        incremental_conversions=incremental_conversions,
        incremental_cost_per_conversion=incr_cpc,
        incremental_revenue=incr_revenue,
        incremental_roi=incr_roi,
        lift=lift,
        standard_error=se,
        z_score=z,
        ci_lower=ci_lower,
        ci_upper=ci_upper,
    )


def _z_from_alpha(alpha: float) -> float:
    """
    Hard-coded z-scores for common alpha values.
    """
    mapping = {
        0.10: 1.64,
        0.05: 1.96,
        0.01: 2.58,
    }
    return mapping.get(alpha, 1.96)
