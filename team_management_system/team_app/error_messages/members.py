from global_utils.choice_enum_utils import ChoiceEnum


class MemberErrors(ChoiceEnum):
    INVALID_EMAIL = "Invalid Email Address."
    INVALID_PHONE = "Invalid Phone Number."
    MISSING_MEMBER_ID = "Member ID is missing."
    NO_UPDATE_PARAMS = "At least one param should be present for updation."