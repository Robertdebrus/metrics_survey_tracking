class FunctionsController < ApplicationController

  def index
    @functions = Function.all
  end

end
