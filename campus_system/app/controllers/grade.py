from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from app import app, db
from app.models import Grade, Student, Course, OperationLog, Teacher
from app.views.grade_forms import GradeForm


#记录操作日志
def log_operation(user_id, operation_type, operation_content, operation_ip, operation_result):
    log = OperationLog(
        user_id=user_id,
        operation_type=operation_type,
        operation_content=operation_content,
        operation_ip=operation_ip,
        operation_result=operation_result
    )
    db.session.add(log)
    db.session.commit()


# 返回成绩列表页面。可以查看所有成绩，也可以根据课程或学生进行筛选。
# 教师只能查看他们自己教的课程的学生成绩，管理员可以查看所有成绩，学生只能查看他们自己的成绩。
@login_required
def index():
    # 获取所有班级
    classes = Class.query.all()
    
    # 获取选择的班级和学生
    selected_class_id = request.args.get('class_id', type=int)
    selected_student_id = request.args.get('student_id')
    
    if current_user.role == 'student':
        # 学生只能查看自己的成绩
        grades = Grade.query.filter_by(student_id=current_user.username).all()
        return render_template('grade/index.html', grades=grades, title='查看成绩')
    elif current_user.role == 'teacher':
        # 教师只能管理自己教授课程的学生成绩
        teacher = Teacher.query.filter_by(teacher_id=current_user.username).first()
        if teacher:
            # 获取教师教授的课程ID
            course_id = teacher.course_id
            # 只显示该课程的成绩
            query = Grade.query.filter_by(course_id=course_id)
            
            if selected_class_id:
                # 获取班级的所有学生
                class_ = Class.query.get(selected_class_id)
                if class_:
                    student_ids = [s.student_id for s in class_.students]
                    query = query.filter(Grade.student_id.in_(student_ids))
            
            if selected_student_id:
                query = query.filter_by(student_id=selected_student_id)
            
            grades = query.all()
        else:
            grades = []
        
        # 获取选中班级的学生
        selected_class_students = []
        if selected_class_id:
            class_ = Class.query.get(selected_class_id)
            if class_:
                selected_class_students = class_.students
        
        return render_template('grade/index.html', 
                               grades=grades, 
                               classes=classes, 
                               selected_class_id=selected_class_id, 
                               selected_student_id=selected_student_id, 
                               selected_class_students=selected_class_students, 
                               title='成绩管理')
    else:
        # 管理员可以查看所有成绩
        query = Grade.query
        
        if selected_class_id:
            # 获取班级的所有学生
            class_ = Class.query.get(selected_class_id)
            if class_:
                student_ids = [s.student_id for s in class_.students]
                query = query.filter(Grade.student_id.in_(student_ids))
        
        if selected_student_id:
            query = query.filter_by(student_id=selected_student_id)
        
        grades = query.all()
        
        # 获取选中班级的学生
        selected_class_students = []
        if selected_class_id:
            class_ = Class.query.get(selected_class_id)
            if class_:
                selected_class_students = class_.students
        
        return render_template('grade/index.html', 
                               grades=grades, 
                               classes=classes, 
                               selected_class_id=selected_class_id, 
                               selected_student_id=selected_student_id, 
                               selected_class_students=selected_class_students, 
                               title='成绩管理')


