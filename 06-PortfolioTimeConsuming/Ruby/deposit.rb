require './transaction'

class Deposit < Transaction

  def initialize(value)
    @value = value
  end

  def value
    @value
  end

  def affect_balance(balance)
    balance+@value
  end

  def accept(transaction_visitor)
    transaction_visitor.visit_deposit(self)
  end
end