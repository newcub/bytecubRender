# from django.shortcuts import render, redirect, get_object_or_404
# from django.urls import reverse
# from .models import QuizQuestion,QuizAttempt
# from django.contrib.auth.decorators import login_required


# @login_required(login_url="login")
# def quiz_page(request):
#     question = QuizQuestion.objects.first()
#     if not question:
#         return render(request, 'multiple_choice/quiz.html', {'error': 'No questions available.'})

#     # Check if user has already answered this question
#     answered = QuizAttempt.objects.filter(user=request.user, question=question).exists()
#     if answered:
#         # Redirect to answer/result page or show message
#         return redirect(reverse('quiz_answer', kwargs={'question_id': question.id}))

#     options = {
#         'A': question.option_a,
#         'B': question.option_b,
#         'C': question.option_c,
#         'D': question.option_d,
#     }

#     return render(request, 'multiple_choice/quiz.html', {
#         'question_obj': question,
#         'question': question.question_text,
#         'options': options,
#     })

# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect, get_object_or_404
# from django.urls import reverse
# from .models import QuizQuestion, Profile

# @login_required(login_url="login")
# def quiz_answer(request, question_id=None):
#     # If question_id is None (like redirected from quiz_page), get it from GET or show message
#     if request.method == 'GET':
#         if not question_id:
#             return redirect(reverse('quiz_page'))
#         question = get_object_or_404(QuizQuestion, pk=question_id)
#         # Fetch user's previous attempt
#         attempt = QuizAttempt.objects.filter(user=request.user, question=question).first()
#         if not attempt:
#             # User hasn't answered yet, redirect to quiz page
#             return redirect(reverse('quiz_page'))
        
#         context = {
#             'question': question.question_text,
#             'user_answer_key': attempt.user_answer,
#             'user_answer_text': getattr(question, f"option_{attempt.user_answer.lower()}"),
#             'correct_answer_key': question.correct_option,
#             'correct_answer_text': getattr(question, f"option_{question.correct_option.lower()}"),
#             'is_correct': attempt.is_correct,
#             'explanation': question.explanation,
#             'user_points': request.user.profile.points,
#         }
#         return render(request, 'multiple_choice/answer.html', context)

#     # POST method - user submitting answer
#     if request.method == 'POST':
#         question_id = request.POST.get('question_id')
#         user_answer = request.POST.get('answer')

#         question = get_object_or_404(QuizQuestion, pk=question_id)
#         options = {
#             'A': question.option_a,
#             'B': question.option_b,
#             'C': question.option_c,
#             'D': question.option_d,
#         }

#         if user_answer not in options:
#             return redirect(reverse('quiz_page'))

#         # Check if user already answered this question
#         if QuizAttempt.objects.filter(user=request.user, question=question).exists():
#             # Prevent multiple attempts - redirect to answer page
#             return redirect(reverse('quiz_answer', kwargs={'question_id': question.id}))

#         is_correct = (user_answer == question.correct_option)

#         # Save attempt
#         QuizAttempt.objects.create(
#             user=request.user,
#             question=question,
#             user_answer=user_answer,
#             is_correct=is_correct,
#         )

#         # Update points if correct
#         if is_correct:
#             profile, created = Profile.objects.get_or_create(user=request.user)
#             profile.points += 10
#             profile.save()

#         context = {
#             'question': question.question_text,
#             'user_answer_key': user_answer,
#             'user_answer_text': options[user_answer],
#             'correct_answer_key': question.correct_option,
#             'correct_answer_text': options[question.correct_option],
#             'is_correct': is_correct,
#             'explanation': question.explanation,
#             'user_points': request.user.profile.points,
#         }
#         return render(request, 'multiple_choice/answer.html', context)

# from django.contrib.auth.models import User

# def get_leaderboard():
#     return User.objects.select_related('profile').order_by('-profile__points')

# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from django.db.models import Count

# @login_required(login_url="login")
# def profile_view(request):
#     user_profile = request.user.profile
#     user_points = user_profile.points

#     # Get all profiles sorted by points descending
#     leaderboard = user_profile.__class__.objects.select_related('user').order_by('-points')

#     # Calculate user rank (1-based)
#     # More efficient ways exist, but for simplicity:
#     rank = list(leaderboard).index(user_profile) + 1 if user_profile in leaderboard else None
#     total_users = leaderboard.count()

#     context = {
#         'user_points': user_points,
#         'user_rank': rank,
#         'total_users': total_users,
#         'leaderboard_top': leaderboard[:10],  # show top 10 users
#     }
#     return render(request, 'multiple_choice/profile.html', context)

# from django.shortcuts import render
# from django.views.decorators.http import require_http_methods
# from .models import CodeQuiz
# import re

# def code_quiz(request):
#     return render(request, 'multiple_choice/code_quiz.html' )

# @require_http_methods(["POST"])
# def code_quiz_answer(request):
#     user_code = request.POST.get('user_code', '').strip()
#     # For demo, fetch the correct answer from DB or hardcode
#     # Assuming you have a QuizQuestion model with a 'correct_code' field
#     # For example:
#     question = CodeQuiz.objects.first()
#     correct_code = question.correct_code.strip() if question and hasattr(question, 'correct_code') else ""

