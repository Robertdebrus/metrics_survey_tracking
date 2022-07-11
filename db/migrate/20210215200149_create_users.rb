class CreateUsers < ActiveRecord::Migration[5.1]
  def change
    create_table :users do |t|
      t.string :email
      t.string :password_digest
      t.integer :current_function
      t.string :current_phase
      t.integer :group

      t.timestamps
    end
  end
end
