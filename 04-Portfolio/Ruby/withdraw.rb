require './transaction'

class Withdraw < Transaction
  def initialize(value)
    @value = value
  end

  def value
    @value
  end
end