require './transaction_visitor'

class InvestmentEarnings < TransactionVisitor
  def initialize(account)
    @account = account
  end

  def value
    sleep(1)
    @earmings = 0
    @account.visit_transactions_with(self)
    return @earmings
  end

  def visit_deposit(deposit)
  end

  def visit_withdraw(withdraw)
  end

  def visit_transfer_deposit(deposit)
  end

  def visit_transfer_withdraw(withdraw)
  end

  def visit_certificate_of_deposit(certificate_of_deposit)
    @earmings = @earmings+certificate_of_deposit.earnings
  end
end