from flask import render_template, Blueprint, redirect, request, current_app, url_for, flash
from jobplus.decorators import admin_required
from jobplus.models import User, db, Job
from jobplus.forms import CompanyForm, UserForm, CompanyProfileForm, UserProfileForm

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')

@admin.route('/users')
@admin_required
def users():
    page = request.args.get('page', default=1, type=int)
    pagination = User.query.paginate(
            page=page,
            per_page=current_app.config['ADMIN_PER_PAGE'],
            error_out=False
            )
    return render_template('admin/users.html', pagination=pagination)

@admin.route('/users/adduser', methods=['GET','POST'])
@admin_required
def adduser():
    form = UserForm()
    if form.validate_on_submit():
        form.create_user()
        flash('求职者创建成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/adduser.html', form=form)

@admin.route('/users/addcompany', methods=['GET', 'POST'])
@admin_required
def addcompany():
    form = CompanyForm()
    if form.validate_on_submit():
        form.create_company()
        flash('企业创建成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/addcompany.html', form=form)

@admin.route('/users/<int:user_id>/edituser', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_company:
        form = CompanyProfileForm(obj=user)
    else:
        form = UserProfileForm(obj=user)
    if form.validate_on_submit():
        form.updated_profile(user)
        flash('更新成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/edit_user.html', form=form, user=user)

@admin.route('/users/<int:user_id>/disableuser', methods=['GET', 'POST'])
@admin_required
def disable_user(user_id):
    user = User.query.get_or_404(user_id)
    if not user.is_disable:
        user.is_disable = True
        flash('已经禁用成功', 'success')
    else:
        user.is_disable = False
        flash('已经启用成功', 'success')
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('admin.users'))

@admin.route('/users/<int:user_id>/deleteuser', methods=['GET', 'POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('已经删除成功', 'success')
    return redirect(url_for('admin.users'))
