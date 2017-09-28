class Query

    @@DEFAULT = 0

	def consult(account)
		self.should_implement_by_subclass
	end

 	def affect_query_with_deposit(deposit)
        self.DEFAULT
    end 

    def affect_query_with_withdraw(withdraw)
        self.DEFAULT
    end

    def affect_query_with_transference_withdraw(transference_withdraw)
        self.DEFAULT
    end

    def affect_query_with_transference_deposit(transference_deposit)
        self.DEFAULT
    end

    def affect_query_with_certificate_of_deposit(certificate_of_deposit)
        self.DEFAULT
    end

end