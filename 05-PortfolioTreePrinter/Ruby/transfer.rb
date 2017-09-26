require './transaction'

class Transfer
  def self.register(amount,fromAccount,toAccount)
    self.should_implement
  end

  def deposit_leg
    self.should_implement
  end

  def withdraw_leg
    self.should_implement
  end

end

