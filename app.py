from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for quizzes
# Structure: {'id': 0, 'question': '', 'options': [], 'correct': ''}
quizzes = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        new_quiz = {
            'id': len(quizzes),
            'question': request.form.get('question'),
            'options': [
                request.form.get('option1'),
                request.form.get('option2'),
                request.form.get('option3'),
                request.form.get('option4')
            ],
            'correct': request.form.get('correct')
        }
        quizzes.append(new_quiz)
        return redirect(url_for('list_quizzes'))
    return render_template('create.html')

@app.route('/quizzes')
def list_quizzes():
    return render_template('quizzes.html', quizzes=quizzes)

@app.route('/quiz', methods=['GET', 'POST'])
def take_quiz():
    if not quizzes:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        score = 0
        total = len(quizzes)
        
        # Check answers
        for quiz in quizzes:
            user_answer = request.form.get(f"q_{quiz['id']}")
            if user_answer == quiz['correct']:
                score += 1
        
        return render_template('result.html', score=score, total=total)
    
    return render_template('quiz_take.html', quizzes=quizzes)

if __name__ == '__main__':
    app.run(debug=True)