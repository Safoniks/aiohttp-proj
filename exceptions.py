__all__ = (
    'AcceptOwnMeeting',
    'AlreadyHasTripOnThisDate',
    'AlreadyRatedUser',
    'DomainException',
    'EmailSendingInternal',
    'InvalidInputData',
    'ExpiredToken',
    'GroupAlreadyExists',
    'InactiveUser',
    'InvalidJWTAuthorization',
    'InvalidJWTToken',
    'InvalidUserId',
    'InviteGroupCodeLimitExpired',
    'MeetingOutOfDate',
    'MustRegisterToDoAction',
    'NoAcceptedMeetingWithUserToRate',
    'NoContactsInThisGroupToCreate',
    'NoEmailToRestore',
    'NoGetParameters',
    'NoLookingForToDelete',
    'NoMultipartFormData',
    'NoPassedCredentials',
    'NoRequestToContactsToThisUser',
    'NoSuchEmail',
    'NoSuchGroup',
    'NoSuchInviteCode',
    'NoSuchMeetingType',
    'NoSuchNotification',
    'NoSuchPendingMeeting',
    'NoSuchTag',
    'NoSuchTrip',
    'NoSuchUser',
    'NoSuchUserInContactsToMeet',
    'NoSuchUserToInviteOnMeeting',
    'NoUserForThisEmail',
    'NoUserPhotoFile',
    'NotAllTagsExist',
    'NotAuthorized',
    'NotJSONData',
    'NowSuchMeeting',
    'Ok',
    'RequestToContactsAlreadySent',
    'RestoreNotDeletedUser',
    'TargetUserNotRegistered',
    'TooLateToRestoreProfile',
    'UnableToChangeLookingFor',
    'UnblockUnblockedUser',
    'UniqueEmailRequired',
    'UniqueNicknameRequired',
    'UserAcceptsHimself',
    'UserAlreadyBlocked',
    'UserAlreadyRegistered',
    'UserBlocked',
    'UserInvitedOnMeetingHimself',
    'UserInvitesHimselfContacts',
    'UserIsAlreadyInContacts',
    'UserIsAlreadyRemovedFromContacts',
    'UserIsBlocked',
    'UserIsNotInContacts',
    'UserIsNotInMeeting',
    'UserRatesHimself',
    'UserReportsHimself',
    'UserTriedToRemoveHimselfFromContacts',
    'WrongEmailVerificationUrl',
    'WrongPassword',
    'WrongRestoreConfirmationUrl',
)

class DomainException(Exception):
    """
    Общее исключение (приходит в случае непохендленных ошибок)

    Структура всех ислючений одинаковая


    detail = `string` или `dictionary` описание ошибки

    status_code = http код (статус) ответа

    code = `string` идентификато ошибки, примерный формат: <domain_object_or_field>_<error_description>

    """
    detail = 'A server error occurred.'
    status_code = 500
    exception = None

    def __init__(self, detail=None, exception=None, status_code=None, code=None):
        self.detail = detail if detail is not None else self.__class__.detail
        self.exception = exception if exception is not None else self.__class__.exception
        self.status_code = status_code if status_code is not None else self.__class__.status_code
        self.code = code if code is not None else self.__class__.__name__

    def str(self):
        return '{0}: {1!r}'.format(self.__class__.name, self.detail)

    def to_dict(self):
        return {
            'code': self.code,
            'detail': self.detail
        }


class Ok(DomainException):
    status_code = 200
    detail = ''


class NotJSONData(DomainException):
    status_code = 400
    detail = 'Input data are not in JSON'


class NoSuchInviteCode(DomainException):
    status_code = 400
    detail = 'No such invite code'


class InviteGroupCodeLimitExpired(DomainException):
    status_code = 400
    detail = 'The invite group code is over.'


class ExpiredToken(DomainException):
    status_code = 400
    detail = 'The token expired'


class InvalidJWTAuthorization(DomainException):
    status_code = 400
    detail = 'Wrong jwt authorization format'


class InvalidJWTToken(DomainException):
    status_code = 400
    detail = 'Token is invalid'


class AlreadyAuthenticated(DomainException):
    status_code = 400
    detail = 'User already logged in'


class NotAuthorized(DomainException):
    status_code = 400
    detail = 'No token'


class NoMultipartFormData(DomainException):
    status_code = 400
    detail = 'Multipart content needed'


class InvalidInputData(DomainException):
    status_code = 400
    detail = {}


class NoSuchUser(DomainException):
    status_code = 400
    detail = 'No such user'


class WrongPassword(DomainException):
    status_code = 400
    detail = 'Invalid password'


class UserAlreadyRegistered(DomainException):
    status_code = 400
    detail = 'User with this email already registered'


class GetInviteCodeProcessed(DomainException):
    status_code = 400
    detail = 'The request for this email is currently being processed'


class GetInviteCodeAccepted(DomainException):
    status_code = 400
    detail = 'The request for this email is already accepted'


class GetInviteCodeRejected(DomainException):
    status_code = 400
    detail = 'The request for this email is rejected'


class EmailSendingInternal(DomainException):
    status_code = 500
    detail = 'Cannot send email'


class NoGetParameters(DomainException):
    status_code = 400
    detail = 'Invalid GET arguments'


class InvalidUserId(DomainException):
    status_code = 400
    detail = 'Invalid user Id'


