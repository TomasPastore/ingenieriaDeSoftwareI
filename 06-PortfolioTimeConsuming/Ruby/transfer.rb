require './transaction'

class Transfer
  def self.register(amount,fromAccount,toAccount)
    transfer = Transfer.new(amount,fromAccount,toAccount)
    fromAccount.register(transfer.withdraw_leg)
    toAccount.register(transfer.deposit_leg)
    return transfer
  end

  def initialize(amount,fromAccount,toAccount)
    @amount = amount
    @fromAccount = fromAccount
    @toAccount = toAccount
    @depositLeg = TransferDepositLeg.new(self)
    @withdrawLeg = TransferWithdrawLeg.new(self)
  end

  def deposit_leg
    @depositLeg
  end

  def withdraw_leg
    @withdrawLeg
  end

  def value
    @amount
  end
end

class TransferLeg < Transaction
  def initialize(transfer)
    @transfer = transfer
  end

  def transfer
    @transfer
  end

  def value
    @transfer.value
  end
end

class TransferDepositLeg < TransferLeg
  def affect_balance(balance)
    balance+self.value
  end

  def accept(transaction_visitor)
    transaction_visitor.visit_transfer_deposit(self)
  end
end

class TransferWithdrawLeg < TransferLeg
  def affect_balance(balance)
    balance-self.value
  end

  def accept(transaction_visitor)
    transaction_visitor.visit_transfer_withdraw(self)
  end
end