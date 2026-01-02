from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='../templates')

# Temporary storage (Will reset when Vercel goes idle)
vote_records = []
CANDIDATES = ["Safwat", "Arpan", "Ashiya (Worst Friend)"]

def get_totals():
    totals = {name: 0 for name in CANDIDATES}
    for record in vote_records:
        if 'friend' in record and record['friend'] in totals:
            totals[record['friend']] += 1
    return totals

@app.route('/')
def index():
    totals = get_totals()
    winner = next((name for name, count in totals.items() if count >= 12), None)
    return render_template('index.html', candidates=CANDIDATES, winner=winner)

@app.route('/vote', methods=['POST'])
def vote():
    # Only allow voting if no one has won yet
    totals = get_totals()
    if any(count >= 12 for count in totals.values()):
        return redirect(url_for('results'))

    new_vote = {
        "voter": request.form.get('name', '').strip(),
        "friend": request.form.get('friend', '').strip(),
        "gender": request.form.get('gender', '').strip(),
        "roll": request.form.get('roll', '').strip()
    }
    
    # Validate all required fields and that friend is a valid candidate
    if (new_vote["voter"] and 
        new_vote["friend"] and 
        new_vote["friend"] in CANDIDATES and
        new_vote["gender"] and 
        new_vote["roll"]):
        vote_records.append(new_vote)
        
    return redirect(url_for('results'))

@app.route('/results')
def results():
    totals = get_totals()
    return render_template('results.html', totals=totals, records=vote_records)

if __name__ == "__main__":
    app.run(debug=True)