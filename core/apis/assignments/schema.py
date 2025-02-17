from marshmallow import Schema, EXCLUDE, fields, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_enum import EnumField
from core.models.assignments import Assignment, GradeEnum
from core.models.users import User
from core.libs.helpers import GeneralObject
from core.models.teachers import Teacher


class AssignmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Assignment
        unknown = EXCLUDE

    id = auto_field(required=False, allow_none=True)
    content = auto_field()
    created_at = auto_field(dump_only=True)
    updated_at = auto_field(dump_only=True)
    teacher_id = auto_field(dump_only=True)
    student_id = auto_field(dump_only=True)
    grade = auto_field(dump_only=True)
    state = auto_field(dump_only=True)

    @post_load
    def initiate_class(self, data_dict, many, partial):
        # pylint: disable=unused-argument,no-self-use
        return Assignment(**data_dict)


class AssignmentSubmitSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(required=True, allow_none=False)
    teacher_id = fields.Integer(required=True, allow_none=False)

    @post_load
    def initiate_class(self, data_dict, many, partial):
        # pylint: disable=unused-argument,no-self-use
        return GeneralObject(**data_dict)


class AssignmentGradeSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(required=True, allow_none=False)
    grade = EnumField(GradeEnum, required=True, allow_none=False)

    @post_load
    def initiate_class(self, data_dict, many, partial):
        # pylint: disable=unused-argument,no-self-use
        return GeneralObject(**data_dict)
    
class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True
    
    id = auto_field()


class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        include_relationships = True
        load_instance = True

    id = auto_field()
    created_at = auto_field()
    updated_at = auto_field()
    user_id = auto_field(attribue='user.id', nested=UserSchema())



class PrincipalAssignmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Assignment
        load_instance = True

    teacher_id = auto_field()
    student_id = auto_field()
    content = auto_field()

