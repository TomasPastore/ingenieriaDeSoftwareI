require './account_summary_with_investment_earnings'

class AccountSummaryWithAllInvestmentInformation
  def initialize(account)
    @account = account
  end

  def lines
    investment_line = nil
    thread = Thread.new {
        investment_line = InvestmentNet.new(@account).value.to_s
    }
    lines = AccountSummaryWithInvestmentEarnings.new(@account).lines
    thread.join
    lines << "Inversiones por " + investment_line 
    return lines
  end

end