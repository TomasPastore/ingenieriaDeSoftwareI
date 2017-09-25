require './transaction'

class Deposit < Transaction

  def initialize(value)
    @value = value
  end

  def value
    @value
  end

end