#     # Normalize inputs: split by whitespace and punctuation to get words
#     def tokenize(text):
#         # Split on any non-word character to get words
#         return [w for w in re.split(r'\W+', text) if w]

#     user_words = tokenize(user_code)
#     correct_words = tokenize(correct_code)

#     # Compare word by word and compute similarity ratio
#     matches = sum(1 for uw, cw in zip(user_words, correct_words) if uw == cw)
#     total = max(len(correct_words), 1)  # avoid division by zero

#     score = matches / total * 10  # score out of 10
#     score = round(score, 2)

#     context = {
#         'user_code': user_code,
#         'correct_code': correct_code,
#         'score': score,
#         'question_text': question.question if question else "Code Quiz",
#     }
    
#     return render(request, 'multiple_choice/code_quiz_answer.html', context)


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, QuizSubmission, Answer, LeaderboardEntry
from django.db.models import Sum, F
from django.db import transaction

def base_view(request):
    return render(request, 'base.html')

@login_required(login_url="login")
def quiz_page(request, quiz_name):
    quizzes = Quiz.objects.filter(quiz_name=quiz_name)
    if not quizzes:
        return HttpResponse("No quizzes with this name found.")
    return render(request, 'quizApp/quiz_page.html', {'quizzes': quizzes})

@login_required(login_url="login")
def submit_quiz(request, quiz_name):
    if request.method == 'POST':
        quizzes = Quiz.objects.filter(quiz_name=quiz_name)
        if not quizzes:
            return HttpResponse("No quizzes with this name found.")

        total_score = 0
        answers_data = []

        for quiz in quizzes:
            print(f" Quiz one is: {quiz}")
            
            # Check if user already submitted this quiz and delete it
            existing_submission = QuizSubmission.objects.filter(
                user=request.user, 
                quiz=quiz
            ).first()
            
            if existing_submission:
                # Delete the entire existing submission (including answers via cascade)
                existing_submission.delete()
            
            # Create new submission
            submission = QuizSubmission.objects.create(user=request.user, quiz=quiz)
            quiz_score = 0

            for question in quiz.questions.all():
                chosen_answer = request.POST.get(f'question_{question.id}')
                is_correct = (chosen_answer == question.correct_answer)

                Answer.objects.create(submission=submission, question=question, chosen_answer=chosen_answer)

                if is_correct:
                    quiz_score += 1

            submission.score = quiz_score
            submission.save()

            total_score += quiz_score

            answers_data.append({
                'quiz': quiz,
                'submission': submission,
                'answers': submission.answers.all(),
            })

        update_leaderboard(request.user, total_score)  # Call the leaderboard update function
        return redirect('quizApp:answer_page', quiz_name=quiz_name)
    else:
        return HttpResponse("Invalid request method.")

@login_required(login_url="login")
def answer_page(request, quiz_name):
    quizzes = Quiz.objects.filter(quiz_name=quiz_name)
    if not quizzes:
        return HttpResponse("No quizzes with this name found.")

    recent_submission = QuizSubmission.objects.filter(user=request.user, quiz__in=quizzes).latest('submission_time')

    answers_data = []
    for quiz in quizzes:
        print(f" Quiz two is: {quiz}")
        try:
            submission = QuizSubmission.objects.get(user=request.user, quiz=quiz)
            answers = submission.answers.all()
            answers_data.append({
                'quiz': quiz,
                'submission': submission,
                'answers': submission.answers.all(),
            })
        except QuizSubmission.DoesNotExist:
            answers_data.append({
                'quiz': quiz,
                'submission': None,
                'answers': None,
            })

    recent_score = recent_submission.score
    total_score = QuizSubmission.objects.filter(user=request.user).aggregate(Sum('score'))['score__sum'] or 0
    leaderboard = LeaderboardEntry.objects.order_by('-total_score')
    # rank = LeaderboardEntry.objects.filter(total_score__gt=LeaderboardEntry.objects.get(user=request.user).total_score).count() + 1
    # Get the current user's LeaderboardEntry
    current_entry = LeaderboardEntry.objects.get(user=request.user)

    # Calculate the rank by counting users in the same level with a higher score
    rank = LeaderboardEntry.objects.filter(
        ranking_score=current_entry.ranking_score,  # Same level
        total_score__gt=current_entry.total_score   # Higher score
    ).count() + 1

    return render(request, 'quizApp/answer_page.html', {
        'quiz':quiz,
        'answers_data': answers_data,
        'recent_score': recent_score,
        'total_score': total_score,
        'leaderboard': leaderboard,
        'rank': rank,
        'quiz_name': quiz_name,
    })

@transaction.atomic
def update_leaderboard(user, score):
    try:
        leaderboard_entry = LeaderboardEntry.objects.get(user=user)
        leaderboard_entry.total_score = F('total_score') + score
        leaderboard_entry.save()
    except LeaderboardEntry.DoesNotExist:
        LeaderboardEntry.objects.create(user=user, total_score=score)