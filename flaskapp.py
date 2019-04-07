from flask import Flask,render_template,request

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])

def method_post():
    bmi_cal = ''
    if request.method == 'POST' and 'weight' and 'height' in request.form:
        weight = float(request.form.get('weight'))
        height = float(request.form.get('height'))
        bmi_cal = 'BMI = {}'.format(bmi(weight,height))
    return render_template("bmi_calc.html",bmi_cal=bmi_cal)

def bmi(weight,height):
    final_bmi = round((weight/((height/100)**2)),2)
    if final_bmi >= 18.5 and final_bmi <= 24.9:
        final_print = '{} (Normal Weight)'.format(final_bmi)
        return final_print
    elif final_bmi >= 25 and final_bmi <= 29.9:
        final_print = '{} (Overweight)'.format(final_bmi)
        return final_print
    elif final_bmi > 29.9  :
        final_print = '{} (Obese)'.format(final_bmi)
        return final_print
    else:
        final_print = '{} (Under Weight)'.format(final_bmi)
        return final_print

if __name__ == '__main__':
    app.run()
