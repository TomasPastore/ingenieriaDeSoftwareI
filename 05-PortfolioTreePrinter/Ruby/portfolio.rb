require './summarizing_account'

class Portfolio < SummarizingAccount

  def self.create_with(account1,account2)
    portfolio = self.new
    portfolio.add_account(account1)
    portfolio.add_account(account2)
    portfolio
  end

  def self.ACCOUNT_ALREADY_MANAGED
    'Account already managed'
  end

  def initialize
    @accounts = []
  end

  def add_account(account)
    raise self.class.ACCOUNT_ALREADY_MANAGED if 
    	self.manages(account) or 
    	@accounts.any? {|accountInside| account.manages accountInside}
    @accounts << account
  end

  def balance
    @accounts.inject(0) { |balance,account | balance + account.balance }
  end

  def registers(transaction)
    @accounts.any? { |account| account.registers(transaction) }
  end

  def manages(account)
    self == account or @accounts.any? {|component_account | component_account.manages(account)}
  end

  def transactions
    @accounts.inject([]) { |transactions,account |
      transactions.concat(account.transactions)
      transactions
    }
  end

end