#返回添加新成绩的表单页面，并处理从该表单提交的数据。
# 教师只能为他们自己教的课程添加成绩，管理员可以为任何课程添加成绩。
# 如果表单数据验证通过，新的成绩将被添加到数据库中，并记录此操作。
@login_required
def add():
    form = GradeForm()
    
    if current_user.role == 'teacher':
        # 教师只能为自己教授的课程添加成绩
        teacher = Teacher.query.filter_by(teacher_id=current_user.username).first()
        if teacher:
            # 只显示教师教授的课程
            course = Course.query.get(teacher.course_id)
            if course:
                form.course_id.choices = [(course.id, f'{course.course_code} - {course.course_name}')]
                # 只显示选择该课程的学生
                from app.models import StudentCourse
                student_courses = StudentCourse.query.filter_by(course_id=course.id).all()
                student_ids = [sc.student_id for sc in student_courses]
                students = Student.query.filter(Student.student_id.in_(student_ids)).all()
                form.student_id.choices = [(s.student_id, f'{s.student_id} - {s.name}') for s in students]
            else:
                form.course_id.choices = []
                form.student_id.choices = []
        else:
            form.course_id.choices = []
            form.student_id.choices = []
    else:
        form.student_id.choices = [(s.student_id, f'{s.student_id} - {s.name}') for s in Student.query.all()]
        form.course_id.choices = [(c.id, f'{c.course_code} - {c.course_name}') for c in Course.query.all()]
    
    if form.validate_on_submit():
        # 检查是否已存在
        existing = Grade.query.filter_by(student_id=form.student_id.data, course_id=form.course_id.data).first()
        if existing:
            flash('该学生的该课程成绩已存在', 'danger')
            return redirect(url_for('grade.add'))
        
        # 计算总评成绩（平时成绩*0.4 + 期末成绩*0.6）
        total_score = form.daily_score.data * 0.4 + form.exam_score.data * 0.6
        
        grade = Grade(
            student_id=form.student_id.data,
            course_id=form.course_id.data,
            daily_score=form.daily_score.data,
            exam_score=form.exam_score.data,
            total_score=total_score,
            status='unlocked'
        )
        db.session.add(grade)
        db.session.commit()
        log_operation(current_user.id, 'add_grade', f'添加成绩: {form.student_id.data} - {Course.query.get(form.course_id.data).course_name}', request.remote_addr, 'success')
        flash('成绩添加成功', 'success')
        return redirect(url_for('grade.index'))
    return render_template('grade/add.html', form=form, title='添加成绩')


#返回更新特定成绩的表单页面，并处理从表单提交的数据。
# 如果表单数据验证通过，对应的成绩将被更新，并记录此操作。
@login_required
def update(id):
    grade = Grade.query.get_or_404(id)
    if grade.status == 'locked':
        flash('成绩已锁定，无法修改', 'danger')
        return redirect(url_for('grade.index'))
    
    form = GradeForm(obj=grade)
    form.student_id.choices = [(s.student_id, f'{s.student_id} - {s.name}') for s in Student.query.all()]
    form.course_id.choices = [(c.id, f'{c.course_code} - {c.course_name}') for c in Course.query.all()]
    if form.validate_on_submit():
        # 计算总评成绩
        total_score = form.daily_score.data * 0.4 + form.exam_score.data * 0.6
        
        grade.daily_score = form.daily_score.data
        grade.exam_score = form.exam_score.data
        grade.total_score = total_score
        db.session.commit()
        log_operation(current_user.id, 'update_grade', f'更新成绩: {grade.student_id} - {Course.query.get(grade.course_id).course_name}', request.remote_addr, 'success')
        flash('成绩更新成功', 'success')
        return redirect(url_for('grade.index'))
    return render_template('grade/update.html', form=form, grade=grade, title='更新成绩')

@login_required
def delete(id):
    grade = Grade.query.get_or_404(id)
    if grade.status == 'locked':
        flash('成绩已锁定，无法删除', 'danger')
        return redirect(url_for('grade.index'))
    
    db.session.delete(grade)
    db.session.commit()
    log_operation(current_user.id, 'delete_grade', f'删除成绩: {grade.student_id} - {Course.query.get(grade.course_id).course_name}', request.remote_addr, 'success')
    flash('成绩删除成功', 'success')
    return redirect(url_for('grade.index'))


#锁定特定的成绩，防止它被进一步修改，并记录此操作
@login_required
def lock(id):
    grade = Grade.query.get_or_404(id)
    grade.status = 'locked'
    db.session.commit()
    log_operation(current_user.id, 'lock_grade', f'锁定成绩: {grade.student_id} - {Course.query.get(grade.course_id).course_name}', request.remote_addr, 'success')
    flash('成绩已锁定', 'success')
    return redirect(url_for('grade.index'))


#解锁特定的成绩，允许它被进一步修改，并记录此操作
@login_required
def unlock(id):
    grade = Grade.query.get_or_404(id)
    grade.status = 'unlocked'
    db.session.commit()
    log_operation(current_user.id, 'unlock_grade', f'解锁成绩: {grade.student_id} - {Course.query.get(grade.course_id).course_name}', request.remote_addr, 'success')
    flash('成绩已解锁', 'success')
    return redirect(url_for('grade.index'))

from app.models import Grade, Student, Course, OperationLog, Class

import math



