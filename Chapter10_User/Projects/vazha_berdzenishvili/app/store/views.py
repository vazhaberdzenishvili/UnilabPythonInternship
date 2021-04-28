from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import db
from app.models.store import StoreModel
from app import pages
from flask_user import current_user

store_blueprint = Blueprint('StoreModel',
                            __name__,
                            template_folder='templates/store'
                            )


@store_blueprint.route('/store', methods=['GET', 'POST'])
def store():
    if current_user.is_authenticated:
        data = StoreModel.query.all()
        return render_template('store.html', pages=pages, items=data)
    return redirect(url_for('UserModel.login'))


@store_blueprint.route('/add', methods=['GET', 'POST'])
def Store_add():
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']
    item = StoreModel(name, price, quantity)
    if StoreModel.find_by_name(name) is None:
        item.add_item()
        flash(f" ნივთი {name} წარმატებით დაემატა ბაზაში")
        return redirect(url_for('StoreModel.store'))
    else:
        flash(F"პროდუქტი {name} დასახელებით უკვე არსებობს ")
        return redirect(url_for('StoreModel.store'))


@store_blueprint.route('/delete/<id>/', methods=['GET', 'POST'])
def store_delete(id):
    item = StoreModel.query.get(id)
    item.delete_item()
    flash("პროდუქტი  წარმატებით წაიშალა ბაზიდან")

    return redirect(url_for('StoreModel.store'))


@store_blueprint.route('/update', methods=['GET', 'POST'])
def store_edit():
    if request.method == 'POST':
        item_data = StoreModel.query.get(request.form.get('id'))
        item_data.name = request.form['name']
        item_data.price = request.form['price']
        item_data.quantity = request.form['quantity']
        db.session.commit()
        flash(f"პროდუქტი  {item_data.name}  წარმატებით განახლდა ")
        return redirect(url_for('StoreModel.store'))
