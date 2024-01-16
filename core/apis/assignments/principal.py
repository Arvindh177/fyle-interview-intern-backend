from flask import Blueprint
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher;
from core import db
from .schema import AssignmentSchema, AssignmentGradeSchema, TeacherSchema, PrincipalAssignmentSchema

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_submitted_graded_assignments(p):
    """List all submitted and graded assignments"""
    submitted_graded_assignments = Assignment.get_submitted_graded_assignments()
    assignments_dump = AssignmentSchema().dump(submitted_graded_assignments, many=True)
    return APIResponse.respond(data=assignments_dump)


@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_all_teachers(p):
    """List all teachers"""
    teachers = Assignment.get_all_teachers()
    teachers_dump = TeacherSchema().dump(teachers, many=True)  # Replace YourTeacherSchema with your actual schema
    return APIResponse.respond(data=teachers_dump)

@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    assignments = Assignment.get_all_assignments_for_principal()  # Implement this method in your model
    assignments_dump = PrincipalAssignmentSchema().dump(assignments, many=True)
    return APIResponse.respond(data=assignments_dump)


@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_or_regrade_assignment(p, incoming_payload):
    """Grade or re-grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)


    graded_assignment = Assignment.grade_or_regrade_assignment(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
