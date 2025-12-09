from eta import app, db
from flask_restful import Resource, Api, marshal_with, fields, abort, reqparse
from eta.models import Expense


api = Api(app)

#GETTING INPUT FROM SUER

user_Args= reqparse.RequestParser()

user_Args.add_argument("title", type = str, required = True, help = "Title cannot be Blank")
user_Args.add_argument("category", type = str, required = True, help = "Category cannot be Blank")
user_Args.add_argument("date", type = str, required = True, help = "Date cannot be Blank")
user_Args.add_argument("amount", type = float, required = True, help = "Amount cannot be Blank")



#TO SERIALIZE DATA
exp_fields= {"id": fields.Integer,
          "title": fields.String,
          "amount": fields.Integer,
          "category":fields.String,
           "date": fields.String
        }


#SHOW EXPENSE API
class ExpenseList(Resource):   
    @marshal_with(exp_fields)
    def get(self,user_id):
        expens = Expense.query.filter_by(user_id=user_id).all()
        return expens, 200

api.add_resource(ExpenseList,"/api/expenses/<int:user_id>")
  
# ADD EXPENSE API
class ExpenseAdd(Resource):
    @marshal_with(exp_fields)
    def post(self,user_id):
        args = user_Args.parse_args()
        u1 = Expense(
                     title = args["title"] ,
                     amount = args["amount"],
                     category=args["category"],
                     date = args["date"],
                     user_id = user_id)
        db.session.add(u1)
        db.session.commit()
        return u1, 201

  
api.add_resource(ExpenseAdd,"/api/a_expenses/<int:user_id>")

class ExpenseDelete(Resource):

    def delete(self, id):
        data =  Expense.query.get(id)
        if not data:
            abort(404, description ="That category's record is not available in database")
        db.session.delete(data)
        db.session.commit()
       
        return {"message": "Deleted successfully"}, 200
        

api.add_resource(ExpenseDelete,"/api/delete/<int:id>")


class MonthlySummary(Resource):   
    
    def get(self, month,user_id):
        tot = 0.0
        
        expenses = Expense.query.filter_by(user_id = user_id).all()
        for exp in expenses:
            if exp.date[5:7]==month:
                tot+=exp.amount
                
        return {"Month": month,"Total_Spent": tot}, 200
  

api.add_resource(MonthlySummary,"/api/monthly/<string:month>/<int:user_id>")
 #-------- 
