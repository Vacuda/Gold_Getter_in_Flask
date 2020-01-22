from flask import Flask, render_template, request, redirect, session
import random, datetime

app = Flask(__name__)
app.secret_key="persist"

########################

def getRandom(min,max):
    amount=random.randint(min,max)
    return amount

actArr=[]

########################

@app.route('/', methods=['GET'])
def index():
    if 'gold' not in session:
        session['gold']=0
    if 'place' not in session:
        session['place']=""
    return render_template('index.html', 
        gold=session['gold'], 
        x=actArr,
        place=session['place'],
        timestamp=datetime.datetime.now()
    )

##RESET BUTTON
@app.route('/reset', methods=['POST'])
def reset():
    session['gold']=0
    global actArr
    actArr=[]
    return redirect('/')
    
##GET RANDOM, CHANGE GOLD, CHANGE PLACE
@app.route('/process', methods=['POST'])
def process():
    amount=getRandom(int(request.form['min']),int(request.form['max']))
    session['gold']=session['gold'] + amount
    session['place']=request.form['place']
    ##BUILD STRING
    now=datetime.datetime.now()
    timestamp=now.strftime("%m/%d/%Y, %I:%M:%S %p")
    if amount >= 0:
        new_activity="<p style='color:green;'>Earned " + str(amount) + " golds from the " + session['place'] + "! (" + timestamp + ")"
    else:
        new_activity="<p style='color:red;'>Entered a casino and lost " + str(abs(amount)) + " golds... OUCH... (" + timestamp + ")"
    ##ADD TO ARRAY
    global actArr
    actArr.append(new_activity)

    return redirect('/')

########################
if __name__=="__main__":
    app.run(debug=True)
########################
