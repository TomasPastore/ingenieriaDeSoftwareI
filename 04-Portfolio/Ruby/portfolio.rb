require './summarizing_account'

class Portfolio < SummarizingAccount

  def initialize
    @accounts = []
  end

  def self.create_with(account1,account2)
    a_portfolio = Portfolio.new
    raise self.ACCOUNT_ALREADY_MANAGED if account1.manages account2 or account2.manages account1
    a_portfolio.add_account account1
    a_portfolio.add_account account2
    a_portfolio
    #This could be refactored...
  end

  def balance
    @accounts.inject(0) { |sum, account| sum + account.balance }
  end

  def manages(account)
    self == account or @accounts.any? { |acc| acc.manages account }
  end

  def registers(transaction)
    @accounts.any? {|account| account.registers transaction}
  end

  def transactions
    @accounts.inject([]) {|union, other| union + other.transactions}
  end

  def self.ACCOUNT_ALREADY_MANAGED
    'Account already managed'
  end

  def add_account(account)
    @accounts.push account
  end
end