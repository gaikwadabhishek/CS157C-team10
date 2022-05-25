from app import models
from random import choice
from app.final_new import get_tags

topc_counter = 2
topf_counter = 2
ffcounter = 1
form_id_counter = 1
q_id_counter = 1

PARAMS = [1,2,3,3,4,4,4,5,5]

first_names = []
last_names = []
fin_names = open('Names.csv','r').read().split('\n')
for name in fin_names:
	namel = name.split(',')
	#print(namel)
	first_names.append(namel[0])
	last_names.append(namel[1])

def gen_name():
	name = []
	name.append(choice(first_names))
	name.append(choice(last_names))
	#print(name)
	return ' '.join(name)


with open("FeedbackQuestions.txt", "r") as f:
	questions = f.readlines()
	# print(questions)

def gen_question_types():
	models.QuestionType(q_type_id = 1, title='Academics').save()
	models.QuestionType(q_type_id = 2, title='Infrastructure').save()
	models.QuestionType(q_type_id = 3, title='Faculty').save()

def gen_student(rollno):
	user = models.User.objects.create_user(username="student" + str(rollno), password='admin123')
	user.save()
	name =  gen_name()
	email = str(rollno)+'@college.com'
	phone_number = '9090909090'
	profile = models.Profile(name=name,email=email,phone_number=phone_number)
	profile.save()
	student = models.Student(student_id = rollno, user=user,profile=profile,)
	student.save()

def fill_feedback(student, questions, course_professors):
	acadq = questions["Academics"]
	for q in acadq:
		models.FeedbackResponse(id = ffcounter, student_id = student.student_id, question = q.question_id, answer = choice(PARAMS)).save()
		ffcounter += 1
	infraq = questions["Infrastructure"]
	for q in infraq:
		models.FeedbackResponse(id = ffcounter, student_id = student.student_id, question = q.question_id, answer = choice(PARAMS)).save()
		ffcounter += 1
	facultyq = questions["Faculty"]
	for course_professor in course_professors:
		for q in facultyq:
			models.FeedbackResponse(id = ffcounter, student_id = student.student_id, question = q.question_id, answer = choice(PARAMS), cp_id = course_professor.cp_id).save()
			ffcounter += 1
	print(student,'feedback generated')


gen_question_types()

forms = ["Feedback Form 1", "Feedback Form 2", "Feedback Form 3", "Feedback Form 4", "Feedback Form 5"]
print(forms)

for form in forms:
	print(form)

for i in range(5):
	title = str("Feedback Form " + str(i))
	print("creating", title)
	form = models.FeedbackForm(form_id = form_id_counter, title=title, is_active=True,is_published=True)
	form.save()
	form_id_counter += 1
	print('%s created' % title)
	for i in range(0, len(questions), 3):
		question = questions[i].strip()
		question_type = models.QuestionType.objects.get(title=questions[i+1].strip())
		tag = questions[i+2].strip()
		cur_tag = None
		try:
			cur_tag = models.Tag.objects.get(tag_title=tag)
		except:
			if cur_tag == None and tag != "None":
				cur_tag = models.Tag(tag_title=tag)
				cur_tag.save()
		models.Question(question_id = q_id_counter, text=question, type=question_type, tag=cur_tag, feedback_form=form).save()
		q_id_counter += 1
		# print('question created:', question, cur_tag)
	all_questions = models.Question.objects.filter(feedback_form=form.form_id)
	print("all questions", all_questions)
	question_dict = {}
	for a_q in all_questions:
		if not a_q.type.title in question_dict:
			question_dict[a_q.type.title] = []
		question_dict[a_q.type.title].append(a_q)
	print(question_dict)
	for student in models.Student.objects.all():
		fill_feedback(student, question_dict, models.CourseProfessor.objects.all())
		
print("done")