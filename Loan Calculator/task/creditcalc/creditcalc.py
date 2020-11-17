from math import floor, ceil, log
from sys import exit
from argparse import ArgumentParser


# function create object of class ArgumentParser(). This object get arguments after parse of command from terminal
def parser_command():
    parser = ArgumentParser()
    parser.add_argument("--type", type=str, help="type")
    parser.add_argument("--principal", type=int, help="principal")
    parser.add_argument("--interest", type=float, help="interest")
    parser.add_argument("--periods", type=int, help="periods")
    parser.add_argument("--payment", type=int, help="payment")
    return parser.parse_args()


# it's a error handler. Gets arguments from command and check out contains invalid value or wrong and excess arguments
def error_handler(args):
    # list with boolean expressions, if some return True, function return error's message and will stop
    errors = [args.type not in ("diff", "annuity"),
              args.type is None,
              args.interest is None,
              args.payment or args.principal or args.periods or args.interest <= 0]
    if True in errors:
        print("Incorrect parameters.")
        # stop the program
        exit()


# main function
def main():
    args = parser_command()
    error_handler(args)

    # get principal
    if args.type == "annuity" and args.principal is None:
        get_principal(args.periods, args.payment, args.interest)
    # get periods
    elif args.type == "annuity" and args.periods is None:
        get_periods(args.principal, args.payment, args.interest)
    # get annuity payment
    elif args.type == "annuity" and args.payment is None:
        annuity_payment(args.principal, args.periods, args.interest)
    # get diff payment
    elif args.type == "diff":
        diff_payment(args.principal, args.periods, args.interest)


# calculation principal of loan
def get_principal(periods, payment, interest):
    # the nominal needs in formula of cal a principal
    nominal = interest / (12 * 100)
    # formula of cal the principal
    principal = floor(payment / ((nominal * pow(1 + nominal, periods)) / ((pow(1 + nominal, periods)) - 1)))
    # cal overpayment (payments with overpay multiple on periods minus the principal)
    overpayment = payment * periods - principal
    print(f"Your loan principal = {principal}!")
    print(f"Overpayment = {overpayment}")


# calculation periods
def get_periods(principal, payment, interest):
    nominal = interest / (12 * 100)
    # formula for calculation the periods like month
    month = ceil(log(payment / (payment - nominal * principal), 1 + nominal))
    # transfer month to years
    years = month // 12

    # depending on the value of periods print correct info message
    if month % 12 == 0:
        if years > 1:
            print(f"It will take {years} years to repay this loan!")
        else:
            print("It will take 1 year to repay this loan!")
    else:
        if years == 0:
            print(f"It will take {month % 12} months to repay this loan!")
        elif years == 1:
            print(f"It will take 1 year and {month % 12} months to repay this loan!")
        else:
            print(f"It will take {years} years and {month % 12} months to repay this loan!")
    overpayment = payment * month - principal
    print(f"Overpayment = {overpayment}")


# calculation annuity payment
def annuity_payment(principal, periods, interest):
    nominal = interest / (12 * 100)
    # formula for calculation the annuity
    payment = ceil(principal * (nominal * pow(1 + nominal, periods) / (pow(1 + nominal, periods) - 1)))
    overpayment = payment * periods - principal
    print(f"Your annuity payment = {payment}!")
    print(f"Overpayment = {overpayment}")


# calculation differentiate payment
def diff_payment(principal, periods, interest):
    nominal = interest / (12 * 100)
    # the var month it's like a count for working of while loop and it's value will be print into info message
    month = 1
    # the var summary it sum of payment, there is it will be uses for calculation overpayment
    summary = 0
    # this loop will be print message with value of diff payment for every month during periods
    while month <= periods:
        # formula for calculation the diff payment for every month in periods
        diff = ceil(principal / periods + nominal * (principal - ((principal * (month - 1)) / periods)))
        print(f"Month {month}: payment is {diff}")
        month += 1
        summary += diff
    overpayment = summary - principal
    print(f"\nOverpayment = {overpayment}")


# running the program from here
if __name__ == '__main__':
    main()
