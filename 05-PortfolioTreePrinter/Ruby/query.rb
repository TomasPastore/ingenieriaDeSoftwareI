class Query

    @@DEFAULT = 0

	def consult
		self.should_implement
	end

 	def affect_query_with_deposit(deposit)
        @@DEFAULT
    end 

    def affect_query_with_withdraw(withdraw)
        @@DEFAULT
    end

    def affect_query_with_transference_withdraw(transference_withdraw)
        @@DEFAULT
    end

    def affect_query_with_transference_deposit(transference_deposit)
        @@DEFAULT
    end

    def affect_query_with_certificate_of_deposit(certificate_of_deposit)
        @@DEFAULT
    end

end