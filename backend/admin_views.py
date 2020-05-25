from flask_admin.contrib.sqla import ModelView

class FlexModelView(ModelView):
    column_list = ('users', 'responses', 'testid')
    form_widget_args = {
        'users': { 'readonly': True },
        'responses': { 'readonly': True },
    }
