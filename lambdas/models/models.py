from flask_restx import Model, fields

# ----------------------------------------------------------------------------------------------------------------------
#                                    Announcements
# ----------------------------------------------------------------------------------------------------------------------
announcement_model = Model('AnnouncementModel', {
    'title': fields.String(required=True, example='My title'),
    'description': fields.String(required=False),
})

list_announcement_model = announcement_model.clone('ListAnnouncementModel', {
    'date': fields.DateTime(required=False)
})

# ----------------------------------------------------------------------------------------------------------------------
#                                    Auth
# ----------------------------------------------------------------------------------------------------------------------

auth_model =  Model('AuthModel', {
    'token': fields.String(required=True, example='abcdefg'),
})
