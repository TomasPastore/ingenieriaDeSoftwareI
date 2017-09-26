require './object'

class SummarizingAccount
  def balance
    self.should_implement
  end

  def registers(transaction)
    self.should_implement
  end

  def manages(account)
    self.should_implement
  end

  def transactions
    self.should_implement
  end
end