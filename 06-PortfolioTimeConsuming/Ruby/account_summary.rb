# encoding: utf-8

require './transaction_visitor'

class AccountSummary < TransactionVisitor
  def initialize(account)
    @account = account
  end

  def lines
    sleep(1)
    @lines = []
    @account.visit_transactions_with(self)
    return @lines
  end

  def visit_deposit(deposit)
    @lines << "Depósito por " + deposit.value.to_s
  end

  def visit_withdraw(withdraw)
    @lines << "Extracción por " + withdraw.value.to_s
  end

  def visit_transfer_deposit(deposit)
    @lines << "Transferencia por " + deposit.value.to_s
  end

  def visit_transfer_withdraw(withdraw)
    @lines << "Transferencia por " + (-withdraw.value).to_s
  end

  def visit_certificate_of_deposit(certificate_of_deposit)
    @lines << "Plazo fijo por " + certificate_of_deposit.value.to_s +
        " durante " + certificate_of_deposit.days.to_s +
        " días a una tna de " + certificate_of_deposit.tna.to_s
  end

end