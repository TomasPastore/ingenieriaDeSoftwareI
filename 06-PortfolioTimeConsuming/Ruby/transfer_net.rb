require './transaction_visitor'

class TransferNet < TransactionVisitor
  def initialize(account)
    @account = account
  end

  def value
    @net = 0
    @account.visit_transactions_with(self)
    return @net
  end

  def visit_deposit(deposit)
  end

  def visit_withdraw(withdraw)
  end

  def visit_transfer_deposit(deposit)
    @net = @net + deposit.value
  end

  def visit_transfer_withdraw(withdraw)
    @net = @net - withdraw.value
  end

  def visit_certificate_of_deposit(certificate_of_deposit)
  end

end