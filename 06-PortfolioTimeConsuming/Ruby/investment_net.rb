require './transaction_visitor'

class InvestmentNet < TransactionVisitor
  def initialize(account)
    @account = account
  end

  def value
    sleep(1)
    @net = 0
    @account.visit_transactions_with(self)
    return @net
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
    @net = @net+certificate_of_deposit.value
  end
end