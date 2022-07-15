# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from flask import Flask
from apps.home import blueprint
from flask import render_template, request, jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.home.forms import OrderForm
from apps.authentication.forms import LoginForm
order_queue = []

@blueprint.route('/')
def index():
    return render_template('home/index.html', segment='index')


@blueprint.route('/orderform', methods=['GET', 'POST'])
def orderform():
    app = Flask(__name__)
    bobaform = OrderForm()
    # print(request.values['shot1'])
    order = dict(ordername = bobaform.ordername.data,
        is_tapioca = bobaform.tapioca_pearls.data,
        is_shot1 = bobaform.shot1.data,
        is_shot2 = bobaform.shot2.data,
        syrup_level = bobaform.syrup.data)
    order_queue.append(order)

    # app.boba_machine.update(order_queue)



    return render_template('home/orderform.html', segment='index', form=bobaform)


# @blueprint.route('/<template>')
# def route_template(template):
#     try:
#         if not template.endswith('.html'):
#             template += '.html'

#         # Detect the current page
#         segment = get_segment(request)
#         # Serve the file (if exists) from app/templates/home/FILE.html
#         print("home/" + template)
#         return render_template("home/" + template, segment=segment)

#     except TemplateNotFound:
#         return render_template('home/page-404.html'), 404

#     # except:
#     #     return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):
    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
