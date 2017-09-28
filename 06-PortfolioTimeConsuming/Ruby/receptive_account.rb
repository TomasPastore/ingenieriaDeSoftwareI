require './summarizing_account'

class ReceptiveAccount < SummarizingAccount

  def initialize
    @transactions = []
  end

  def register(transaction)
    @transactions << transaction
  end

  def balance
    @transactions.inject(0) { |balance,transaction | transaction.affect_balance(balance) }
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

  def visit_transactions_with(transaction_visitor)
    @transactions.each {|transaction| transaction.accept(transaction_visitor)}
  end

  def accept(visitor)
    visitor.visit_receptive_account(self)
  end
end