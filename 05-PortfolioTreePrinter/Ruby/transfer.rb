require './transaction'
require './transference_Deposit'
require './transference_Withdraw'

class Transfer
  
  def self.register(amount,fromAccount,toAccount)
    
    deposit_leg = TransferenceDeposit.register_for_on(amount, toAccount, self) 
  	withdraw_leg = TransferenceWithdraw.register_for_on(amount, fromAccount, self) 
  	self.new(amount, deposit_leg, withdraw_leg )
  end

  def initialize(value, deposit_leg, withdraw_leg)
    @value = value
    @deposit_leg = deposit_leg
    @withdraw_leg = withdraw_leg
  end

  def value
    @value
  end

  def deposit_leg
    @deposit_leg
  end

  def withdraw_leg
    @withdraw_leg
  end

end

