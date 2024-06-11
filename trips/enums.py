import enum


class PurposeType(enum.StrEnum):
    NOT_SELECTED = "NOT SELECTED"
    TOURISM = "Tourism"
    TRANSIT = "Transit"
    VISITING_FRIENDS_OR_RELATIVES = "Visiting friends or relatives"
    BUSINESS_TRIP = "Business trip"
    EDUCATION_OR_TRAINING = "Education or training"
    MEDICAL_TREATMENT = "Medical treatment"
    SPORTS_EVENTS_OR_COMPETITIONS_PARTICIPATION = (
        "Sports events or competitions participation"
    )
    OTHER = "Other"
