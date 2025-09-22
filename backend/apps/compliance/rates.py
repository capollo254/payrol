# compliance/rates.py

from decimal import Decimal

# --- General Payroll Constants ---
MONTHLY_WORKING_HOURS = Decimal('225') # Standard for calculating hourly rates for salaried staff
NITA_LEVY_RATE = Decimal('50.00')    # Flat rate, payable by employer

# --- PAYE (Pay-As-You-Earn) ---
# Monthly tax bands and corresponding rates as of the Finance Act 2024.
# Source: KRA and other tax advisory firms.
# The `amount` is the upper limit of the band, and `rate` is the tax percentage.
PAYE_RATES = [
    (Decimal('24000.00'), Decimal('0.10')),
    (Decimal('8333.00'), Decimal('0.25')),
    (Decimal('467667.00'), Decimal('0.30')),
    (Decimal('300000.00'), Decimal('0.325')),
    (Decimal('inf'), Decimal('0.35')),  # `inf` represents all income above the previous band
]
PAYE_PERSONAL_RELIEF = Decimal('2400.00')

# --- NSSF (National Social Security Fund) ---
# Rates for Year 3 (Effective from February 2025).
# Source: NSSF Act, 2013, Third Schedule.
NSSF_RATE = Decimal('0.06')
NSSF_LOWER_EARNINGS_LIMIT = Decimal('8000.00')
NSSF_UPPER_EARNINGS_LIMIT = Decimal('72000.00')

# --- SHIF (Social Health Insurance Fund) ---
# Replaced NHIF from October 2024.
SHIF_RATE = Decimal('0.0275')
SHIF_MINIMUM_CONTRIBUTION = Decimal('300.00')

# --- Affordable Housing Levy (AHL) ---
# Based on the Affordable Housing Act, 2024.
AHL_RATE = Decimal('0.015')

# --- Overtime Rates ---
# As per the Employment Act and Wages Regulations Orders.
OVERTIME_WEEKDAY_MULTIPLIER = Decimal('1.5')
OVERTIME_WEEKEND_MULTIPLIER = Decimal('2.0')

# --- Other Constant Rates (if applicable) ---
# ... you can add other rates here as needed, e.g., for pension schemes, etc.
PENSION_MAX_RELIEF = Decimal('30000.00') # Example only, refer to current KRA rules.
INSURANCE_RELIEF_RATE = Decimal('0.15') # 15% of premiums, capped at KSh 5,000 per month
INSURANCE_RELIEF_MAX = Decimal('5000.00')