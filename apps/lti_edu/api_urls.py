from django.conf.urls import url
from lti_edu.api import BadgeClassLtiContextListView, CurrentContextView, BadgeClassLtiContextDetailView, \
    BadgeClassLtiContextStudentListView
from lti_edu.api import StudentsEnrolledList, CheckIfStudentIsEnrolled, StudentEnrollmentList, StudentsEnrolledDetail

urlpatterns = [
    url(r'^enroll$', StudentsEnrolledList.as_view(), name='api_lti_edu_enroll_student'),
    url(r'^withdraw', StudentEnrollmentList.as_view(), name='api_lti_edu_withdraw_student'),
    url(r'^enrollment', StudentsEnrolledDetail.as_view(), name='api_lti_edu_update_enrollment'),
    url(r'^enrolledstudents/(?P<badgeclass_slug>[^/]+)$', StudentsEnrolledList.as_view(), name='api_lti_edu_enrolled_students'),
    url(r'^isstudentenrolled', CheckIfStudentIsEnrolled.as_view(), name='api_lti_is_student_enrolled'),
    url(r'^student/(?P<eduID>[^/]+)/enrollments', StudentEnrollmentList.as_view(), name='api_lti_edu_student_enrollment_list'),
    url(r'^badgeclasslticontext/(?P<lti_context_id>[^/]+)', BadgeClassLtiContextListView.as_view(), name='badgeclasslticontext_list'),
    url(r'^badgeclasslticontextstudent/(?P<lti_context_id>[^/]+)', BadgeClassLtiContextStudentListView.as_view(),
        name='badgeclasslticontextstudent_list'),
    url(r'^addbadgeclasslticontext', BadgeClassLtiContextDetailView.as_view(), name='badgeclasslticontext_add'),
    url(r'^lticontext', CurrentContextView.as_view(), name='lticontext'),
 ]


