# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 2021_02_15_200727) do

  create_table "comments", force: :cascade do |t|
    t.string "text"
    t.string "source"
    t.integer "function_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["function_id"], name: "index_comments_on_function_id"
  end

  create_table "comparisons", force: :cascade do |t|
    t.integer "similarity"
    t.integer "comment1_id"
    t.integer "comment2_id"
    t.integer "user_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["comment1_id"], name: "index_comparisons_on_comment1_id"
    t.index ["comment2_id"], name: "index_comparisons_on_comment2_id"
    t.index ["user_id"], name: "index_comparisons_on_user_id"
  end

  create_table "functions", force: :cascade do |t|
    t.string "fid"
    t.string "name"
    t.string "file"
    t.string "text"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "ratings", force: :cascade do |t|
    t.integer "accurate"
    t.integer "adequate"
    t.integer "concise"
    t.integer "user_id"
    t.integer "comment_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["comment_id"], name: "index_ratings_on_comment_id"
    t.index ["user_id"], name: "index_ratings_on_user_id"
  end

  create_table "users", force: :cascade do |t|
    t.string "email"
    t.string "password_digest"
    t.integer "current_function"
    t.string "current_phase"
    t.integer "group"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  add_foreign_key "comparisons", "comments", column: "comment1_id"
  add_foreign_key "comparisons", "comments", column: "comment2_id"
end
