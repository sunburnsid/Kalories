from kalories import db
from kalories import Food, API

def initiate():
	db.create_all()

	pizza = Food('Pizza', 1,2,3,4,5,6,7,8,False, 45, 'slice')
	db.session.add(pizza)
	burger = Food('Burger', 1,2,3,4,5,6,7,8,False, 60, 'piece')
	db.session.add(burger)
	coke = Food('Coke', 1,2,4,5,6,7,8,9,False, 50, 'bottle')
	db.session.add(coke)
	honey = Food('Honeydew', 1,2,3,4,5,6,7,9,True, 20, 'slice')
	db.session.add(honey)

	br = API(120316, 0, 2, '/static/yyy.png')
	lunch = API(120316, 0, 1, '/static/yygg.png')
	din = API(120316, 0, 3, '/static/yuy.png')

	db.session.add(lunch)
	db.session.add(br)
	db.session.add(din)

	db.session.commit()

if __name__ == '__main__':
	initiate()
