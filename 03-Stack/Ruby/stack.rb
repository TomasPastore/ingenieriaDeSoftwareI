
class Stack

  @@stack_empty_error_description = "No element found"

  def initialize
    @stack = [EmptyNode.new(@@stack_empty_error_description)]
  end

  def push(an_object)
    @stack << (Node.new an_object)
  end

  def pop   
    @stack.last.call_with_value proc {
      |value|
      @stack.pop
      return value
    }
  end

  def top
    @stack.last.call_with_value proc {|value| return value}
  end

  def empty?
    @stack.size == 1
  end

  def size
    @stack.size - 1
  end

  def self.stack_empty_error_description
    @@stack_empty_error_description
  end

  def should_implement
    raise 'Should be implemented'
  end

  class Node
    def initialize(anObject)
      @value = anObject
    end

    def call_with_value(aProc)
      aProc.call @value
    end
  end

  class EmptyNode
    def initialize(error_message_to_raise)
      @error_message = error_message_to_raise
    end

    def call_with_value(aProc)
      raise @error_message
    end
  end

end