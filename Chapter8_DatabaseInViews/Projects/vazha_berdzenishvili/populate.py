from app import db, StoreModel, UserModel

db.create_all()
# create
user1 = UserModel("vazha123", "qwerty123", "qwerty123", "vazha.berdzenishvili.1@iliauni.edu.ge")
db.session.add(user1)
db.session.commit()

product1 = StoreModel("mouse", 15.20, 12)
product2 = StoreModel("keyboard", 20, 3)
db.session.add_all([product1,product2])
db.session.commit()
# read

users = UserModel.query.all()

# update
userX = UserModel.query.filter_by(username='userX').first()

# delete
user_by_id = UserModel.query.get(1)  # ამოვიღეთ id-ით მეორე ობიექტი ბაზიდან
db.session.delete(user_by_id)  # წავშალე ობიექტი სესიიდან
db.session.commit()  # გადავიტანე სასეიაში შეტანილი ცვლილებები ბაზაში
