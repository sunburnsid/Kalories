from kalories import db
from kalories import Food, API
import csv

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

def importCSV():
    db.create_all()
    with open('ABBREV.csv', 'rb') as csvfile:
        reader=csv.reader(csvfile)
        #x=0
        reader.next() #skip header
        for row in reader:
            #if (x<5):
                #print (row[1]+" "+ row[4]+" "+ row[7]+ row[5]+ row[10]+row[33]+row[31]+row[20]+row[43]+row[3]+row[49])
                #x+=1
            #Format: name, protein, carbs, fat, calcium, vitA, vitB, vitC, vitK, healthy, calories, unit
            #temp=Food(row[1], float(row[4]), float(row[7]), float(row[5]), float(row[10]),float(row[33]),float(row[31]),float(row[20]),float(row[43]),True,float(row[3]),row[49])
            temp=Food(row[1], row[4], row[7], row[5], row[10],row[33],row[31],row[20],row[43],True,row[3],row[49])
            db.session.add(temp)
            db.session.commit()

if __name__ == '__main__':
	#initiate()
        importCSV()