class UserAlreadyBlocked(DomainException):
    status_code = 400
    detail = 'User is already blocked'


class UnblockUnblockedUser(DomainException):
    status_code = 400
    detail = 'Cannot unblock unblocked user'


# -----------------------  NOT USED --------------------------------

class NoSuchEmail(DomainException):
    status_code = 400
    detail = 'No user with such email'


class MustRegisterToDoAction(DomainException):
    status_code = 400
    detail = 'User is not registered completely'


class NoPassedCredentials(DomainException):
    status_code = 400
    detail = 'Invalid credentials'


class NoEmailToRestore(DomainException):
    status_code = 400
    detail = 'No specified target email'


class NoUserForThisEmail(DomainException):
    status_code = 400
    detail = 'No such user'


class NoUserPhotoFile(DomainException):
    status_code = 400
    detail = 'No specified file'


class UniqueEmailRequired(DomainException):
    status_code = 400
    detail = 'Email must be unique'


class UniqueNicknameRequired(DomainException):
    status_code = 400
    detail = 'Nickname must be unique'


class UserTriedToRemoveHimselfFromContacts(DomainException):
    status_code = 400
    detail = 'User cannot remove himself'


class UserIsNotInContacts(DomainException):
    status_code = 400
    detail = 'Requested user is not in contacts'


class UserIsAlreadyRemovedFromContacts(DomainException):
    status_code = 400
    detail = 'User is already deleted'


class NoSuchTag(DomainException):
    status_code = 400
    detail = 'No tag with this name'


class NoContactsInThisGroupToCreate(DomainException):
    status_code = 400
    detail = 'No contacts for this group'


class GroupAlreadyExists(DomainException):
    status_code = 400
    detail = 'This group already exists'


class NoSuchGroup(DomainException):
    status_code = 400
    detail = 'No group with this name'


class NoSuchNotification(DomainException):
    status_code = 400
    detail = 'User has not such notification'


class WrongEmailVerificationUrl(DomainException):
    status_code = 400
    detail = 'Wrong Url'


class UnableToChangeLookingFor(DomainException):
    status_code = 400
    detail = 'Can change this one per month'


class NoLookingForToDelete(DomainException):
    status_code = 400
    detail = 'User are not looking for anybody'


class InactiveUser(DomainException):
    status_code = 403
    detail = 'User must be active'


class NoSuchMeetingType(DomainException):
    status_code = 400
    detail = 'No such meeting type'


class UserInvitedOnMeetingHimself(DomainException):
    status_code = 400
    detail = 'User cannot invite himself'


class NoSuchUserToInviteOnMeeting(DomainException):
    status_code = 400
    detail = 'No user with this ID'


class NoSuchUserInContactsToMeet(DomainException):
    status_code = 400
    detail = 'No user with this ID in user contacts'


class AcceptOwnMeeting(DomainException):
    status_code = 400
    detail = 'Meeting initiator cannot accept/decline own meeting invitation'


class NoSuchPendingMeeting(DomainException):
    status_code = 400
    detail = 'No such pending meeting'


class UserIsNotInMeeting(DomainException):
    status_code = 403
    detail = 'User is not in this meeting'


class NowSuchMeeting(DomainException):
    status_code = 400
    detail = 'No such meeting'


class UserRatesHimself(DomainException):
    status_code = 400
    detail = 'User tried to rate himself'


class AlreadyRatedUser(DomainException):
    status_code = 400
    detail = 'This user had been already rated for this meeting'


class NoAcceptedMeetingWithUserToRate(DomainException):
    status_code = 400
    detail = 'No Accepted Meeting With User To Rate'


class MeetingOutOfDate(DomainException):
    status_code = 400
    detail = 'Cannot accept out of date meeting'


class UserIsAlreadyInContacts(DomainException):
    status_code = 400
    detail = 'User is already in contacts'


class NoRequestToContactsToThisUser(DomainException):
    status_code = 400
    detail = 'Request to this user had not been sent'


class UserInvitesHimselfContacts(DomainException):
    status_code = 400
    detail = 'User tried to add/cancel himself'


class TargetUserNotRegistered(DomainException):
    status_code = 400
    detail = 'This users is not registered completely so you could not sent contact request'


class RequestToContactsAlreadySent(DomainException):
    status_code = 400
    detail = 'Request is already sent'


class UserAcceptsHimself(DomainException):
    status_code = 400
    detail = 'User tried to accept himself'


class NoSuchTrip(DomainException):
    status_code = 400
    detail = 'No such trip'


class NotAllTagsExist(DomainException):
    status_code = 400
    detail = 'Not all tags exist'


class AlreadyHasTripOnThisDate(DomainException):
    status_code = 400
    detail = 'User already has trip on this date'


class UserReportsHimself(DomainException):
    status_code = 400
    detail = 'User tried to report himself'


class UserBlocked(DomainException):
    status_code = 400
    detail = 'This user is blocked'


class UserIsBlocked(DomainException):
    status_code = 400
    detail = 'Target user blocked current user'


class RestoreNotDeletedUser(DomainException):
    status_code = 400
    detail = 'User is not deleted'


class WrongRestoreConfirmationUrl(DomainException):
    status_code = 400
    detail = 'Wrong Url'


class TooLateToRestoreProfile(DomainException):
    status_code = 400
    detail = 'Allowed time to restore profile already passed. This user is deleted'
