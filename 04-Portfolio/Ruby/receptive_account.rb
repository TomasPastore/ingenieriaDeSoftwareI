require './summarizing_account'

class ReceptiveAccount < SummarizingAccount

  def initialize
    @transactions = []
  end

  def register(transaction)
    @transactions << transaction
  end

  def balance
    @transactions.inject(0) { |balance,transaction | balance+transaction.value }
  end

  def registers(transaction)
    @transactions.include? (transaction)
  end

  def manages(account)
    self == account
  end

  def transactions
    @transactions.clone
  end

end