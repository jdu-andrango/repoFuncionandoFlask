from flask import Flask, request,jsonify,send_file
from psycopg2 import connect, extras
from cryptography.fernet import Fernet 
app = Flask(__name__)
key= Fernet.generate_key()

host='localhost'
port=5432
database='conexion'
user='postgres'
password='david'


def getConetion():
    conn=connect(host=host, port=port, database=database, user=user, password=password)
    return conn


#@app.get('/')
#def home():
#       conn = getConetion()
 #      cur  = conn.cursor()
 #      cur.execute("SELECT 1+1")
  #     result=cur.fetchone()
  #     print(result)
  #     
#   return 'hello word'

@app.get('/api/users')
def getUser():
    conn= getConetion()
    cur= conn.cursor(cursor_factory=extras.RealDictCursor)
    
    cur.execute('SELECT * FROM users')
    users= cur.fetchall()
    
    cur.close()
    conn.close()
    
    
    return jsonify(users)

@app.post('/api/users')
def createUser():
    newUser= request.get_json()
    
    user= newUser['username']
    email=newUser['email']
    password=Fernet(key).encrypt(bytes(newUser['password'],'utf-8'))
    
    conn= getConetion()
    cur= conn.cursor(cursor_factory=extras.RealDictCursor)
    
    cur.execute('INSERT INTO users (username, email, password) VALUES (%s,%s,%s)RETURNING *', (user,email,password))
    
    newCreatedUser=cur.fetchone()
    print(newCreatedUser)
    conn.commit()
    
    cur.close()
    conn.close()
    
    print(user,email,password)
    
    return jsonify(newCreatedUser)

@app.delete('/api/users/<id>')
def deleteUser(id):
    conn=getConetion()
    cur=conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute('DELETE FROM users WHERE id=%s RETURNING *',(id,))
    user=cur.fetchone()
    print(user)
    conn.close()
    cur.close()
    
    if user is None:
        return jsonify({'message':'user no fount'}),404
    
    
    return jsonify(user)

@app.put('/api/users/<id>')
def updateUser(id):
    conn=getConetion()
    cur=conn.cursor(cursor_factory=extras.RealDictCursor)
    newUser= request.get_json()
    username=newUser['username']
    email=newUser['email']
    password=Fernet(key).encrypt(bytes(newUser['password'],'utf-8'))
    cur.execute('UPDATE users SET username=%s,email=%s,password=%s WHERE id=%s RETURNING *',(username,email,password,id))
    
    updateUser= cur.fetchone()
    conn.commit()
    cur.close()
    conn.close
    if updateUser is None:
        return jsonify({'message':'user no fount'}),404
    
    return jsonify(updateUser)
@app.get('/api/users/<id>')
def getUsers(id):
    conn= getConetion()
    cur=conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute('SELECT * FROM users WHERE id=%s',(id,))
    user=cur.fetchone()
    
    if user is None:
        return jsonify({'message':'no found'}), 404
    
    return jsonify(user)


@app.get('/')
def home():
    return send_file('static/index.html')


if __name__=='__main__':
    app.run(debug=True)