from models.entities.User import User

class ModelUser():

    @classmethod
    def LoggedUser(self,db,user):

        try:
            cursor=db.connect.cursor()
            QUERY_USER="""SELECT idUsers,UserName,Password
                    FROM users
                    WHERE UserName='{}'""".format(user.username)
            cursor.execute(QUERY_USER)
            answer=cursor.fetchone()
            if answer !=None:
                user=User(answer[0],answer[1],User.CheckPassword(answer[2],user.password))
                return user

            else:
                return None

        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_by_id(self,db,id):
        try:
            cursor=db.connect.cursor()
            QUERY_ID="""SELECT idUsers,UserName
                FROM users
                WHERE idUsers={}""".format(id)
            cursor.execute(QUERY_ID)
            answer=cursor.fetchone()
            if answer !=None:
                user=User(answer[0],answer[1],None)
                return user

            else:
                return None
        
        except Exception as ex:
            raise Exception(ex)
    