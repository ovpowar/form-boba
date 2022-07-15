# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from flask import Flask
from flask import render_template, request, jsonify, redirect
from .forms import OrderForm
from . import app

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home/index.html', segment='index')


@app.route('/orderform', methods=['GET', 'POST'])
def orderform():
    bobaform = OrderForm()
    # print(request.values['shot1'])
    bobaform.shot1.label.text = app.boba_machine.flavors['shot1']
    bobaform.shot2.label.text = app.boba_machine.flavors['shot2']
    if bobaform.validate_on_submit():
        order = dict(queue_number = len(app.boba_machine.order_queue.q)+1,
            ordername = bobaform.ordername.data,
            is_tapioca = bobaform.tapioca_pearls.data,
            is_shot1 = bobaform.shot1.data,
            is_shot2 = bobaform.shot2.data,
            syrup_level = bobaform.syrup.data,
            status = "Queued")

        app.boba_machine.order_queue.update(order)

    return render_template('home/orderform.html', segment='index', form=bobaform)

@app.route('/orderlist', methods=['GET', 'POST'])
def orderlist():
    if request.form.get('Start'):
        print("STARTING")
    elif request.form.get('Delete'):
        print("Deleting")
    return render_template('home/orderqueue.html', segment='index', orderlist=app.boba_machine.order_queue.q, flavors=app.boba_machine.flavors)

@app.route('/delete_order', methods=['GET', 'POST'])
def delete_order():
    if request.method == "POST":
        app.boba_machine.order_queue.remove_order_number(int(request.form["delete"]))
        app.boba_machine.order_queue.update_sequence()
    return redirect('/orderlist')
    # return render_template('home/orderqueue.html', segment='index', orderlist=app.boba_machine.order_queue.q, flavors=app.boba_machine.flavors)

@app.route('/start_order', methods=['GET', 'POST'])
def start_order():
    if request.method == "POST":
        status = app.boba_machine.check_order(int(request.form["start"]))
        if status == "Ready":
            app.boba_machine.start_preparing_order(int(request.form["start"])-1)
    return redirect('/orderlist')
    # return render_template('home/orderqueue.html', segment='index', orderlist=app.boba_machine.order_queue.q, flavors=app.boba_machine.flavors)
