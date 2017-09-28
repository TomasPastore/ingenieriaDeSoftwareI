# encoding: utf-8

require 'minitest/autorun'
require 'minitest/reporters'
require 'benchmark'
require './deposit'
require './withdraw'
require './transfer'
require './certificate_of_deposit'
require './receptive_account'
require './portfolio'
require './account_summary'
require './transfer_net'
require './investment_net'
require './investment_earnings'
require './portfolio_tree_printer'
require './reverse_portfolio_tree_printer'
require './account_summary_with_investment_earnings'
require './account_summary_with_all_investment_information'

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
    Withdraw.register_for_on(50, account)

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

  def test_18aTransferShouldRegistersATransferDepositOnToAccount
    fromAccount = ReceptiveAccount.new
    toAccount = ReceptiveAccount.new

    transfer = Transfer.register(100,fromAccount, toAccount)

    assert(toAccount.registers(transfer.deposit_leg))
  end

  def test_18bTransferShouldRegistersATransferWithdrawOnFromAccount
    fromAccount = ReceptiveAccount.new
    toAccount = ReceptiveAccount.new

    transfer = Transfer.register(100,fromAccount, toAccount)

    assert(fromAccount.registers(transfer.withdraw_leg))
  end

  def test_18cTransferLegsKnowTransfer
    fromAccount = ReceptiveAccount.new
    toAccount = ReceptiveAccount.new

    transfer = Transfer.register(100,fromAccount, toAccount)

    assert_equal(transfer.deposit_leg.transfer,transfer.withdraw_leg.transfer)
  end

  def test_18dTransferKnowsItsValue
    fromAccount = ReceptiveAccount.new
    toAccount = ReceptiveAccount.new

    transfer = Transfer.register(100,fromAccount, toAccount)

    assert_equal(100,transfer.value)
  end

  def test_18eTransferShouldWithdrawFromFromAccountAndDepositIntoToAccount
    fromAccount = ReceptiveAccount.new
    toAccount = ReceptiveAccount.new

    Transfer.register(100,fromAccount, toAccount)

    assert_equal(-100, fromAccount.balance)
    assert_equal(100, toAccount.balance)
  end

  def test_19AccountSummaryShouldProvideHumanReadableTransactionsDetail
    fromAccount = ReceptiveAccount.new
    toAccount = ReceptiveAccount.new

    Deposit.register_for_on(100,fromAccount)
    Withdraw.register_for_on(50,fromAccount)
    Transfer.register(100,fromAccount, toAccount)

    lines = self.accountSummaryLines(fromAccount)

    assert_equal(3,lines.size)
    assert_equal("Depósito por 100", lines[0])
    assert_equal("Extracción por 50", lines[1])
    assert_equal("Transferencia por -100", lines[2])
  end

  def accountSummaryLines(fromAccount)
    summary = AccountSummary.new(fromAccount)
    summary.lines
  end

  def test_20ShouldBeAbleToBeQueryTransferNet
    fromAccount = ReceptiveAccount.new
    toAccount = ReceptiveAccount.new

    Deposit.register_for_on(100,fromAccount)
    Withdraw.register_for_on(50,fromAccount)
    Transfer.register(100,fromAccount, toAccount)
    Transfer.register(250,toAccount, fromAccount)

    assert_equal(150,accountTransferNet(fromAccount))
    assert_equal(-150,accountTransferNet(toAccount))
  end

  def accountTransferNet(account)
    accountTransferNet = TransferNet.new(account)
    accountTransferNet.value
  end

  def test_21CertificateOfDepositShouldWithdrawInvestmentValue
    account = ReceptiveAccount.new
    toAccount = ReceptiveAccount.new

    Deposit.register_for_on(1000,account)
    Withdraw.register_for_on(50,account)
    Transfer.register(100,account, toAccount)
    CertificateOfDeposit.register_for_on(100,30,0.1,account)

    assert_equal(100,investmentNet(account))
    assert_equal(750,account.balance)
  end

  def investmentNet(account)
    accountInvestmentNet = InvestmentNet.new(account)
    accountInvestmentNet.value
  end

  def test_22ShouldBeAbleToQueryInvestmentEarnings
    account = ReceptiveAccount.new

    CertificateOfDeposit.register_for_on(100,30,0.1,account)
    CertificateOfDeposit.register_for_on(100,60,0.15,account)

    investmentEarnings = 100.0*(0.1/360)*30 + 100.0*(0.15/360)*60

    assert_equal(investmentEarnings,self.investmentEarnings(account))
  end

  def investmentEarnings(account)
    accountInvestmentEarnings = InvestmentEarnings.new(account)
    accountInvestmentEarnings.value
  end

  def test_23AccountSummaryShouldWorkWithCertificateOfDeposit
    fromAccount = ReceptiveAccount.new
    toAccount = ReceptiveAccount.new

    Deposit.register_for_on(100,fromAccount)
    Withdraw.register_for_on(50,fromAccount)
    Transfer.register(100,fromAccount, toAccount)
    CertificateOfDeposit.register_for_on(1000, 30, 0.1, fromAccount)

    lines = self.accountSummaryLines(fromAccount)

    assert_equal(4,lines.size)
    assert_equal("Depósito por 100", lines[0])
    assert_equal("Extracción por 50", lines[1])
    assert_equal("Transferencia por -100", lines[2])
    assert_equal("Plazo fijo por 1000 durante 30 días a una tna de 0.1", lines[3])
  end

  def test_24ShouldBeAbleToBeQueryTransferNetWithCertificateOfDeposit
    fromAccount = ReceptiveAccount.new
    toAccount = ReceptiveAccount.new

    Deposit.register_for_on(100,fromAccount)
    Withdraw.register_for_on(50,fromAccount)
    Transfer.register(100,fromAccount, toAccount)
    Transfer.register(250,toAccount, fromAccount)
    CertificateOfDeposit.register_for_on(1000, 30, 0.1, fromAccount)

    assert_equal(150,self.accountTransferNet(fromAccount))
    assert_equal(-150,self.accountTransferNet(toAccount))
  end

  def test_25PortfolioTreePrinter
    account1 = ReceptiveAccount.new
    account2 = ReceptiveAccount.new
    account3 = ReceptiveAccount.new
    complexPortfolio = Portfolio.create_with(account1,account2)
    composedPortfolio = Portfolio.create_with(complexPortfolio,account3)

    accountNames = {}
    accountNames[composedPortfolio] = "composedPortfolio"
    accountNames[complexPortfolio] = "complexPortfolio"
    accountNames[account1] = "account1"
    accountNames[account2] = "account2"
    accountNames[account3] = "account3"

    lines = self.portfolio_tree_of(composedPortfolio,accountNames)

    assert_equal(5, lines.size)
    assert_equal("composedPortfolio", lines[0])
    assert_equal(" complexPortfolio", lines[1])
    assert_equal("  account1", lines[2])
    assert_equal("  account2", lines[3])
    assert_equal(" account3", lines[4])
  end

  def portfolio_tree_of(portfolio,accountNames)
    printer = PortfolioTreePrinter.new(portfolio,accountNames)
    return printer.lines
  end

  def test_26ReversePortfolioTreePrinter
    account1 = ReceptiveAccount.new
    account2 = ReceptiveAccount.new
    account3 = ReceptiveAccount.new
    complexPortfolio = Portfolio.create_with(account1,account2)
    composedPortfolio = Portfolio.create_with(complexPortfolio,account3)

    accountNames = {}
    accountNames[composedPortfolio] = "composedPortfolio"
    accountNames[complexPortfolio] = "complexPortfolio"
    accountNames[account1] = "account1"
    accountNames[account2] = "account2"
    accountNames[account3] = "account3"

    lines = self.reverse_portfolio_tree_of(composedPortfolio, accountNames)

    assert_equal(5, lines.size)
    assert_equal(" account3", lines[0])
    assert_equal("  account2", lines[1])
    assert_equal("  account1", lines[2])
    assert_equal(" complexPortfolio", lines[3])
    assert_equal("composedPortfolio", lines[4])

  end

  def reverse_portfolio_tree_of(portfolio,accountNames)
    printer = ReversePortfolioTreePrinter.new(portfolio,accountNames)
    return printer.lines
  end

  def test_27AccountSummaryWithInvestmentEarningsShouldNotTakeTooLong
    fromAccount = ReceptiveAccount.new
    toAccount = ReceptiveAccount.new

    Deposit.register_for_on(100,fromAccount)
    Withdraw.register_for_on(50,fromAccount)
    Transfer.register(100,fromAccount, toAccount)
    CertificateOfDeposit.register_for_on(1000, 360, 0.1, fromAccount)

    lines = []
    elapsed_time = Benchmark.realtime {
      lines = AccountSummaryWithInvestmentEarnings.new(fromAccount).lines }

    assert(elapsed_time<1.5)

    assert_equal(lines.size,5)
    assert_equal("Depósito por 100", lines[0])
    assert_equal("Extracción por 50", lines[1])
    assert_equal("Transferencia por -100", lines[2])
    assert_equal("Plazo fijo por 1000 durante 360 días a una tna de 0.1", lines[3])
    assert_equal("Ganacias por 100.0", lines[4])

  end

  def test_28AccountSummaryWithInvestmentFullInfoShouldNotTakeTooLong
    fromAccount = ReceptiveAccount.new
    toAccount = ReceptiveAccount.new

    Deposit.register_for_on(100,fromAccount)
    Withdraw.register_for_on(50,fromAccount)
    Transfer.register(100,fromAccount, toAccount)
    CertificateOfDeposit.register_for_on(1000, 360, 0.1, fromAccount)

    lines = []
    elapsed_time = Benchmark.realtime {
      lines = AccountSummaryWithAllInvestmentInformation.new(fromAccount).lines }

    assert(elapsed_time<1.5)

    assert_equal(lines.size,6)
    assert_equal("Depósito por 100", lines[0])
    assert_equal("Extracción por 50", lines[1])
    assert_equal("Transferencia por -100", lines[2])
    assert_equal("Plazo fijo por 1000 durante 360 días a una tna de 0.1", lines[3])
    assert_equal("Ganacias por 100.0", lines[4])
    assert_equal("Inversiones por 1000", lines[5])
  end

end