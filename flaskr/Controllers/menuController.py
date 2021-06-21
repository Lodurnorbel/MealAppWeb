from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

from flaskr.Controllers.authController import login_required
from flaskr.Models.Services import mealService

bp = Blueprint('config', __name__)


@bp.route('/')
def index():
    meals = mealService.getAllMeals()

    return render_template('config/index.html', meals=meals)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        error = mealService.checkValues(request.form['name'], request.form['price'])

        if error is not None:
            flash(error)
        else:
            mealService.create(request.form['name'], request.form['price'])
            return redirect(url_for('config.index'))

    return render_template('config/create.html')


@bp.route('/<mealId>/update', methods=('GET', 'POST'))
@login_required
def update(mealId):
    meal = mealService.get_meal(mealId)

    if request.method == 'POST':
        error = mealService.checkValues(request.form['name'], request.form['price'])

        if error is not None:
            flash(error)
        else:
            mealService.update(request.form['name'], request.form['price'], mealId)
            return redirect(url_for('config.index'))

    return render_template('config/update.html', meal=meal)


@bp.route('/<mealId>/delete', methods=('POST',))
@login_required
def delete(mealId):
    mealService.delete(mealId)

    return redirect(url_for('config.index'))


@bp.route('/<mealId>/updateMenu', methods=('GET',))
@login_required
def updateMenu(mealId):
    mealService.updateOnMenuById(mealId)

    return redirect(url_for('config.index'))
