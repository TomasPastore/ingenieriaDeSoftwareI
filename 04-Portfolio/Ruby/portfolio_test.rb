require 'minitest/autorun'
require 'minitest/reporters'
require './deposit'
require './withdraw'
require './receptive_account'
require './portfolio'

MiniTest::Reporters.use!

class PortfolioTest < Minitest::Test
  def test_01_balance_is_cero_when_receptive_account_is_created
    account = ReceptiveAccount.new
    assert_equal(0,account.balance)
  end

  def test_02_deposit_increases_balance_by_deposit_value
    account = ReceptiveAccount.new
    Deposit.register_for_on(100, account)

    assert_equal(100,account.balance)
  end

  def test_03WithdrawDecreasesBalanceOnTransactionValue
    account = ReceptiveAccount.new 
    Deposit.register_for_on(100, account)
    Withdraw.register_for_on(-50, account)

    assert_equal(50,account.balance)
  end

  def test_04PortfolioBalanceIsSumOfManagedAccountsBalance
    account1 = ReceptiveAccount.new 
    account2 = ReceptiveAccount.new 
    complexPortfolio = Portfolio.new
    complexPortfolio.add_account(account1)
    complexPortfolio.add_account(account2)

    Deposit.register_for_on(100, account1)
    Deposit.register_for_on(200, account2)

    assert_equal(300,complexPortfolio.balance)
  end

  def test_05PortfolioCanManagePortfolios
    account1 = ReceptiveAccount.new 
    account2 = ReceptiveAccount.new 
    account3 = ReceptiveAccount.new 
    complexPortfolio = Portfolio.create_with(account1,account2)
    composedPortfolio = Portfolio.create_with(complexPortfolio,account3)

    Deposit.register_for_on(100, account1)
    Deposit.register_for_on(200, account2)
    Deposit.register_for_on(300, account3)

    assert_equal(600,composedPortfolio.balance)
  end

  def test_06ReceptiveAccountsKnowsRegisteredTransactions
      account = ReceptiveAccount.new 
      deposit = Deposit.register_for_on(100, account)
      withdraw = Withdraw.register_for_on(-50, account)

      assert(account.registers(deposit))
      assert(account.registers(withdraw))
    end
    
  def test_07ReceptiveAccountsDoNotKnowNotRegisteredTransactions
    account = ReceptiveAccount.new 
    deposit = Deposit.new(100)
    withdraw = Withdraw.new(-50)

    assert(!account.registers(deposit))
    assert(!account.registers(withdraw))
  end
  
  def test_08PortofoliosKnowsTransactionsRegisteredByItsManagedAccounts
    account1 = ReceptiveAccount.new 
    account2 = ReceptiveAccount.new 
    account3 = ReceptiveAccount.new 
    complexPortfolio = Portfolio.create_with(account1,account2)
    composedPortfolio = Portfolio.create_with(complexPortfolio,account3)

    deposit1 = Deposit.register_for_on(100, account1)
    deposit2 = Deposit.register_for_on(200, account2)
    deposit3 = Deposit.register_for_on(300, account3)

    assert(composedPortfolio.registers(deposit1))
    assert(composedPortfolio.registers(deposit2))
    assert(composedPortfolio.registers(deposit3))
  end

  def test_09PortofoliosDoNotKnowTransactionsNotRegisteredByItsManagedAccounts
    account1 = ReceptiveAccount.new 
    account2 = ReceptiveAccount.new 
    account3 = ReceptiveAccount.new 
    complexPortfolio = Portfolio.create_with(account1,account2)
    composedPortfolio = Portfolio.create_with(complexPortfolio,account3)

    deposit1 = Deposit.new(100)
    deposit2 = Deposit.new(200)
    deposit3 = Deposit.new(300)

    assert(!composedPortfolio.registers(deposit1))
    assert(!composedPortfolio.registers(deposit2))
    assert(!composedPortfolio.registers(deposit3))
  end

  def test_10ReceptiveAccountManageItSelf
    account1 = ReceptiveAccount.new 

    assert(account1.manages(account1))
  end

  
  def test_11ReceptiveAccountDoNotManageOtherAccount
    account1 = ReceptiveAccount.new 
    account2 = ReceptiveAccount.new 

    assert(!account1.manages(account2))
  end

  def test_12PortfolioManagesComposedAccounts
    account1 = ReceptiveAccount.new 
    account2 = ReceptiveAccount.new 
    account3 = ReceptiveAccount.new 
    complexPortfolio = Portfolio.create_with(account1,account2)

    assert(complexPortfolio.manages(account1))
    assert(complexPortfolio.manages(account2))
    assert(!complexPortfolio.manages(account3))
  end

  def test_13PortfolioManagesComposedAccountsAndPortfolios
    account1 = ReceptiveAccount.new 
    account2 = ReceptiveAccount.new 
    account3 = ReceptiveAccount.new 
    complexPortfolio = Portfolio.create_with(account1,account2)
    composedPortfolio = Portfolio.create_with(complexPortfolio,account3)

    assert(composedPortfolio.manages(account1))
    assert(composedPortfolio.manages(account2))
    assert(composedPortfolio.manages(account3))
    assert(composedPortfolio.manages(complexPortfolio))
  end

  def test_14AccountsKnowsItsTransactions
    account1 = ReceptiveAccount.new 

    deposit1 = Deposit.register_for_on(100, account1)

    assert_equal(1,account1.transactions.size)
    assert(account1.transactions.include?(deposit1))
  end

  def test_15PortfolioKnowsItsAccountsTransactions
    account1 = ReceptiveAccount.new 
    account2 = ReceptiveAccount.new 
    account3 = ReceptiveAccount.new 
    complexPortfolio = Portfolio.create_with(account1,account2)
    composedPortfolio = Portfolio.create_with(complexPortfolio,account3)

    deposit1 = Deposit.register_for_on(100, account1)
    deposit2 = Deposit.register_for_on(200, account2)
    deposit3 = Deposit.register_for_on(300, account3)

    assert_equal(3,composedPortfolio.transactions.size)
    assert(composedPortfolio.transactions.include?(deposit1))
    assert(composedPortfolio.transactions.include?(deposit2))
    assert(composedPortfolio.transactions.include?(deposit3))
  end

  def test_16CanNotCreatePortfoliosWithRepeatedAccount
    account1 = ReceptiveAccount.new
    invalidPortfolio = assert_raises Exception do
      Portfolio.create_with(account1,account1)
    end
    assert_equal(Portfolio.ACCOUNT_ALREADY_MANAGED, invalidPortfolio.message)
  end
  
  def test_17CanNotCreatePortfoliosWithAccountsManagedByOtherManagedPortfolio
    account1 = ReceptiveAccount.new 
    account2 = ReceptiveAccount.new 
    complexPortfolio = Portfolio.create_with(account1,account2)
    invalidPortfolio = assert_raises Exception do
      Portfolio.create_with(complexPortfolio,account1)
    end
    assert_equal(Portfolio.ACCOUNT_ALREADY_MANAGED, invalidPortfolio.message)
  end
end