require './transaction'

class Deposit < Transaction

  def initialize(value)
    @value = value
  end

  def value
    @value
  end

  def affect_balance(balance)
  	balance + @value
  end

  def affect_transferNet(trasnfer_net)
  	trasnfer_net + 0
  end	

  def description
  	"Depósito por #{@value}"
  end

end

