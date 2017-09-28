require './account_summary'
require './investment_earnings'

class AccountSummaryWithInvestmentEarnings

  def initialize(account)
    @account = account
  end

  def lines
    investment_lines = ''
    thread = Thread.new {
        investment_lines = InvestmentEarnings.new(@account).value.to_s
    }
    lines = AccountSummary.new(@account).lines
    thread.join
    lines << "Ganacias por " + investment_lines
    return lines
  end
end