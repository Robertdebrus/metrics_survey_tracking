module UsersHelper
  def current_user
    if session[:user_id]
      return User.find_by(id: session[:user_id])
    else
      return nil
    end
  end

  def translate_index(function_index)
    if function_index.to_i<1
      return 1
    end
    items = [*1..Function.count]
    items.shuffle!(random: Random.new(session[:user_id]))
    return items[function_index.to_i - 1]
  end
end
