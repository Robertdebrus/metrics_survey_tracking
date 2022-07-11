Rails.application.routes.draw do
  root 'home#index'

  get '/', to: "home#index", as: :home
  get 'tutorial', to: "home#tutorial", as: :tutorial

  get    '/signup',   to: 'users#new', as: :signup
  post   '/signup',   to: 'users#create'

  get    '/login',   to: 'sessions#new', as: :login
  post   '/login',   to: 'sessions#create'
  delete '/logout',  to: 'sessions#destroy', as: :logout

  get '/experiment', to: "home#experiment", as: :experiment
  get '/rate', to: "home#rate", as: :rate
  post '/rate', to: "home#submit_rating", as: :submit_rating
  get '/compare', to: "home#compare", as: :compare
  post '/compare', to: "home#submit_comparison", as: :submit_comparison

  get '/completed', to: "home#completed", as: :completed
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
end
