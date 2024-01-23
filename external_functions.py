import json
class FLAGS:
    GREEN = 1
    AMBER = 2
    RED = 0
    MEDIUM_RISK = 3  # diplay purpose only
    WHITE = 4  # data is missing for this field

# This is a already written for your reference
def latest_financial_index(data: dict):
    """
    Determine the index of the latest standalone financial entry in the data.

    This function iterates over the "financials" list in the given data dictionary.
    It returns the index of the first financial entry where the "nature" key is equal to "STANDALONE".
    If no standalone financial entry is found, it returns 0.

    Parameters:
    - data (dict): A dictionary containing a list of financial entries under the "financials" key.

    Returns:
    - int: The index of the latest standalone financial entry or 0 if not found.
    """
    for index, financial in enumerate(data.get("financials")):
        if financial.get("nature") == "STANDALONE":
            return index
    return 0


def total_revenue(data: dict, financial_index): 
    """
    Calculate the total revenue from the financial data at the given index.

    This function accesses the "financials" list in the data dictionary at the specified index.
    It then retrieves the net revenue from the "pnl" (Profit and Loss) section under "lineItems".

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for calculation.

    Returns:
    - float: The net revenue value from the financial data.
    """
    financials = data.get("financials")[financial_index]
    if financials is None:
        return 4 # for missing data
    pnl = financials.get("pnl")
    if pnl is None:
        return 4
    lineItems = pnl.get("lineItems")
    if lineItems is None:
        return 4
    netRevenue = lineItems.get("net_revenue")
    if netRevenue is None:
        return 4
    return netRevenue


def total_borrowing(data: dict, financial_index):
    """
    Calculate the ratio of total borrowings to total revenue for the financial data at the given index.

    This function sums the long-term and short-term borrowings from the balance sheet ("bs")
    section of the financial data. It then divides this sum by the total revenue, calculated
    by calling the `total_revenue` function.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for calculation.

    Returns:
    - float: The ratio of total borrowings to total revenue.
    """
    financials = data.get("financials")[financial_index]
    if financials is None:
        print("financials is none")
        return 4
    bs = financials.get("bs")
    if bs is None:
        print("bs is none")
        return 4
    liabilities = bs.get("liabilities")
    if liabilities is None:
        print("liabilities is none")
        return 4
    longTermBorrowings = liabilities.get("long_term_borrowings")
    if longTermBorrowings is None:
        print("longTermBorrowings is none")
        return 4
    shortTermBorrowings = liabilities.get("short_term_borrowings")
    if shortTermBorrowings is None:
        print("shortTermBorrowings is none")
        return 4
    total_borrowings = longTermBorrowings + shortTermBorrowings
    #print(total_borrowings)
    return total_borrowings / total_revenue(data, financial_index)


def iscr_flag(data: dict, financial_index):
    """
    Determine the flag color based on the Interest Service Coverage Ratio (ISCR) value.

    This function calculates the ISCR value by calling the `iscr` function and then assigns a flag color
    based on the ISCR value. If the ISCR value is greater than or equal to 2, it assigns a GREEN flag,
    otherwise, it assigns a RED flag.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the ISCR calculation.

    Returns:
    - FLAGS.GREEN or FLAGS.RED: The flag color based on the ISCR value.
    """
    iscr_value = iscr(data, financial_index)
    #print(iscr_value , "iscr_value")
    if iscr_value >= 2:
        return FLAGS.GREEN
    else:
        return FLAGS.RED


def total_revenue_5cr_flag(data: dict, financial_index):
    """
    Determine the flag color based on whether the total revenue exceeds 50 million.

    This function calculates the total revenue by calling the `total_revenue` function and then assigns
    a flag color based on the revenue amount. If the total revenue is greater than or equal to 50 million,
    it assigns a GREEN flag, otherwise, it assigns a RED flag.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the revenue calculation.

    Returns:
    - FLAGS.GREEN or FLAGS.RED: The flag color based on the total revenue.
    """
    total_revenue_value = total_revenue(data, financial_index)
    #print(total_revenue_value)
    if total_revenue_value >= 50000000: #if greater than 50 million
        return FLAGS.GREEN
    else:
        return FLAGS.RED


def iscr(data: dict, financial_index):
    """
    Calculate the Interest Service Coverage Ratio (ISCR) for the financial data at the given index.

    ISCR is a ratio that measures how well a company can cover its interest payments on outstanding debt.
    It is calculated as the sum of profit before interest and tax, and depreciation, increased by 1,
    divided by the sum of interest expenses increased by 1. The addition of 1 is to avoid division by zero.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the ISCR calculation.

    Returns:
    - float: The ISCR value.
    """
    financials = data.get("financials")[financial_index]
    if financials is None:
        print("financials is none")
        return 4
    pnl = financials.get("pnl")
    if pnl is None:
        print("pnl is none")
        return 4
    lineItems = pnl.get("lineItems")
    if lineItems is None:
        print("lineItems is noneeeee")
        return 4
    profit_before_interest_and_tax = lineItems.get("profit_before_interest_and_tax")
    if profit_before_interest_and_tax is None:
        print("profit_before_interest_and_tax is none")
        return 4
    depreciation = lineItems.get("depreciation")
    if depreciation is None:
        print("depreciation is none")
        return 4
    interest_expenses = lineItems.get("interest")
    if interest_expenses is None:
        print("interest_expenses is none")
        return 4
    
    iscr_value = (profit_before_interest_and_tax + depreciation + 1) / (interest_expenses + 1)
    return iscr_value


def borrowing_to_revenue_flag(data: dict, financial_index):
    """
    Determine the flag color based on the ratio of total borrowings to total revenue.

    This function calculates the ratio of total borrowings to total revenue by calling the `total_borrowing`
    function and then assigns a flag color based on the calculated ratio. If the ratio is less than or equal
    to 0.25, it assigns a GREEN flag, otherwise, it assigns an AMBER flag.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the ratio calculation.

    Returns:
    - FLAGS.GREEN or FLAGS.AMBER: The flag color based on the borrowing to revenue ratio.
    """
    total_borrowing_value = total_borrowing(data, financial_index)
    #print(total_borrowing_value)
    if total_borrowing_value <= 0.25:
        return FLAGS.GREEN
    else:
        return FLAGS.AMBER

def probe_model_5l_profit(data: dict):
    """
    Evaluate various financial flags for the model.

    :param data: A dictionary containing financial data.
    :return: A dictionary with the evaluated flag values.
    """
    lastest_financial_index_value = latest_financial_index(data)

   
    total_revenue_5cr_flag_value = total_revenue_5cr_flag(
        data, lastest_financial_index_value
    )
   
   

    borrowing_to_revenue_flag_value = borrowing_to_revenue_flag(
        data, lastest_financial_index_value
    )

    

    iscr_flag_value = iscr_flag(data, lastest_financial_index_value)

    return {
        "flags": {
            "TOTAL_REVENUE_5CR_FLAG": total_revenue_5cr_flag_value,
            "BORROWING_TO_REVENUE_FLAG": borrowing_to_revenue_flag_value,
            "ISCR_FLAG": iscr_flag_value,
        }
    }



  