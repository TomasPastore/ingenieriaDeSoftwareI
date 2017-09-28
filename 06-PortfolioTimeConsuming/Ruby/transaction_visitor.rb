require './object'

class TransactionVisitor

  def visit_deposit(deposit)
    self.should_implement
  end

  def visit_withdraw(withdraw)
    self.should_implement
  end

  def visit_transfer_deposit(deposit)
    self.should_implement
  end

  def visit_transfer_withdraw(withdraw)
    self.should_implement
  end

  def visit_certificate_of_deposit(certificate_of_deposit)
    self.should_implement
  end

end