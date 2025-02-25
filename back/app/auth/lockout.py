"""
Module for handling account lockout.
"""

from datetime import UTC, datetime, timedelta


class LockoutConfig:
    """
    Configuration for account lockout.
    """

    INITIAL_LOCKOUT_THRESHOLD = 5  # Attempts required for initial lockout
    EXTRA_TRIES_AFTER_LOCKOUT = 5  # Additional tries after each lockout
    LOCKOUT_DURATIONS = [5, 15, 30, 60]  # Lockout durations in minutes

    @staticmethod
    def calculate_lockout_duration(attempts: int, locked_time) -> timedelta:
        """Calculate lockout duration based on attempts."""
        if attempts < LockoutConfig.INITIAL_LOCKOUT_THRESHOLD and not locked_time:
            return None

        locked_time = datetime.now(UTC)
        for i, duration in enumerate(LockoutConfig.LOCKOUT_DURATIONS):
            if (
                attempts
                == LockoutConfig.INITIAL_LOCKOUT_THRESHOLD
                + i * LockoutConfig.EXTRA_TRIES_AFTER_LOCKOUT
            ):
                return locked_time + timedelta(minutes=duration)

        if (
            attempts
            > LockoutConfig.INITIAL_LOCKOUT_THRESHOLD
            + len(LockoutConfig.LOCKOUT_DURATIONS)
            * LockoutConfig.EXTRA_TRIES_AFTER_LOCKOUT
        ):
            return locked_time + timedelta(minutes=LockoutConfig.LOCKOUT_DURATIONS[-1])
        return locked_time
