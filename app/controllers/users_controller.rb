class UsersController < ApplicationController

  # GET /signup
  def new
    @user = current_user
    if @user 
        redirect_to :experiment
    end
  end

  # POST /signup
  def create
    @user = User.new(user_params)
    @user.email = @user.email.downcase
    respond_to do |format|
      if @user.save
        @user.update(current_function: 1)
        format.html { log_in @user
          redirect_to :tutorial }
        format.json { render :show, status: :created, location: @user }
      else
        format.html { flash.now[:alert] =  @user.errors.full_messages.first if @user.errors.any?
          render :new }
        format.json { render json: @user.errors, status: :unprocessable_entity }
      end
    end
  end

  private 
    def user_params
      params.require(:user).permit(:email, :password, :password_confirmation, :group)
    end
end
