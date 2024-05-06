import numpy as np
from datetime import datetime


def date_diff_in_years(date_initial: str, date_final: str):
    # Parse the date strings into datetime objects
    # if type()
    date1 = datetime.strptime(date_initial, "%Y-%m-%d")
    date2 = datetime.strptime(date_final, "%Y-%m-%d")

    # Calculate the difference between the dates
    difference = date2 - date1

    # Convert difference in days to years
    years_difference = (
        difference.days / 365.25
    )  # Using 365.25 to account for leap years

    return years_difference


def time_interval_to_normalize_realized(df, date_key="TransactionDate"):
    """
    Use time interval between first purchase and last sale
    """
    first_purchase = df[df["Transaction"] == "Purchase"]["TransactionDate"].min()
    last_sale = df[df["Transaction"] == "Sale"]["TransactionDate"].max()
    return date_diff_in_years(first_purchase, last_sale)


def time_interval_to_normalize_unrealized(
    df, date_key="TransactionDate", current_price_date="2024-05-03"
):
    """
    Use time interval between first purchase and date of current_price (2024-05-03)
    """
    first_purchase = df[df["Transaction"] == "Purchase"]["TransactionDate"].min()
    return date_diff_in_years(first_purchase, current_price_date)


def calc_gains(group):
    group = group.sort_values(["TransactionDate"])
    percent_gain_realized = []
    realized_percent_gain_weighted = None
    realized_gains_per_year = None
    unrealized_percent_gains = None
    unrealized_gains_per_year = None
    total_cost = 0
    cost_basis = 0
    total_value = 0
    shares_owned = [0]
    shares_sold = []
    for i, trade in enumerate(group.iterrows()):
        trade = trade[1]
        print(f"__________________RECORD: {i} __________________")
        print(trade)

        # skip first trade if it is a sale
        # no previous purchase and we assume no short selling
        if trade["Transaction"] == "Purchase":
            total_value += trade["Amount"]
            total_cost += trade["Amount"] * trade["trade_price"]
            cost_basis = total_cost / total_value
            shares_owned.append(
                trade["Amount"] / trade["trade_price"] + shares_owned[-1]
            )
            print(f"{total_value=}")
            print(f"{total_cost=}")
            print(f"Cost Basis: {cost_basis}")
        if trade["Transaction"] == "Sale" and shares_owned[-1] != 0:
            r_gain = round(100 * (trade["trade_price"] - cost_basis) / cost_basis, 2)
            pending_shares_sold = trade["Amount"] / trade["trade_price"]
            pending_shares_owned = shares_owned[-1] - pending_shares_sold
            # dont allow short selling enforce shares_owned cant be negative
            if pending_shares_owned <= 0:
                # sell all of shares owned
                pending_shares_sold = shares_owned[-1]
                # update shares owned to 0
                pending_shares_owned = 0
                total_value = 0
                total_cost = 0

            shares_sold.append(pending_shares_sold)
            shares_owned.append(pending_shares_owned)

            print(f"{cost_basis=}")
            print(f"{r_gain=}%")
            percent_gain_realized.append(r_gain)
        if (
            i == len(group) - 1 and shares_owned[-1] != 0
        ):  # calculate unrealized profits on shares owned
            unrealized_percent_gains = round(
                100 * (trade["current_price"] - cost_basis) / cost_basis, 2
            )
            print(f"{unrealized_percent_gains=}%")
            unrealized_gains_per_year = (
                unrealized_percent_gains / time_interval_to_normalize_unrealized(group)
            )

        # calculate realized percent gain weighted by number of shares sold
        print(f"{shares_owned=}")
    print(f"{shares_sold}")

    if shares_sold != []:

        realized_percent_gain_weighted = round(
            sum(np.array(shares_sold) * np.array(percent_gain_realized))
            / sum(np.array(shares_sold)),
            2,
        )
        realized_gains_per_year = (
            realized_percent_gain_weighted / time_interval_to_normalize_realized(group)
        )
        print(f"{realized_percent_gain_weighted=}%")

    return (
        realized_percent_gain_weighted,
        unrealized_percent_gains,
        realized_gains_per_year,
        unrealized_gains_per_year,
    )