#返回成绩分析页面，显示成绩的统计信息，
#包括各个分数段的人数、平均分、最高分、最低分、及格率，优秀率，标准差等。
@login_required
def analysis():
    # 获取所有班级
    classes = Class.query.all()
    
    # 获取选择的班级和学生
    selected_class_id = request.args.get('class_id', type=int)
    selected_student_id = request.args.get('student_id')
    
    if current_user.role == 'student':
        # 学生只能查看自己的成绩分析
        grades = Grade.query.filter_by(student_id=current_user.username).all()
        selected_student_id = current_user.username
    else:
        # 教师可以按班级和学生筛选
        query = Grade.query
        
        if selected_class_id:
            class_ = Class.query.get(selected_class_id)
            if class_:
                student_ids = [s.student_id for s in class_.students]
                query = query.filter(Grade.student_id.in_(student_ids))
        
        if selected_student_id:
            query = query.filter_by(student_id=selected_student_id)
        
        grades = query.all()
    
    # 计算统计数据
    stats = {}
    grade_distribution = [0, 0, 0, 0, 0]  # 不及格, 及格, 中等, 良好, 优秀
    course_scores = {}
    all_scores = []
    
    if grades:
        total_score = sum(g.total_score for g in grades)
        average_score = total_score / len(grades)
        max_score = max(g.total_score for g in grades)
        min_score = min(g.total_score for g in grades)
        
        # 计算成绩分布
        for grade in grades:
            score = grade.total_score
            all_scores.append(score)
            if score < 60:
                grade_distribution[0] += 1
            elif score < 70:
                grade_distribution[1] += 1
            elif score < 80:
                grade_distribution[2] += 1
            elif score < 90:
                grade_distribution[3] += 1
            else:
                grade_distribution[4] += 1
            
            # 按课程统计
            course_name = grade.course.course_name
            if course_name not in course_scores:
                course_scores[course_name] = []
            course_scores[course_name].append(score)
        
        # 计算标准差
        variance = sum((x - average_score) ** 2 for x in all_scores) / len(all_scores)
        std_dev = math.sqrt(variance)
        
        # 计算及格率和优秀率
        total_count = len(grades)
        pass_count = sum(1 for x in all_scores if x >= 60)
        excellent_count = sum(1 for x in all_scores if x >= 90)
        
        stats = {
            'total_courses': len(grades),
            'average_score': average_score,
            'max_score': max_score,
            'min_score': min_score,
            'fail_count': grade_distribution[0],
            'pass_rate': (pass_count / total_count) * 100,
            'excellent_rate': (excellent_count / total_count) * 100,
            'std_dev': std_dev
        }
        
        # 计算课程平均成绩
        course_names = []
        course_avg_scores = []
        for course, scores in course_scores.items():
            course_names.append(course)
            course_avg_scores.append(sum(scores) / len(scores))
        
        # 计算成绩频率分布（每10分为一个区间）
        score_bins = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-100']
        score_counts = [0] * 10
        for score in all_scores:
            if score >= 100:
                score_counts[9] += 1
            else:
                index = int(score // 10)
                if index >= 10:
                    index = 9
                score_counts[index] += 1
    else:
        stats = {
            'total_courses': 0,
            'average_score': 0,
            'max_score': 0,
            'min_score': 0,
            'fail_count': 0,
            'pass_rate': 0,
            'excellent_rate': 0,
            'std_dev': 0
        }
        course_names = []
        course_avg_scores = []
        score_bins = []
        score_counts = []
    
    # 获取选中班级的学生
    selected_class_students = []
    if selected_class_id:
        class_ = Class.query.get(selected_class_id)
        if class_:
            selected_class_students = class_.students
    
    # 获取学生信息
    selected_student = None
    if selected_student_id:
        selected_student = Student.query.filter_by(student_id=selected_student_id).first()
    
    # 计算各班级各科目统计
    class_info_list = []
    for class_ in classes:
        class_grades = Grade.query.filter(Grade.student.has(class_id=class_.id)).all()
        if class_grades:
            course_stats = {}
            for grade in class_grades:
                course_name = grade.course.course_name
                if course_name not in course_stats:
                    course_stats[course_name] = {'count': 0, 'total': 0}
                course_stats[course_name]['count'] += 1
                course_stats[course_name]['total'] += grade.total_score
            
            class_info_list.append({
                'class_name': class_.class_name,
                'class_id': class_.id,
                'students': class_.students,
                'course_stats': course_stats
            })
    
    return render_template('grade/analysis.html', 
                           grades=grades, 
                           stats=stats,
                           grade_distribution=grade_distribution,
                           course_names=course_names,
                           course_avg_scores=course_avg_scores,
                           score_bins=score_bins,
                           score_counts=score_counts,
                           selected_class_id=selected_class_id,
                           selected_student_id=selected_student_id,
                           selected_student=selected_student,
                           class_info_list=class_info_list,
                           title='成绩分析')