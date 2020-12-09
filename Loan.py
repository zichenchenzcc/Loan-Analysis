class Loan:
    """ Single Loan class
    With input principal, rate, payment, and extra payment, compute the amortization schedule, as well as
    overall metrics such as time to loan termination, total principal paid, and total interest paid.
    """
    def __init__(self, principal, rate, payment, extra_payment=0.0):
        """ Constructor to setup a single loan.
            :param principal:  principal amount left on the loan
            :param rate: annualized interest rate as a percentage
            :param payment: minimum expected payment
            :param extra_payment: additional payment applied to the interest
        """
        self.principal = principal
        self.rate = rate
        self.payment = payment
        self.extra_payment = extra_payment
        self.schedule = {}
        self.time_to_loan_termination = None
        self.total_principal_paid = 0.0
        self.total_interest_paid = 0.0

    def check_loan_parameters(self):
        er = None
        if self.principal <= 0.0:
#            raise ValueError('Principal must be greater than 0.0')
            er = 'Principal must be greater than 0.0'
        if self.rate <= 0.0:
#            raise ValueError('Rate must be greater than 0.0')
            er = 'Rate must be greater than 0.0'
        if self.payment <= 0.0:
#            raise ValueError('Payment must be greater than 0.0')
            er = 'Payment must be greater than 0.0'
        if self.extra_payment < 0.0:
#            raise ValueError('Extra payment must be greater than or equal to 0.0')
            er = 'Extra payment must be greater than or equal to 0.0'
        payment_critical = self.principal * self.rate/12.0/100.0
        if self.payment < payment_critical:
#            raise ValueError(f'Payment must be greater than {payment_critical}')
            er = f'Payment must be greater than {payment_critical}'
        return er
    def compute_schedule(self):
        """ Compute the loan schedule.
            :return: None, the schedule is stored in an instance dictionary
        """
        begin_principal = self.principal
        payment = self.payment
        payment_number = 0

        while begin_principal > 0.0:
            payment_number += 1
            applied_interest = begin_principal * self.rate / 12.0 / 100.0
            applied_principal = payment - applied_interest + self.extra_payment
            if applied_principal > begin_principal:
                payment = begin_principal + applied_interest
                extra_payment = 0.0
                applied_principal = payment - applied_interest + extra_payment
            end_principal = begin_principal - applied_principal
            self.schedule[payment_number] = (payment_number, round(begin_principal,2), payment,self.extra_payment, round(applied_principal,2), round(applied_interest,2), round(end_principal,2))
            begin_principal = end_principal

        self.time_to_loan_termination = max(self.schedule.keys()) if len(self.schedule.keys()) > 0 else None
        self.total_interest_paid = 0.0
        self.total_principal_paid = 0.0
        for pay in self.schedule.values():
            self.total_interest_paid += pay[5]
            self.total_principal_paid += pay[4]
        return self.schedule

