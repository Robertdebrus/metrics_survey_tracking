class HomeController < ApplicationController
  before_action :set_user, only: [:experiment, :rate, :submit_rating, :compare, :submit_comparison]
  before_action :check_completed, only: [:experiment, :rate, :submit_rating, :compare, :submit_comparison]
  before_action :set_function, only: [:rate, :submit_rating, :compare, :submit_comparison]
  before_action :set_comment, only: [:rate, :submit_rating]
  before_action :set_comments, only: [:compare, :submit_comparison]

  def index
    if current_user
      redirect_to :experiment
    end
  end

  def tutorial
  end

  def experiment
    if @user.current_phase == "compare"
      redirect_to :compare
    else
      redirect_to :rate
    end
  end

  def rate
    if @user.current_phase == "compare"
      redirect_to :compare
    end
  end

  def demo
    
  end

  def compare
    if @user.current_phase != "compare"
      redirect_to :rate
    end
  end

  def submit_rating
    if !params[:accurate] or !params[:adequate] or !params[:concise]
      return redirect_to :rate, alert: "Please answer all questions."
    end 

    @rating = Rating.new do |t|
      t.user = @user
      t.comment = @comment
      t.accurate = params[:accurate]
      t.adequate = params[:adequate]
      t.concise = params[:concise]
    end

    #Save rating 
    if @rating.save
      @user.update(current_phase: "compare")
      return redirect_to :experiment
    else
      return redirect_to :rate, alert: 'Something went wrong!'
    end
  end

  def submit_comparison
    if !params[:similarity]
      return redirect_to :rate, alert: "Please indicate the comment similarity."
    end 

    @comparison = Comparison.new do |t|
      t.user = @user
      t.comment1 = @comment1
      t.comment2 = @comment2
      t.similarity = params[:similarity]
    end

    #Save rating 
    if @comparison.save
      @user.increment!(:current_function)
      @user.update(current_phase: "rate")
      return redirect_to :experiment
    else
      return redirect_to :compare, alert: 'Something went wrong!'
    end

  end

  def completed

  end

  private
    def set_user
      if !session[:user_id]
        redirect_to root_path
      else 
        @user = current_user
        if @user.nil?
          log_out
          redirect_to root_path
        end
      end
    end
  
    def check_completed
      if @user.current_function > Function.count
        redirect_to :completed
      end
    end

    def set_function
      @function = Function.find(translate_index(@user.current_function))
    end

    def set_comment
      case @user.group
      when 0
        if @function.id <= Function.count/2
          @comment=Comment.find_by(function:@function, source:"reference")
        else
          @comment=Comment.find_by(function:@function, source:"alex1")
        end
      when 1
        if @function.id <= Function.count/2
          @comment=Comment.find_by(function:@function, source:"alex1")
        else
          @comment=Comment.find_by(function:@function, source:"reference")
        end
      when 2
        if @function.id%2==0
          @comment=Comment.find_by(function:@function, source:"reference")
        else
          @comment=Comment.find_by(function:@function, source:"alex1")
        end
      when 3
        if @function.id%2==0
          @comment=Comment.find_by(function:@function, source:"alex1")
        else
          @comment=Comment.find_by(function:@function, source:"reference")
        end
      when 4
        if (@function.id <= Function.count/2 and @function.id%2==0) or (@function.id > Function.count/2 and @function.id%2==1) 
          @comment=Comment.find_by(function:@function, source:"reference")
        else
          @comment=Comment.find_by(function:@function, source:"alex1")
        end
      when 5
        if (@function.id <= Function.count/2 and @function.id%2==0) or (@function.id > Function.count/2 and @function.id%2==1) 
          @comment=Comment.find_by(function:@function, source:"alex1")
        else
          @comment=Comment.find_by(function:@function, source:"reference")
        end
      end
    end

    def set_comments
      case @user.group
      when 0
        if @function.id <= Function.count/2
          @comment1=Comment.find_by(function:@function, source:"reference")
          @comment2=Comment.find_by(function:@function, source:"alex1")
        else
          @comment1=Comment.find_by(function:@function, source:"alex1")
          @comment2=Comment.find_by(function:@function, source:"reference")
        end
      when 1
        if @function.id <= Function.count/2
          @comment1=Comment.find_by(function:@function, source:"alex1")
          @comment2=Comment.find_by(function:@function, source:"reference")
        else
          @comment1=Comment.find_by(function:@function, source:"reference")
          @comment2=Comment.find_by(function:@function, source:"alex1")
        end
      when 2
        if @function.id%2==0
          @comment1=Comment.find_by(function:@function, source:"reference")
          @comment2=Comment.find_by(function:@function, source:"alex1")
        else
          @comment1=Comment.find_by(function:@function, source:"alex1")
          @comment2=Comment.find_by(function:@function, source:"reference")
        end
      when 3
        if @function.id%2==0
          @comment1=Comment.find_by(function:@function, source:"alex1")
          @comment2=Comment.find_by(function:@function, source:"reference")
        else
          @comment1=Comment.find_by(function:@function, source:"reference")
          @comment2=Comment.find_by(function:@function, source:"alex1")
        end
      when 4
        if (@function.id <= Function.count/2 and @function.id%2==0) or (@function.id > Function.count/2 and @function.id%2==1) 
          @comment1=Comment.find_by(function:@function, source:"reference")
          @comment2=Comment.find_by(function:@function, source:"alex1")
        else
          @comment1=Comment.find_by(function:@function, source:"alex1")
          @comment2=Comment.find_by(function:@function, source:"reference")
        end
      when 5
        if (@function.id <= Function.count/2 and @function.id%2==0) or (@function.id > Function.count/2 and @function.id%2==1) 
          @comment1=Comment.find_by(function:@function, source:"alex1")
          @comment2=Comment.find_by(function:@function, source:"reference")
        else
          @comment1=Comment.find_by(function:@function, source:"reference")
          @comment2=Comment.find_by(function:@function, source:"alex1")
        end
      end
    end

    def user_params
      params.require(:user).permit(:email, :password, :password_confirmation)
    end
end
